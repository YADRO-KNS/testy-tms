import React from "react";
import {myCase} from "../models.interfaces";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Grid";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import CloseIcon from '@mui/icons-material/Close';
import SuiteCaseService from "../../services/suite.case.service";

interface Props {
    myCase: myCase;
    setDetailedCaseInfo: (data: { show: boolean, myCase: myCase }) => void
}

const DetailedCaseInfo: React.FC<Props> = ({myCase, setDetailedCaseInfo}) => {
    return (
        <Grid style={{padding: 20, wordBreak: "break-word"}}>
            <Grid>
                <Grid style={{display: "flex", justifyContent: "space-between"}}>
                    <Typography variant="h6">
                        Название
                    </Typography>
                    <IconButton size={"small"} onClick={() => setDetailedCaseInfo(SuiteCaseService.getEmptyDetailedCaseInfo())}>
                        <CloseIcon/>
                    </IconButton>
                </Grid>
                <Grid>
                    {myCase.name}
                </Grid>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </Grid>
            <Grid>
                <Typography variant="h6">
                    Описание
                </Typography>
                <Grid>
                    {myCase.scenario}
                </Grid>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </Grid>
            {myCase.setup && <Grid>
                <Typography variant="h6">
                    Подготовка теста
                </Typography>
                <Grid>
                    {myCase.setup}
                </Grid>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </Grid>}
            {myCase.teardown && <Grid>
                <Typography variant="h6">
                    Очистка после теста
                </Typography>
                <Grid>
                    {myCase.teardown}
                </Grid>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </Grid>}
            {myCase.estimate && <Grid>
                <Typography variant="h6">
                    Время выполнения
                </Typography>
                <Grid>
                    {myCase.estimate}
                </Grid>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </Grid>}
        </Grid>
    )
}

export default DetailedCaseInfo