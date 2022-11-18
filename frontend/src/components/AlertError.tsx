import React from "react";
import {Alert} from "antd";

interface AlertErrorProps {
    error: any,
    fields: any
}

const AlertError = ({error, fields}: AlertErrorProps) => {
    const _errors: React.ReactNode = Object.keys(error)
        .filter(key => !fields.includes(key))
        .reduce((obj: any, key) => {
            obj[key] = error[key];
            return obj;
        }, {});

    return (
        <Alert style={{marginBottom: 24}} description={ JSON.stringify(_errors, null, 2)} type="error"/>
    )
}

export default AlertError