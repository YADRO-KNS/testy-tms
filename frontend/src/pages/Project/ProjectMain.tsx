import React from "react";
import {Link, Outlet, useParams} from "react-router-dom";
import {PageHeader, Breadcrumb, Layout} from "antd";
import {useGetProjectQuery} from "../../features/project/projectApi";
import ContainerLoader from "../../components/Loader/ContainerLoader";
import ProjectTabs from "./ProjectTabs";

const {Content} = Layout


const ProjectMain: React.FC = () => {
    const {projectId} = useParams<{ projectId: any }>();

    const {data: project, isLoading} = useGetProjectQuery(projectId)

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

            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                    <ProjectTabs projectId={projectId}/>
                    <Outlet/>
                </div>
            </Content>

        </>
    )
}

export default ProjectMain