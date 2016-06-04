export function next() {
    return {
        type: 'PLAYER_NEXT',
    }
}

export function prev() {
    return {
        type: 'PLAYER_PREV',
    }
}

export function add_next(item) {
    return {
        type: 'PLAYLIST_ADD_NEXT',
        item: item,
    }
}

export function add_last(item) {
    return {
        type: 'PLAYLIST_ADD_LAST',
        item: item,
    }
}

export function add_now(item) {
    return {
        type: 'PLAYLIST_ADD_NOW',
        item: item,
    }
}

export function load_album(id) {
    return (dispatch,getState) => {
        const { browser } = getState()
        var url

        if (browser.complete || browser.loading)
            return

        dispatch({
            type: 'BROWSER_LOAD_ALBUM',
        })

        const query = {
            album__id: id,
        }

        utils.get('/audiofiles',query).then((items) => {
            dispatch({
                type: 'PLAYLIST_REPLACE',
                items,
            })
        })
    }
}
