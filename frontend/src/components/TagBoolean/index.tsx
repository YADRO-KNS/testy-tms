import {Tag} from "antd";
import React from "react";

interface TagBooleanProps {
    value: boolean,
    trueText: string,
    falseText: string
}

const TagBoolean = ({value, trueText, falseText}: TagBooleanProps) => {
    return value ? <Tag color="green">{trueText}</Tag> : <Tag color="volcano">{falseText}</Tag>
}

export default TagBoolean