import {
    Table,
    TableCell,
    Collapse,
    IconButton,
    Checkbox,
    Link,
    Box
} from "@mui/material";
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import React, {useEffect, useMemo, useState} from "react";
import useStyles from "../../styles/styles";
import {myCase, suite, treeSuite} from "./suites.component";
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import DetailedCaseInfo from "./detailed.case.info.component";
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import DeletionDialogElement from "./deletion.dialog.element.component";
import DeletionDialogElements from "./deletion.dialog.elements.component";
import SplitterLayout from 'react-splitter-layout';
import 'react-splitter-layout/lib/index.css';
import useStylesTestCases from "./styles.testcases"
import SuiteCaseService from "../../services/suite.case.service";

function TableRowCase(props: {
    row: treeSuite, setShowCreationCase: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: { id: number, name: string } | null) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, setInfoCaseForEdit: (myCase: myCase) => void,
    onecase: myCase,
    selected: number [], setSelected: (ids: number[]) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void,
    setOpenDialogDeletion: (show: boolean) => void,
    setComponentForDeletion: (component: { type: string, id: number }) => void,
    classesTableSuitesCases: any
}) {
    const {
        row,
        setShowCreationCase,
        setSelectedSuiteCome,
        setDetailedCaseInfo,
        setInfoCaseForEdit,
        onecase,
        selected,
        setSelected,
        setOpenDialogDeletion,
        setComponentForDeletion,
        classesTableSuitesCases
    } = props;
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
        <tr
            className={classesTableSuitesCases.tableRow}
        >
            <td className={classesTableSuitesCases.cellForCheckBoxAndId}>
                <Checkbox
                    className={classesTableSuitesCases.checkBox}
                    onClick={(event) => handleClick(event, onecase.id)}
                    color="primary"
                    checked={selected.indexOf(onecase.id) !== -1}
                />
            </td>
            <TableCell component="th"
                       scope="row"
                       padding="none">
                {onecase.id}
            </TableCell>
            <TableCell className={classesTableSuitesCases.caseNameCell}>
                {onecase.name}
            </TableCell>
            <td className={classesTableSuitesCases.deleteEditShowCaseCell}>
                <div id="gridEditDelete" className={classesTableSuitesCases.gridEditDelete}>
                    <IconButton size={"small"} onClick={() => {
                        setComponentForDeletion({type: "case", id: onecase.id})
                        setOpenDialogDeletion(true)
                    }}>
                        <DeleteIcon fontSize={"small"}/>
                    </IconButton>
                    <IconButton size={"small"} onClick={() => {
                        setShowCreationCase(true)
                        setSelectedSuiteCome({id: row.id, name: row.name})
                        setInfoCaseForEdit(onecase)
                    }}>
                        <EditIcon fontSize={"small"}/>
                    </IconButton>
                </div>
                <div id={onecase.id.toString() + "Arrow"}>
                    <IconButton size={"small"} onClick={() => {
                        setDetailedCaseInfo({
                            show: true,
                            myCase: onecase
                        })
                    }}>
                        <KeyboardArrowRightIcon/>
                    </IconButton>
                </div>
            </td>
        </tr>)
}

function Row(props: {
    row: treeSuite, setShowCreationCase: (show: boolean) => void, setShowCreationSuite: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: { id: number, name: string } | null) => void, treeSuitesOpenMap: Map<number, boolean>,
    setTreeSuitesOpenMap: (newMap: (prev: Map<number, boolean>) => any) => void, setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, setInfoCaseForEdit: (myCase: myCase) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void, selectedCases: number[], setSelectedCases: (cases: number[]) => void,
    setOpenDialogDeletion: (show: boolean) => void,
    setComponentForDeletion: (component: { type: string, id: number }) => void,
    classesTableSuitesCases: any, setInfoSuiteForEdit: (suite: { id: number, name: string }) => void,
}) {
    const {
        row,
        setShowCreationCase,
        setShowCreationSuite,
        setSelectedSuiteCome,
        treeSuitesOpenMap,
        setTreeSuitesOpenMap,
        setDetailedCaseInfo,
        detailedCaseInfo,
        setInfoCaseForEdit,
        setTreeSuites,
        selectedCases,
        setSelectedCases,
        setOpenDialogDeletion,
        setComponentForDeletion,
        classesTableSuitesCases,
        setInfoSuiteForEdit
    } = props;
    const [localOpen, setLocalOpen] = React.useState<boolean | undefined>(true);

    const checkIfAllSelected = () => {
        if (row.test_cases.length > 0) {
            for (let i = 0; i < row.test_cases.length; i++) {
                if (selectedCases.indexOf(row.test_cases[i].id) === -1) {
                    return false
                }
            }
            return true
        }
        return false
    };

    const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
        const caseIdsInCurrentRow = row.test_cases.map((onecase) => onecase.id)
        if (event.target.checked) {
            const newSelected = caseIdsInCurrentRow.filter((caseid) => selectedCases.indexOf(caseid) === -1)
            setSelectedCases(newSelected.concat(selectedCases))
            return;
        } else {
            const newSelected = selectedCases.filter((caseid) => caseIdsInCurrentRow.indexOf(caseid) === -1)
            setSelectedCases(newSelected)
        }
    };

    useEffect(() => {
        if (treeSuitesOpenMap.get(row.id) === undefined) {
            setTreeSuitesOpenMap(prev => (prev.set(row.id, true)))
            setLocalOpen(true)
        } else {
            setLocalOpen(treeSuitesOpenMap.get(row.id))
        }
    }, [treeSuitesOpenMap])

    const setOpenClose = () => {
        const flag = treeSuitesOpenMap.get(row.id)
        setTreeSuitesOpenMap(prev => (prev.set(row.id, !flag)))
        setLocalOpen(!flag)
    }

    return (
        <React.Fragment>
            <tr>
                <td className={classesTableSuitesCases.cellSuiteChip} colSpan={4}>
                    <div className={classesTableSuitesCases.suiteNameGrid}
                         id={row.id.toString()}>
                        <div className={classesTableSuitesCases.suiteChip} onClick={setOpenClose}>
                            <KeyboardArrowUpIcon sx={{
                                transform: localOpen ? 'rotate(0deg)' : 'rotate(180deg)',
                                transition: '0.2s', marginRight: 0.6
                            }}/>
                            {row.name}
                        </div>
                        <IconButton size={"small"} onClick={() => {
                            SuiteCaseService.getSuiteById(row.id).then((response) => {
                                if (response.data.parent) {
                                    SuiteCaseService.getSuiteById(response.data.parent).then((response) => {
                                        setSelectedSuiteCome({id: response.data.id, name: response.data.name})
                                        setShowCreationSuite(true)
                                    })
                                } else {
                                    setSelectedSuiteCome(null)
                                    setShowCreationSuite(true)
                                }
                            })
                            setInfoSuiteForEdit({id: row.id, name: row.name})
                        }}>
                            <EditIcon fontSize={"small"}/>
                        </IconButton>
                        <IconButton size={"small"} onClick={() => {
                            setComponentForDeletion({type: "suite", id: row.id})
                            setOpenDialogDeletion(true)
                        }}>
                            <DeleteIcon fontSize={"small"}/>
                        </IconButton>
                    </div>
                </td>
            </tr>
            <tr>
                <td className={classesTableSuitesCases.tables}
                    colSpan={4}>
                    <Collapse
                        in={(treeSuitesOpenMap.get(row.id) === undefined || treeSuitesOpenMap.get(row.id) === true)}
                        mountOnEnter>
                        <Table size="small">
                            <tbody className={classesTableSuitesCases.headerTableBodyCases}>
                            <tr>
                                <td className={classesTableSuitesCases.cellForCheckBoxAndId}>
                                    <Checkbox
                                        className={classesTableSuitesCases.checkBox}
                                        checked={checkIfAllSelected()}
                                        onChange={(e) => handleSelectAllClick(e)}
                                        color="primary"

                                    />
                                </td>
                                <TableCell component="th"
                                           scope="row"
                                           padding="none"
                                           className={classesTableSuitesCases.cellForCheckBoxAndId}>ID</TableCell>
                                <TableCell colSpan={2}>Название</TableCell>
                            </tr>
                            </tbody>
                            <tbody className={classesTableSuitesCases.tableForCases}>
                            {row.test_cases.map((onecase) => (
                                <TableRowCase key={onecase.id} onecase={onecase} row={row}
                                              selected={selectedCases}
                                              detailedCaseInfo={detailedCaseInfo}
                                              setDetailedCaseInfo={setDetailedCaseInfo}
                                              setInfoCaseForEdit={setInfoCaseForEdit}
                                              setSelected={setSelectedCases}
                                              setSelectedSuiteCome={setSelectedSuiteCome}
                                              setShowCreationCase={setShowCreationCase}
                                              setTreeSuites={setTreeSuites}
                                              setOpenDialogDeletion={setOpenDialogDeletion}
                                              setComponentForDeletion={setComponentForDeletion}
                                              classesTableSuitesCases={classesTableSuitesCases}
                                />
                            ))}
                            </tbody>
                            <tbody>
                            <tr>
                                <td colSpan={4}>
                                    <div className={classesTableSuitesCases.addingCaseSuite}>
                                        <Link component="button" onClick={() => {
                                            setShowCreationCase(true)
                                            setSelectedSuiteCome({id: row.id, name: row.name})
                                        }}>
                                            Добавить тест-кейс
                                        </Link>
                                        <Link underline="none">&nbsp;&nbsp;|&nbsp;&nbsp;</Link>
                                        <Link component="button"
                                              onClick={() => {
                                                  setShowCreationSuite(true)
                                                  setSelectedSuiteCome({id: row.id, name: row.name})
                                              }}>
                                            Добавить сьюту
                                        </Link>
                                    </div>
                                </td>
                            </tr>
                            </tbody>
                            {row && row.children &&
                            <tbody className={classesTableSuitesCases.childTable}>
                            {row.children.map((suite: any) => (
                                <Row key={suite.id} row={suite}
                                     setShowCreationCase={setShowCreationCase}
                                     setShowCreationSuite={setShowCreationSuite}
                                     setSelectedSuiteCome={setSelectedSuiteCome}
                                     treeSuitesOpenMap={treeSuitesOpenMap}
                                     setTreeSuitesOpenMap={setTreeSuitesOpenMap}
                                     detailedCaseInfo={detailedCaseInfo}
                                     setDetailedCaseInfo={setDetailedCaseInfo}
                                     setInfoCaseForEdit={setInfoCaseForEdit}
                                     setTreeSuites={setTreeSuites}
                                     selectedCases={selectedCases}
                                     setSelectedCases={setSelectedCases}
                                     setOpenDialogDeletion={setOpenDialogDeletion}
                                     setComponentForDeletion={setComponentForDeletion}
                                     classesTableSuitesCases={classesTableSuitesCases}
                                     setInfoSuiteForEdit={setInfoSuiteForEdit}
                                />
                            ))}
                            </tbody>
                            }
                        </Table>
                    </Collapse>
                </td>
            </tr>
        </React.Fragment>
    );
}

const TableSuites = (props: {
    selected: readonly string[], setSelected: (array: readonly string[]) => void,
    setShowCreationCase: (show: boolean) => void, setShowCreationSuite: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: { id: number, name: string } | null) => void,
    setInfoCaseForEdit: (myCase: myCase) => void, setInfoSuiteForEdit: (suite: { id: number, name: string }) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, lastEditCase: number,
    setLastEditCase: (id: number) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void;
    selectedSuiteForTreeView: treeSuite,
    setSelectedSuiteForTreeView: (suite: treeSuite) => void,
}) => {
    const classes = useStyles()
    const {
        setShowCreationCase,
        setShowCreationSuite,
        setSelectedSuiteCome,
        setInfoCaseForEdit,
        setDetailedCaseInfo,
        detailedCaseInfo,
        lastEditCase,
        setLastEditCase,
        setTreeSuites,
        selectedSuiteForTreeView,
        setSelectedSuiteForTreeView,
        setInfoSuiteForEdit
    } = props;
    const [treeSuitesOpenMap, setTreeSuitesOpenMap] = useState(new Map())
    const [shownCase, setShownCase] = useState<{ show: boolean, myCaseId: number }>({show: false, myCaseId: -1})
    const [selectedCases, setSelectedCases] = React.useState<number []>([]);
    const [openDialogDeletion, setOpenDialogDeletion] = useState(false);
    const [openDialogDeletionElements, setOpenDialogDeletionElements] = useState(false);
    const [componentForDeletion, setComponentForDeletion] = useState<{ type: string, id: number }>({type: "", id: -1})

    const openAll = () => {
        let newMap = new Map()
        const setAllInTrue = (childrenSuitesArr: treeSuite[]) => {
            childrenSuitesArr.map((suite) => {
                newMap.set(suite.id, true)
                if (suite.children.length > 0) {
                    setAllInTrue(suite.children)
                }
            })
        }
        newMap.set(selectedSuiteForTreeView.id, true)
        setAllInTrue(selectedSuiteForTreeView.children)
        setTreeSuitesOpenMap(newMap)
    }

    const closeAll = () => {
        let newMap = new Map()
        const setAllInFalse = (childrenSuitesArr: treeSuite[]) => {
            childrenSuitesArr.map((suite) => {
                newMap.set(suite.id, false)
                if (suite.children.length > 0) {
                    setAllInFalse(suite.children)
                }
            })
        }
        newMap.set(selectedSuiteForTreeView.id, false)
        setAllInFalse(selectedSuiteForTreeView.children)
        setTreeSuitesOpenMap(newMap)
    }
    const classesTableSuitesCases = useStylesTestCases()

    const memoizedValue = useMemo(() => <table
        className={classesTableSuitesCases.mainTable}>
        <tbody>
        <Row key={selectedSuiteForTreeView.id} row={selectedSuiteForTreeView}
             setShowCreationCase={setShowCreationCase}
             setShowCreationSuite={setShowCreationSuite}
             setSelectedSuiteCome={setSelectedSuiteCome}
             treeSuitesOpenMap={treeSuitesOpenMap}
             setTreeSuitesOpenMap={setTreeSuitesOpenMap}
             detailedCaseInfo={detailedCaseInfo}
             setDetailedCaseInfo={setDetailedCaseInfo}
             setInfoCaseForEdit={setInfoCaseForEdit}
             setInfoSuiteForEdit={setInfoSuiteForEdit}
             setTreeSuites={setTreeSuites}
             selectedCases={selectedCases}
             setSelectedCases={setSelectedCases}
             setOpenDialogDeletion={setOpenDialogDeletion}
             setComponentForDeletion={setComponentForDeletion}
             classesTableSuitesCases={classesTableSuitesCases}
        />
        </tbody>
    </table>, [selectedSuiteForTreeView, treeSuitesOpenMap, selectedCases]);
    useEffect(() => {
        if (detailedCaseInfo.show) {
            if (shownCase.show && detailedCaseInfo.myCase.id === shownCase.myCaseId && lastEditCase !== detailedCaseInfo.myCase.id) {
                document.getElementById(shownCase.myCaseId + "Arrow")!.style.transform = ""
                setDetailedCaseInfo({
                    show: false, myCase: {
                        id: -1,
                        name: "",
                        suite: -1,
                        scenario: "",
                        project: -1,
                        setup: "",
                        teardown: "",
                        estimate: -1
                    }
                })
                setShownCase({show: false, myCaseId: -1})
            } else if (lastEditCase !== detailedCaseInfo.myCase.id) {
                document.getElementById(detailedCaseInfo.myCase.id + "Arrow")!.style.transform = 'rotate(180deg)'
                if (shownCase.show) {
                    document.getElementById(shownCase.myCaseId + "Arrow")!.style.transform = ""
                }
                setShownCase({show: true, myCaseId: detailedCaseInfo.myCase.id})
            } else {
                setLastEditCase(-1)
            }
        } else if (shownCase.myCaseId >= 0) {
            document.getElementById(shownCase.myCaseId + "Arrow")!.style.transform = ""
            setDetailedCaseInfo({
                show: false, myCase: {
                    id: -1,
                    name: "",
                    suite: -1,
                    scenario: "",
                    project: -1,
                    setup: "",
                    teardown: "",
                    estimate: -1
                }
            })
            setShownCase({show: false, myCaseId: -1})
        }
    }, [detailedCaseInfo])

    return (

        <SplitterLayout customClassName={classes.splitter} primaryIndex={0} primaryMinSize={40} secondaryMinSize={35}
                        percentage>
            <div>
                <Box className={classesTableSuitesCases.box}>
                    <div
                        style={{marginLeft: 10, marginTop: 5}}
                    >
                        <Link
                            sx={{maxHeight: "50%"}}
                            component="button" onClick={() => {
                            openAll()
                        }}>
                            Раскрыть все
                        </Link>
                        <Link underline="none">&nbsp;&nbsp;|&nbsp;&nbsp;</Link>
                        <Link
                            sx={{maxHeight: "50%"}}
                            component="button"
                            onClick={() => {
                                closeAll()
                            }}>
                            Закрыть все
                        </Link>
                        <IconButton size={"small"} disabled={!(selectedCases.length > 0)} onClick={() => {
                            setOpenDialogDeletionElements(true)
                        }}
                                    sx={{marginLeft: 1}}
                        >
                            <DeleteIcon fontSize={"small"}/>
                        </IconButton>
                    </div>
                </Box>
                <div className={classesTableSuitesCases.gridForMainTable}>
                    {memoizedValue}
                </div>
                <DeletionDialogElement openDialogDeletion={openDialogDeletion}
                                       setOpenDialogDeletion={setOpenDialogDeletion}
                                       componentForDeletion={componentForDeletion}
                                       setTreeSuites={setTreeSuites}
                                       selectedForDeletion={selectedCases}
                                       setSelectedForDeletion={setSelectedCases}
                                       selectedSuiteForTreeView={selectedSuiteForTreeView}
                                       setSelectedSuiteForTreeView={setSelectedSuiteForTreeView}
                                       detailedCaseInfo={detailedCaseInfo}
                                       setDetailedCaseInfo={setDetailedCaseInfo}
                />
                <DeletionDialogElements openDialogDeletion={openDialogDeletionElements}
                                        setOpenDialogDeletion={setOpenDialogDeletionElements}
                                        selectedForDeletion={selectedCases}
                                        setTreeSuites={setTreeSuites}
                                        setSelectedForDeletion={setSelectedCases}
                                        selectedSuiteForTreeView={selectedSuiteForTreeView}
                                        setSelectedSuiteForTreeView={setSelectedSuiteForTreeView}
                                        detailedCaseInfo={detailedCaseInfo}
                                        setDetailedCaseInfo={setDetailedCaseInfo}
                />
            </div>
            {detailedCaseInfo.show &&
            <div>
                <DetailedCaseInfo myCase={detailedCaseInfo.myCase} setDetailedCaseInfo={setDetailedCaseInfo}/>
            </div>
            }
        </SplitterLayout>

    );
}
export default TableSuites