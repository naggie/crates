import { combineReducers } from 'redux'


function playlist(state = {
    last: true,
    first: true,
    cursor: 0,
    playlist: [],
}, action) {
    switch (action.type) {
        // can also be used to empty playlist. Good for loading albums.
        case "REPLACE_PLAYLIST":
            return Object.assign({}, state, {
                playlist:action.playlist,
                cursor:0,
                last:true,
                first:true,
            })
        case "ADD_ITEM_LAST":
            return Object.assign({}, state, {
                playlist:[...state.playlist,action.item],
                last:false,
            })
        case "REMOVE_ITEM":
            return Object.assign({},state,{
                playlist: state.playlist.filter((item,i) => action.index == i)
                cursor: Math.min(state.cursor,state.playlist.length-2),
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


// may use later
const rootReducer = combineReducers({
    playlist,
})

export default rootReducer

