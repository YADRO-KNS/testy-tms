import IconButton from "@mui/material/IconButton";
import Link from "@mui/material/Link";
import Box from "@mui/material/Box";
import React, {useEffect, useMemo, useState} from "react";
import {mainFieldInSuite, treeSuite} from "./suites.component";
import {myCase} from "../models.interfaces";
import DetailedCaseInfo from "./detailed.case.info.component";
import DeleteIcon from '@mui/icons-material/Delete';
import DeletionDialogElement from "./deletion.dialog.element.component";
import DeletionDialogElements from "./deletion.dialog.elements.component";
import SplitterLayout from 'react-splitter-layout';
import 'react-splitter-layout/lib/index.css';
import useStylesTestCases from "./styles.testcases"
import SuiteCaseService from "../../services/suite.case.service";
import Row from "./row.table.suites.component";

const TableSuites = (props: {
    selected: readonly string[], setSelected: (array: readonly string[]) => void,
    setShowCreationCase: (show: boolean) => void, setShowCreationSuite: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: mainFieldInSuite | null) => void,
    setInfoCaseForEdit: (myCase: myCase) => void, setInfoSuiteForEdit: (suite: mainFieldInSuite) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, lastEditCase: number,
    setLastEditCase: (id: number) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void;
    selectedSuiteForTreeView: treeSuite,
    setSelectedSuiteForTreeView: (suite: treeSuite) => void,
}) => {
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
    const [componentForDeletion, setComponentForDeletion] = useState<myCase | treeSuite>()

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
                setDetailedCaseInfo(SuiteCaseService.getEmptyDetailedCaseInfo())
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
            setDetailedCaseInfo(SuiteCaseService.getEmptyDetailedCaseInfo())
            setShownCase({show: false, myCaseId: -1})
        }
    }, [detailedCaseInfo])

    return (

        <SplitterLayout customClassName={classesTableSuitesCases.splitter} primaryIndex={0} primaryMinSize={40}
                        secondaryMinSize={35}
                        percentage>
            <div>
                <Box className={classesTableSuitesCases.box}>
                    <div
                        style={{marginLeft: 10, marginTop: 5}}
                    >
                        <Link
                            data-cy="open-all-suites"
                            sx={{maxHeight: "50%"}}
                            component="button" onClick={() => {
                            openAll()
                        }}>
                            Раскрыть все
                        </Link>
                        <Link underline="none">&nbsp;&nbsp;|&nbsp;&nbsp;</Link>
                        <Link
                            data-cy="close-all-suites"
                            sx={{maxHeight: "50%"}}
                            component="button"
                            onClick={() => {
                                closeAll()
                            }}>
                            Закрыть все
                        </Link>
                        <IconButton
                            data-cy="delete-cases-using-checkbox"
                            size={"small"} disabled={!(selectedCases.length > 0)} onClick={() => {
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