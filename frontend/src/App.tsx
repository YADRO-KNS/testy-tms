import React, {FC} from 'react';
import "./App.css"
import Main from "./layouts/Main";
import Dashboard from "./pages/Dashboard";
import {Routes, Route} from "react-router-dom";
import RequireAuth from "./features/auth/RequireAuth";
import Logout from "./features/auth/Logout";
import ProjectMain from "./pages/Project/ProjectMain";
import Login from "./pages/Login";
import Users from "./pages/Administration/Users";
import Projects from "./pages/Administration/Projects";
import ProjectOverview from "./pages/Project/ProjectOverview";
import ProjectSuites from "./pages/Project/ProjectSuites";
import ProjectPlans from "./pages/Project/ProjectPlans";

const App: FC = () => {
    return (
        <Routes>
            {/* protected routes */}
            <Route element={<RequireAuth/>}>
                <Route path="/" element={<Main/>}>
                    <Route index element={<Dashboard/>}/>

                    {/* projects routes */}
                    <Route path="projects" element={<ProjectMain/>}>
                        <Route path=":projectId" element={<ProjectOverview/>}/>
                        <Route path=":projectId/suites" element={<ProjectSuites/>}/>
                        <Route path=":projectId/plans" element={<ProjectPlans/>}/>
                    </Route>

                    {/* administrations routes */}
                    <Route path="administration">
                        <Route path="projects" element={<Projects/>}/>
                        <Route path="users" element={<Users/>}/>
                    </Route>
                </Route>
            </Route>

            {/* public routes */}
            <Route path="/login" element={<Login/>}/>
            <Route path="/logout" element={<Logout/>}/>
        </Routes>
    )
}

export default App;
