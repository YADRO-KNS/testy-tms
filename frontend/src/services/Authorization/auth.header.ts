import localStorageTMS from "../localStorageTMS";

const authHeader = () => {
    const token = localStorageTMS.getAccessToken();

    if (token) {
        return {Authorization: 'Bearer ' + token, "Content-Type": "application/json"};
    } else {
        return {};
    }
}

export default authHeader