import React from 'react';
import {BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer} from 'recharts';
import {statuses} from "../model.statuses";

const BarChartComponent = (props: { statistics: { label: string, value: number }[] }) => {
    const {statistics} = props
    let dataRecord: Record<string, number> = {}
    for (const i of statistics) {
        i.label = i.label.toLowerCase()
        dataRecord[i.label] = i.value
    }
    let data = [dataRecord]

    const fill = (label: string) => {
        return statuses.find(status => status.name.toLowerCase() === label)?.color
    }

    return (
        <ResponsiveContainer width="100%" aspect={4.0 / 1.1} data-cy="bar-chart">
            <BarChart data={data} layout="vertical">
                <XAxis hide type="number"/>
                <YAxis hide dataKey="name" reversed type="category"/>
                <Tooltip wrapperStyle={{zIndex: 100}} isAnimationActive={false}/>
                {statistics.map((tests, index) =>
                    (<Bar textAnchor={tests.label} key={index} legendType="star" label={tests.label}
                          dataKey={tests.label} stackId="a" barSize={20} fill={fill(tests.label)}/>)
                )}
            </BarChart>
        </ResponsiveContainer>
    );
};

export default BarChartComponent;