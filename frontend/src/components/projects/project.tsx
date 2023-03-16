import React, {ChangeEvent, useEffect, useMemo, useState} from 'react';
import {DesktopDatePicker, LocalizationProvider} from "@mui/x-date-pickers";
import moment, {Moment} from "moment";
import {AdapterMoment} from "@mui/x-date-pickers/AdapterMoment";
import {test, testPlan, testResult, user} from "../models.interfaces";
import ProjectService from "../../services/project.service";
import {statuses} from "../model.statuses";
import useStyles from "../../styles/styles";
import ProjectSettings from "./project.settings";
import Grid from "@mui/material/Grid";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import TableBody from "@mui/material/TableBody";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Switch from "@mui/material/Switch";
import Button from "@mui/material/Button";
import TableContainer from "@mui/material/TableContainer";
import Table from "@mui/material/Table";
import TableHead from "@mui/material/TableHead";
import LineChartComponent from "./charts/line.chart.component";
import PieChartComponent from "./charts/pie.chart.component";
import {useNavigate} from "react-router-dom";
import {useSelector} from "react-redux";
import {RootState} from "../../app/store";
import localStorageTMS from "../../services/localStorageTMS";

const Project: React.FC = () => {
    const classes = useStyles();
    const navigate = useNavigate();
    const labels = useMemo(() => [['ID', '#000000'], ['НАЗВАНИЕ ТЕСТ-ПЛАНА', '#000000'], ['ВСЕГО ТЕСТОВ', '#000000']]
        .concat(statuses.map((status) => [status.name.toUpperCase(), status.color])
            .concat([['ДАТА ИЗМЕНЕНИЯ', '#000000'], ['КЕМ ИЗМЕНЕНО', '#000000']])), [])

    /// From that index starts statuses in const `labels`
    const minStatusIndex = labels.findIndex((el) => el[0].toUpperCase() === "ВСЕГО ТЕСТОВ") + 1;
    /// Till that index contains statuses in const `labels`
    const maxStatusIndex = minStatusIndex + statuses.length - 1;

    const [isSwitched, setSwitch] = React.useState(false);
    const [showFilter, setShowFilter] = React.useState(false);
    const [startDate, setStartDate] = React.useState<Moment | null>(moment("01.01.1970", "DD.MM.YYYY"));
    const [endDate, setEndDate] = React.useState<Moment | null>(moment());
    const [showProjectSettings, setShowProjectSettings] = useState(false);
    const [tests, setTests] = useState<test[]>([]);
    const [testPlans, setTestPlans] = useState<testPlan[]>([]);
    const [testResults, setResults] = useState<testResult[]>([]);
    const [currentUsername, setCurrentUsername] = useState<string>();
    const [users, setUsers] = useState<user[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);
    const [statusesShow, setStatusesToShow] = React.useState<{ [key: string]: boolean; }>({});

    const handleOnSwitch = (event: ChangeEvent<HTMLInputElement>) => setSwitch(event.target.checked);
    const handleOnOpenFilter = () => setShowFilter(!showFilter);
    const handleChangeStartDate = (newValue: Moment | null) => setStartDate(newValue);
    const handleChangeEndDate = (newValue: Moment | null) => setEndDate(newValue);
    const handleShowProjectSettings = () => {
        setShowProjectSettings(true)
    }
    const handleOnShowStatus = (status: string) => {
        setStatusesToShow({...statusesShow, [status]: !statusesShow[status]})
    };

    const projectValue = localStorageTMS.getCurrentProject()
    if (!projectValue) {
        console.log("Redux state currentProject is empty")
    }

    // Collecting data to display in table.

    const projectTableData = useMemo(() => {
        const result = testPlans.map((value) => {
            const currentTests: test[] = tests.filter((test) => test.plan === value.id)
            let date = value.started_at
            const results: { [key: string]: number; } = {
                "all": currentTests.length,
            }
            statuses.map((status) => results[status.name.toLowerCase()] = 0)
            let editorId: number | null = null;
            const tests_ids = currentTests.map((test) => test.id)
            testResults.sort((a, b) =>
                moment(b.updated_at, "YYYY-MM-DDThh:mm").valueOf() - moment(a.updated_at, "YYYY-MM-DDThh:mm").valueOf())
            for (let test_result of testResults) {
                if (tests_ids.includes(test_result.test)) {
                    editorId = test_result?.user ?? editorId
                    date = test_result?.updated_at ?? date
                    break
                }
            }
            currentTests.forEach((test) => {
                test.last_status ? results[String(test.last_status).toLowerCase()]++ : results["untested"]++
            });
            const editor = (editorId != null) ?
                users.find((value) => value.id === editorId) : null
            const editorName = (editor != null) ? editor.username : "Не назначен"

            const toReturn = [value.id, value.name, results.all]
            statuses.map((status) => toReturn.push(results[status.name.toLowerCase()]))
            toReturn.push(date, editorName)
            return toReturn
        })
        result.sort((a, b) =>
            (moment(b.slice(-2)[0], "YYYY-MM-DDThh:mm").valueOf() - moment(a.slice(-2)[0], "YYYY-MM-DDThh:mm").valueOf()))
        return result
    }, [testPlans, testResults]);
    const personalTableData = projectTableData.filter((value) => value[value.length - 1] === currentUsername)

    useEffect(() => {
        if (!projectValue) {
            navigate("/")
            return
        }
        ProjectService.getMe().then((response) => {
            const currentUser: user = response.data
            setCurrentUsername(currentUser.username)
        }).catch((e) => console.log(e))

        ProjectService.getTestPlans().then((response) => {
            let testPlansData: testPlan[] = response.data
            testPlansData = testPlansData.filter((value) => value.project === projectValue.id)
            setTestPlans(testPlansData)

            ProjectService.getTests().then((response) => {
                const testsData: test[] = response.data
                setTests(testsData.filter((value) => value.project === projectValue.id))

                ProjectService.getTestResults().then((response) => {
                    const testResultsData: testResult[] = response.data
                    setResults(testResultsData.filter((value) => value.project === projectValue.id))
                })

                ProjectService.getUsers().then((response) => {
                    setUsers(response.data)

                })
            })
            statuses.forEach((status) => {
                const temporaryValue = statusesShow
                temporaryValue[status.name.toLowerCase()] = true
                setStatusesToShow(temporaryValue)
            })
            setIsLoaded(true)
        })
            .catch((e) => {
                console.log(e);
            });
    }, [])

    const charts = [<LineChartComponent tests={tests}/>, <PieChartComponent tests={tests}/>];

    const filter = useMemo(() => {
        if (!isLoaded) {
            statuses.forEach((status) => {
                const temporaryValue = statusesShow
                temporaryValue[status.name.toLowerCase()] = true
                setStatusesToShow(temporaryValue)
            })
        }

        return <Grid style={{display: 'flex', justifyContent: 'center', marginBottom: '10px', marginTop: "10px"}}>
            <FormGroup style={{display: 'flex', justifyContent: 'center', flexDirection: 'row'}}>
                {statuses.map((status, index) =>
                    <FormControlLabel key={index}
                                      control={<Checkbox checked={statusesShow[status.name.toLowerCase()]}
                                                         onClick={() => handleOnShowStatus(status.name.toLowerCase())}/>}
                                      label={<Chip key={index} label={status.name.toUpperCase()}
                                                   style={{
                                                       margin: 3,
                                                       maxWidth: "95%",
                                                       backgroundColor: status.color,
                                                       color: "white"
                                                   }}/>}/>
                )}
                <LocalizationProvider dateAdapter={AdapterMoment}>
                    <div style={{marginLeft: '10px'}}>
                        <DesktopDatePicker
                            className={classes.centeredField}
                            label="Выберите дату начала"
                            inputFormat="DD/MM/YYYY"
                            value={startDate}
                            onChange={handleChangeStartDate}
                            renderInput={(params) => <TextField className={classes.centeredField} {...params} />}
                        />
                    </div>
                    <div style={{marginLeft: '10px'}}>
                        <DesktopDatePicker
                            className={classes.centeredField}
                            label="Выберите дату окончания"
                            inputFormat="DD/MM/YYYY"
                            value={endDate}
                            onChange={handleChangeEndDate}
                            renderInput={(params) => <TextField className={classes.centeredField} {...params} />}
                        />
                    </div>
                </LocalizationProvider>
            </FormGroup>
        </Grid>
    }, [statusesShow, startDate, endDate])

    const tableDataToShow = useMemo(() => <TableBody>
        {(isSwitched ? personalTableData : projectTableData)?.map(
            (testplanData, planIndex) =>
                // Checking if last date of test plan is between filter dates
                (!moment(testplanData[testplanData.length - 2], "YYYY-MM-DDThh:mm")
                    .isBetween(startDate, endDate, undefined, "[]")) ? null :
                    (
                        // Returning table row with data
                        <TableRow id={`row-${planIndex}`} key={planIndex} style={{cursor: "pointer"}} hover={true}
                                  onClick={() => navigate("/testplans/" + testplanData[0])}>
                            {testplanData.slice(0, testplanData.length - 2)
                                .concat([moment(testplanData[testplanData.length - 2], "YYYY-MM-DDThh:mm").format("DD.MM.YYYY"),
                                    testplanData[testplanData.length - 1]]).map(
                                    // Filling table cells with data
                                    (value, index) => {
                                        if (index < minStatusIndex || index > maxStatusIndex) {
                                            return <TableCell key={planIndex + "." + index}>
                                                <Typography align={'center'}>{value}</Typography>
                                            </TableCell>
                                        }
                                        // Checking if status is selected in filter
                                        if (statusesShow[statuses[index - minStatusIndex].name.toLowerCase()]) {
                                            return <TableCell
                                                id={statuses[index - minStatusIndex].name.toLowerCase()}
                                                key={planIndex + "." + statuses[index - minStatusIndex].name.toLowerCase()}>
                                                <Typography align={'center'}>{value}</Typography>
                                            </TableCell>
                                        }
                                        return <></>;
                                    }
                                )}
                        </TableRow>)
        )}
    </TableBody>, [personalTableData, projectTableData])

    if (!isLoaded)
        return <></>
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <Grid
                sx={{
                    width: "90%",
                    display: {xs: "none", sm: "flex"},
                    flexWrap: "wrap",
                    justifyContent: 'center',
                    alignSelf: 'center',
                    alignItems: "center",
                    marginTop: '20px'
                }}>
                {tests.length > 0 ? charts.map((chart, index) =>
                        <div key={index} style={{width: "50%"}}>
                            {chart}
                        </div>)
                    : <></>}
            </Grid>
            <Grid sx={{
                width: "90%",
                alignSelf: 'center',
                display: {xs: "flex", sm: "none"},
                flexWrap: "wrap",
                justifyContent: 'center',
                alignItems: "center",
                marginTop: '20px'
            }}>
                {tests.length > 0 ? charts.map((chart) => chart)
                    : <></>}
            </Grid>
            <Grid style={{width: '90%', justifyContent: 'center', alignSelf: 'center', paddingTop: '50px'}}>
                <Paper
                    elevation={5}
                    style={{
                        alignSelf: 'center',
                        justifyContent: 'center',
                        padding: "20px 10px 10px 10px",
                    }}>
                    <Stack>
                        <Stack flexWrap={"wrap"} display={'flex'} flexDirection={"row"} justifyContent={"center"}
                               mb={'10px'}>
                            <Stack direction={"row"}>
                                {isSwitched ?
                                    <Typography fontSize={24} mr={'5px'} ml={'5px'} color={'grey'}>
                                        Проекта
                                    </Typography>
                                    :
                                    <Typography fontSize={24} mr={'5px'} ml={'5px'}>
                                        Активность проекта
                                    </Typography>
                                }
                                <Switch checked={isSwitched} onChange={handleOnSwitch}/>
                                {isSwitched ?
                                    <Typography fontSize={24} mr={'5px'} ml={'5px'}>
                                        Моя активность
                                    </Typography>
                                    :
                                    <Typography fontSize={24} mr={'5px'} ml={'5px'} color={'grey'}>
                                        Моя
                                    </Typography>
                                }
                            </Stack>
                            <Button variant="contained"
                                    style={{marginLeft: '10px', backgroundColor: "#696969"}}
                                    onClick={handleOnOpenFilter}>Фильтр</Button>
                            <Button data-cy="openProjectSettingsPage"
                                    variant="contained"
                                    style={{marginLeft: '10px', backgroundColor: "#696969"}}
                                    onClick={handleShowProjectSettings}
                            >Настройки</Button>
                        </Stack>
                        <ProjectSettings show={showProjectSettings} setShow={setShowProjectSettings}/>
                        {showFilter ? filter : null}
                        <TableContainer component={Paper}>
                            <Table stickyHeader>
                                <TableHead style={{marginBottom: '20px'}}>
                                    <TableRow>
                                        {labels.map(([value, color], index) => {
                                            if (!statuses.find((status) => status.name.toLowerCase() === value.toLowerCase())) {
                                                return <TableCell key={index}>
                                                    <Typography color={color} fontWeight={'bolder'}
                                                                align={'center'}>{value}</Typography>
                                                </TableCell>
                                            }
                                            if (statusesShow[value.toLowerCase()]) {
                                                return <TableCell key={index}>
                                                    <div style={{textAlign: "center"}}>
                                                        <Chip key={index} label={value}
                                                              style={{
                                                                  margin: 3,
                                                                  maxWidth: "95%",
                                                                  backgroundColor: statuses[index - minStatusIndex].color,
                                                                  color: "white"
                                                              }}/>
                                                    </div>
                                                </TableCell>
                                            }
                                            return <></>;
                                        })}
                                    </TableRow>
                                </TableHead>
                                {tableDataToShow}
                            </Table>
                        </TableContainer>
                    </Stack>
                </Paper>
            </Grid>
        </div>
    );
};

export default Project;