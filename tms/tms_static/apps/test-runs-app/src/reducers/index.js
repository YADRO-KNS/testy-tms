import { combineReducers } from 'redux'
import testplans from "./testplans";
import testplaninfo from  "./testplaninfo";
import test from "./test";

const createRootReducer = combineReducers({
    testplans: testplans,
    testplaninfo: testplaninfo,
    test: test,
});

export default createRootReducer