import React, {ChangeEvent, SyntheticEvent, useEffect, useState} from "react";
import {user} from "./models.interfaces";
import ProfileService from "../services/profile.service";
import Settings from "./settings";
import useStyles from "../styles/styles";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import AuthService from "../services/Authorization/auth.service";

const Profile: React.FC = () => {
    const classes = useStyles()
    const [isLoaded, setIsLoaded] = useState<boolean>(false)
    const [view, setView] = useState("profile")
    const handleOnChangeView = (event: SyntheticEvent, newValue: string) => {
        setNewPassword("")
        setRepeatNewPassword("")
        setPassword("")
        setPasswordProfile("")
        setMessage("")
        setRepeatError(false)
        setPasswordError(false)
        setRepeatHelperText("Пожалуйста, введите новый пароль повторно")
        setPasswordHelperText("")
        setView(newValue)
    }

    const [currentUser, setCurrentUser] = useState<user>()
    const [currentUsername, setCurrentUsername] = useState<string>("")
    const [username, setUsername] = useState<string>("")
    const [firstName, setFirstName] = useState<string>("")
    const [lastName, setLastName] = useState<string>()
    const [email, setEmail] = useState<string>()
    const [passwordProfile, setPasswordProfile] = useState<string>("")
    const [passwordProfileError, setPasswordProfileError] = useState(false)
    const [passwordProfileHelperText, setPasswordProfileHelperText] = useState<string>("")

    const [newPassword, setNewPassword] = useState<string>("")
    const [repeatNewPassword, setRepeatNewPassword] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [repeatError, setRepeatError] = useState(false)
    const [passwordError, setPasswordError] = useState(false)
    const [repeatHelperText, setRepeatHelperText] = useState<string>("Пожалуйста, введите новый пароль повторно")
    const [passwordHelperText, setPasswordHelperText] = useState<string>("")
    const [message, setMessage] = useState<string>("")

    const handleChangeUsername = (event: ChangeEvent<HTMLInputElement>) => setUsername(event.target.value)
    const handleChangeFirstName = (event: ChangeEvent<HTMLInputElement>) => setFirstName(event.target.value)
    const handleChangeLastName = (event: ChangeEvent<HTMLInputElement>) => setLastName(event.target.value)
    const handleChangeEmail = (event: ChangeEvent<HTMLInputElement>) => setEmail(event.target.value)
    const handleChangePasswordProfile = (event: ChangeEvent<HTMLInputElement>) => setPasswordProfile(event.target.value)

    const handleChangeNewPassword = (event: ChangeEvent<HTMLInputElement>) => setNewPassword(event.target.value)
    const handleChangeRepeatNewPassword = (event: ChangeEvent<HTMLInputElement>) => setRepeatNewPassword(event.target.value)
    const handleChangePassword = (event: ChangeEvent<HTMLInputElement>) => setPassword(event.target.value)

    const handleOnSavePersonalData = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        AuthService.login(currentUsername, passwordProfile).then(() => {
            setPasswordProfileHelperText("")
            setPasswordProfileError(false)
            if (currentUser) {
                ProfileService.changeUser(currentUser?.id, {
                    username: username,
                    password: passwordProfile,
                    first_name: firstName,
                    last_name: lastName,
                    email: email
                }).then(() => setMessage("Изменения успешно сохранены"))
                    .catch((error) => {
                        setMessage("Пожалуйста, проверьте введенные данные")
                        console.log(error)
                    })
            }
        }).catch(() => {
            setPasswordProfileHelperText("Текущий пароль не совпадает с указанным")
            setPasswordProfileError(true)
        })
    }
    const handleOnSavePassword = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (newPassword !== repeatNewPassword) {
            setRepeatHelperText("Новый пароль не совпадает с указанным")
            setRepeatError(true)
            return;
        }
        setRepeatHelperText("")
        setRepeatError(false)
        AuthService.login(currentUsername, password).then(() => {
            setPasswordHelperText("")
            setPasswordError(false)
            if (currentUser && currentUsername) {
                setMessage("")
                ProfileService.changeUser(currentUser?.id, {
                    username: currentUsername,
                    password: newPassword,
                }).then(() => {
                    setMessage("Изменения успешно сохранены")
                })
                    .catch((error) => {
                        setMessage("Пожалуйста, проверьте введенные данные")
                        console.log(error)
                    })
            }
        }).catch(() => {
            setPasswordHelperText("Текущий пароль не совпадает с указанным")
            setPasswordError(true)
        })
    }

    useEffect(() => {
        ProfileService.getMe().then((response) => {
            const user: user = response.data
            setCurrentUser(user)
            setIsLoaded(true)
            setCurrentUsername(user.username)
            setUsername(user.username ?? username)
            setFirstName(user?.first_name ?? firstName)
            setLastName(user?.last_name ?? lastName)
            setEmail(user?.email ?? email)
        })
            .catch((e) => {
                console.log(e);
            });
    }, [])

    if (!isLoaded)
        return <></>
    return <>
        <Typography textAlign={"center"} mt={'15px'}>
            {message}
        </Typography>
        <Paper style={{
            padding: '10px 10px 10px 10px',
            display: 'flex',
            flexDirection: 'column',
            margin: '15px auto auto auto',
            width: '50%',
            alignItems: 'center'
        }}>
            <TabContext value={view}>
                <Box sx={{display: {xs: 'none', md: 'flex'}, borderBottom: 1, borderColor: 'divider'}}>
                    <TabList onChange={handleOnChangeView}>
                        <Tab label="Личные данные" value={"profile"}/>
                        <Tab label="Смена пароля" value={"changePassword"}/>
                        <Tab label="Настройки" value={"settings"}/>
                    </TabList>
                </Box>
                <Box sx={{display: {xs: 'flex', md: 'none'}, borderBottom: 1, borderColor: 'divider'}}>
                    <TabList orientation="vertical" onChange={handleOnChangeView}>
                        <Tab label="Личные данные" value={"profile"}/>
                        <Tab label="Смена пароля" value={"changePassword"}/>
                        <Tab label="Настройки" value={"settings"}/>
                    </TabList>
                </Box>
                <TabPanel value={"profile"}>
                    <form onSubmit={handleOnSavePersonalData}
                          style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
                        <TextField id={"username"} className={classes.centeredField} variant={"outlined"} required
                                   label={'Имя пользователя'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={username} onChange={handleChangeUsername}/>
                        <TextField id={"first_name"} className={classes.centeredField} variant={"outlined"}
                                   label={'Имя'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={firstName}
                                   onChange={handleChangeFirstName}/>
                        <TextField id={"last_name"} className={classes.centeredField} variant={"outlined"}
                                   label={'Фамилия'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={lastName}
                                   onChange={handleChangeLastName}/>
                        <TextField id={"email"} type={"email"} className={classes.centeredField} variant={"outlined"}
                                   label={'Адрес электронной почты'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={email} onChange={handleChangeEmail}/>
                        <TextField id={"passwordProfile"} className={classes.centeredField} variant={"outlined"}
                                   required
                                   error={passwordProfileError} type={"password"}
                                   label={'Текущий пароль'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={passwordProfile} onChange={handleChangePasswordProfile}
                                   helperText={passwordProfileHelperText}/>

                        <Button type="submit" variant={"contained"}
                                sx={{margin: '10px 10px 10px 10px'}}>Сохранить</Button>
                    </form>
                </TabPanel>
                <TabPanel value={"changePassword"}>
                    <form onSubmit={handleOnSavePassword}
                          style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
                        <TextField id={"new_password"} className={classes.centeredField} variant={"outlined"} required
                                   label={'Новый пароль'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   type={"password"}
                                   value={newPassword}
                                   onChange={handleChangeNewPassword}/>
                        <TextField id={"repeat_password"} className={classes.centeredField} variant={"outlined"}
                                   required
                                   error={repeatError} label={'Подтверждение пароля'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   type={"password"} value={repeatNewPassword}
                                   onChange={handleChangeRepeatNewPassword}
                                   helperText={repeatHelperText}/>
                        <TextField id={"password"} className={classes.centeredField} variant={"outlined"} required
                                   error={passwordError} type={"password"}
                                   label={'Текущий пароль'}
                                   style={{margin: '10px 10px 10px 10px'}}
                                   value={password} onChange={handleChangePassword}
                                   helperText={passwordHelperText}/>

                        <Button type="submit" variant={"contained"}
                                sx={{margin: '10px 10px 10px 10px'}}>Сохранить</Button>
                    </form>
                </TabPanel>
                <TabPanel value={"settings"}>
                    <Settings/>
                </TabPanel>
            </TabContext>
        </Paper></>
}

export default Profile