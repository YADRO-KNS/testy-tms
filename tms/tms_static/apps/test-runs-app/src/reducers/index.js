import { combineReducers } from 'redux'
import testplans from "./testplans";

const createRootReducer = combineReducers({
    testplans: testplans
});

export default createRootReducer