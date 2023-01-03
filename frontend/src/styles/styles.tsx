import {makeStyles} from "@material-ui/core/styles";
import {alpha} from "@mui/material";


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
    textFieldSelectCreationCaseSuiteNotFilled: {
        maxWidth: "90%",
        "& .MuiFormLabel-root": {
            marginTop: 0,
            color: '#000000',
        },
        "& .MuiFormHelperText-root": {
            marginLeft: 3,
            fontSize: 13,
            color: '#000000',
            fontWeight: 550
        },
        '& label.Mui-focused': {
            color: '#000000',
        },
        '& .MuiOutlinedInput-root': {
            '& fieldset': {
                borderColor: '#000000',
                borderWidth: "2px",
            },
            '&.Mui-focused fieldset': {
                borderColor: '#000000',
                borderWidth: "3px",
            },
            '&:hover fieldset': {
                borderColor: '#000000',
                borderWidth: "3px",
            },
        },
    },
    textFieldSelectCreationCaseSuite: {
        maxWidth: "90%",
        "& .MuiFormLabel-root": {
            marginTop: 0
        }
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
    checkboxTests: {
        margin: 0,
        "& .MuiFormControlLabel-root": {
            margin: 0
        },
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
        // width: 500,
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
        // width: '60%',
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
    icons: {
        // fontSize: 'small',
        width: '1em',
        textAlign: 'center',
        color: 'primary',
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
        // height: "50%",
        // marginBottom: 100,
        width: "max-content",
        maxHeight: "50%",
        // "& .MuiCollapse-wrapperInner":{
        //     textAlign: "center"
        // },
        // "& .MuiPaper-root":{
        //     height: "50%",
        alignItems: "center",
        // borderRadius: "20px 10px 10px 20px",
        // },
        "& .MuiAlert-message": {
            fontSize: 12,
            overflowY: "hidden",
        },
        "& .MuiAlert-icon": {
            fontSize: 17
        },
        // '&::after': {
        //     content: '',
        //     position: "absolute",
        //     left: 0,
        //     right: 0,
        //     margin: "0 auto",
        //     borderBottom: "10px solid #6A0136",
        //     width: 0,
        //     height: 0,
        //     borderTop: "25px solid #6A0136",
        //     borderLeft: "50px solid transparent",
        //     borderRight: "50px solid transparent",
        //     // border-top: "25px solid #6A0136",
        //     // border-left: "50px solid transparent",
        //     // border-right: "50px solid transparent",
        // },
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
        // marginBottom: 10,
        "&::before": {
            marginBottom: 10,
            border: "1px solid #000",
            backgroundColor: "#fff",
            boxSizing: "border-box"
        }
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
    centeredField: {
        "& .MuiFormLabel-root": {
            marginTop: 0
        }
    },
    /*clickableLabels: {
        display: 'flex',

        /!*> *
            {
                width: 50 %,
            }*!/
    },


    expandAllContainer: {
    maxWidth
:
    400
    px;
}

.
rct - node - icon.far
{
    width: 1
    em;
    text - align
:
    center;
}

.
filter - container >
.
filter - text
{
    display: block;
    margin - bottom
:
    .75
    rem;
    border: 1
    px
    solid
    $input - border - color;
    border - radius
:
    .25
    rem;
    background - clip
:
    padding - box;
    padding: .375
    rem
    .75
    rem;
    line - height
:
    1.5;
    font - size
:
    1
    rem;
}*/
})
;
