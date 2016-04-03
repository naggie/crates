import { combineReducers } from 'redux'


function playlist(state = {
    last: true,
    first: true,
    cursor: 0,
    playlist: [],
    current:null,
}, action) {
    switch (action.type) {
        // can also be used to empty playlist. Good for loading albums.
        case "REPLACE_PLAYLIST":
            return Object.assign({}, state, {
                playlist:action.playlist,
                cursor:0,
                last:true,
                first:true,
                current:action.playlist[0],
            })
        case "ADD_ITEM_LAST":
            return Object.assign({}, state, {
                playlist:[...state.playlist,action.item],
                last:false,
            })
        case "REMOVE_ITEM":
            var next_cursor = Math.min(state.cursor,state.playlist.length-2)
            var next_items = state.playlist.filter((item,i) => action.index == i)
            return Object.assign({},state,{
                playlist:next_items,
                cursor: next_cursor,
                current:next_items[next_cursor],
            })
        case "ADD_ITEM_NEXT":
            return Object.assign({}, state, {
                playlist:[
                    ...state.playlist.slice(0,cursor),
                    action.item,
                    ...state.playlist.slice(cursor),
                ],
                last:false,
            })
        case "PLAY_NEXT":
            return Object.assign({}, state, {
                cursor:Math.max(cursor,state.playlist.length-1),
                first:state.playlist.length == 1,
                last:state.cursor >= state.playlist.length-2,
            })
        case "PLAY_PREV":
            return Object.assign({}, state, {
                cursor:Math.min(cursor,0),
                first:state.cursor <= 1,
                last:state.playlist.length == 1,
            })
        default:
            return state
    }
}


const rootReducer = combineReducers({
    playlist,
})

export default rootReducer

