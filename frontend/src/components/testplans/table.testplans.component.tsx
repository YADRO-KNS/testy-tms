import React, {useEffect, useState} from "react";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableCell from "@mui/material/TableCell";
import Typography from "@mui/material/Typography";
import BarChartComponent from "./bar.chart.component";
import {treeTestPlan} from "./testplans.component";
import TestPlanService from "../../services/testplan.service";
import {planStatistic, testPlan} from "../models.interfaces";
import useStyles from "./styles.testplans";

const TableTestPlans = (props: {
    testplan: treeTestPlan, selected: number[], setSelected: (data: number[]) => void,
}) => {
    const classes = useStyles()
    const {testplan, selected, setSelected} = props;
    const [currentTestPlan, setCurrentTestPlan] = useState<testPlan>()
    const [testPlanStatistics, setTestPlanStatistics] = useState<{ label: string, value: number }[]>()
    const [testNumber, setTestNumber] = useState<number>()

    useEffect(() => {
        if (!currentTestPlan) {
            TestPlanService.getTestPlan(testplan.id).then((response) => {
                setCurrentTestPlan(response.data)
            })
                .catch((e) => {
                    console.log(e);
                });
        }
    }, [currentTestPlan, testplan.id])

    useEffect(() => {
        if (!testPlanStatistics) {
            TestPlanService.getStatistics(testplan.id).then((response) => {
                setTestPlanStatistics(response.data)
                const number = response.data.reduce((sum: number, current: planStatistic) => sum + current.value, 0)
                setTestNumber(number)
            })
                .catch((e) => {
                    console.log(e);
                });
        }
    }, [testPlanStatistics, testplan.id])

    const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
        const selectedIndex = selected.indexOf(id);
        let newSelected: number[] = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };

    return (
        <tr>
            <td style={{paddingBottom: 3}}>
                <Table size="small">
                    {<tbody style={{border: '1px solid'}}>
                    <tr>
                        <td className={classes.cellCheckbox}>
                            <FormControlLabel
                                label={testplan.id}
                                control={<Checkbox
                                    sx={{height: 20}}
                                    checked={selected.indexOf(testplan.id) !== -1}
                                    onClick={(event) => handleClick(event, testplan.id)}
                                    color="primary"
                                />}
                            />
                        </td>
                        <td style={{width: "auto", maxWidth: "30%", wordBreak: "break-all"}}>
                            <div>
                                <Link href={"/testplans/" + testplan.id} underline="none"
                                      style={{display: 'flex', color: '#282828'}}>
                                    <Typography style={{paddingBottom: 2}}>
                                        {testplan.title}
                                    </Typography>
                                </Link>

                            </div>
                            <div>
                                {"Количество дочерних тест-планов: " + testplan.children.length + ". Количество тестов: " + testNumber}
                            </div>
                        </td>

                        <TableCell align="right" style={{width: "25%"}}>
                            {testPlanStatistics && <BarChartComponent statistics={testPlanStatistics}/>}
                        </TableCell>

                    </tr>
                    </tbody>}
                </Table>
            </td>
        </tr>
    )
}

export default TableTestPlans