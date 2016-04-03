import utils from '../utils'

export function filter_by_letter(letter) {
    return dispatch => {
        dispatch({
            type: 'BROWSER_FILTER_BY_LETTER',
            letter: letter,
        })
    }
}

export function filter_by_text(text) {
    return {
        type: 'BROWSER_FILTER_BY_TEXT',
        text: text
    }
    utils.get('/albums',query).then((albums) => {
        ...........
        this.setState({
            albums: this.state.albums.concat(albums),
            loading: false,
            exhausted: !albums.length,
        })
    })
}

export function clear(text) {
    return {
        type: 'BROWSER_CLEAR',
        text: text
    }
}
