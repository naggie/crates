// loading = !complete
function albumBrowser(state = {
    complete: false,
    loading: false,
    model: 'Album',
    nextPage: 0,
    items: [],
    letter:null,
    searchText:null,
    cover_ref:null,
}, action) {
    switch (action.type) {
        case "BROWSER_BROWSE_ALL":
            return Object.assign({},state,{
                nextPage: 0,
                letter:null,
                items: [],
                complete: false,
                searchText:null,
            })
        case "BROWSER_FILTER_BY_TEXT":
            return Object.assign({},state,{
                nextPage: 0,
                letter:null,
                items: [],
                complete: false,
                searchText:action.text,
            })
        case "BROWSER_FILTER_BY_LETTER":
            return Object.assign({},state,{
                nextPage: 0,
                letter:action.letter,
                items: [],
                complete: false,
                searchText:null,
            })
        case "BROWSER_REQUEST_ITEMS":
            return Object.assign({},state,{
                loading:true,
            })
        case "BROWSER_RECEIVE_ITEMS":
            return Object.assign({}, state, {
                items:[...state.items,...action.items],
                nextPage:state.nextPage+1,
                // assuming homogeneous
                model: state.items.length? state.items[0].model:null,
                complete: !action.items.length,
                loading:false,
            })
        default:
            return state
    }
}


// may use later
export default albumBrowser

