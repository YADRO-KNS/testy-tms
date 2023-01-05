import React from 'react';
import {CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {test} from "../../../../../../TMS/tms-ts/src/components/models.interfaces";
import moment from "moment/moment";
import {statuses} from "../../../../../../TMS/tms-ts/src/components/model.statuses";

const LineChartComponent = (props: {
    tests: test[]
}) => {
    const sliceOfTests = props.tests.slice(0, 100)
    // Sort tests by ascending date
    sliceOfTests.sort((a, b) =>
        moment(a.updated_at, "YYYY-MM-DDThh:mm").valueOf() - moment(b.updated_at, "YYYY-MM-DDThh:mm").valueOf())
    const result: { [key: string]: number; }[] = []
    const dates: string[] = []

    // Filling lists with date and results statuses on that date
    sliceOfTests.forEach((test) => {
        const testDate = moment(test.updated_at, "YYYY-MM-DDThh:mm").format("DD/MM/YYYY")
        if (dates[dates.length - 1] !== testDate) {
            const currentResult: { [key: string]: number; } = {}
            statuses.map((status) => currentResult[status.name.toLowerCase()] = 0)
            currentResult[String(test.current_result).toLowerCase()]++
            result.push(currentResult)
            dates.push(testDate)
        } else {
            result[result.length - 1][String(test.current_result).toLowerCase()]++
        }
    })

    // Joining date and statuses for creating data for line chart
    const lineData = dates.map((value, index) => {
            const dateData: { [key: string]: number | string | undefined; } = {
                name: value
            }
            statuses.map((status) => dateData[status.name.toLowerCase()] = result[index][status.name.toLowerCase()])
            return dateData
        }
    )


    return (
        <ResponsiveContainer height={200}>
            <LineChart data={lineData}>
                <CartesianGrid/>
                <XAxis dataKey="name"/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                {statuses.map((status, index) =>
                    <Line key={index} name={status.name} type="monotone" dataKey={status.name.toLowerCase()}
                          stroke={status.color}
                          strokeWidth={3}
                          dot={false}/>)}
            </LineChart>
        </ResponsiveContainer>
    );
};

export default LineChartComponent;