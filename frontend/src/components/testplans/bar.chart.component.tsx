import React from 'react';
import {BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer} from 'recharts';

interface Props {
    passed: number;
    skipped: number;
    failed: number;
    blocked: number;
    untested: number;
    broken: number
}

const BarChartComponent: React.FC<Props> = ({passed, skipped, failed, blocked, untested, broken}) => {
    const data = [
        {
            passed: passed,
            skipped: skipped,
            failed: failed,
            blocked: blocked,
            untested: untested,
            broken: broken
        },
    ];

    return (
        <ResponsiveContainer width="100%" aspect={4.0 / 1.3}>
            <BarChart data={data} layout="vertical">
                <XAxis hide type="number"/>
                <YAxis hide dataKey="name" reversed type="category"/>
                <Tooltip wrapperStyle={{zIndex: 100}} isAnimationActive={false}/>
                <Bar legendType="star" label="passed" dataKey="passed" barSize={20} stackId="a" fill="#24b124"/>
                <Bar legendType="star" label="skipped" dataKey="skipped" stackId="a" fill="#c4af30"/>
                <Bar legendType="star" label="failed" dataKey="failed" stackId="a" fill="#bd2828"/>
                <Bar legendType="star" label="blocked" dataKey="blocked" stackId="a" fill="#6c6c6c"/>
                <Bar legendType="star" label="untested" dataKey="untested" stackId="a" fill="#a5a4a4"/>
                <Bar legendType="star" label="broken" dataKey="broken" stackId="a" fill="#724127"/>
            </BarChart>
        </ResponsiveContainer>
    );
};

export default BarChartComponent;