import {Button, Dialog, DialogActions, DialogContent, DialogContentText} from "@mui/material";
import React from "react";
import SuiteCaseService from "../../services/suite.case.service";
import {treeSuite} from "./suites.component";
import {myCase} from "./suites.component";

function DeletionDialogElements(props: {
    openDialogDeletion: boolean, setOpenDialogDeletion: (show: boolean) => void,
    selectedForDeletion: number[], setSelectedForDeletion: (idCases: number[]) => void
    setTreeSuites: (treeSuites: treeSuite[]) => void,
    selectedSuiteForTreeView: treeSuite,
    setSelectedSuiteForTreeView: (treeSuite: treeSuite) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }
}) {
    const {
        openDialogDeletion,
        setOpenDialogDeletion,
        selectedForDeletion,
        setSelectedForDeletion,
        setSelectedSuiteForTreeView, selectedSuiteForTreeView,
        setDetailedCaseInfo, detailedCaseInfo
    } = props


    function disagreeToDelete() {
        setOpenDialogDeletion(false)
    }

    async function agreeToDelete() {
        SuiteCaseService.deleteCases(selectedForDeletion).then(() => {
            if (detailedCaseInfo.show && selectedForDeletion.indexOf(detailedCaseInfo.myCase.id) !== -1) {
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
            }
            SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                setSelectedSuiteForTreeView(response.data)
                setSelectedForDeletion([])
            }).catch((e) => {
                console.log(e)
            })
        }).catch((e) => {
            console.log(e)
        })
        setOpenDialogDeletion(false)
    }

    return (
        <Dialog
            open={openDialogDeletion}
            onClose={disagreeToDelete}
        >
            <DialogContent>
                <DialogContentText style={{fontSize: 20, color: "black", whiteSpace: "pre"}}>
                    Вы уверены, что хотите удалить выбранные тест-кейсы?
                    <br/>
                </DialogContentText>
                <DialogActions style={{padding: 0}}>
                    <Button
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

export default DeletionDialogElements