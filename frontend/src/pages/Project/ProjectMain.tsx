import React, {useContext, useEffect, useState} from "react";
import {Link, Outlet, useParams} from "react-router-dom";
import {PageHeader, Breadcrumb, Layout} from "antd";
import {useGetProjectQuery} from "../../features/project/projectApi";
import ContainerLoader from "../../components/Loader/ContainerLoader";
import ProjectTabs from "./ProjectTabs";
import {MenuContext} from "../../layouts/Main";

const {Content} = Layout

export const ProjectActiveTabContext = React.createContext<any>("")

const ProjectMain: React.FC = () => {
    const {setActiveMenu} = useContext(MenuContext)
    useEffect(() => {
        setActiveMenu(["dashboard"])
    }, [])
    const {projectId} = useParams<{ projectId: any }>();
    const {data: project, isLoading} = useGetProjectQuery(projectId)
    const [projectActiveTab, setProjectActiveTab] = useState("")
    if (isLoading) return <ContainerLoader/>

    const breadcrumbItems = [
        <Breadcrumb.Item key="dashboard">
            <Link to="/">Dashboard</Link>
        </Breadcrumb.Item>,
        <Breadcrumb.Item key={projectId}>
            {project?.name}
        </Breadcrumb.Item>,
    ]

    return (
        <>
            <PageHeader
                breadcrumbRender={() => <Breadcrumb>{breadcrumbItems}</Breadcrumb>}
                title={project?.name}
            >
            </PageHeader>
            <ProjectActiveTabContext.Provider value={{projectActiveTab, setProjectActiveTab}}>
                <Content style={{margin: '24px'}}>
                    <div className="site-layout-background" style={{padding: 24}}>
                        <ProjectTabs projectId={projectId}/>
                        <Outlet context={projectId}/>
                    </div>
                </Content>
            </ProjectActiveTabContext.Provider>
        </>
    )
}

export default ProjectMain