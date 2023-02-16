import {treeSuite} from "./suites.component";
import {myCase} from "../models.interfaces";
import React from "react";
import Checkbox from "@mui/material/Checkbox";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";

function RowCase(props: {
    row: treeSuite, setShowCreationCase: (show: boolean) => void,
    setSelectedSuiteCome: (selectedSuite: { id: number, name: string } | null) => void,
    setDetailedCaseInfo: (myCase: { show: boolean, myCase: myCase }) => void,
    detailedCaseInfo: { show: boolean, myCase: myCase }, setInfoCaseForEdit: (myCase: myCase) => void,
    onecase: myCase,
    selected: number [], setSelected: (ids: number[]) => void,
    setTreeSuites: (treeSuites: treeSuite[]) => void,
    setOpenDialogDeletion: (show: boolean) => void,
    setComponentForDeletion: (component: myCase | treeSuite) => void,
    classesTableSuitesCases: any
}) {
    const {
        row,
        setShowCreationCase,
        setSelectedSuiteCome,
        setDetailedCaseInfo,
        setInfoCaseForEdit,
        onecase,
        selected,
        setSelected,
        setOpenDialogDeletion,
        setComponentForDeletion,
        classesTableSuitesCases
    } = props;
    const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
        const selectedIndex = selected.indexOf(id);
        let newSelected: number[] = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };

    return (
        <tr
            className={classesTableSuitesCases.tableRow}
        >
            <td className={classesTableSuitesCases.cellForCheckBoxAndId}>
                <Checkbox
                    className={classesTableSuitesCases.checkBox}
                    onClick={(event) => handleClick(event, onecase.id)}
                    color="primary"
                    checked={selected.indexOf(onecase.id) !== -1}
                />
            </td>
            <TableCell component="th"
                       scope="row"
                       padding="none">
                {onecase.id}
            </TableCell>
            <TableCell className={classesTableSuitesCases.caseNameCell}>
                {onecase.name}
            </TableCell>
            <td className={classesTableSuitesCases.deleteEditShowCaseCell}>
                <div id="gridEditDelete" className={classesTableSuitesCases.gridEditDelete}>
                    <IconButton size={"small"} onClick={() => {
                        setComponentForDeletion(onecase)
                        setOpenDialogDeletion(true)
                    }}>
                        <DeleteIcon fontSize={"small"}/>
                    </IconButton>
                    <IconButton size={"small"} onClick={() => {
                        setShowCreationCase(true)
                        setSelectedSuiteCome({id: row.id, name: row.name})
                        setInfoCaseForEdit(onecase)
                    }}>
                        <EditIcon fontSize={"small"}/>
                    </IconButton>
                </div>
                <div id={onecase.id.toString() + "Arrow"}>
                    <IconButton size={"small"} onClick={() => {
                        setDetailedCaseInfo({
                            show: true,
                            myCase: onecase
                        })
                    }}>
                        <KeyboardArrowRightIcon/>
                    </IconButton>
                </div>
            </td>
        </tr>)
}

export default RowCase