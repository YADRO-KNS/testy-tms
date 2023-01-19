const authHeader = () => {
    const token = localStorage.getItem("accessToken");

    if (token) {
        return {Authorization: 'Bearer ' + token, "Content-Type": "application/json"};
    } else {
        return {};
    }
}

export default authHeader