import React, {useState} from "react";
import {Alert, Button, Form, Input} from 'antd';
import {SubmitHandler, useForm, Controller} from "react-hook-form";
import {useLoginMutation} from "./authApi";
import {useNavigate} from "react-router-dom";
import {setCredentials} from "./authSlice";
import {useDispatch} from "react-redux";

type Inputs = {
    username: string,
    password: string,
};

const Auth: React.FC = () => {
    const [login, {isLoading}] = useLoginMutation()
    const [errMsg, setErrMsg] = useState('')
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const {handleSubmit, reset, control} = useForm<Inputs>();

    const onSubmit: SubmitHandler<Inputs> = async (data) => {
        setErrMsg('')
        try {
            const response = await login(data).unwrap()
            dispatch(setCredentials(response))
            reset()
            navigate('/')
        } catch (err: any) {
            if (!err?.status) {
                setErrMsg('No Server Response');
            } else if (err.status === 400) {
                setErrMsg('Missing Username or Password');
            } else if (err.status === 401) {
                setErrMsg('Unauthorized');
            } else {
                setErrMsg('Login Failed');
            }
        }
    }

    return (
        <>
            {errMsg ? <Alert style={{marginBottom: 24}} description={errMsg} type="error"/> : null}

            <Form onFinish={handleSubmit(onSubmit)} layout="vertical">
                <Form.Item label="Username">
                    <Controller
                        name="username"
                        control={control}
                        render={({field}) => (
                            <Input {...field}/>
                        )}
                    />
                </Form.Item>
                <Form.Item label="Password" name="password">
                    <Controller
                        name="password"
                        control={control}
                        render={({field}) => (
                            <Input.Password {...field}/>
                        )}
                    />
                </Form.Item>
                <Form.Item>
                    <Button size="large" type="primary" htmlType="submit" block>
                        Login
                    </Button>
                </Form.Item>
            </Form>
        </>
    )
}

export default Auth