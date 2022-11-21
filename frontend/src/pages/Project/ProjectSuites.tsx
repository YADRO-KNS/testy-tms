import React, {useContext, useEffect, useState} from "react";
import {Col, Divider, Row, Tree, Input, Empty, TreeProps, Button, Modal, Form, TreeSelect} from "antd";
import ContainerLoader from "../../components/Loader/ContainerLoader";
import {useOutletContext} from "react-router-dom";
import {useGetProjectSuitesQuery} from "../../features/project/projectApi";
import ProjectSuiteDetail from "./ProjectSuiteDetail";
import {PlusCircleOutlined} from "@ant-design/icons";
import ProjectCreateSuiteModal from "./ProjectCreateSuiteModal";
import {ProjectActiveTabContext} from "./ProjectMain";

const {Search} = Input;

const ProjectSuites = () => {
    const {setProjectActiveTab} = useContext(ProjectActiveTabContext)
    useEffect(() => {
        setProjectActiveTab('suites')
    }, [])

    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [suiteId, setSuiteId] = useState<string | null>(null)
    const projectId: number = useOutletContext()
    const {data: treeSuites, isLoading} = useGetProjectSuitesQuery(projectId)

    if (isLoading) return <ContainerLoader/>

    const onSelect: TreeProps['onSelect'] = (selectedKeys) => {
        setSuiteId(selectedKeys[0].toString())
    };

    const showModal = () => {
        setIsModalOpen(true);
    };

    return (
        <>
            <Row style={{minHeight: 360}}>
                <Col flex="350px">
                    <Button icon={<PlusCircleOutlined/>} type="dashed" block onClick={showModal}>Create Test
                        Suite</Button>
                    <Search style={{marginBottom: 8, marginTop: 8}} placeholder="Search"/>
                    <Tree showLine treeData={treeSuites} onSelect={onSelect}/>
                </Col>
                <Col>
                    <Divider type="vertical" style={{height: "100%"}}/>
                </Col>
                <Col flex="auto">
                    {suiteId ? <ProjectSuiteDetail suiteId={suiteId}/> : <Empty/>}
                </Col>
            </Row>
            <ProjectCreateSuiteModal
                isModalOpen={isModalOpen}
                closeModal={() => setIsModalOpen(false)}
                treeSuites={treeSuites}
                projectId={projectId}
            />
        </>
    )
}

export default ProjectSuites