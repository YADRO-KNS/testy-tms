import React from "react";
import {useNavigate} from "react-router-dom";
import {Tabs} from "antd";

interface ProjectTabsProps {
    projectId: string
}

const ProjectTabs = ({projectId}: ProjectTabsProps) => {
    const navigate = useNavigate()

    const tabItems = [
        {label: 'Overview', key: `/projects/${projectId}`},
        {label: 'Test Suites & Cases', key: `/projects/${projectId}/suites`},
        {label: 'Test Plans & Results', key: `/projects/${projectId}/plans`},
    ]
    return (
        <Tabs items={tabItems} onChange={(key) => {
            navigate(key)
        }}/>
    )
}

export default ProjectTabs