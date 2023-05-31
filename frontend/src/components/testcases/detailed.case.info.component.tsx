import React, {useEffect} from "react";
import {myCase} from "../models.interfaces";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import CloseIcon from '@mui/icons-material/Close';
import SuiteCaseService from "../../services/suite.case.service";
import Attachments from "../attachment/attachments";
import {attachment} from "../models.interfaces";

interface Props {
    myCase: myCase;
    setDetailedCaseInfo: (data: { show: boolean, myCase: myCase }) => void
}

const DetailedCaseInfo: React.FC<Props> = ({myCase, setDetailedCaseInfo}) => {
    const [, setAttachments] = React.useState<attachment[]>()
    useEffect(() => {
        SuiteCaseService.getCaseById(myCase.id).then((response) => {
                myCase.attachments = response.data.attachments
                setAttachments(response.data.attachments)
            }
        )
    }, [myCase])

    return (
        <div style={{padding: 20, wordBreak: "break-word"}}>
            <div>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <Typography variant="h6">
                        Название
                    </Typography>
                    <IconButton data-cy="close-info-case" size={"small"}
                                onClick={() => setDetailedCaseInfo(SuiteCaseService.getEmptyDetailedCaseInfo())}>
                        <CloseIcon/>
                    </IconButton>
                </div>
                <div data-cy="detailed-info-case-name">
                    {myCase.name}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>
            <div>
                <Typography variant="h6">
                    Сценарий
                </Typography>
                <div data-cy="detailed-info-case-scenario">
                    {myCase.scenario}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>
            {myCase.description && <div>
                <Typography variant="h6">
                    Описание
                </Typography>
                <div data-cy="detailed-info-case-setup">
                    {myCase.description}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>}
            {myCase.setup && <div>
                <Typography variant="h6">
                    Подготовка теста
                </Typography>
                <div data-cy="detailed-info-case-setup">
                    {myCase.setup}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>}
            {myCase.teardown && <div>
                <Typography variant="h6">
                    Очистка после теста
                </Typography>
                <div data-cy="detailed-info-case-teardown">
                    {myCase.teardown}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>}
            {myCase.estimate && <div>
                <Typography variant="h6">
                    Время выполнения
                </Typography>
                <div data-cy="detailed-info-case-estimate">
                    {myCase.estimate}
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>}
            {myCase.attachments && myCase.attachments?.length !== 0 && <div>
                <Typography variant="h6">
                    Прикрепленные файлы
                </Typography>
                <div>
                    <Attachments attachments={myCase.attachments}/>
                </div>
                <Divider style={{margin: "10px 0px 10px 0px"}}/>
            </div>}
        </div>
    )
}

export default DetailedCaseInfo