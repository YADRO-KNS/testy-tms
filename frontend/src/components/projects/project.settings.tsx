import AddCircleIcon from "@mui/icons-material/AddCircle";
import {Chip, Dialog, InputAdornment, TextField} from "@mui/material";
import React, {ChangeEvent, useState} from "react";
import useStyles from "../../styles/styles";
import ProjectService from "../../services/project.service";
import SuiteCaseService from "../../services/suite.case.service";
import {XMLParser} from "fast-xml-parser";
import {suite} from "../testcases/suites.component";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import localStorageTMS from "../../services/localStorageTMS";
import {project} from "../models.interfaces";

interface Props {
    show: boolean;
    setShow: (show: boolean) => void
}

interface Node {
    label: string;
    value: string;
    children?: Array<Node>;
    disabled?: boolean;
    icon?: boolean
    showCheckbox?: boolean;
}

const ProjectSettings: React.FC<Props> = ({show, setShow}) => {
    const classes = useStyles()

    const [statusInput, setStatusInput] = useState("")
    const [status, setStatus] = useState("")
    const [statusPresence, setStatusPresence] = useState(false)
    const defaultStatuses: { name: string, color: string }[] = [
        {name: 'PASSED', color: '#24b124'}, {name: 'SKIPPED', color: '#c4af30'}, {name: 'FAILED', color: '#bd2828'},
        {name: 'RETEST', color: '#6c6c6c'}, {name: 'UNTESTED', color: '#a5a4a4'}]
    const [statuses, setStatuses] = useState<string[]>([])

    const [link, setLink] = useState("")
    const [links, setLinks] = useState<string []>([])
    const [linkPresence, setLinkPresence] = useState(false)
    const projectValue = localStorageTMS.getCurrentProject()
    const [projectName, setProjectName] = useState(projectValue.name)

    const [projectDescription, setProjectDescription] = React.useState(projectValue.description)

    const onChangeProjectName = (e: React.ChangeEvent<HTMLInputElement>) => {
        setProjectName(e.target.value)
    }

    const onChangeProjectDescription = (e: React.ChangeEvent<HTMLInputElement>) => {
        setProjectDescription(e.target.value)
    }

    const handleClose = () => {
        setProjectName(projectValue.name)
        setProjectDescription(projectValue.description)
        setStatus("")
        setStatusInput("")
        setStatuses([])
        setStatusPresence(false)
        setLink("")
        setLinkPresence(false)
        setLinks([])
        setShow(false)
    }

    const handlePatch = () => {
        ProjectService.patchProject({name: projectName, description: projectDescription}, projectValue.id)
            .then(r => {
            });
        setStatus("")
        setStatusInput("")
        setStatuses([])
        setStatusPresence(false)
        setLink("")
        setLinkPresence(false)
        setLinks([])
        setShow(false)
    }

    const handleDelete = (index: number) => {
        let oldStatuses = statuses.slice()
        oldStatuses.splice(index, 1)
        setStatuses(oldStatuses)
    }

    const handleDeleteLink = (index: number) => {
        let oldLinks = links.slice()
        oldLinks.splice(index, 1)
        setLinks(oldLinks)
    }

    const createStatus = () => {
        setStatuses((prevState) => (prevState.concat([status])))
        setStatusPresence(false)
        setStatusInput("")
    }

    const createLink = () => {
        setLinks((prevState) => (prevState.concat([link])))
        setLinkPresence(false)
        setLink("")
    }

    const keyPress = (e: React.KeyboardEvent<HTMLDivElement>) => {
        if (e.key === "Enter" && statusPresence) {
            createStatus()
        }
    }

    const keyPressLink = (e: React.KeyboardEvent<HTMLDivElement>) => {
        if (e.key === "Enter" && linkPresence) {
            createLink()
        }
    }

    const onChangeStatusContent = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        const strInput = e.target.value.trimStart().replace(/ {2,}/g, ' ')
        const status = strInput.trimEnd()
        if (status.length > 0) {
            setStatus(status)
            setStatusInput(strInput)
            setStatusPresence(true)
        } else {
            setStatusInput(strInput)
            setStatusPresence(false)
        }
    }

    const onChangeLinkContent = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        const strInput = e.target.value.trim()
        if (strInput.length > 0) {
            setLink(strInput)
            setLinkPresence(true)
        } else {
            setLink(strInput)
            setLinkPresence(false)
        }
    }

    const parser = new XMLParser();
    const getDescription = (custom: any) => `Preconditions: ${custom['preconds']} \n
    Steps: ${custom['steps']} \n
    Expected: ${custom['expected']}`

    const loadCases = (cases: any, suiteId: number) => {
        let allCases = [cases["case"]]
        if (Symbol.iterator in Object(cases["case"])) {
            allCases = cases["case"]
        }
        Array.prototype.forEach.call(allCases, (testCase: { [key: string]: string; }) => {
            const description = getDescription(testCase["custom"])
            const newCase = {
                name: testCase["title"],
                suite: suiteId,
                project: projectValue.id,
                scenario: description !== "" ? description : "Nothing"
            }
            SuiteCaseService.createCase(newCase).catch(e => console.log(e))
        })
    }
    const loadSuites = (sections: any, parentId: number | null) => {
        let allSections = [sections["section"]]
        if (Symbol.iterator in Object(sections["section"])) {
            allSections = sections["section"]
        }
        Array.prototype.forEach.call(allSections, (section: { [key: string]: string; }) => {
            const suite = {
                name: section["name"],
                parent: parentId,
                project: projectValue.id,
            }
            let suiteId = 0;
            SuiteCaseService.createSuite(suite).then(() => {
                SuiteCaseService.getSuites().then((response) => {
                    const allSuites: suite[] = response.data
                    allSuites.sort((a, b) => b.id - a.id)
                    suiteId = allSuites.find((suite) => suite.name === section["name"])?.id ?? suiteId
                    loadCases(section["cases"], suiteId)
                    console.log(section["name"], section["sections"])
                    if (!section["sections"]) return;
                    loadSuites(section["sections"], suiteId)
                })

            }).catch(e => console.log(e))
        })
    }
    const handleLoadTestCases = (event: ChangeEvent<HTMLInputElement>) => {
        if (!event.target.files) return;
        const uploadedFile = event.target.files[0];

        event.preventDefault()
        const reader = new FileReader()
        if (!uploadedFile) return;
        reader.readAsText(uploadedFile)
        reader.onload = function () {
            if (!reader.result) return;
            const suite = parser.parse(reader.result.toString().replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", ""))["suite"]
            loadSuites(suite["sections"], null)
        };
        reader.onerror = function () {
            console.log(reader.error);
        };
    }

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
                    <div style={{display: 'flex', flexDirection: 'row'}}>
                        <div style={{width: "11%", minWidth: 120, paddingRight: "3%", paddingLeft: "2%"}}>
                            <Typography variant="h6" style={{paddingTop: "24px"}}>
                                Название
                            </Typography>
                        </div>

                        <TextField
                            className={classes.textFieldSelectCreationCaseSuite}
                            style={{paddingRight: "8%"}}
                            variant="outlined"
                            margin="normal"
                            fullWidth
                            id="projectNameEdit"
                            value={projectName}
                            label="Изменить название проекта"
                            onChange={onChangeProjectName}
                        />
                    </div>

                    <div style={{display: 'flex', flexDirection: 'row'}}>
                        <div style={{width: "11%", minWidth: 120, paddingRight: "3%", paddingLeft: "2%"}}>
                            <Typography variant="h6" style={{paddingTop: "24px"}}>
                                Описание
                            </Typography>
                        </div>

                        <TextField
                            className={classes.textFieldSelectCreationCaseSuite}
                            style={{paddingRight: "8%"}}
                            variant="outlined"
                            margin="normal"
                            fullWidth
                            id="projectDescriptionEdit"
                            value={projectDescription}
                            label="Изменить описание проекта"
                            multiline
                            minRows={2}
                            maxRows={5}
                            onChange={onChangeProjectDescription}
                        />
                    </div>

                    <div style={{display: 'flex', flexDirection: 'row'}}>
                        <div style={{width: "11%", minWidth: 120, paddingRight: "3%", paddingLeft: "2%"}}>
                            <Typography variant="h6"
                                        style={{
                                            paddingTop: "14px"
                                        }}>
                                Статусы результатов
                            </Typography>
                        </div>

                        <TextField
                            value={statusInput}
                            onChange={(content) => onChangeStatusContent(content)}
                            className={classes.textFieldSelectCreationCaseSuite}
                            style={{paddingRight: "8%"}}
                            variant="outlined"
                            margin="normal"
                            fullWidth
                            disabled
                            label="Введите новый статус"
                            onKeyPress={(key) => keyPress(key)}
                            InputProps={{
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <IconButton size={"small"} onClick={() => {
                                            if (statusPresence) {
                                                createStatus()
                                            }
                                        }}>
                                            <AddCircleIcon fontSize={"large"}/>
                                        </IconButton>
                                    </InputAdornment>
                                ),
                            }}
                        />
                    </div>
                    <div style={{display: 'flex', flexDirection: 'row'}}>
                        <div style={{width: "11%", minWidth: 120, paddingRight: "3%", paddingLeft: "2%"}}/>
                        <div style={{width: "76%"}}>
                            <Grid className={classes.stackTags}>
                                {defaultStatuses.map((status, index) =>
                                    <Chip key={index} label={status.name}
                                          style={{
                                              margin: 3,
                                              maxWidth: "95%",
                                              backgroundColor: status.color,
                                              color: "white"
                                          }}/>
                                )}
                                {statuses.map((status, index) =>
                                    <Chip key={index} label={status} style={{margin: 3, maxWidth: "95%"}}
                                          onDelete={() => handleDelete(index)}/>
                                )}
                            </Grid>
                        </div>
                    </div>
                    <div style={{marginTop: "50px", display: 'flex', flexDirection: 'row'}}>
                        <div style={{width: "11%", minWidth: 120, paddingRight: "3%", paddingLeft: "2%"}}>
                            <Typography variant="h6"
                                        style={{
                                            paddingTop: "14px"
                                        }}>
                                Импорт тест-кейсов (.xml)
                            </Typography>
                        </div>
                        <Button
                            variant="contained"
                            style={{
                                alignSelf: "center"
                            }}
                            component="label"
                        >
                            Импортировать
                            <input
                                type="file"
                                onChange={handleLoadTestCases}
                                hidden
                            />
                        </Button>
                    </div>
                </Grid>
                <Grid xs={3} item style={{
                    backgroundColor: "#eeeeee", paddingTop: 26, display: "flex",
                    flexDirection: "column", justifyContent: "space-between"
                }}>
                    <div style={{marginLeft: 15}}>
                        <div>
                            <Typography>
                                Участники
                            </Typography>
                            <TextField
                                value={link}
                                onChange={(content) => onChangeLinkContent(content)}
                                style={{marginTop: 10}}
                                className={classes.textFieldSelectCreationCaseSuite}
                                variant="outlined"
                                margin="normal"
                                fullWidth
                                label="Введите имя/почту/ссылку "
                                onKeyPress={(key) => keyPressLink(key)}
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton size={"small"} onClick={() => {
                                                if (linkPresence) {
                                                    createLink()
                                                }
                                            }}>
                                                <AddCircleIcon fontSize={"medium"}/>
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                }}
                            />
                            <Grid className={classes.stackTags}>
                                {links.map((link, index) =>
                                    <Grid>
                                        <Chip key={index} label={link} style={{
                                            margin: 3,
                                            maxWidth: "95%",
                                            color: "#0000FF",
                                            textDecoration: "underline"
                                        }}
                                              onDelete={() => handleDeleteLink(index)}
                                              onClick={() => {
                                                  const url = link.match(/^http[s]?:\/\//) ? link : '//' + link;
                                                  window.open(url, '_blank')
                                              }}
                                        />
                                        <br/>
                                    </Grid>
                                )}
                            </Grid>
                        </div>
                    </div>
                    <Grid>
                        <div style={{marginBottom: 15, textAlign: "center"}}>
                            <Button onClick={handleClose} style={{
                                margin: "0px 5px 5px 5px",
                                minWidth: 100,
                                width: "40%",
                                height: "45%",
                                backgroundColor: "#FFFFFF",
                                color: "#000000",
                            }}
                            >
                                Отменить
                            </Button>
                            <Button data-cy="button-change-project"
                                    onClick={handlePatch} style={{
                                margin: "0px 5px 5px 5px",
                                minWidth: 100,
                                width: "40%",
                                height: "45%",
                                backgroundColor: "#696969",
                                color: "#FFFFFF",
                            }}
                            >
                                Сохранить
                            </Button>
                        </div>
                    </Grid>
                </Grid>

            </Grid>
        </Dialog>
    );
}

export default ProjectSettings