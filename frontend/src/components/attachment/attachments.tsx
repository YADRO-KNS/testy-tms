import React from 'react';
import Typography from "@mui/material/Typography";
import DescriptionIcon from '@mui/icons-material/Description';
import {Grid, Tooltip} from "@mui/material";
import {attachment} from "../models.interfaces";
import AttachmentService from "../../services/attachment.servise";

interface Props {
    attachments: attachment[] | undefined
}

const Attachments: React.FC<Props> = ({attachments}) => {
    console.log(attachments)
    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            {attachments && attachments.map((attachment, index) => (
                <a key={index}
                   style={{
                       marginTop: 5,
                       color: 'inherit',
                       textDecoration: 'none'
                   }}
                   href={attachment.link}
                   target="_blank"
                   download>
                    <Tooltip title={attachment.filename} arrow>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <DescriptionIcon/>
                            <Typography style={{marginLeft: 5}}>
                                {AttachmentService.filenameReduce(attachment.filename)}
                            </Typography>
                        </div>
                    </Tooltip>
                </a>
            ))}
        </div>
    );
}

export default Attachments