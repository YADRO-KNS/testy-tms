import React, {useEffect, useState} from "react";
// import MDEditor from '@uiw/react-md-editor';
import {attachment, test, user} from "../models.interfaces";
import Chip from "@mui/material/Chip";
import FormControl from "@mui/material/FormControl";
import Grid from "@mui/material/Grid";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import TableCell from "@mui/material/TableCell";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import CloseIcon from "@mui/icons-material/Close";
import moment from "moment";
import useStyles from "./styles.testplans";
import TestPlanService from "../../services/testplan.service";
import {defaultStatus, statuses} from "../model.statuses";
import ProfileService from "../../services/profile.service";
import Attachments from "../attachment/attachments";
import AttachmentButton from "../attachment/attachment_button";
import AttachmentService from "../../services/attachment.servise";
import MDEditor from "@uiw/react-md-editor";
import {Editor} from "@toast-ui/react-editor";
import SuiteCaseService from "../../services/suite.case.service";

interface Props {
    detailedTestInfo: { show: boolean, test: test };
    setDetailedTestInfo: (data: { show: boolean, test: test }) => void;
    showEnterResult: boolean;
    setShowEnterResult: (show: boolean) => void
}

const DetailedTestInfo: React.FC<Props> = ({
                                               detailedTestInfo,
                                               setDetailedTestInfo,
                                               showEnterResult,
                                               setShowEnterResult
                                           }) => {
    const classes = useStyles()
    const [scenario, setScenario] = useState<string>()
    const [description, setDescription] = useState<string>()
    const [estimate, setEstimate] = useState<number>()
    const [setup, setSetup] = useState<string>()
    const [teardown, setTeardown] = useState<string>()
    const [selectedStatus, setSelectedStatus] = useState<{ id: number, name: string } | null>(null)
    const [attachments, setAttachments] = React.useState<Map<number, attachment[]>>(new Map())
    const [filesSelected, setFilesSelected] = React.useState<File[]>()
    const [value, setValue] = useState("")
    const [num, setNum] = useState<number>()
    const [names, setNames] = useState<Map<number, string>>(new Map())
    const test = detailedTestInfo.test
    const editorRef = React.createRef();

    const onChangeExecutionTime = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        let num = Number(e.target.value)
        setNum(num)
    }

    useEffect(() => {
        new Promise<[Map<number, string>, Map<number, attachment[]>]>(async (resolve) => {
            const namesMap: Map<number, string> = new Map()
            const attachmentsMap: Map<number, attachment[]> = new Map()
            await Promise.all(test.test_results.map(async (result) => {
                if (!result.user_full_name) {
                    await ProfileService.getUser(result.user).then((response) => {
                        const user: user = response.data
                        namesMap.set(result.id, user.username)
                    })
                        .catch((e) => {
                            console.log(e)
                        })
                } else {
                    namesMap.set(result.id, result.user_full_name)
                }
                const response = await TestPlanService.getTestResult(result.id)
                attachmentsMap.set(result.id, response.data.attachments)
            }))
            resolve([namesMap, attachmentsMap])
        }).then(([namesMap, attachmentsMap]) => {
            setNames(namesMap)
            setAttachments(attachmentsMap)
        }).catch((e) => {
            console.log(e)
        })
    }, [detailedTestInfo, test.test_results])

    useEffect(() => {
        SuiteCaseService.getCaseById(test.case).then(response => {
            setScenario(response.data.scenario)
            setDescription(response.data.description)
            setEstimate(response.data.estimate)
            setSetup(response.data.setup)
            setTeardown(response.data.teardown)
        })
    }, [test.case])

    const handleShowEnterResult = () => setShowEnterResult(true)
    const chooseStatus = (e: any) => {
        setSelectedStatus({id: e.target.value.id, name: e.target.value.name})
    }

    const handleClose = () => {
        setNum(0)
        setValue("")
        setSelectedStatus(null)
        setShowEnterResult(false)
        setFilesSelected([])
    }

    const createTestResult = () => {
        let statusId = selectedStatus ? selectedStatus.id : test.last_status_color.id
        // @ts-ignore
        let comment = editorRef.current.editorInst.getMarkdown()
        const testResult = {
            status: statusId,
            comment: comment ?? null,
            execution_time: num ? num : null,
            test: test.id
        }
        TestPlanService.createTestResult(testResult).then((response) => {
            AttachmentService.postAttachments(filesSelected, response.data.id, 14).then(() =>
                TestPlanService.getAllTestResults(test.id).then((response) => {
                    test.test_results = response.data
                    let status = statuses.find(i => i.id === statusId)
                    test.last_status_color = status ? status : defaultStatus
                    test.test_results.forEach(y => {
                        let status = statuses.find(i => i.id === y.status)
                        y.status_color = status ? status : defaultStatus
                    })
                    setDetailedTestInfo({show: true, test: test})
                })
                    .catch((e) => {
                        console.log(e)
                    })
            )
        })
            .catch((e) => {
                console.log(e);
            });
        handleClose()
    }

    return (
        <div className={classes.divTestInfo}>
            <div className={classes.divTestInfoTitle}>
                <Grid container spacing={3}>
                    <Grid item>
                        <Typography variant="h5">
                            {test.id}
                        </Typography>
                    </Grid>
                    <Grid item>
                        <Typography variant="h5">
                            {test.name}
                        </Typography>
                    </Grid>
                </Grid>
                <IconButton size={"small"} onClick={() => setDetailedTestInfo({show: false, test: test})}>
                    <CloseIcon/>
                </IconButton>
            </div>
            <Grid container spacing={1}>
                <Grid item sx={{fontWeight: 'bold'}}>
                    Дата создания:
                </Grid>
                <Grid item>
                    {moment(test.created_at, 'YYYY-MM-DDTHH:mm').format('DD/MM/YYYY HH:mm')}
                </Grid>
            </Grid>
            <Grid container spacing={1}>
                <Grid item sx={{fontWeight: 'bold'}}>
                    Назначенный пользователь:
                </Grid>
                <Grid item>
                    {test.username ?? "не назначен"}
                </Grid>
            </Grid>
            {description &&
            (<div>
                <div className={classes.divBold}>
                    Описание:
                </div>
                <div>
                    <MDEditor.Markdown source={description} style={{whiteSpace: 'pre-wrap'}}/>
                </div>
            </div>)}
            {setup &&
            (<div>
                <div className={classes.divBold}>
                    Подготовка теста:
                </div>
                <div>
                    <MDEditor.Markdown source={setup} style={{whiteSpace: 'pre-wrap'}}/>
                </div>
            </div>)}
            {teardown &&
            (<div>
                <div className={classes.divBold}>
                    Очистка после теста:
                </div>
                <div>
                    <MDEditor.Markdown source={teardown} style={{whiteSpace: 'pre-wrap'}}/>
                </div>
            </div>)}
            {estimate &&
            (<Grid container spacing={2}>
                <Grid item sx={{fontWeight: 'bold'}}>
                    Ожидаемое время выполнения:
                </Grid>
                <Grid item>
                    <MDEditor.Markdown source={estimate.toString()} style={{whiteSpace: 'pre-wrap'}}/>
                </Grid>
            </Grid>)}

            <div className={classes.divBold}>
                Сценарий:
            </div>
            <div className={classes.divTestInfoScenario}>
                <MDEditor.Markdown source={scenario} style={{whiteSpace: 'pre-wrap'}}/>
            </div>

            <Grid container spacing={1}>
                <Grid item sx={{fontWeight: 'bold', paddingTop: 0}}>
                    Результат:
                </Grid>
                {showEnterResult ?
                    <Grid item>
                        <FormControl size="small">
                            <Select
                                value={selectedStatus ? selectedStatus.name : test.last_status_color.name}
                                onChange={(e) => chooseStatus(e)}
                                autoFocus={true}
                                renderValue={(selected) => <Grid>{selected}</Grid>}>
                                {statuses.map((status, index) => <MenuItem key={index}
                                                                           value={status as any}>{status.name}</MenuItem>)}
                            </Select>
                        </FormControl>
                    </Grid>
                    :
                    <Grid item>
                        <Chip label={test.last_status_color.name}
                              sx={{
                                  margin: "3px",
                                  maxWidth: "95%",
                                  backgroundColor: test.last_status_color.color,
                                  color: "white"
                              }}/>
                    </Grid>}

            </Grid>
            {showEnterResult && (
                <div>
                    <div className={classes.divBold}>
                        Комментарии:
                    </div>
                    {/*<TextField*/}
                    {/*    id="enterResultTextField"*/}
                    {/*    className={classes.textFieldTestplansAndTests}*/}
                    {/*    onChange={(content) => onChangeComment(content)}*/}
                    {/*    variant="outlined"*/}
                    {/*    value={comment}*/}
                    {/*    margin="normal"*/}
                    {/*    autoComplete="off"*/}
                    {/*    fullWidth*/}
                    {/*    multiline*/}
                    {/*    minRows={2}*/}
                    {/*    maxRows={3}*/}
                    {/*    label="Введите комментарии к результату теста"*/}
                    {/*/>*/}
                    {/*<div className="container" style={{marginTop: "2px", marginBottom: "10px"}}>*/}
                    {/*    <MDEditor*/}
                    {/*        value={value}*/}
                    {/*        onChange={(str) => setValue(str ? str : "")}*/}
                    {/*    />*/}
                    {/*</div>*/}
                    <div className="container" style={{marginTop: "2px", marginBottom: "10px"}}>
                        <Editor
                            ref={editorRef}
                            initialValue={value}
                            height="200px"
                            autoFocus={false}
                            useCommandShortcut={true}
                            usageStatistics={false}
                            hideModeSwitch={true}
                            extendedAutolinks={true}
                            toolbarItems={[
                                ['heading', 'bold', 'italic', 'quote', 'code', 'codeblock', 'link', 'ul', 'ol', 'task']
                            ]}
                        />
                    </div>
                    <Grid container spacing={1}>
                        <Grid item sx={{fontWeight: 'bold'}}>
                            Время выполнения:
                        </Grid>
                        <Grid item>
                            <TextField
                                type="number"
                                id="executionTimeTextField"
                                size="small"
                                InputProps={{inputProps: {min: 0}}}
                                onChange={(content) => onChangeExecutionTime(content)}
                                value={num}
                                autoComplete="off"
                            />
                        </Grid>
                    </Grid>
                    <AttachmentButton setFilesSelected={setFilesSelected}/>
                </div>
            )}
            <Grid sx={{
                marginTop: 1,
                marginBottom: 3
            }}>
                <Button variant="outlined" sx={{
                    borderColor: "#000000",
                    minWidth: "20%",
                    height: "33%",
                    backgroundColor: "#696969",
                    color: "#FFFFFF",
                    "&:hover": {
                        backgroundColor: "#939393",
                        borderColor: "#000000",
                    }
                }} onClick={showEnterResult ? createTestResult : handleShowEnterResult}>
                    {showEnterResult ? "Сохранить" : "Внести результат"}
                </Button>
                {showEnterResult && <Button variant="outlined" sx={{
                    borderColor: "#000000",
                    minWidth: "20%",
                    height: "33%",
                    backgroundColor: "#FFFFFF",
                    marginLeft: "3%",
                    color: "#000000",
                    "&:hover": {
                        backgroundColor: "#eeeeee",
                        borderColor: "#000000",
                    }
                }} onClick={() => setShowEnterResult(false)}>
                    Отмена
                </Button>}
            </Grid>
            {test.test_results.length !== 0 &&
            (<div>
                <div className={classes.divBold}>
                    Предыдущие результаты:
                </div>
                <table>
                    <tbody>
                    {test.test_results.map((testResult, index) =>
                        <tr key={index}>
                            <TableCell sx={{maxWidth: "max-content", paddingTop: 0}}>
                                <div>
                                    <Grid item>
                                        <Chip label={testResult.status_color.name}
                                              sx={{
                                                  margin: "3px",
                                                  maxWidth: "95%",
                                                  backgroundColor: testResult.status_color.color,
                                                  color: "white"
                                              }}/>
                                    </Grid>
                                    <Grid item>
                                        {moment(testResult.updated_at, 'YYYY-MM-DDTHH:mm').format('DD/MM/YY HH:mm')}
                                    </Grid>
                                    <Grid item sx={{fontWeight: 'bold', wordBreak: "break-word"}}>
                                        {names.get(testResult.id) ?? ""}
                                    </Grid>

                                </div>
                            </TableCell>

                            <TableCell align="left" sx={{verticalAlign: 'top', paddingTop: "9px"}}>
                                <div className={classes.divBold}>
                                    Комментарий:
                                </div>
                                <MDEditor.Markdown source={testResult?.comment} style={{whiteSpace: 'pre-wrap'}}/>
                                <Attachments attachments={attachments.get(testResult.id)}/>
                            </TableCell>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>)}
        </div>
    )
}

export default DetailedTestInfo