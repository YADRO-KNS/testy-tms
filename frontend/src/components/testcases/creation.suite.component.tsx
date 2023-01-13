import React, {useEffect, useState} from "react";
import useStyles from "../../styles/styles";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import FormControl from "@mui/material/FormControl";
import Grid from "@mui/material/Grid";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import SuiteCaseService from "../../services/suite.case.service";
import {CustomWidthTooltip, treeSuite} from "./suites.component";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";


interface Props {
    show: boolean;
    setShow: (show: boolean) => void;
    selectedSuiteCome: { id: number, name: string } | null
    setTreeSuites: (treeSuites: treeSuite[]) => void
    setSelectedSuiteForTreeView: (suite: treeSuite | undefined) => void,
    selectedSuiteForTreeView: treeSuite | undefined,
    infoSuiteForEdit: { id: number, name: string } | null;
    setInfoSuiteForEdit: (suite: { id: number, name: string } | null) => void,
    treeSuites: treeSuite []
}

const CreationSuite: React.FC<Props> = ({
                                            show,
                                            setShow,
                                            selectedSuiteCome,
                                            setTreeSuites,
                                            setSelectedSuiteForTreeView,
                                            selectedSuiteForTreeView,
                                            infoSuiteForEdit,
                                            setInfoSuiteForEdit,
                                            treeSuites
                                        }) => {
    const classes = useStyles()
    const [selectedSuite, setSelectedSuite] = useState<{ id: number; name: string } | null>(selectedSuiteCome)
    const [name, setName] = useState("")
    const [namePresence, setNamePresence] = useState(false)
    const [fillFieldName, setFillFieldName] = useState(false)
    const [suitesForSelect, setSuitesForSelect] = useState<{ id: number, name: string }[] | treeSuite[]>([])

    const handleClose = () => {
        setShow(false)
        setName("")
        setNamePresence(false)
        setFillFieldName(false)
        setInfoSuiteForEdit(null)
    }

    useEffect(() => {
        setSelectedSuite(selectedSuiteCome)
        if (selectedSuiteForTreeView) {
            const suitesForSelect: { id: number, name: string }[] = []
            const fillSuitesForSelect = (childrenSuitesArr: treeSuite[]) => {
                childrenSuitesArr.map((suite) => {
                    suitesForSelect.push({id: suite.id, name: suite.name})
                    if (suite.children.length > 0) {
                        fillSuitesForSelect(suite.children)
                    }
                })
            }
            suitesForSelect.push({id: selectedSuiteForTreeView.id, name: selectedSuiteForTreeView.name})
            fillSuitesForSelect(selectedSuiteForTreeView.children)
            setSuitesForSelect(suitesForSelect)
        } else {
            setSuitesForSelect(treeSuites)
        }
        if (infoSuiteForEdit) {
            setName(infoSuiteForEdit.name)
            setNamePresence(true)
        }
    }, [selectedSuiteCome, infoSuiteForEdit, treeSuites])

    const chooseSuite = (e: any) => {
        setSelectedSuite(e.target.value ? {id: e.target.value.id, name: e.target.value.name} : null)
    }

    const createSuite = () => {
        const projectId = JSON.parse(localStorage.getItem("currentProject") ?? '{"id" : null}').id
        if (namePresence && projectId) {
            const suite = {
                name: name,
                parent: selectedSuite?.id ?? null,
                project: projectId,
            }

            if (infoSuiteForEdit) {
                SuiteCaseService.editSuite({id: infoSuiteForEdit.id, ...suite}).then(() => {
                    if (selectedSuiteForTreeView === undefined) {
                        SuiteCaseService.getTreeSuites().then((response) => {
                            setTreeSuites(response.data)
                        }).catch((e) => {
                            console.log(e)
                        })
                    } else {
                        SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                            setSelectedSuiteForTreeView(response.data)
                        }).catch((e) => {
                            console.log(e)
                        })
                    }
                }).catch((e) => {
                    console.log(e)
                })
            } else {
                SuiteCaseService.createSuite(suite).then(() => {
                    if (selectedSuiteForTreeView === undefined) {
                        SuiteCaseService.getTreeSuites().then((response) => {
                            setTreeSuites(response.data)
                        }).catch((e) => {
                            console.log(e)
                        })
                    } else {
                        SuiteCaseService.getTreeBySetSuite(selectedSuiteForTreeView.id).then((response) => {
                            setSelectedSuiteForTreeView(response.data)
                        }).catch((e) => {
                            console.log(e)
                        })
                    }
                }).catch((e) => {
                    console.log(e)
                })
            }
            handleClose()
        } else if (!namePresence) {
            document.getElementById("nameTextField")?.focus();
            setFillFieldName(true)
        }
    }

    const onChangeName = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        let str = e.target.value.trimStart()
        if (str.length > 0) {
            setName(str)
            setNamePresence(true)
            setFillFieldName(false)
        } else {
            setName(str)
            setNamePresence(false)
        }
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
            classes={{paper: classes.paperCreationSuite}}
        >
            <Grid
                style={{
                    display: "flex"
                }}
            >
                <Grid container style={{
                    position: "absolute",
                    height: "100%",
                    width: "100%"
                }}>
                    <Grid xs={9} item style={{padding: 20}}>
                        <Grid>
                            <Typography variant="h6">
                                Название сьюты
                            </Typography>

                            <CustomWidthTooltip
                                title={<Grid style={{display: "flex", flexDirection: 'row'}}><WarningAmberIcon
                                    sx={{fontSize: 25, marginRight: 1}}/> <Typography> Заполните это
                                    поле.</Typography></Grid>} placement="top-start" arrow
                                open={fillFieldName}>
                                <TextField
                                    id="nameTextField"
                                    onChange={(content) => onChangeName(content)}
                                    className={classes.textFieldSelectCreationCaseSuite}
                                    variant="outlined"
                                    margin="normal"
                                    required
                                    fullWidth
                                    autoComplete="off"
                                    value={name}
                                    label="Введите название сьюты"
                                />
                            </CustomWidthTooltip>
                        </Grid>
                    </Grid>
                    <Grid xs={3} item style={{
                        backgroundColor: "#eeeeee", paddingTop: 26, display: "flex",
                        flexDirection: "column", justifyContent: "space-between"
                    }}>
                        <Grid style={{marginLeft: 15}}>
                            <Typography style={{marginBottom: 10}}>
                                Родительская сьюта
                            </Typography>

                            <FormControl style={{minWidth: "90%"}} className={classes.textFieldSelectCreationCaseSuite}>
                                <InputLabel id="select-suite">Выберите сьюту</InputLabel>
                                <Select
                                    labelId="select-suite"
                                    value={selectedSuite ? selectedSuite.name : "Не выбрано"}
                                    label="Выберите сьюту"
                                    onChange={(e) => chooseSuite(e)}
                                    renderValue={(selected) => <Grid>{selected}</Grid>}
                                    MenuProps={MenuProps}
                                >
                                    {!selectedSuiteForTreeView && <MenuItem value={null as any}>
                                        <em>Не выбрано</em>
                                    </MenuItem>}
                                    {suitesForSelect.map((suite, index) => <MenuItem key={index}
                                                                                     value={suite as any}>{suite.name}</MenuItem>)}
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid style={{textAlign: "center"}}>
                            <Grid>
                                <Button onClick={handleClose} style={{
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
                                    onClick={createSuite}
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
            </Grid>
        </Dialog>
    )
}

export default CreationSuite