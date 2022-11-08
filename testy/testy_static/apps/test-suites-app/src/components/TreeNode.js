import React, {useState} from "react";
import {connect, useDispatch} from "react-redux";
import {setActiveSuite} from "../actions/treesuites";
import {hideCaseDetail} from "../actions/testcase";

const TreeNode = ({suite, treesuites}) => {
    const dispatch = useDispatch()
    const [isVisible, setIsVisible] = useState(false);
    const expand = () => {
        setIsVisible(!isVisible);
    };

    const handleClick = () => {
        dispatch(setActiveSuite(suite.id))
        dispatch(hideCaseDetail())
    }

    return (
        <div className="ps-2">
            <div className={"tree-node d-flex " + (isVisible ? 'open' : '')}>
                {suite.children.length ?
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
                    className={"tree-node--text fs-6 p-2 flex-fill" + (suite.children.length ? '' : ' ps-4 ') + (suite.id === treesuites.active ? ' active ' : '')}>
                    {suite.name}
                </span>
            </div>
            {isVisible && suite.children.map(suite => <ConnectedTreeNode suite={suite} key={suite.id}/>)}
        </div>
    )
}

const mapStateToProps = state => ({
    treesuites: state.treesuites
})

const ConnectedTreeNode = connect(mapStateToProps, null)(TreeNode)
export default ConnectedTreeNode