import React from 'react';
import Button from "@mui/material/Button";

interface Props {
    setFilesSelected: (files: File[]) => void;
}

const AttachmentButton: React.FC<Props> = ({setFilesSelected}) => {

    const handleFileChange = function (e: React.ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files;

        if (!fileList) return;
        console.log(Array.from(fileList))

        setFilesSelected(Array.from(fileList));
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
        </div>
    );
}

export default AttachmentButton