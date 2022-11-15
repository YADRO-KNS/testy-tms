import React from "react";
import {Card, List, Tooltip} from "antd";
import BriefcaseIcon from "../../components/Icons/BriefcaseIcon";
import {useGetProjectsQuery} from "../../features/project/projectApi";
import ContainerLoader from "../../components/Loader/ContainerLoader";

const ProjectCards: React.FC = () => {

    const {data: projects, isLoading} = useGetProjectsQuery();

    if (isLoading) {
        return <ContainerLoader/>
    }

    return (
        <List
            rowKey="id"
            grid={{gutter: 24, xxl: 3, xl: 2, lg: 2, md: 2, sm: 2, xs: 1}}
            dataSource={projects}
            renderItem={item => (
                <List.Item key={item.id}>
                    <Card
                        hoverable
                        bodyStyle={{paddingBottom: 20}}
                        actions={[
                            <Tooltip title="Overview">
                                <a>Overview</a>
                            </Tooltip>,
                            <Tooltip title="Test Suites">
                                <a>Test Suites</a>
                            </Tooltip>,
                            <Tooltip title="Test Plans">
                                <p>Test Plans</p>
                            </Tooltip>,
                        ]}
                    >
                        <Card.Meta avatar={<BriefcaseIcon style={{fontSize: 24}}/>} title={item.name}/>
                    </Card>
                </List.Item>
            )}
        />
    )
}

export default ProjectCards