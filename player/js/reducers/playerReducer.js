import { combineReducers } from 'redux'


function playlist(state = {
    last: true,
    first: true,
    cursor: 0,
    items: []
}, action) {
    switch (action.type) {
        // can also be used to empty playlist. Good for loading albums.
        case "REPLACE_PLAYLIST":
            return Object.assign({}, state, {
                items:action.items,
                cursor:0,
                last:true,
                first:true,
            })
        case "ENQUEUE_ITEM":
            return Object.assign({}, state, {
                items:[...state.items,action.item],
                last:false,
            })
        case "PLAYLIST_REMOVE_ITEM":
            return Object.assign({},state,{
                items:state.items.filter((item,i) => action.index == i),
                cursor: Math.max(state.cursor,items.length-2)
            })
        case "PLAY_ITEM_NEXT":
            return Object.assign({}, state, {
                items:[
                    ...items.slice(0,cursor),
                    action.item,
                    ...items.slice(cursor),
                ],
                last:false,
            })
        default:
            return state
    }
}


const rootReducer = combineReducers({
    playlist,
})

export default rootReducer

