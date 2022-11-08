import { combineReducers } from 'redux'
import treesuites from "./treesuites";
import suite from "./suite";
import suiteinfo from "./suiteinfo";
import testcase from "./testcase";

const createRootReducer = combineReducers({
    treesuites: treesuites,
    suite: suite,
    suiteinfo: suiteinfo,
    testcase: testcase,
});

export default createRootReducer