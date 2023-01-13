import {makeStyles} from "@mui/styles";


export default makeStyles({
    mainGrid: {
        marginTop: 0,
        position: "absolute",
        display: "flex",
        height: "95%",
        width: "100%"
    },
    leftGrid: {
        overflowY: "auto",
        maxHeight: "100%",
        width: "80%"
    },
    rightGrid: {
        backgroundColor: "#eeeeee",
        width: "20%",
    },
    rightGridButtons: {
        textAlign: "center"
    },
    buttonCreateCase: {
        margin: "15px 15px 0 15px",
        minWidth: "70%",
        height: "45%",
        backgroundColor: "#FFFFFF",
        color: "#000000",
        "&:hover": {
            backgroundColor: "#fffafa",
        },
    },
    buttonCreateSuite: {
        marginTop: 15,
        minWidth: "70%",
        height: "45%",
        backgroundColor: "#696969",
        color: "#FFFFFF",
        "&:hover": {
            backgroundColor: "#777676",
        },
    },
    mainGridFolderStructure: {
        height: "67%"
    },
    tableRow: {
        "& div[id=gridEditDelete]": {
            visibility: "hidden",
        },
        "&:hover": {
            "& div[id=gridEditDelete]": {
                visibility: "visible",
            },
            backgroundColor: "#eeeeee",
        },
    },
    gridEditDelete: {
        display: "flex"
    },
    caseNameCell: {
        wordBreak: "break-word"
    },
    deleteEditShowCaseCell: {
        display: "flex",
        justifyContent: "flex-end",
        padding: 5
    },
    suiteNameGrid: {
        display: "flex",
        flexDirection: "row",
        marginTop: 1,
        marginBottom: 0.32,
        maxWidth: "100%",
    },
    iconButtonDeleteSuite: {
        marginLeft: 20,
        marginTop: 15
    },
    tables: {
        padding: "9px 0 0 15px",
        marginRight: 10,
        minWidth: 300
    },
    headerTableBodyCases: {
        border: "solid",
        borderWidth: "1px 1px 1px 1px",
        backgroundColor: "#eeeeee"
    },
    cellForCheckBoxAndId: {
        width: "5%",
        padding: "7px 15px 13px 15px",
        textAlign: "center",
        marginBottom:2
    },
    cellForIdCase: {
        padding: "7px 0px 13px 0px",
    },
    tableForCases: {
        border: "solid",
        borderWidth: "0px 1px 1px 1px"
    },
    addingCaseSuite: {
        display: "flex",
        margin: "8px 0px 2px 2px",
        flexDirection: "row"
    },
    childTable: {
        borderLeft: "1px dashed"
    },
    mainTable: {
        minWidth: "99%",
        "& .MuiTableCell-root": {
            borderBottom: "none",
        }
    },
    box: {
        boxShadow: "0 3px 5px rgba(161,150,150,0.75)",
        display: "flex",
        flexDirection: "row",
        position: "sticky",
        top: 0,
        backgroundColor: "white",
        border: "1px solid",
        zIndex: 1,
        height: 40
    },
    linkOpenClose: {
        maxHeight: "50%",
        margin: 50
    },
    gridForMainTable: {
        padding: "0px 35px 20px 24px"
    },
    checkBox: {
        height: 20,
        width: 20,
    },
    suiteChip: {
        borderRadius: 20,
        backgroundColor: "#eeeeee",
        padding: "8px 13px 8px 8px",
        cursor: "pointer",
        display: "flex",
        flexDirection: "row",
        wordBreak: "break-all"
    },
    suitePaper: {
        borderRadius: 20,
        backgroundColor: "#eeeeee",
        padding: 7,
        margin: 10,
        width: "50%",
        wordBreak: "break-all"
    },
    cellSuiteChip:{
        padding: "8px 0px 1px 20px"
    },
    addCaseSuiteCell: {
        marginLeft: 10
    },
    numOfSuitesCases: {
        margin: 5
    },
    linkSuite: {
        textDecoration: "none",
        color: "black",
        fontSize: 18,
        marginLeft: 5,
        fontWeight: 500,
        "&:hover": {
            textDecoration: "underline",
        },
    }
})