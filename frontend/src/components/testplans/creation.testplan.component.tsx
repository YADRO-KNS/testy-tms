import React, {useEffect, useState} from "react";
import useStyles from "./styles.testplans";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import FormControl from "@mui/material/FormControl";
import Grid from "@mui/material/Grid";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import {AdapterMoment} from "@mui/x-date-pickers/AdapterMoment";
import {DesktopDatePicker, LocalizationProvider} from "@mui/x-date-pickers";
import moment, {Moment} from "moment";
import TestPlanService from "../../services/testplan.service";
import CheckboxTree from 'react-checkbox-tree';
import 'react-checkbox-tree/lib/react-checkbox-tree.css';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxOutlinedIcon from '@mui/icons-material/CheckBoxOutlined';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import FolderCopyOutlinedIcon from '@mui/icons-material/FolderCopyOutlined';
import BlockIcon from '@mui/icons-material/Block';
import {treeSuite} from "../testcases/suites.component";
import {param, testPlan} from "../models.interfaces";
import SuiteCaseService from "../../services/suite.case.service";
import MDEditor from "@uiw/react-md-editor";
import '@toast-ui/editor/dist/toastui-editor.css';
import {Editor, EditorCore, EditorProps} from '@toast-ui/react-editor';
import localStorageTMS from "../../services/localStorageTMS";

interface Props {
    show: boolean;
    setShow: (show: boolean) => void;
    testPlans: testPlan[];
    isForEdit: testPlan | null;
    setIsForEdit: (isForEdit: null) => void;
}

interface Node {
    label: string;
    value: string;
    children?: Array<Node>;
    disabled?: boolean;
    icon?: boolean;
    showCheckbox?: boolean;
    title?: string;
    className?: string;
}

const CreationTestplanComponent: React.FC<Props> = ({
                                                        show,
                                                        setShow,
                                                        testPlans,
                                                        isForEdit,
                                                        setIsForEdit,
                                                    }) => {
    const classes = useStyles()

    const [selectedTestPlan, setSelectedTestPlan] = useState<{ id: number, name: string } | null>(null)

    const [name, setName] = useState("")
    const [message, setMessage] = useState("")
    const [description, setDescription] = useState("")
    const editorRef = React.createRef();

    const [startDate, setStartDate] = useState<Moment | null>(isForEdit ? moment.utc(isForEdit.started_at) : moment.utc())
    const [endDate, setEndDate] = useState<Moment | null>(isForEdit ? moment.utc(isForEdit.due_date) : moment.utc())

    const [params, setParams] = useState<param [] | null>(null)
    const [paramsChecked, setParamsChecked] = useState<Array<string>>([])
    const [paramsExpanded, setParamsExpanded] = useState<Array<string>>([])
    const [disable, setDisable] = useState(false)

    const [treeSuites, setTreeSuites] = useState<treeSuite[]>([])
    const [testsChecked, setTestsChecked] = useState<Array<string>>([])
    const [testsExpanded, setTestsExpanded] = useState<Array<string>>([])
    const [testPlansForSelect, setTestPlansForSelect] = useState<testPlan[]>([])

    useEffect(() => {
        TestPlanService.getParameters().then((response) => {
            const localParams = response.data
            setParams(localParams)
        })
            .catch((e) => {
                console.log(e);
            });
        SuiteCaseService.getTreeSuites().then((response) => {
            setTreeSuites(response.data)
        })
            .catch((e) => {
                console.log(e);
            });
    }, [])

    useEffect(() => {
        if (!isForEdit) return
        setName(isForEdit.name)
        if (isForEdit.parent) {
            const parent = testPlans.find(x => x.id === isForEdit.parent)
            if (parent) {
                setSelectedTestPlan({id: isForEdit.parent, name: parent.title})
            }
        }
        if (isForEdit.parameters) {
            setParamsChecked(isForEdit.parameters.map(x => String(x)))
        }
        setTestsChecked(isForEdit.tests.map(x => String(x.case)))
        setStartDate(moment.utc(isForEdit.started_at))
        setEndDate(moment.utc(isForEdit.due_date))
    }, [isForEdit, testPlans])

    useEffect(() => {
        const projectId = localStorageTMS.getCurrentProject().id
        if (projectId) {
            const newTestPlansForSelect: testPlan[] = []
            testPlans.forEach(testPlan => {
                if (testPlan.project === projectId) {
                    newTestPlansForSelect.push(testPlan)
                }
            })
            setTestPlansForSelect(newTestPlansForSelect)
        }
    }, [testPlans])

    const handleStartDate = (newValue: Moment | null) => {
        setStartDate(newValue);
    };

    const handleEndDate = (newValue: Moment | null) => {
        setEndDate(newValue);
    };

    const handleClose = () => {
        setShow(false)
        setName("")
        setDescription("")
        setStartDate(isForEdit ? moment.utc(isForEdit.started_at) : moment.utc())
        setEndDate(isForEdit ? moment.utc(isForEdit.due_date) : moment.utc())
        setParamsChecked([])
        setParamsExpanded([])
        setDisable(false)
        setTestsChecked([])
        setTestsExpanded([])
        setIsForEdit(null)
        setSelectedTestPlan(null)
    }

    const chooseTestPlan = (e: any) => {
        setSelectedTestPlan({id: e.target.value.id, name: e.target.value.name})
    }

    const onChangeName = (e: React.ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value)
    }

    const labelReduce = (filename: string) => {
        const maxLengthOfName = 35;
        if (filename.length > maxLengthOfName) {
            return filename.slice(0, maxLengthOfName) + "..."
        } else {
            return filename
        }
    }

    function nodesChildren() {
        let arr: Node[] = [];
        params?.forEach((param) => {
            let flag = false
            for (let node in arr) {
                if (arr[node].label === param.group_name) {
                    if (arr[node].children) {
                        arr[node].children?.push({
                            value: String(param.id),
                            label: labelReduce(param.data),
                            disabled: disable,
                            icon: false,
                            className: classes.nodes
                        })
                    }
                    flag = true
                }
            }
            if (!flag) {
                arr.push({
                    value: param.group_name,
                    label: labelReduce(param.group_name),
                    children: [{
                        value: String(param.id),
                        label: labelReduce(param.data),
                        disabled: disable,
                        icon: false
                    }],
                    disabled: disable,
                    className: classes.nodes
                })
            }
        })
        return arr
    }


    const nodes = [{
        value: 'no',
        label: 'Без параметров',
        icon: <BlockIcon fontSize={"small"} className={classes.icons}/>,
        className: classes.nodes
    },
        {
            value: 'all',
            label: 'Все параметры',
            children: nodesChildren(),
            disabled: disable,
            title: "all-parameters",
            className: classes.nodes
        }];

    function testsNodes(treeSuites: treeSuite[]) {
        let arr: Node[] = []
        treeSuites.forEach((suite) => {
            if (suite.children.length !== 0) {
                let children: Node[] = []
                if (suite.test_cases.length !== 0) {
                    suite.test_cases.forEach((test) => children.push({
                        value: String(test.id),
                        label: labelReduce(test.name),
                        icon: false,
                        className: classes.nodes
                    }))
                }
                const temp = testsNodes(suite.children)
                if (temp.length > 0 || suite.test_cases.length !== 0) {
                    children = children.concat(temp)
                    arr.push({
                        value: "s" + suite.id,
                        label: labelReduce(suite.name),
                        children: children,
                        className: classes.nodes
                    })
                }

            } else {
                if (suite.test_cases.length !== 0) {
                    let tests: Node[] = []
                    suite.test_cases.forEach((test) => tests.push({
                        value: String(test.id),
                        label: labelReduce(test.name),
                        icon: false,
                        className: classes.nodes
                    }))
                    arr.push({
                        value: "s" + suite.id,
                        label: labelReduce(suite.name),
                        children: tests,
                        className: classes.nodes
                    })
                }
            }
        })
        return arr
    }

    const createTestPlan = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const projectId = localStorageTMS.getCurrentProject().id
        if (!projectId) return

        let params = []
        if (!paramsChecked.includes('no') && paramsChecked.length !== 0) {
            for (let i of paramsChecked) {
                params.push(Number(i))
            }
        }
        let tests = []
        for (let i of testsChecked) {
            tests.push(Number(i))
        }
        // @ts-ignore
        let desc = editorRef.current.editorInst.getMarkdown()
        const testPlan = {
            name: name,
            description: desc ?? undefined,
            project: projectId,
            parent: selectedTestPlan ? selectedTestPlan.id : undefined,
            test_cases: tests,
            parameters: params,
            started_at: startDate ? startDate.format('YYYY-MM-DDTHH:mm') : "01.01.1970",
            due_date: endDate ? endDate.format('YYYY-MM-DDTHH:mm') : "01.01.1970",
        }
        console.log(testPlan)
        if (isForEdit) {
            TestPlanService.editTestPlan({
                ...testPlan,
                id: isForEdit.id,
                is_archive: isForEdit.is_archive
            }).catch((e) => {
                console.log(e)
                setMessage("Не удалось изменить тест-план")
            })
            window.location.reload()
        } else {
            TestPlanService.createTestPlan(testPlan).then((response) => {
                window.location.assign("/testplans/" + response.data[0].id)
            })
                .catch((e) => {
                    console.log(e);
                    setMessage("Не удалось создать тест-план")
                });
        }
        handleClose()

    }

    const MenuProps = {
        PaperProps: {
            style: {
                maxHeight: "50%",
                maxWidth: "20%",
                overflow: "auto"
            },
        },
    };

    return (
        <Dialog
            disableEnforceFocus
            open={show}
            onClose={handleClose}
            classes={{paper: classes.paperCreation}}
        >
            <form className={classes.formTestPlan}
                  onSubmit={createTestPlan}
            >
                <Grid container sx={{
                    position: "absolute",
                    height: "100%",
                    width: "100%"
                }}>

                    <Grid xs={9} item sx={{padding: "20px"}}>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <div style={{width: "11%", minWidth: 120, paddingRight: "2%", paddingLeft: "2%"}}>
                                <Typography variant="h6" style={{paddingTop: "24px"}}>
                                    Название
                                </Typography>
                            </div>
                            <TextField
                                id="nameTestPlanTextField"
                                className={classes.textFieldTestplansAndTests}
                                style={{paddingRight: "5%"}}
                                onChange={onChangeName}
                                variant="outlined"
                                value={name}
                                margin="normal"
                                autoComplete="off"
                                autoFocus={true}
                                required
                                fullWidth
                                label="Введите название тест-плана"
                            />
                        </div>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <div style={{width: "11%", minWidth: 120, paddingRight: "2%", paddingLeft: "2%"}}>
                                <Typography variant="h6" style={{paddingTop: "10px"}}>
                                    Описание
                                </Typography>
                            </div>
                            <div style={{marginTop: '9px', width: "100%", paddingRight: "5%"}}>
                                {/*<MDEditor
                                    enableScroll={true}
                                    preview={"edit"}
                                    height={120}
                                    maxHeight={240}
                                    value={description}
                                    onChange={(str) => setDescription(str ? str : "")}
                                />*/}
                                {/*Docs: https://github.com/nhn/tui.editor/blob/master/docs/en/extended-autolinks.md#customizing-the-extended-autolinks*/}
                                {/*<link rel="stylesheet" href="https://uicdn.toast.com/editor/latest/toastui-editor.min.css"/>*/}
                                <Editor
                                    ref={editorRef}
                                    initialValue={description}
                                    height="200px"
                                    useCommandShortcut={true}
                                    usageStatistics={false}
                                    hideModeSwitch={true}
                                    extendedAutolinks={true}
                                    toolbarItems={[
                                        ['heading', 'bold', 'italic', 'quote', 'code', 'codeblock', 'link', 'ul', 'ol', 'task']
                                    ]}
                                />
                            {/*    TODO устанавливать ширину?*/}
                            </div>
                        </div>

                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <div style={{width: "11%", minWidth: 120, paddingRight: "1%", paddingLeft: "2%"}}>
                                <Typography variant="h6" style={{paddingTop: "3px"}}>
                                    Параметры
                                </Typography>
                            </div>
                            <FormControl style={{marginTop: '9px', width: "60%"}}
                                         className={classes.textFieldTestplansAndTests}>
                                {nodes[1]?.children?.length !== 0 ? (<CheckboxTree
                                        nodes={nodes}
                                        checked={paramsChecked}
                                        expanded={paramsExpanded}
                                        disabled={isForEdit !== null}
                                        onCheck={(paramsChecked) => {
                                            setParamsChecked(paramsChecked)
                                            if (paramsChecked.find(x => x === 'no')) {
                                                setDisable(true)
                                                setParamsChecked(['no'])
                                                setParamsExpanded([])
                                            } else {
                                                setDisable(false)
                                            }
                                        }}
                                        onExpand={(paramsExpanded) => setParamsExpanded(paramsExpanded)}
                                        showExpandAll={true}
                                        icons={{
                                            check: <CheckBoxOutlinedIcon fontSize={"small"} className={classes.icons}/>,
                                            uncheck: <CheckBoxOutlineBlankIcon fontSize={"small"}
                                                                               className={classes.icons}/>,
                                            halfCheck: <CheckBoxOutlinedIcon fontSize={"small"}
                                                                             style={{color: 'rgba(52, 52, 52, 0.6)'}}/>,
                                            expandClose: <KeyboardArrowRightIcon fontSize={"small"}
                                                                                 className={classes.icons}/>,
                                            expandOpen: <KeyboardArrowUpIcon fontSize={"small"} className={classes.icons}/>,
                                            expandAll: <AddIcon fontSize={"small"} className={classes.icons}
                                                                sx={{marginTop: '6px'}}/>,
                                            collapseAll: <RemoveIcon fontSize={"small"} className={classes.icons}/>,
                                            parentClose: <FolderCopyOutlinedIcon fontSize={"small"}
                                                                                 className={classes.icons}/>,
                                            parentOpen: <FolderCopyOutlinedIcon fontSize={"small"}
                                                                                className={classes.icons}/>,
                                        }}
                                    />) :
                                    (<CheckboxTree nodes={[{
                                        value: 'no',
                                        label: 'Без параметров (необходимо создать параметр)',
                                        disabled: true,
                                        showCheckbox: false,
                                        icon: <BlockIcon fontSize={"small"} className={classes.icons}/>
                                    }]}
                                    />)
                                }

                            </FormControl>
                        </div>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <div style={{width: "11%", minWidth: 120, paddingRight: "1%", paddingLeft: "2%"}}>
                                <Typography variant="h6" style={{paddingTop: "3px"}}>
                                    Тест-кейсы
                                </Typography>
                            </div>
                            <FormControl sx={{marginTop: '9px', width: "60%"}}
                                         className={classes.textFieldTestplansAndTests}>
                                {testsNodes(treeSuites).length !== 0 ? (<CheckboxTree
                                        nodes={testsNodes(treeSuites)}
                                        checked={testsChecked}
                                        expanded={testsExpanded}
                                        onCheck={(testsChecked) => {
                                            setTestsChecked(testsChecked)
                                        }}
                                        onExpand={(testsExpanded) => setTestsExpanded(testsExpanded)}
                                        showExpandAll={true}
                                        icons={{
                                            check: <CheckBoxOutlinedIcon fontSize={"small"} className={classes.icons}/>,
                                            uncheck: <CheckBoxOutlineBlankIcon fontSize={"small"}
                                                                               className={classes.icons}/>,
                                            halfCheck: <CheckBoxOutlinedIcon fontSize={"small"}
                                                                             style={{color: 'rgba(52, 52, 52, 0.6)'}}/>,
                                            expandClose: <KeyboardArrowRightIcon fontSize={"small"}
                                                                                 className={classes.icons}/>,
                                            expandOpen: <KeyboardArrowUpIcon fontSize={"small"}
                                                                             className={classes.icons}/>,
                                            expandAll: <AddIcon fontSize={"small"} className={classes.icons}/>,
                                            collapseAll: <RemoveIcon fontSize={"small"} className={classes.icons}/>,
                                            parentClose: <FolderCopyOutlinedIcon fontSize={"small"}
                                                                                 className={classes.icons}/>,
                                            parentOpen: <FolderCopyOutlinedIcon fontSize={"small"}
                                                                                className={classes.icons}/>,
                                        }}/>) :
                                    (<CheckboxTree nodes={[{
                                        value: 'no_tests',
                                        label: 'Без тестов (необходимо создать тест-кейс)',
                                        disabled: true,
                                        showCheckbox: false,
                                        icon: <BlockIcon fontSize={"small"} className={classes.icons}/>
                                    }]}
                                    />)
                                }
                            </FormControl>
                        </div>
                    </Grid>

                    <Grid xs={3} item style={{
                        backgroundColor: "#eeeeee", paddingTop: 26, display: "flex",
                        flexDirection: "column", justifyContent: "space-between"
                    }}>
                        <Grid style={{marginLeft: 15}}>
                            <Grid style={{marginBottom: 34}}>
                                <Typography style={{marginBottom: 10}}>
                                    Родительский тест-план
                                </Typography>

                                <FormControl style={{minWidth: "90%"}} className={classes.textFieldTestplansAndTests}>
                                    <InputLabel id="select-test-plan">Выберите тест-план</InputLabel>
                                    <Select
                                        data-cy="select-parent-test-plan"
                                        labelId="select-test-plan"
                                        value={selectedTestPlan ? selectedTestPlan.name : "Не выбрано"}
                                        label="Выберите тест-план"
                                        onChange={(e) => chooseTestPlan(e)}
                                        renderValue={(selected) => <Grid>{selected}</Grid>}
                                        MenuProps={MenuProps}
                                    >
                                        {testPlansForSelect.map((plan, index) => <MenuItem key={index}
                                                                                           value={plan as any}>{plan.title}</MenuItem>)}
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid sx={{marginBottom: "10px"}}>
                                <LocalizationProvider dateAdapter={AdapterMoment}>
                                    <DesktopDatePicker
                                        label="Дата начала *"
                                        inputFormat="DD/MM/YYYY"
                                        value={startDate}
                                        onChange={handleStartDate}
                                        className={classes.textFieldTestplansAndTests}
                                        renderInput={(params) => <TextField
                                            data-cy="testplan-started-at" {...params} />}
                                    />
                                </LocalizationProvider>
                            </Grid>
                            <Grid sx={{marginBottom: "34px"}}>
                                <LocalizationProvider dateAdapter={AdapterMoment}>
                                    <DesktopDatePicker
                                        label="Дата окончания *"
                                        inputFormat="DD/MM/YYYY"
                                        value={endDate}
                                        onChange={handleEndDate}
                                        className={classes.textFieldTestplansAndTests}
                                        renderInput={(params) => <TextField data-cy="testplan-due-date" {...params} />}
                                    />
                                </LocalizationProvider>
                            </Grid>
                        </Grid>
                        <Grid sx={{textAlign: "center"}}>
                            <Grid>
                                <Button
                                    data-cy="disagree-to-create-testplan"
                                    onClick={handleClose}
                                    sx={{
                                        margin: "0px 5px 20px 3px",
                                        minWidth: 100,
                                        width: "40%",
                                        height: "45%",
                                        backgroundColor: "#FFFFFF",
                                        color: "#000000",
                                    }}
                                >
                                    Отменить
                                </Button>
                                <Button
                                    data-cy="agree-to-create-testplan"
                                    type="submit"
                                    sx={{
                                        margin: "0px 3px 20px 5px",
                                        minWidth: 100,
                                        width: "40%",
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
                    {message && (
                        <div className="form-group">
                            <div className="alert alert-danger" role="alert">
                                {message}
                            </div>
                        </div>
                    )}
                </Grid>
            </form>
        </Dialog>
    );
}

export default CreationTestplanComponent