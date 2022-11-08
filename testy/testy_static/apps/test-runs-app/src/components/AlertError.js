import React from "react";

const AlertError = ({error, fields}) => {
    const _errors = Object.keys(error)
        .filter(key => !fields.includes(key))
        .reduce((obj, key) => {
            obj[key] = error[key];
            return obj;
        }, {});

    return (
        Object.keys(_errors).length ?
            <div className="alert alert-danger">
                <pre className="m-0">{JSON.stringify(_errors, null, 2)}</pre>
            </div>
            : ''
    )
}

export default AlertError