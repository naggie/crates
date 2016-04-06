import { combineReducers } from 'redux'


// loading = !complete
function browser(state = {
    complete: false,
    loading: true,
    class: null,
    nextPage: 0,
    items: [],
    letter:null,
    searchText:null,
}, action) {
    switch (action.type) {
        case "BROWSER_FILTER_BY_LETTER":
            return Object.assign({},state,{
                nextPage: -1,
                letter:action.letter,
                loading:true,
                items: [],
                complete: false,
                searchText:null,
            })
        case "BROWSER_FILTER_BY_TEXT":
            return Object.assign({},state,{
                nextPage: -1,
                letter:null,
                loading:true,
                items: [],
                complete: false,
                searchText:action.text,
            })
        case "BROWSER_RECEIVE_ITEMS":
            return Object.assign({}, state, {
                items:[...state.items,action.items],
                nextPage:state.nextPage+1,
                // assuming homogeneous
                class: state.items? state.items[0].class:null,
                complete: !action.items.length,
                loading:false,
            })
        default:
            return state
    }
}


// may use later
//const rootReducer = combineReducers({
//    browser,
//})

//export default rootReducer
export default browser

