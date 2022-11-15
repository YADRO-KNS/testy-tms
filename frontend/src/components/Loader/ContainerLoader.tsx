import React from "react";
import {Spin} from "antd";
import './ContainerLoader.css'

const ContainerLoader: React.FC = () => {
    return (
        <div className="container-loader">
            <Spin/>
        </div>
    )
}

export default ContainerLoader

