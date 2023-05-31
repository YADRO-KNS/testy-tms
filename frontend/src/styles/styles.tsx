import {makeStyles} from "@mui/styles";


export default makeStyles({
    button: {
        backgroundColor: "#ff0000",
    },
    paperCreationTestCase: {
        minWidth: "94%",
        minHeight: "93%",
    },
    paperCreationSuite: {
        minWidth: "65%",
        minHeight: "65%",
    },
    dialogTitle: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: -20
    },
    textFieldSelectCreationCaseSuite: {
        maxWidth: "90%",
        "& .MuiFormLabel-root": {
            marginTop: 0
        }
    },
    gridContent: {
        marginTop: 17,
    },
    stackTags: {
        maxWidth: "90%",
        maxHeight: 150,
        marginTop: 8,
        overflowY: "auto",
    },
    tagsInput: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginTop: -20
    },
    tut: {
        backgroundColor: "red"
    },
    buttonTxt: {
        "& .MuiButton-textSizeMedium": {
            fontSize: 50
        },
    },
    rootLogin: {
        "& .MuiFormLabel-root": {
            margin: 0
        }
    },
    divLogin: {
        margin: 20,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    paperLogin: {
        marginTop: 40,
        minWidth: 300,
        minHeight: 300
    },
    formLogin: {
        width: '100%',
        marginTop: 5,
    },
    submitLogin: {
        backgroundColor: '#3f51b5',
    },
    divProjectSelectionPage: {
        marginTop: 100,
        alignItems: 'center',
        flexDirection: 'column',
    },
    divProjectSelectionPageLine: {
        flexDirection: 'row',
        display: 'flex',
        marginTop: 10,
    },
    paperCreationProject: {
        borderRadius: 10
    },
    chipTagsStatusInSuites: {
        minWidth: 90,
        maxHeight: 25,
        padding: 3,
    },
    gridTags: {
        overflowY: "hidden",
        maxHeight: 70,
    },
    gridScenario: {
        overflowY: "hidden",
        maxHeight: 43,
    },
    tree: {
        fontSize: 'small'
    },
    collapse: {
        "& .MuiCollapse-root": {
            maxHeight: 40
        }
    },
    alertNotFilled: {
        width: "max-content",
        maxHeight: "50%",
        alignItems: "center",
        "& .MuiAlert-message": {
            fontSize: 12,
            overflowY: "hidden",
        },
        "& .MuiAlert-icon": {
            fontSize: 17
        },
    },
    triangle: {
        width: 0,
        height: 0,
        marginLeft: 158.2,
        backgroundColor: 'transparent',
        borderStyle: 'solid',
        borderTopWidth: 15,
        borderRightWidth: 10,
        borderBottomWidth: 0,
        borderLeftWidth: 10,
        borderBottomColor: 'transparent',
        borderRightColor: 'transparent',
        borderTopColor: '#fff4e5',
        borderLeftColor: 'transparent',
        borderTopRightRadius: 5,
        marginTop: -1.9,
    },
    tooltip: {
        background: "#fff",
        color: "#000",
        border: "1px solid #000",
        borderRadius: 0,
    },
    arrow: {
        fontSize: 16,
        width: 17,
        "&::before": {
            marginBottom: 10,
            border: "1px solid #000",
            backgroundColor: "#fff",
            boxSizing: "border-box"
        }
    },
    centeredField: {
        "& .MuiFormLabel-root": {
            marginTop: 0
        }
    },
})
;
