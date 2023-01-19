import React, {useEffect, useState} from "react";
import TableTestPlans from "./table.testplans.component";
import TestPlanService from "../../services/testplan.service";
import CreationTestplanComponent from "./creation.testplan.component";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableContainer from "@mui/material/TableContainer";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Breadcrumbs from "@mui/material/Breadcrumbs";
import {test, testPlan} from "../models.interfaces";
import TestplanInfoComponent from "./testplan.info.component";
import SplitterLayout from "react-splitter-layout";
import useStyles from "./styles.testplans";
import DetailedTestInfoComponent from "./detailed.test.info.component";
import DeletionDialogTestPlans from "./deletion.dialog.testplans.component";
import {defaultStatus, statuses} from "../model.statuses";
import ProfileService from "../../services/profile.service";

export interface treeTestPlan {
    id: number,
    name: string,
    level: number,
    children: treeTestPlan[],
    title: string;
}

const bfs = (startTrees: treeTestPlan[], testPlanId: number) => {
    let q: treeTestPlan[] = new Array<treeTestPlan>();

    for (let tree of startTrees) {
        q.push(tree);
        if (tree.id === testPlanId)
            return tree;
    }

    while (q.length > 0) {
        const v = q.shift();
        if (v !== undefined) {
            for (let child of v.children) {
                if (child.id === testPlanId)
                    return child;
                q.push(child);
            }
        }
    }
}

const TestplansComponent: React.FC = () => {
    const classes = useStyles()
    const [showCreationTestPlan, setShowCreationTestPlan] = useState(false)
    const [isForEdit, setIsForEdit] = useState<testPlan | null>(null)
    const [testPlans, setTestPlans] = useState<testPlan []>([])
    const [treeTestPlans, setTreeTestPlans] = useState<treeTestPlan[]>([])
    const [currentTestPlan, setCurrentTestPlan] = useState<testPlan | undefined>()
    const [detailedTestInfo, setDetailedTestInfo] = useState<{ show: boolean, test: test } | null>(null)
    const [showEnterResult, setShowEnterResult] = useState(false)
    const testPlanId = window.location.pathname === "/testplans" ? null : Number(window.location.pathname.slice("/testplans/".length))
    const [breadcrumbs, setBreadcrumbs] = useState<{ name: string, link: string | number }[]>()
    const [flag, setFlag] = useState(true)
    const [openDialogDeletionTestPlans, setOpenDialogDeletionTestPlans] = useState(false);
    const [selected, setSelected] = React.useState<number []>([]);
    const [tests, setTests] = useState<test[]>([])

    const handleShowCreationTestPlan = () => setShowCreationTestPlan(true)

    useEffect(() => {
            TestPlanService.getAllTestPlans().then((response) => {
                setTestPlans(response.data)
            })
                .catch((e) => {
                    console.log(e);
                });
            if (testPlanId) {
                TestPlanService.getTestPlan(testPlanId).then((response) => {
                    let curTestPlan: testPlan = response.data
                    curTestPlan.tests.forEach(x => {
                        if (x.current_result) {
                            let status = statuses.find(i => i.name === x.current_result)
                            x.last_status_color = status ? status : defaultStatus
                        } else {
                            x.last_status_color = defaultStatus
                        }
                        x.test_results.forEach(y => {
                            let status = statuses.find(i => i.id === y.status)
                            y.status_color = status ? status : defaultStatus
                        })
                    })
                    setCurrentTestPlan(curTestPlan)
                })
                    .catch((e) => {
                        console.log(e);
                    });
            }

            TestPlanService.getTreeTestPlans().then((response) => {
                const localTreeTestPlans = response.data;
                if (testPlanId) {
                    const testTreeTestPlan = bfs(localTreeTestPlans, testPlanId);
                    if (testTreeTestPlan === undefined) {
                        setTreeTestPlans([]);
                    } else {
                        setTreeTestPlans(testTreeTestPlan.children);
                    }
                } else {
                    setTreeTestPlans(localTreeTestPlans);
                }
            })
                .catch((e) => {
                    console.log(e);
                });
        }, [testPlanId]
    )

    useEffect(() => {
        if (currentTestPlan && flag && testPlans.length !== 0) {
            const newBreadcrumbs = []
            newBreadcrumbs.push({name: currentTestPlan.name, link: currentTestPlan.id})
            let plan = currentTestPlan.parent
            while (plan) {
                const parent = testPlans.find(x => x.id === plan)
                if (parent) {
                    newBreadcrumbs.push({name: parent.name, link: parent.id})
                    plan = parent.parent
                }
            }
            newBreadcrumbs.push({name: "Тест-планы", link: ""})
            setBreadcrumbs(newBreadcrumbs.reverse())
            setFlag(false)
        }

        if (currentTestPlan && currentTestPlan.tests) {
            new Promise<test[]>(async (resolve) => {
                await Promise.all(currentTestPlan.tests.map(async (test) => {
                    await TestPlanService.getTest(test.id).then(async (response) => {
                        test.user = response.data.user
                        if (test.user) {
                            await ProfileService.getUser(test.user).then((response) => {
                                test.username = response.data.username
                            }).catch((e) => console.log(e))
                        }
                    }).catch((e) => console.log(e))
                }))
                resolve(currentTestPlan.tests)
            }).then((response: test[]) => {
                setTests(response)
            })
        }

    }, [currentTestPlan, testPlans, flag])

    return (
        <div className={classes.mainGrid}>
            <div className={classes.leftGrid}>
                <SplitterLayout customClassName={classes.splitter} primaryIndex={0} primaryMinSize={45}
                                secondaryMinSize={35}
                                percentage>
                    <TableContainer className={classes.tableContainer}>
                        <Table size="small" className={classes.mainTable}>
                            <tbody className={classes.mainBody}>
                            <tr>
                                <td>
                                    <Button sx={{color: "#000000"}} disabled={!(selected.length > 0)}
                                            onClick={() => {
                                                setOpenDialogDeletionTestPlans(true)
                                            }}>
                                        Удалить
                                    </Button>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <Breadcrumbs aria-label="breadcrumb">
                                        {breadcrumbs?.map((breadcrumb, index) =>
                                            index === breadcrumbs.length - 1 ?
                                                (<Link
                                                    color="textPrimary"
                                                    href={"/testplans/" + breadcrumb.link}
                                                    aria-current="page"
                                                    key={index}
                                                >
                                                    {breadcrumb.name}
                                                </Link>) :
                                                (<Link color="inherit" href={"/testplans/" + breadcrumb.link}
                                                       key={index}>
                                                    {breadcrumb.name}
                                                </Link>)
                                        )}
                                    </Breadcrumbs>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    {currentTestPlan && <TestplanInfoComponent currentTestPlan={currentTestPlan}
                                                                               tests={tests}
                                                                               setShowCreationTestPlan={setShowCreationTestPlan}
                                                                               setIsForEdit={setIsForEdit}
                                                                               detailedTestInfo={detailedTestInfo}
                                                                               setDetailedTestInfo={setDetailedTestInfo}
                                                                               showEnterResult={showEnterResult}
                                                                               setShowEnterResult={setShowEnterResult}/>}
                                </td>
                            </tr>
                            {treeTestPlans.map((testPlan, index) =>
                                <TableTestPlans key={index} testplan={testPlan} selected={selected}
                                                setSelected={setSelected}/>
                            )}
                            <DeletionDialogTestPlans openDialogDeletion={openDialogDeletionTestPlans}
                                                     setOpenDialogDeletion={setOpenDialogDeletionTestPlans}
                                                     selectedForDeletion={selected}
                                                     setSelectedForDeletion={setSelected}
                                                     setTreeTestplans={setTreeTestPlans}/>
                            </tbody>
                        </Table>
                    </TableContainer>
                    {detailedTestInfo && detailedTestInfo.show &&
                    <Grid>
                        <DetailedTestInfoComponent detailedTestInfo={detailedTestInfo} setDetailedTestInfo={setDetailedTestInfo}
                                                   showEnterResult={showEnterResult}
                                                   setShowEnterResult={setShowEnterResult}/>
                    </Grid>}
                </SplitterLayout>
            </div>
            <div className={classes.rightGrid}>
                <div className={classes.rightGridButton}>
                    <Button sx={{
                        margin: "15px",
                        minWidth: "70%",
                        height: "45%",
                        backgroundColor: "#FFFFFF",
                        color: "#000000",
                        "&:hover": {
                            backgroundColor: "#f6f6f6",
                            borderColor: "#000000",
                        }
                    }} onClick={handleShowCreationTestPlan}>Создать тест-план</Button>
                    <CreationTestplanComponent show={showCreationTestPlan} setShow={setShowCreationTestPlan}
                                               testPlans={testPlans}
                                               isForEdit={isForEdit} setIsForEdit={setIsForEdit}/>
                </div>
            </div>
        </div>
    )
}

export default TestplansComponent