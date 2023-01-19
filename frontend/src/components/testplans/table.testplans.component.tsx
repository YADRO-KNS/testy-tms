import React, {useEffect, useState} from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import Typography from "@mui/material/Typography";
import BarChartComponent from "./bar.chart.component";
import {treeTestPlan} from "./testplans.component";
import TestPlanService from "../../services/testplan.service";
import {testPlan} from "../models.interfaces";
import useStyles from "./styles.testplans";

const TableTestPlans = (props: {
    testplan: treeTestPlan, selected: number[], setSelected: (data: number[]) => void,
}) => {
    const classes = useStyles()
    const {testplan, selected, setSelected} = props;
    const [currentTestPlan, setCurrentTestPlan] = useState<testPlan>()

    useEffect(() => {
        if (!currentTestPlan) {
            TestPlanService.getTestPlan(testplan.id).then((response) => {
                setCurrentTestPlan(response.data)
            })
                .catch((e) => {
                    console.log(e);
                });
        }
    }, [currentTestPlan, testplan.id])

    const getTestsResults = (currentTestPlan: testPlan | undefined) => {
        const testsResults: { passed: number, skipped: number, failed: number, blocked: number, untested: number, broken: number } = {
            passed: 0,
            skipped: 0,
            failed: 0,
            blocked: 0,
            untested: 0,
            broken: 0
        }
        if (currentTestPlan?.tests) {
            for (const cur_test of currentTestPlan?.tests) {
                if (cur_test.current_result === "Passed") {
                    testsResults.passed++
                } else if (cur_test.current_result === "Skipped") {
                    testsResults.skipped++
                } else if (cur_test.current_result === "Failed") {
                    testsResults.failed++
                } else if (cur_test.current_result === "Blocked") {
                    testsResults.blocked++
                } else if (cur_test.current_result === "Untested") {
                    testsResults.untested++
                } else if (cur_test.current_result === "Broken") {
                    testsResults.broken++
                } else {
                    testsResults.untested++
                }
            }
        }
        return testsResults
    }

    const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
        const selectedIndex = selected.indexOf(id);
        let newSelected: number[] = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };

    return (
        <tr>
            <td style={{paddingBottom: 3}}>
                <Table size="small">
                    {<tbody style={{border: '1px solid'}}>
                        <tr>
                            <td className={classes.cellCheckbox}>
                                <FormControlLabel
                                    label={testplan.id}
                                    control={<Checkbox
                                        sx={{height: 20}}
                                        checked={selected.indexOf(testplan.id) !== -1}
                                        onClick={(event) => handleClick(event, testplan.id)}
                                        color="primary"
                                    />}
                                />
                            </td>
                            <td style={{width: "auto", maxWidth: "30%", wordBreak: "break-all"}}>
                                <div>
                                    <Link href={"/testplans/" + testplan.id} underline="none"
                                          style={{display: 'flex', color: '#282828'}}>
                                        <Typography style={{paddingBottom: 2}}>
                                            {testplan.title}
                                        </Typography>
                                    </Link>

                                </div>
                                <div>
                                    {"Количество дочерних тест-планов: " + testplan.children.length + ". Количество тестов: " + currentTestPlan?.tests?.length}
                                </div>
                            </td>
                            <TableCell align="right" style={{width: "25%"}}>
                                <BarChartComponent passed={getTestsResults(currentTestPlan).passed}
                                                   skipped={getTestsResults(currentTestPlan).skipped}
                                                   failed={getTestsResults(currentTestPlan).failed}
                                                   blocked={getTestsResults(currentTestPlan).blocked}
                                                   untested={getTestsResults(currentTestPlan).untested}
                                                   broken={getTestsResults(currentTestPlan).broken}/>
                            </TableCell>
                        </tr>
                    </tbody>}
                </Table>
            </td>
        </tr>
    )
}

export default TableTestPlans