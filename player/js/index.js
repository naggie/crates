var React = require("react")
var classNames = require('classnames')
var utils = require('./utils')

var AlbumBrowser = require('./components/AlbumBrowser.jsx')
var Player = require('./components/Player.jsx')
var Playlist = require('./components/Playlist.jsx')


React.render(
    <div>
        <Playlist
            cover_art_ref="7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f"
            name="Whatbruv, what?"
            artist="DJ BONE (for a reason)"
        />
        <Player
            cover_art_ref="7dd2fb3e4ccff0058f5459346f6fef49bee6e5fae71e979febc1198a20d8e55f"
            title="Jungle music (original)"
            album="Fast Jungle Music"
            album_artist="Hospital records"
            _ref="6c1efd7cbc14ab9a8444bd62caeb878cd3879c5dac8eec3fa0aab7e358a97d0b"
        />
    </div>,
    document.getElementById('main')
)
