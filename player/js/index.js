var React = require("react")
var classNames = require('classnames')
var utils = require('./utils')

var AlbumBrowser = require('./components/AlbumBrowser.jsx')

React.render(
    <AlbumBrowser />,
    document.getElementById('main')
)
