import React from 'react';
import Typography from "@mui/material/Typography";
import DescriptionIcon from '@mui/icons-material/Description';
import {Grid, Tooltip} from "@mui/material";
import {attachment} from "../models.interfaces";

interface Props {
    attachments: attachment[] | undefined
}

const Attachments: React.FC<Props> = ({attachments}) => {
    const filenameReduce = (filename: string) => {
        const maxLengthOfName = 35;
        if (filename.length > maxLengthOfName) {
            return filename.slice(0, maxLengthOfName) + "..."
        } else {
            return filename
        }
    }

    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            {attachments && attachments.map((attachment, index) => (
                <Grid key={index}
                      style={{
                          marginTop: 5,
                          color: 'inherit',
                          textDecoration: 'none'
                      }}
                      component="a"
                      href={attachment.file}
                      target="_blank"
                      download>
                    <Tooltip title={attachment.filename} arrow>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <DescriptionIcon/>
                            <Typography style={{marginLeft: 5}}>
                                {filenameReduce(attachment.filename)}
                            </Typography>
                        </div>
                    </Tooltip>
                </Grid>
            ))}
        </div>
    );
}

export default Attachments