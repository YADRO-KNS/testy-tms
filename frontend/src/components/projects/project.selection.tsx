import React, {useEffect} from "react";
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


export interface project {
    id: number;
    name: string;
    description: string;
}

const ProjectSelection: React.FC = () => {
    const classes = useStyles();
    const [expanded, setExpanded] = React.useState(false);
    const [projects, setProjects] = React.useState<project[]>([]);

    useEffect(() => {
        ProjectService.getProjects().then((response) =>
            setProjects(response.data)
        )
            .catch((e) => console.log(e));
    }, []);

    const loginToProject = (project: project) => {
        localStorage.setItem("currentProject", JSON.stringify(project));
        window.location.assign("/project");
    }

    return (
        <Container component="main" maxWidth="md">
            <div className={classes.divProjectSelectionPage}>
                <div className={classes.divProjectSelectionPageLine}>
                    <Typography variant="h6" style={{marginTop: 5}}>
                        Проекты
                    </Typography>
                    <IconButton
                        onClick={() => setExpanded(!expanded)}
                    >
                        <AddCircleOutlineRoundedIcon
                            style={{
                                opacity: expanded ? 0 : 1,
                            }}
                        />
                        <KeyboardArrowDown
                            style={{
                                marginLeft: -24,
                                opacity: expanded ? 1 : 0,
                                transition: '0.2s',
                            }}
                        />
                    </IconButton>

                </div>
                <Collapse in={expanded} timeout="auto">
                    <CreationProject setProjects={setProjects}/>
                </Collapse>

                {projects.map((project) =>
                    <div key={project.name} style={{
                        flexDirection: 'row',
                        display: 'flex',
                        marginTop: 10,
                        cursor: "pointer"
                    }}
                         onClick={() => loginToProject(project)}>
                        <BookIcon style={{marginTop: 0, fontSize: 30}}/>
                        <div style={{marginLeft: "2%", width: "21%", wordBreak: "break-word"}}>
                            <Typography variant="h6">
                                {project.name}
                            </Typography>
                        </div>
                        <div style={{width: "70%", marginLeft: "2%", textAlign: "left", wordBreak: "break-word"}}>
                            <Typography variant="h6">
                                {project.description}
                            </Typography>
                        </div>

                    </div>
                )}
            </div>
        </Container>
    );
}

export default ProjectSelection;
