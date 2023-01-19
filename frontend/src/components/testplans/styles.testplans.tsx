import {makeStyles} from "@mui/styles";


export default makeStyles({
    mainGrid: {
        marginTop: 0,
        position: "absolute",
        display: "flex",
        height: "91.5%",
        width: "100%"
    },
    leftGrid: {
        overflowY: "auto",
        maxHeight: "100%",
        width: "80%",
        justifyContent: "center",
        display: "flex"
    },
    mainTable: {
        [`& .MuiTableCell-root`]: {
            borderBottom: "none",
        }
    },
    mainBody: {
        justifyContent: "center",
    },
    splitter: {
        maxWidth: "80%"
    },
    tableCellTests: {
        "& .MuiTableCell-root": {
            paddingBottom: 0,
            paddingTop: 0
        },

    },
    rightGrid: {
        backgroundColor: "#eeeeee",
        width: "20%",
    },
    rightGridButton: {
        textAlign: "center",
    },
    centeredField: {
        "& .MuiFormLabel-root": {
            marginTop: 0
        }
    },
    tableContainer: {
        maxWidth: "91.5%",
        marginTop: "3%",
        marginLeft: "3%",
        minHeight: "93%"
    },
    icons: {
        width: '1em',
        textAlign: 'center',
        color: 'primary',
    },
    paperCreation: {
        minWidth: "94%",
        minHeight: "93%",
    },
    textFieldTestplansAndTests: {
        "& .MuiFormLabel-root": {
            margin: 0,

        },
        maxWidth: "90%",

    },
    gridContent: {
        marginTop: 17,
    },
    divTestInfo: {
        padding: 20,
        wordBreak: "break-word"
    },
    divTestInfoTitle: {
        display: "flex",
        justifyContent: "space-between"
    },
    divBold: {
        fontWeight: 'bold',
    },
    divTestInfoScenario: {
        paddingBottom: "30px"
    },
    cellCheckbox: {
        width: "5%",
        padding: "7px 15px 13px 15px",
        textAlign: "center",
    },
    checkboxTests: {
        margin: 0,
        "& .MuiFormControlLabel-root": {
            margin: 0
        },
        "& .MuiFormLabel-root": {
            margin: 0
        }
    },

})