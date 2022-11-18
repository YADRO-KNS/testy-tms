import React, {useContext} from "react";
import {useNavigate} from "react-router-dom";
import {Tabs} from "antd";
import {ProjectActiveTabContext} from "./ProjectMain";

interface ProjectTabsProps {
    projectId: string
}

const ProjectTabs = ({projectId}: ProjectTabsProps) => {
    const navigate = useNavigate()
    const {projectActiveTab} = useContext(ProjectActiveTabContext)

    const tabItems = [
        {label: 'Overview', key: 'overview', path: `/projects/${projectId}`},
        {label: 'Test Suites & Cases', key: 'suites', path: `/projects/${projectId}/suites`},
        {label: 'Test Plans & Results', key: 'plans', path: `/projects/${projectId}/plans`},
    ]

    const onChange = (key: string) => {
        const activeTabItem: any = tabItems.find(i => i.key === key)
        navigate(activeTabItem.path)
    }

    return (
        <Tabs activeKey={projectActiveTab} items={tabItems} onChange={onChange}/>
    )
}

export default ProjectTabs