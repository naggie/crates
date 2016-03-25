

export function filter_albums_by_letter(letter) {
    return {
        type: 'FILTER_ALBUMS_BY_LETTER',
        letter: letter
    }
}

export function filter_albums_by_keyword(keyword) {
    return {
        type: 'FILTER_ALBUMS_BY_LETTER',
        keyword: keyword
    }
}
