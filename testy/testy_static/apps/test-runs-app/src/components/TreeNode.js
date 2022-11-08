import React, {useState} from "react";
import {connect, useDispatch} from "react-redux";
import {setActiveTestPlan} from "../actions/testplans";
import {hideTestDetail} from "../actions/test";

const TreeNode = ({testplan, treetestplans}) => {
    const dispatch = useDispatch()
    const [isVisible, setIsVisible] = useState(false);
    const expand = () => {
        setIsVisible(!isVisible);
    };

    const handleClick = () => {
        dispatch(setActiveTestPlan(testplan.id))
        dispatch(hideTestDetail())
    }

    return (
        <div className="ps-2">
            <div className={"tree-node d-flex " + (isVisible ? 'open' : '')}>
                {testplan.children.length ?
                    <div className="tree-node--icon my-auto px-2" onClick={expand}>
                        {isVisible
                            ? <i className="bi bi-caret-down-fill"></i>
                            : <i className="bi bi-caret-right-fill"></i>
                        }
                    </div>
                    :
                    <React.Fragment/>
                }
                <span
                    onClick={handleClick}
                    className={"tree-node--text fs-6 p-2 flex-fill" + (testplan.children.length ? '' : ' ps-4 ') + (testplan.id === treetestplans.active ? ' active ' : '')}>
                    {testplan.title}
                </span>
            </div>
            {isVisible && testplan.children.map(testplan => <ConnectedTreeNode testplan={testplan} key={testplan.id}/>)}
        </div>
    )
}

const mapStateToProps = state => ({
    treetestplans: state.testplans
})

const ConnectedTreeNode = connect(mapStateToProps, null)(TreeNode)
export default ConnectedTreeNode