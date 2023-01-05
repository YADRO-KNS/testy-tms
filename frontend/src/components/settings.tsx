import React, {useState} from "react";
import {
    Box,
    Button,
    InputLabel,
    MenuItem,
    Select,
    SelectChangeEvent, Typography
} from "@mui/material";
import {ThemeProvider, createTheme} from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import IconButton from "@mui/material/IconButton";

const ColorModeContext = React.createContext({
    toggleColorMode: () => {
    }
});

const Settings: React.FC = () => {
    const [mode, setMode] = React.useState<'light' | 'dark'>('light');
    const colorMode = React.useMemo(
        () => ({
            toggleColorMode: () => {
                setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
            },
        }),
        [],
    );

    const theme = React.useMemo(
        () =>
            createTheme({
                palette: {
                    mode,
                },
            }),
        [mode],
    );

    const [language, setLanguage] = useState("Русский")

    const handleOnChangeLanguage = (event: SelectChangeEvent<string>) => setLanguage(event.target.value)

    return <ColorModeContext.Provider value={colorMode}>
        <Typography color={"darkorange"} component={"h3"}>Данная страница находится на доработке</Typography>
        <form
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                margin: 1,
                minWidth: 200
            }}>
            <InputLabel>Язык интерфейса</InputLabel>
            <Select
                autoWidth
                label="Язык интерфейса"
                value={language}
                onChange={handleOnChangeLanguage}
            >
                <MenuItem value={"Русский"}>Русский</MenuItem>
                <MenuItem value={"English"}>English</MenuItem>
            </Select>
            <ThemeProvider theme={theme}>
                <Box
                    sx={{
                        display: 'flex',
                        width: '100%',
                        alignItems: 'center',
                        justifyContent: 'center',
                        bgcolor: 'background.default',
                        color: 'text.primary',
                        borderRadius: 1,
                        p: 3,
                    }}
                >
                    {theme.palette.mode} mode
                    <IconButton sx={{ml: 1}} onClick={colorMode.toggleColorMode} color="inherit">
                        {theme.palette.mode === 'dark' ? <Brightness7Icon/> : <Brightness4Icon/>}
                    </IconButton>
                </Box>

                <Button type={"submit"} variant={"contained"}
                        sx={{margin: '10px 10px 10px 10px'}}>Сохранить</Button>

            </ThemeProvider>
        </form>
    </ColorModeContext.Provider>
}

export default Settings;