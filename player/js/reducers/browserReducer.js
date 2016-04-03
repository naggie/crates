import { combineReducers } from 'redux'


// loading = !complete
function items(state = {
    complete: false,
    class: null,
    page: 0,
    items: [],
}, action) {
    switch (action.type) {
        case "BROWSER_CLEAR":
            return {
                complete: false,
                class: null,
                page: 0,
                items: [],
            }
        case "BROWSER_ADD_ITEMS":
            return Object.assign({}, state, {
                items:[...state.items,action.items],
                cursor:state.cursor+1,
                // assuming homogeneous
                class: state.items? state.items[0].class:null,
                complete: !action.items.length,
            })
        default:
            return state
    }
}


// may use later
const rootReducer = combineReducers({
    items,
})

export default rootReducer

