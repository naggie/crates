import utils from '../utils'

export function filter_by_letter(letter) {
    return dispatch => {
        dispatch({
            type: 'BROWSER_FILTER_BY_LETTER',
            letter,
        })
        dispatch(load_page())
    }
}


export function filter_by_text(text) {
    return dispatch => {
        dispatch({
            type: 'BROWSER_FILTER_BY_TEXT',
            text,
        })
        dispatch(load_page())
    }
}

// load the next (first) page
export function load_page() {
    return (dispatch,getState) => {
        const { browser } = getState()

        if (browser.complete || browser.loading)
            return

        dispatch({
            type: 'BROWSER_REQUEST_ITEMS',
        })

        const query = {
            page: browser.nextPage,
            name__istartswith : browser.letter,
            order_by : 'name',
            name__icontains: browser.searchText,
        }

        utils.get('/albums',query).then((items) => {
            dispatch({
                type: 'BROWSER_RECEIVE_ITEMS',
                items,
            })
        })
    }
}
