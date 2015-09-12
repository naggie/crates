var alt = require('../alt')
var utils = require('../utils')

// NOTE TO READER: Actions are decoupled from stores so that multiple stores can
// subscribe to a given action.
//
// Alt docs mention that there is no correct place for async state management:
// actions or stores. I say if it doesn't depend on state put it in actions.

class NowPlayingActions {
    loadPlaylist(items) {
        this.dispatch(items)
    }

    loadAlbum(id) {
        // dereferencing operator <3
        utils.get('/album',{id}).then(this.loadPlaylist)
    }

    next() { this.dispatch() }
    prev() { this.dispatch() }
}

module.exports = alt.createActions(NowPlayingActions)
