import utils from '../utils'
import push from 'react-router-redux'

export function browse_all() {
    return dispatch => {
        dispatch({
            type: 'BROWSER_BROWSE_ALL',
        })
        dispatch(load_page())
    }
}

export function filter_by_letter(letter) {
    return dispatch => {
        dispatch({
            type: 'BROWSER_FILTER_BY_LETTER',
            letter,
        })
        //dispatch(push(`/albums/letters/${letter}`))
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
        var url

        if (browser.complete || browser.loading)
            return

        dispatch({
            type: 'BROWSER_REQUEST_ITEMS',
        })

        switch (browser.items) {
            case 'Album':
                url = '/albums'
                break;
            case 'AudioFile':
            default:
                url = '/audiofiles'
                break;
        }

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



export function view_album() {
    return dispatch => {
        dispatch({
            type: 'BROWSER_REQUEST_ALBUM',
        })
        dispatch(load_page())
    }
}
