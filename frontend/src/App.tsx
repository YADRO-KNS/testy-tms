import React, {FC} from 'react';
import "./App.css"
import Main from "./layouts/Main";
import Dashboard from "./pages/Dashboard";
import {Routes, Route} from "react-router-dom";
import Projects from "./pages/Projects";
import Login from "./pages/Login";
import Users from "./pages/Users";
import RequireAuth from "./features/auth/RequireAuth";

const App: FC = () => {
    return (
        <Routes>
            {/* protected routes */}
            <Route element={<RequireAuth/>}>
                <Route path="/" element={<Main/>}>
                    <Route index element={<Dashboard/>}/>

                    <Route path="projects" element={<Projects/>}/>
                    <Route path="users" element={<Users/>}/>
                </Route>
            </Route>

            {/* public routes */}
            <Route path="/login" element={<Login/>}/>
        </Routes>
    )
}

export default App;
