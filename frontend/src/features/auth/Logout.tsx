import React, {useEffect} from "react";
import {useDispatch} from "react-redux";
import {useNavigate} from "react-router-dom";
import ContainerLoader from "../../components/Loader/ContainerLoader";
import {logout} from "./authSlice";

const Logout = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        dispatch(logout())
        navigate("/login");
    }, []);

    return <ContainerLoader/>;
};

export default Logout