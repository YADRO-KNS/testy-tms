import React from "react";
import Checkbox from "@mui/material/Checkbox";
import Chip from "@mui/material/Chip";
import FormControlLabel from "@mui/material/FormControlLabel";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import moment from "moment";
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";
import useStyles from "./styles.testplans";
import {test, testPlan} from "../models.interfaces";
import EditIcon from "@mui/icons-material/Edit";

interface Props {
    currentTestPlan: testPlan;
    tests: test[];
    setShowCreationTestPlan: (show: boolean) => void;
    setIsForEdit: (isForEdit: testPlan) => void;
    detailedTestInfo: { show: boolean, test: test } | null;
    setDetailedTestInfo: (data: { show: boolean, test: test }) => void;
    showEnterResult: boolean;
    setShowEnterResult: (show: boolean) => void
}

const TestplanInfo: React.FC<Props> = ({
                                           currentTestPlan,
                                           tests,
                                           setShowCreationTestPlan,
                                           setIsForEdit,
                                           detailedTestInfo,
                                           setDetailedTestInfo,
                                           showEnterResult,
                                           setShowEnterResult
                                       }) => {
    const classes = useStyles()

    return (
        <div style={{paddingBottom: 20}}>
            <div style={{paddingBottom: 20}}>
                <Grid container sx={{paddingBottom: 1}} spacing={2}>
                    <Grid item>
                        <Typography variant="h6" sx={{padding: 0}}>
                            {currentTestPlan.title}
                        </Typography>
                    </Grid>
                    <Grid item>
                        <IconButton size={"small"} onClick={() => {
                            setShowCreationTestPlan(true)
                            setIsForEdit(currentTestPlan)
                        }}>
                            <EditIcon fontSize={"small"}/>
                        </IconButton>
                    </Grid>
                </Grid>
                <Typography>
                    {"Дата начала: " + moment(currentTestPlan.started_at, 'YYYY-MM-DDTHH:mm').format('MMMM D, YYYY HH:mm')}
                </Typography>
                <Typography>
                    {"Дата окончания: " + moment(currentTestPlan.due_date, 'YYYY-MM-DDTHH:mm').format('MMMM D, YYYY HH:mm')}
                </Typography>
            </div>
            <TableContainer component={Paper}>
                <Table>
                    <tbody>
                    {tests.map((test, index) =>
                        (<tr key={index} className={classes.tableCellTests}>
                                <TableCell className={classes.tableCellTests}>
                                    <FormControlLabel
                                        className={classes.checkboxTests}
                                        label={
                                            <Typography sx={{fontSize: 15}}>
                                                {test.id}
                                            </Typography>}
                                        control={<Checkbox sx={{height: 10}} color="primary"/>}
                                    />
                                </TableCell>
                                <TableCell className={classes.tableCellTests}>
                                    {test.case.name}
                                </TableCell>
                                {test.test_results &&
                                <TableCell className={classes.tableCellTests}>
                                    <Chip key={index} label={test.last_status_color.name}
                                          onClick={() => {
                                              setDetailedTestInfo({
                                                  show: true,
                                                  test: test
                                              })
                                              test.id === detailedTestInfo?.test.id ? setShowEnterResult(!showEnterResult) : setShowEnterResult(true)

                                          }}
                                          style={{
                                              margin: 3,
                                              maxWidth: "95%",
                                              backgroundColor: test.last_status_color.color,
                                              color: "white"
                                          }}/>

                                </TableCell>}
                                {(!detailedTestInfo || !detailedTestInfo.show) &&
                                (< TableCell className={classes.tableCellTests}>
                                    {moment(test.updated_at).format('DD/MM/YYYY')}
                                </TableCell>)}
                                {(!detailedTestInfo || !detailedTestInfo.show) &&
                                (<TableCell className={classes.tableCellTests}>
                                    {test.username ?? "не назначен"}
                                </TableCell>)}

                                <TableCell className={classes.tableCellTests}>
                                    <IconButton size={"small"} onClick={() => {
                                        detailedTestInfo ?
                                            detailedTestInfo.test.id === test.id ?
                                                setDetailedTestInfo({
                                                    show: !detailedTestInfo.show,
                                                    test: test
                                                }) : setDetailedTestInfo({
                                                    show: true,
                                                    test: test
                                                }) : setDetailedTestInfo({show: true, test: test})
                                    }}>
                                        <KeyboardArrowRightIcon sx={{
                                            transform: (test.id === detailedTestInfo?.test.id && detailedTestInfo?.show) ? 'rotate(180deg)' : 'rotate(0deg)',
                                            transition: '0.2s',
                                        }}/>
                                    </IconButton>
                                </TableCell>
                            </tr>
                        ))
                    }
                    </tbody>
                </Table>
            </TableContainer>
        </div>
    )
}

export default TestplanInfo