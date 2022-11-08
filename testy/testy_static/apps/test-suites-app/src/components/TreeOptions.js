import React, {Fragment} from "react";
import {connect} from "react-redux";

const TreeOptions = ({item, state}) => {

    const getName = (item) => {
        return '-'.repeat(item.level) + ' ' + item.name
    }

    return (
        <Fragment>
            <option value={item.id}>{getName(item)}</option>
            {item.children.map(item => <ConnectedTreeOptions key={item.id} item={item} />)}
        </Fragment>
    )
}

const mapStateToProps = state => ({
    state: state
})

const ConnectedTreeOptions = connect(mapStateToProps, null)(TreeOptions)
export default ConnectedTreeOptions