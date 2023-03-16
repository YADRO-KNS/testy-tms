import {put} from "../features/currentProject/currentProjectSlice";
import {useDispatch, useSelector} from "react-redux";
import {project} from "../components/models.interfaces";
import {RootState, store} from "../app/store";

export default class localStorageTMS {
    static getAccessToken = () => localStorage.getItem("accessToken");

    static setAccessToken = (token: string) => localStorage.setItem("accessToken", token);

    static removeAccessToken = () => localStorage.removeItem("accessToken");

    static getRefreshToken = () => localStorage.getItem("refreshToken");

    static setRefreshToken = (token: string) => localStorage.setItem("refreshToken", token);

    static removeRefreshToken = () => localStorage.removeItem("refreshToken");

    static getCurrentProject = () => store.getState().currentProject.value ?? {
        id: 0,
        name: "",
        description: ""
    };

    static setCurrentProject = (project: project) => store.dispatch(put(project));

    // static removeCurrentProject = () => localStorage.removeItem("currentProject");

    static getElementByKey = (key: string) => localStorage.getItem(key);

    static setElementByKey = (key: string, value: string) => localStorage.setItem(key, value);

    static removeElementByKey = (key: string) => localStorage.removeItem(key);

}
