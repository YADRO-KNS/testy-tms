import React from 'react';
import {Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip} from "recharts";
import {test} from "../../models.interfaces";

const PieChartComponent = (props: {
    tests: test[]
}) => {
    let nTestsWithoutUser = 0
    // Counting tests with assigned user
    props.tests.forEach((test) => {
        if (test.user == null) {
            nTestsWithoutUser++
        }
    })
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
                <Tooltip formatter={(value, name) => ["Тестов назначено -- " + value, name]}/>
            </PieChart>
        </ResponsiveContainer>
    );
};

export default PieChartComponent;