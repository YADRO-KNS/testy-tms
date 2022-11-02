import React from "react";
import ContentBlock from "./ContentBlock";
import TreeTestPlans from "./TreeTestPlans";
import NotSelectedTestPlan from "./ContentBlock";

const TestPlanContent = () => {

    return (
        <div className="row">
            <div className="col-3">
                <TreeTestPlans/>
            </div>
            <div className="col-9">
                <ContentBlock/>
            </div>
        </div>
    )
}

export default TestPlanContent