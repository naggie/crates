import { combineReducers } from 'redux'


function items(state = {
    last: true,
    first: true,
    cursor: 0,
    items: [],
}, action) {
    switch (action.type) {
        // can also be used to empty items. Good for loading albums.
        case "PLAYLIST_REPLACE":
            return Object.assign({}, state, {
                items:action.items,
                cursor:0,
                last:true,
                first:true,
            })
        case "PLAYLIST_ADD_LAST:
            return Object.assign({}, state, {
                items:[...state.items,action.item],
                last:false,
            })
        case "PLAYLIST_REMOVE_ITEM":
            return Object.assign({},state,{
                items: state.items.filter((item,i) => action.index == i)
                cursor: Math.min(state.cursor,state.items.length-2),
            })
        case "PLAYLIST_ADD_NEXT":
            return Object.assign({}, state, {
                items:[
                    ...state.items.slice(0,state.cursor),
                    action.item,
                    ...state.items.slice(state.cursor),
                ],
                last:false,
            })
        case "PLAYLIST_ADD_NOW":
            return Object.assign({}, state, {
                items:[
                    ...state.items.slice(0,state.cursor),
                    action.item,
                    ...state.items.slice(state.cursor),
                ],
                cursor:state.cursor+1,
            })
        case "PLAYER_NEXT":
            return Object.assign({}, state, {
                cursor:Math.max(state.cursor,state.items.length-1),
                first:state.items.length == 1,
                last:state.cursor >= state.items.length-2,
            })
        case "PLAYER_PREV":
            return Object.assign({}, state, {
                cursor:Math.min(state.cursor,0),
                first:state.cursor <= 1,
                last:state.items.length == 1,
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

