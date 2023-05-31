import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import React, {useEffect, useState} from "react";
import useStyles from "../../styles/styles";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import SuiteCaseService from "../../services/suite.case.service";
import {CustomWidthTooltip, treeSuite} from "./suites.component";
import {myCase} from "../models.interfaces";
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import AttachmentButton from "../attachment/attachment_button";
import AttachmentService from "../../services/attachment.servise";
import localStorageTMS from "../../services/localStorageTMS";

interface Props {
    show: boolean;
    setShow: (show: boolean) => void;
    selectedSuiteCome: { id: number, name: string } | null;
    setTreeSuites: (treeSuites: treeSuite[]) => void;
    infoCaseForEdit: myCase | null;
    setInfoCaseForEdit: (myCase: null) => void
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase },
    setLastEditCase: (id: number) => void,
    setSelectedSuiteForTreeView: (suite: treeSuite) => void,
    selectedSuiteForTreeView: treeSuite
}

const CreationCase: React.FC<Props> = ({
                                           show,
                                           setShow,
                                           selectedSuiteCome,
                                           infoCaseForEdit,
                                           setInfoCaseForEdit,
                                           setDetailedCaseInfo,
                                           detailedCaseInfo,
                                           setLastEditCase,
                                           setSelectedSuiteForTreeView,
                                           selectedSuiteForTreeView
                                       }) => {
    const classes = useStyles()
    const [selectedSuite, setSelectedSuite] = useState<{ id: number; name: string }>({
        id: selectedSuiteForTreeView.id,
        name: selectedSuiteForTreeView.name,
    })

    const [name, setName] = useState("")
    const [namePresence, setNamePresence] = useState(false)

    const [estimate, setEstimate] = useState("")
    const [estimateNumber, setEstimateNumber] = useState<number | null>(null)

    const [scenario, setScenario] = useState("")
    const [scenarioPresence, setScenarioPresence] = useState(false)

    const [fillFieldName, setFillFieldName] = useState(false)
    const [fillFieldScenario, setFillFieldScenario] = useState(false)

    const [description, setDescription] = useState("")
    const [setup, setSetup] = useState("")
    const [teardown, setTeardown] = useState("")

    const [suitesForSelect, setSuitesForSelect] = useState<{ id: number, name: string }[] | treeSuite[]>([])

    const [filesSelected, setFilesSelected] = React.useState<File[]>()

    useEffect(() => {
        const suitesForSelect: { id: number, name: string }[] = []
        const fillSuitesForSelect = (childrenSuitesArr: treeSuite[]) => {
            childrenSuitesArr.forEach((suite) => {
                suitesForSelect.push({id: suite.id, name: suite.name})
                if (suite.children.length > 0) {
                    fillSuitesForSelect(suite.children)
                }
            })
        }
        suitesForSelect.push({id: selectedSuiteForTreeView.id, name: selectedSuiteForTreeView.name})
        fillSuitesForSelect(selectedSuiteForTreeView.children)
        setSuitesForSelect(suitesForSelect)
        if (selectedSuiteCome) {
            setSelectedSuite(selectedSuiteCome)
        }
        if (infoCaseForEdit) {
            setName(infoCaseForEdit.name)
            setNamePresence(true)
            setScenario(infoCaseForEdit.scenario)
            setDescription(infoCaseForEdit.description)
            setScenarioPresence(true)
            setSetup(infoCaseForEdit.setup)
            setTeardown(infoCaseForEdit.teardown)
            if (infoCaseForEdit.estimate) {
                setEstimate(infoCaseForEdit.estimate.toString())
                setEstimateNumber(infoCaseForEdit.estimate)
            }
        }
    }, [selectedSuiteCome, selectedSuiteForTreeView, infoCaseForEdit])

    const handleClose = () => {
        setShow(false)
        setName("")
        setDescription("")
        setNamePresence(false)
        setScenario("")
        setScenarioPresence(false)
        setEstimate("")
        setEstimateNumber(null)
        setFillFieldName(false)
        setFillFieldScenario(false)
        setSetup("")
        setTeardown("")
        setInfoCaseForEdit(null)
        setFilesSelected([])
    }

    const onChangeEstimateContent = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        const strInput = e.target.value
        if (strInput.charCodeAt(strInput.length - 1) >= 48 && strInput.charCodeAt(strInput.length - 1) <= 57) {
            setEstimate(strInput)
            setEstimateNumber(parseInt(strInput, 10))
        } else if (strInput.length === 0) {
            setEstimate("")
            setEstimateNumber(null)
        }
    }


    const onChangeRequiredField = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
                                   setField: (value: string) => void,
                                   setFieldPresence: (value: boolean) => void,
                                   setFillField: (value: boolean) => void) => {
        let str = e.target.value.trimStart()
        if (str.length > 0) {
            setField(str)
            setFieldPresence(true)
            setFillField(false)
        } else {
            setField(str)
            setFieldPresence(false)
        }
    }

    const onChangeNonRequiredField = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, setField: (value: string) => void) => {
        let str = e.target.value
        setField(str)
    }

    const createCase = () => {
        const projectId = localStorageTMS.getCurrentProject().id
        if (namePresence && scenarioPresence && projectId) {
            const myCase = {
                name: name,
                project: projectId,
                suite: selectedSuite.id,
                scenario: scenario,
                estimate: estimateNumber,
                teardown: teardown,
                description: description,
                setup: setup,
                attachments: []
            }
            if (infoCaseForEdit) {
                SuiteCaseService.editCase({...myCase, url: infoCaseForEdit.url, id: infoCaseForEdit.id}).then(() => {
                    AttachmentService.postAttachments(filesSelected, infoCaseForEdit.id, 11)
                        .then(() => {
                        })
                        .catch((e) => {
                            console.log(e)
                        });

                    SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                        setSelectedSuiteForTreeView(response.data)
                    }).catch((e) => {
                        console.log(e)
                    })
                }).catch((e) => {
                    console.log(e)
                })
                if (infoCaseForEdit.id === detailedCaseInfo.myCase.id && detailedCaseInfo.show) {
                    setLastEditCase(infoCaseForEdit.id)
                    setDetailedCaseInfo({show: true, myCase: {...myCase, id: infoCaseForEdit.id}})
                }
            } else {
                SuiteCaseService.createCase(myCase).then((response) => {
                    AttachmentService.postAttachments(filesSelected, response.data.id, 11)
                        .then(() => {
                        })
                        .catch((e) => {
                            console.log(e)
                        });

                    SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                        setSelectedSuiteForTreeView(response.data)
                    }).catch((e) => {
                        console.log(e)
                    })
                }).catch((e) => {
                    console.log(e)
                })
            }
            handleClose()
        } else if (!namePresence && !scenarioPresence) {
            document.getElementById("nameCaseTextField")?.focus();
            setFillFieldName(true)
            setFillFieldScenario(true)
        } else if (!namePresence) {
            document.getElementById("nameCaseTextField")?.focus();
            setFillFieldName(true)
        } else if (!scenarioPresence) {
            document.getElementById("scenarioCaseTextField")?.focus();
            setFillFieldScenario(true)
        }
    }

    const chooseSuite = (e: any) => {
        setSelectedSuite({id: e.target.value.id, name: e.target.value.name})
    }

    const MenuProps = {
        PaperProps: {
            style: {
                maxHeight: "30%",
                maxWidth: "10%",
                overflow: "auto"
            },
        },
    };

    return (
        <Dialog
            disableEnforceFocus
            open={show}
            onClose={handleClose}
            classes={{paper: classes.paperCreationTestCase}}
        >
            <Grid container style={{
                position: "absolute",
                height: "100%",
                width: "100%"
            }}>
                <Grid xs={9} item style={{padding: 20}}>
                    <Grid>
                        <Typography variant="h6">
                            Название тест-кейса
                        </Typography>
                        <CustomWidthTooltip
                            title={<Grid data-cy="fill-field-note"
                                         style={{display: "flex", flexDirection: 'row'}}><WarningAmberIcon
                                sx={{fontSize: 25, marginRight: 1}}/> <Typography> Заполните это
                                поле.</Typography></Grid>} placement="top-start" arrow
                            open={fillFieldName}>
                            <TextField
                                id="nameCaseTextField"
                                className={classes.textFieldSelectCreationCaseSuite}
                                onChange={(content) => onChangeRequiredField(content, setName, setNamePresence, setFillFieldName)}
                                variant="outlined"
                                value={name}
                                margin="normal"
                                autoComplete="off"
                                required
                                fullWidth
                                label="Введите название тест-кейса"
                            />
                        </CustomWidthTooltip>
                    </Grid>

                    <Grid className={classes.gridContent}>
                        <Typography variant="h6">
                            Сценарий
                        </Typography>
                        <CustomWidthTooltip
                            title={<Grid data-cy="fill-field-note"
                                         style={{display: "flex", flexDirection: 'row'}}><WarningAmberIcon
                                sx={{fontSize: 25, marginRight: 1}}/> <Typography> Заполните это
                                поле.</Typography></Grid>} placement="top-start" arrow
                            open={fillFieldScenario}>
                            <TextField
                                id="scenarioCaseTextField"
                                className={classes.textFieldSelectCreationCaseSuite}
                                onChange={(content) => onChangeRequiredField(content, setScenario, setScenarioPresence, setFillFieldScenario)}
                                variant="outlined"
                                value={scenario}
                                margin="normal"
                                fullWidth
                                required
                                label="Введите сценарий тест-кейса"
                                autoComplete="off"
                                multiline
                                minRows={2}
                                maxRows={3}
                            />
                        </CustomWidthTooltip>
                    </Grid>
                    <Grid className={classes.gridContent}>
                        <Typography variant="h6">
                            Описание
                        </Typography>

                        <TextField
                            id="caseDescription"
                            className={classes.textFieldSelectCreationCaseSuite}
                            onChange={(content) => onChangeNonRequiredField(content, setDescription)}
                            variant="outlined"
                            value={description}
                            margin="normal"
                            fullWidth
                            label="Введите описание тест-кейса"
                            autoComplete="off"
                            multiline
                            minRows={2}
                            maxRows={3}
                        />
                    </Grid>
                    <Grid className={classes.gridContent}>
                        <Typography variant="h6">
                            Подготовка теста
                        </Typography>

                        <TextField
                            id="case-setup"
                            className={classes.textFieldSelectCreationCaseSuite}
                            onChange={(content) => onChangeNonRequiredField(content, setSetup)}
                            variant="outlined"
                            value={setup}
                            margin="normal"
                            fullWidth
                            label="Введите инструкции"
                            autoComplete="off"
                            multiline
                            minRows={2}
                            maxRows={3}
                        />
                    </Grid>
                    <Grid className={classes.gridContent}>
                        <Typography variant="h6">
                            Очистка после теста
                        </Typography>
                        <TextField
                            id="case-teardown"
                            className={classes.textFieldSelectCreationCaseSuite}
                            onChange={(content) => onChangeNonRequiredField(content, setTeardown)}
                            variant="outlined"
                            value={teardown}
                            margin="normal"
                            fullWidth
                            label="Введите инструкции"
                            autoComplete="off"
                            multiline
                            minRows={2}
                            maxRows={3}
                        />
                    </Grid>
                </Grid>
                <Grid xs={3} item style={{
                    backgroundColor: "#eeeeee", paddingTop: 26, display: "flex",
                    flexDirection: "column", justifyContent: "space-between"
                }}>
                    <Grid style={{marginLeft: 15}}>
                        <Grid style={{marginBottom: 34}}>
                            <Typography style={{marginBottom: 10}}>
                                Сьюта
                            </Typography>

                            <FormControl required style={{minWidth: "90%"}}
                                         className={classes.textFieldSelectCreationCaseSuite}>
                                <InputLabel id="select-suite">Выберите
                                    сьюту</InputLabel>
                                <Select
                                    data-cy="select-parent-suite-for-case"
                                    labelId="select-suite"
                                    value={selectedSuite.name}
                                    label="Выберите сьюту"
                                    onChange={(e) => chooseSuite(e)}
                                    renderValue={(selected) => <Grid>{selected}</Grid>}
                                    MenuProps={MenuProps}
                                >
                                    {suitesForSelect.map((suite, index) => <MenuItem key={index}
                                                                                     value={suite as any}>{suite.name}</MenuItem>)}
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid style={{marginBottom: 34}}>
                            <Typography>
                                Время выполнения
                            </Typography>
                            <TextField
                                id="case-time-run"
                                value={estimate}
                                style={{marginTop: 10}}
                                className={classes.textFieldSelectCreationCaseSuite}
                                onChange={(content) => onChangeEstimateContent(content)}
                                variant="outlined"
                                margin="normal"
                                autoComplete="off"
                                fullWidth
                                label="Введите время"
                            />
                        </Grid>
                        <Grid>
                            <AttachmentButton setFilesSelected={setFilesSelected}/>
                        </Grid>
                    </Grid>
                    <Grid style={{textAlign: "center"}}>
                        <Grid>
                            <Button
                                data-cy="disagree-to-save-case"
                                onClick={handleClose} style={{
                                margin: "0px 4px 20px 5px",
                                width: "45%",
                                minWidth: 100,
                                height: "45%",
                                backgroundColor: "#FFFFFF",
                                color: "#000000",
                            }}
                            >
                                Отменить
                            </Button>
                            <Button
                                onClick={createCase}
                                data-cy="agree-to-save-case"
                                style={{
                                    margin: "0px 5px 20px 4px",
                                    width: "45%",
                                    minWidth: 100,
                                    height: "45%",
                                    backgroundColor: "#696969",
                                    color: "#FFFFFF",
                                }}
                            >
                                Сохранить
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Dialog>
    );
}

export default CreationCase