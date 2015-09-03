var React = require("react")
var classNames = require('classnames')
var utils = require('./utils')

var AlbumBrowser = require('./components/AlbumBrowser.jsx')
var Player = require('./components/Player.jsx')
var Playlist = require('./components/Playlist.jsx')


var Test = React.createClass({
    render: function() {
        return <div><Playlist /><Player /></div>
    }
})


React.render(
    <Test />,
    document.getElementById('main')
)
