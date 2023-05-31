import React, {useEffect, useState} from "react";
import useStyles from "../../styles/styles";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import BookIcon from '@mui/icons-material/Book';
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import {Collapse} from "@mui/material";
import {KeyboardArrowDown} from "@mui/icons-material";
import IconButton from "@mui/material/IconButton";
import CreationProject from "./creation.project";
import ProjectService from "../../services/project.service";
import DeleteIcon from "@mui/icons-material/Delete";
import {project} from "../models.interfaces";
import DeletionDialogProject from "./deletion.dialog.project.component";
import localStorageTMS from "../../services/localStorageTMS";
import {useNavigate} from "react-router-dom";

const SelectionProject: React.FC = () => {
    const classes = useStyles();
    const navigate = useNavigate();
    const [expanded, setExpanded] = useState(false);
    const [projects, setProjects] = useState<project[]>([]);
    const [openDialogDeletion, setOpenDialogDeletion] = useState(false);
    const [selectedForDeletion, setSelectedForDeletion] = useState<project | null>(null);

    useEffect(() => {
        ProjectService.getProjects().then((response) =>
            setProjects(response.data)
        )
            .catch((e) => console.log(e));
    }, []);

    const loginToProject = (project: project) => {
        localStorageTMS.setCurrentProject(project);
        navigate("/project");
    }

    return (
        <Container component="main" maxWidth="md">
            <div className={classes.divProjectSelectionPage}>
                <div className={classes.divProjectSelectionPageLine}>
                    <Typography variant="h6" style={{marginTop: 5}}>
                        Проекты
                    </Typography>
                    <IconButton data-cy="project-creation" onClick={() => setExpanded(!expanded)}>
                        <AddCircleOutlineRoundedIcon style={{opacity: expanded ? 0 : 1}}/>
                        <KeyboardArrowDown style={{
                            marginLeft: -24,
                            opacity: expanded ? 1 : 0,
                            transition: '0.2s',
                        }}/>
                    </IconButton>

                </div>
                <Collapse data-cy="project-creation-collapse" in={expanded} timeout="auto">
                    <CreationProject setProjects={setProjects}/>
                </Collapse>

                {projects.map((project) =>
                    <div key={project.name} style={{
                        flexDirection: 'row',
                        display: 'flex',
                        marginTop: 10
                    }}>
                        <div style={{
                            flexDirection: 'row',
                            display: 'flex',
                            width: "100%",
                            cursor: "pointer"
                        }} onClick={() => loginToProject(project)}>
                            <BookIcon style={{marginTop: 0, fontSize: 30}}/>
                            <div style={{
                                flexDirection: 'row',
                                display: 'flex',
                                width: "100%"
                            }}>
                                <div style={{marginLeft: "2%", width: "21%", wordBreak: "break-word"}}>
                                    <Typography variant="h6">
                                        {project.name}
                                    </Typography>
                                </div>
                                <div style={{
                                    width: "66%",
                                    marginLeft: "2%",
                                    textAlign: "left",
                                    wordBreak: "break-word"
                                }}>
                                    <Typography variant="h6">
                                        {project.description}
                                    </Typography>
                                </div>
                            </div>
                        </div>
                        <IconButton sx={{marginBottom: "auto"}}
                                    size={"small"}
                                    onClick={() => {
                                        setSelectedForDeletion(project)
                                        setOpenDialogDeletion(true)
                                    }}>
                            <DeleteIcon fontSize={"small"}/>
                        </IconButton>
                    </div>
                )}
                <DeletionDialogProject openDialogDeletion={openDialogDeletion}
                                       setOpenDialogDeletion={setOpenDialogDeletion}
                                       selectedForDeletion={selectedForDeletion} setProjects={setProjects}/>
            </div>
        </Container>
    );
}

export default SelectionProject;
