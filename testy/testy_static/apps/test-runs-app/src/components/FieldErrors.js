import React from "react";


const FieldErrors = ({errors}) => {
    return errors ? errors.map((error, index) => <p className="invalid-feedback" key={index}>{error}</p>) : ''
}

export default FieldErrors