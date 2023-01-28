import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import React from "react";
import SuiteCaseService from "../../services/suite.case.service";
import {treeSuite} from "./suites.component";
import {myCase} from "../models.interfaces";

const DeletionDialogElement = (props: {
    openDialogDeletion: boolean, setOpenDialogDeletion: (show: boolean) => void,
    componentForDeletion: myCase | treeSuite | undefined,
    setTreeSuites: (treeSuites: treeSuite[]) => void,
    selectedForDeletion: number[], setSelectedForDeletion: (idCases: number[]) => void,
    selectedSuiteForTreeView: treeSuite,
    setSelectedSuiteForTreeView: (treeSuite: treeSuite) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }
}) => {
    const {
        openDialogDeletion, setOpenDialogDeletion, componentForDeletion,
        selectedForDeletion, setSelectedForDeletion, setSelectedSuiteForTreeView, selectedSuiteForTreeView,
        setDetailedCaseInfo, detailedCaseInfo
    } = props

    function disagreeToDelete() {
        setOpenDialogDeletion(false)
    }

    function deleteFromSelectedForDeletion(indexInSelected: number, selectedForDeletion: number[]) {
        let newSelected: number[] = [];
        if (indexInSelected === 0) {
            newSelected = newSelected.concat(selectedForDeletion.slice(1));
        } else if (indexInSelected === selectedForDeletion.length - 1) {
            newSelected = newSelected.concat(selectedForDeletion.slice(0, -1));
        } else if (indexInSelected > 0) {
            newSelected = newSelected.concat(
                selectedForDeletion.slice(0, indexInSelected),
                selectedForDeletion.slice(indexInSelected + 1),
            );
        }
        return newSelected
    }

    function isTypeMyCase(obj: any): obj is myCase {
        if (obj !== undefined) {
            return obj.scenario !== undefined
        } else {
            return false
        }
    }

    function isTypeTreeSuite(obj: any): obj is treeSuite {
        if (obj !== undefined) {
            return obj.test_cases !== undefined
        } else {
            return false
        }
    }

    function agreeToDelete() {
        if (isTypeMyCase(componentForDeletion)) {
            SuiteCaseService.deleteCase(componentForDeletion.id).then(() => {
                if (detailedCaseInfo.show && detailedCaseInfo.myCase.id === componentForDeletion.id) {
                    setDetailedCaseInfo(SuiteCaseService.getEmptyDetailedCaseInfo())
                }
                SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                    setSelectedSuiteForTreeView(response.data)
                    const indexInSelected = selectedForDeletion.indexOf(componentForDeletion.id)
                    if (indexInSelected !== -1) {
                        setSelectedForDeletion(deleteFromSelectedForDeletion(indexInSelected, selectedForDeletion))
                    }
                }).catch((e) => {
                    console.log(e)
                })
            }).catch((e) => {
                console.log(e)
            })
        } else if (isTypeTreeSuite(componentForDeletion)) {
            if (selectedForDeletion.length > 0 && componentForDeletion.test_cases.length > 0) {
                let newSelected = selectedForDeletion
                componentForDeletion.test_cases.forEach((myCase: myCase) => {
                    const indexInSelected = newSelected.indexOf(myCase.id)
                    if (indexInSelected !== -1) {
                        newSelected = deleteFromSelectedForDeletion(indexInSelected, newSelected)
                    }
                })
                setSelectedForDeletion(newSelected)
            }
            SuiteCaseService.deleteSuite(componentForDeletion.id).then(() => {

                SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                    setSelectedSuiteForTreeView(response.data)
                }).catch((e) => {
                    if (e.response.status === 404) {
                        window.location.assign("/testcases");
                    }
                })
            }).catch((e) => {
                console.log(e)
            })
        }
        setOpenDialogDeletion(false)
    }

    return (
        <Dialog
            open={openDialogDeletion}
            onClose={disagreeToDelete}
        >
            <DialogContent>
                <DialogContentText style={{fontSize: 20, color: "black", whiteSpace: "pre"}}>
                    {(isTypeMyCase(componentForDeletion) && "Вы уверены, что хотите удалить тест-кейс?")
                        || ("Вы уверены, что хотите удалить сьюту? \n" +
                            "Это повлечет за собой удаление всех дочерних элементов.")}
                    <br/>
                </DialogContentText>
                <DialogActions style={{padding: 0}}>
                    <Button
                        data-cy="disagree-to-delete"
                        style={{
                            margin: "20px 4px 0px 5px",
                            width: "30%",
                            minWidth: 100,
                            height: "30%",
                            backgroundColor: "#FFFFFF",
                            border: '1px solid',
                            color: "#000000",
                        }}
                        onClick={disagreeToDelete}
                        title={"Нет"}>
                        Нет
                    </Button>
                    <Button
                        data-cy="agree-to-delete"
                        style={{
                            margin: "20px 5px 0px 4px",
                            width: "30%",
                            minWidth: 100,
                            height: "30%",
                            backgroundColor: "#696969",
                            color: "#FFFFFF",
                        }}
                        onClick={agreeToDelete}
                        title={"Да"}>
                        Да
                    </Button>
                </DialogActions>
            </DialogContent>
        </Dialog>
    );
}

export default DeletionDialogElement