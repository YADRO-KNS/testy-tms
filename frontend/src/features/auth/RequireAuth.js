import React from "react";
import {selectAccessToken} from "./authSlice";
import {useLocation, Navigate, Outlet} from "react-router-dom";
import {useSelector} from "react-redux";

const RequireAuth = () => {
    const token = useSelector(selectAccessToken)
    const location = useLocation()

    return (
        token
            ? <Outlet/>
            : <Navigate to="/login" state={{ form: location }} replace/>
    )
}

export default RequireAuth