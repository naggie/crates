NowPlayingActions = require('../actions/NowPlayingActions')

class NowPlayingStore {
    constructior() {
        this.items = []
        this.cursor = 0

        this.prev_available = false
        this.next_available = false

        this.bindListeners({
            newPlaylist: NowPlayingActions.LOAD_PLAYLIST,
            next: NowPlayingActions.NEXT,
            prev: NowPlayingActions.PREV,
        })
    }

    newPlaylist(items) {
        this.items = items
        this.cursor = 0
    }

    // next/prev always loop. If you don't want that, pay attention to
    // next_available and prev_available
    next() {
        this.cursor++

        if (this.cursor >= this.items.length) {
            this.cursor == 0
        }

        this.next_available = this.cursor != this.items.length-1
        this.prev_available = this.cursor > 0
    },

    prev() {
        this.cursor--

        if (this.cursor < 0) {
            this.cursor == this.items.length-1
        }

        if (this.cursor == this.items.length-1) {
            this.next_available = False
        }

        this.next_available = this.cursor != this.items.length-1
        this.prev_available = this.cursor > 0
    },

}

module.exports = alt.createStore(NowPlayingStore, 'NowPlayingStore');
