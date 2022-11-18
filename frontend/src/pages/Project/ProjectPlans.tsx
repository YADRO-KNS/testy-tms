import React, {useContext, useEffect} from "react";
import {ProjectActiveTabContext} from "./ProjectMain";

const ProjectPlans = () => {
    const {setProjectActiveTab} = useContext(ProjectActiveTabContext)
    useEffect(() => {
        setProjectActiveTab('plans')
    }, [])
    return (
        <p>Project Plans</p>
    )
}

export default ProjectPlans