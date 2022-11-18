import React, {useState} from "react";
import {Button, Form, Input, Modal, TreeSelect, notification, Alert} from "antd";
import {Controller, SubmitHandler, useForm} from "react-hook-form";
import {useCreateSuiteMutation} from "../../features/suite/suiteApi";
import AlertError from "../../components/AlertError";
import {useLazyGetProjectSuitesQuery} from "../../features/project/projectApi";

type Inputs = {
    name: string,
    parent: string,
};

interface ProjectCreateSuiteModalProps {
    treeSuites: any,
    projectId: number,
    isModalOpen: boolean,
    closeModal: any
}

const ProjectCreateSuiteModal = ({isModalOpen, closeModal, projectId, treeSuites}: ProjectCreateSuiteModalProps) => {
    const [createSuite, {isLoading: isLoading}] = useCreateSuiteMutation()
    const [getProjectSuites] = useLazyGetProjectSuitesQuery()
    const [errors, setErrors] = useState<any>(null)
    const {handleSubmit, reset, control} = useForm<Inputs>();
    const [parent, setParent] = useState<string | undefined>(undefined);

    const handleCancel = () => {
        if (!isLoading) {
            closeModal();
        }
    };

    const onChangeParent = (parent: string) => {
        setParent(parent)
    }

    const onSubmit: SubmitHandler<Inputs> = async (data) => {
        setErrors(null)
        try {
            await createSuite({...data, project: projectId}).unwrap()
            reset()
            closeModal()
            notification.success({
                message: "Success",
                description: "Test Suite created successfully"
            })
            getProjectSuites(projectId)
        } catch (err: any) {
            console.log(err);
            if (err?.status && err.status === 400) {
                setErrors(err.data);
            } else {
                notification.error({
                    message: 'Error!',
                    description: 'Internal server error. Showing in console log.',
                })
            }
        }
    }

    return (
        <Modal
            title="Create Test Suite"
            open={isModalOpen}
            onCancel={handleCancel}
            footer={[
                <Button key="back" onClick={handleCancel}>
                    Return
                </Button>,
                <Button key="submit" type="primary" loading={isLoading} onClick={handleSubmit(onSubmit)}>
                    Create
                </Button>,
            ]}
        >
            {errors ? <AlertError error={errors} fields={['name']}/> : null}

            <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
                <Form.Item
                    label="Name"
                    validateStatus={errors?.name ? "error" : ""}
                    help={errors?.name ? errors.name : ""}
                >
                    <Controller
                        name="name"
                        control={control}
                        render={({field}) => (
                            <Input {...field}/>
                        )}
                    />
                </Form.Item>
                <Form.Item
                    label="Parent Test Suite"
                    validateStatus={errors?.parent ? "error" : ""}
                    help={errors?.parent ? errors.parent : ""}
                >
                    <Controller
                        name="parent"
                        control={control}
                        render={({field}) => (
                            <TreeSelect
                                {...field}
                                style={{width: '100%'}}
                                dropdownStyle={{maxHeight: 400, overflow: 'auto'}}
                                treeData={treeSuites}
                                placeholder="Please select"
                                allowClear
                                treeDefaultExpandAll
                                onChange={(date) => field.onChange(date)}
                                value={field.value}
                            />
                        )}
                    />
                </Form.Item>
            </Form>
        </Modal>
    )
}

export default ProjectCreateSuiteModal