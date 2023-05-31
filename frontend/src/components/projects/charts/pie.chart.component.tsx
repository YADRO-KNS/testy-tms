import React, {useMemo} from 'react';
import {Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip} from "recharts";
import {test} from "../../models.interfaces";

const PieChartComponent = (props: {
    tests: test[]
}) => {
    let nTestsWithoutUser = useMemo(() => {
        let temp = 0
        props.tests.forEach((test) => {
            if (test.user == null) {
                temp++
            }
        })
        return temp
    }, [])
    // Counting tests with assigned user

    const pieData = [
        {name: 'Назначено', value: props.tests.length - nTestsWithoutUser},
        {name: 'Не назначено', value: nTestsWithoutUser},
    ];

    return (
        <ResponsiveContainer height={200}>
            <PieChart>
                <Pie data={pieData} dataKey={"value"} labelLine={true}>
                    <Cell fill={"#98d589"}/>
                    <Cell fill={"#d99292"}/>
                </Pie>
                <Legend/>
                <Tooltip formatter={(value, name) => ["Тестов: " + value, name]}/>
            </PieChart>
        </ResponsiveContainer>
    );
};

export default PieChartComponent;