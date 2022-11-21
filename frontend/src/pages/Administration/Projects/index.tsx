import React from "react";
import {Breadcrumb, Layout, PageHeader} from "antd";
import {Link} from "react-router-dom";

const {Content} = Layout

const Projects = () => {
    const breadcrumbItems = [
        <Breadcrumb.Item key="administration">
            Administration
        </Breadcrumb.Item>,
        <Breadcrumb.Item key="projects">
            Projects
        </Breadcrumb.Item>,
    ]

    return (
        <>
            <PageHeader
                breadcrumbRender={() => <Breadcrumb>{breadcrumbItems}</Breadcrumb>}
                title="Projects"
            >
            </PageHeader>

            <Content style={{margin: '24px'}}>
                <div className="site-layout-background" style={{padding: 24, minHeight: 360}}>
                    <p>Projects</p>
                </div>
            </Content>
        </>
    )
}

export default Projects