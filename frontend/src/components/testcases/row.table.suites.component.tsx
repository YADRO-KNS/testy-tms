import {treeSuite} from "./suites.component";
import {myCase} from "../models.interfaces";
import React, {useEffect, useMemo} from "react";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import IconButton from "@mui/material/IconButton";
import SuiteCaseService from "../../services/suite.case.service";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import Collapse from "@mui/material/Collapse";
import Table from "@mui/material/Table";
import Checkbox from "@mui/material/Checkbox";
import TableCell from "@mui/material/TableCell";
import Link from "@mui/material/Link";
import RowCase from "./row.case.table.suites.component";

function Row(props: {
    row: treeSuite, setShowCreationCase: (show: boolean) => void, setShowCreationSuite: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: { id: number, name: string } | null) => void, treeSuitesOpenMap: Map<number, boolean>,
    setTreeSuitesOpenMap: (newMap: (prev: Map<number, boolean>) => any) => void, setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, setInfoCaseForEdit: (myCase: myCase) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void, selectedCases: number[], setSelectedCases: (cases: number[]) => void,
    setOpenDialogDeletion: (show: boolean) => void,
    setComponentForDeletion: (component: myCase | treeSuite) => void,
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

    const checkIfAllSelected = useMemo(() => {
        if (row.test_cases.length > 0) {
            for (let i = 0; i < row.test_cases.length; i++) {
                if (selectedCases.indexOf(row.test_cases[i].id) === -1) {
                    return false
                }
            }
            return true
        }
        return false
    }, [selectedCases])

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
                                    }).catch((e) => {
                                        console.log(e)
                                    })
                                } else {
                                    setSelectedSuiteCome(null)
                                    setShowCreationSuite(true)
                                }
                            }).catch((e) => {
                                console.log(e)
                            })
                            setInfoSuiteForEdit({id: row.id, name: row.name})
                        }}>
                            <EditIcon fontSize={"small"}/>
                        </IconButton>
                        <IconButton size={"small"} onClick={() => {
                            setComponentForDeletion(row)
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
                                        checked={checkIfAllSelected}
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
                                <RowCase key={onecase.id} onecase={onecase} row={row}
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
                                        <Link component="button"
                                              data-cy="add-case-in-suite"
                                              onClick={() => {
                                                  setShowCreationCase(true)
                                                  setSelectedSuiteCome({id: row.id, name: row.name})
                                              }}>
                                            Добавить тест-кейс
                                        </Link>
                                        <Link underline="none">&nbsp;&nbsp;|&nbsp;&nbsp;</Link>
                                        <Link component="button"
                                              data-cy="add-suite-in-parent"
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

export default Row