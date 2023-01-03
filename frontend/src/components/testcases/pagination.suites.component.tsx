import {treeSuite} from "./suites.component";
import {Pagination, TextField} from "@mui/material";
import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import useStylesTestCases from "./styles.testcases"

function PaginationSuitesComponent(props: { treeSuites: treeSuite[], countOfSuitesOnPage: number }) {
    const {treeSuites, countOfSuitesOnPage} = props;
    const [page, setPage] = useState(1);
    const classes = useStylesTestCases()
    const [foundSuites, setFoundSuites] = useState<treeSuite[]>(treeSuites)

    useEffect(() => {
        setFoundSuites(treeSuites)
    }, [treeSuites])

    const onChangeName = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const foundSuites2 = treeSuites.filter(suite => suite.name.toLowerCase().includes(e.target.value.toLowerCase()))
        setFoundSuites(foundSuites2)
        setPage(1)
    }


    return (
        <div style={{display: "flex", flexDirection: "column", margin: "0 0 0 30px"}}>
            <TextField
                onChange={(content) => onChangeName(content)}
                autoComplete="off"
                style={{width: "50%", margin: 10}}
                placeholder="Поиск..."
                variant={"outlined"}
            />
            {foundSuites.slice(page * countOfSuitesOnPage - countOfSuitesOnPage,
                page * countOfSuitesOnPage)
                .map((suite) => (
                    <div key={suite.id} className={classes.suitePaper}>
                        <Link className={classes.linkSuite} to={`${suite.id}`}>
                            {suite.name}
                        </Link>
                        <div className={classes.numOfSuitesCases}>Количество сьют: 10</div>
                        <div className={classes.numOfSuitesCases}>Количество тест-кейсов: 10</div>
                    </div>
                ))}
            <Pagination
                count={Math.ceil(foundSuites.length / countOfSuitesOnPage)}
                page={page}
                onChange={(_, num) => setPage(num)}
                sx={{marginY: 1, marginX: 1}}
            />
        </div>
    )
}

export default PaginationSuitesComponent