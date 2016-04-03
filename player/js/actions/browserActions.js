

export function filter_by_letter(letter) {
    return {
        type: 'BROWSER_FILTER_BY_LETTER',
        letter: letter
    }
}

export function filter_by_text(text) {
    return {
        type: 'BROWSER_FILTER_BY_TEXT',
        text: text
    }
}

export function clear(text) {
    return {
        type: 'BROWSER_CLEAR',
        text: text
    }
}
