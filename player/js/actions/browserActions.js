import utils from '../utils'

export function filter_by_letter(letter) {
    return dispatch => {
        dispatch({
            type: 'BROWSER_FILTER_BY_LETTER',
            letter,
        })
    }
}


export function filter_by_text(text) {
    return {
        type: 'BROWSER_FILTER_BY_TEXT',
        text,
    }
}

// load the next (first) page
export function load_page(letter) {
    return (dispatch,getState) => {
        const { browser } = getState()

        const query = {
            page: browser.nextPage,
            name__istartswith : browser.letter,
            order_by : 'name',
        }

        utils.get('/albums',query).then((items) => {
            dispatch({
                type: 'BROWSER_RECEIVE_ITEMS',
                items,
            })
        })
    }
}

export function clear(text) {
    return {
        type: 'BROWSER_CLEAR',
        text
    }
}
