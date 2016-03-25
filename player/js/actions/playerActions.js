// human

export function play() {
    return {
        type: 'PLAYER_PLAY',
    }
}

export function pause() {
    return {
        type: 'PLAYER_PAUSE',
    }
}

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

export function enqueue(file) {
    return {
        type: 'PLAYER_ENQUEUE',
        file: file,
    }
}


// machine

export function update_progress(seconds) {
    return {
        type: 'PLAYER_UPDATE_PROGRESS',
        seconds: seconds,
    }
}

export function update_buffer_progress(seconds) {
    return {
        type: 'PLAYER_UPDATE_BUFFER_PROGRESS',
        seconds: seconds,
    }
}

