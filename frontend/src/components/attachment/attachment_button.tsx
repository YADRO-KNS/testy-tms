import React from 'react';
import Button from "@mui/material/Button";
import {Grid, Tooltip} from "@mui/material";
import DescriptionIcon from "@mui/icons-material/Description";
import Typography from "@mui/material/Typography";
import AttachmentService from "../../services/attachment.servise";

interface Props {
    setFilesSelected: (files: File[]) => void;
}

const AttachmentButton: React.FC<Props> = ({setFilesSelected}) => {
    const [attachments, setAttachments] = React.useState<File[]>()

    const handleFileChange = function (e: React.ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files;

        if (!fileList) return;
        console.log(Array.from(fileList))

        setFilesSelected(Array.from(fileList));
        setAttachments(Array.from(fileList));
    };

    return (
        <div style={{display: 'flex', flexDirection: 'column'}}>
            <label style={{marginBottom: 5}} htmlFor="fileSelection">
                <input
                    style={{display: "none"}}
                    id="fileSelection"
                    name="file"
                    type="file"
                    multiple={true}
                    onChange={handleFileChange}
                />
                <Button
                    sx={{
                        backgroundColor: "#e0e0e0",
                        color: "#1d1d1d",
                        "&:hover": {
                            backgroundColor: "#d5d5d5",
                        }
                    }}
                    component="span"
                    variant="contained"
                >
                    Прикрепить файл
                </Button>
            </label>
            {attachments && attachments.map((attachment, index) => (
                <Grid key={index} style={{marginTop: 5}}>
                    <Tooltip title={attachment.name} arrow>
                        <div style={{display: 'flex', flexDirection: 'row'}}>
                            <DescriptionIcon/>
                            <Typography style={{marginLeft: 5}}>
                                {AttachmentService.filenameReduce(attachment.name)}
                            </Typography>
                        </div>
                    </Tooltip>
                </Grid>
            ))}
        </div>
    );
}

export default AttachmentButton