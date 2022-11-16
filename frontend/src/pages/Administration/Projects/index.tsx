import React from "react";
import {Layout, PageHeader} from "antd";

const {Content} = Layout

const Projects = () => {
    const routes = [
        {
            path: '#',
            breadcrumbName: 'Administration',
        },
        {
            path: '#',
            breadcrumbName: 'Projects',
        },
    ];

    return (
        <>
            <PageHeader
                breadcrumb={{routes}}
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