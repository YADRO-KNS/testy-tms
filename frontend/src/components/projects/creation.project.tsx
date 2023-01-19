import {Card, TextField} from "@mui/material";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import React from "react";
import ProjectService from "../../services/project.service";
import {project} from "./project.selection";

interface Props {
    setProjects: (projects: project[]) => void
}

const CreationProject: React.FC<Props> = ({setProjects}) => {
    const [name, setName] = React.useState("")
    const [description, setDescription] = React.useState("")

    const onChangeProjectName = (e: React.ChangeEvent<HTMLInputElement>) => {
        setName(e.target.value)
    }

    const onChangeProjectDescription = (e: React.ChangeEvent<HTMLInputElement>) => {
        setDescription(e.target.value)
    }

    const createProject = () => {
        ProjectService.createProject({name: name, description: description})
            .then(() =>
                ProjectService.getProjects()
                    .then((response) => {
                        setProjects(response.data)
                    })
            )
    }

    return (
        <Card elevation={3} style={{
            borderRadius: 15,
            marginBottom: 20,
            marginTop: 10,
            marginLeft: 5,
            marginRight: 5,
            // minWidth: 750
        }}>
            <div style={{
                alignItems: 'center',
                flexDirection: 'column',
                display: 'flex',
                paddingBottom: 20,
            }}>
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    marginTop: 10,
                    width: "85%"
                }}>
                    <Typography variant="h6"
                                style={{marginTop: 25, paddingRight: 5, width: 300}}>
                        Название проекта
                    </Typography>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        placeholder="Введите название проекта"
                        required
                        fullWidth
                        id="projectName"
                        name="projectName"
                        autoComplete="on"
                        autoFocus
                        value={name}
                        onChange={onChangeProjectName}
                    />
                </div>
                <div style={{
                    display: 'flex',
                    flexDirection: 'row',
                    marginTop: 10,
                    width: "85%"
                }}>
                    <Typography variant="h6"
                                style={{marginTop: 25, marginRight: 5, width: 300}}>
                        О проекте
                    </Typography>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        placeholder="Введите описание проекта"
                        multiline
                        minRows={6}
                        maxRows={12}
                        required
                        fullWidth
                        id="projectDescription"
                        name="projectDescription"
                        autoComplete="on"
                        value={description}
                        onChange={onChangeProjectDescription}
                    />
                </div>
                <div style={{
                    textAlign: 'right',
                    marginTop: 10,
                    width: "85%"
                }}>
                    <Button
                        // type="submit"
                        onClick={createProject}
                        variant={'contained'}
                        color={'secondary'}
                    >
                        Создать
                    </Button>
                </div>
            </div>

        </Card>
    )
}

export default CreationProject