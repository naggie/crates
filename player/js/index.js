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
        <Player />
    </div>,
    document.getElementById('main')
)
