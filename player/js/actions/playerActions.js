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

export function add_next(file) {
    return {
        type: 'PLAYLIST_ADD_NEXT',
        file: file,
    }
}

export function add_last(file) {
    return {
        type: 'PLAYLIST_ADD_LAST',
        file: file,
    }
}

export function add_now(file) {
    return {
        type: 'PLAYLIST_ADD_NOW',
        file: file,
    }
}
