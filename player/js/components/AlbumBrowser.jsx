var React = require("react")

var Album = require('./Album.jsx')
var AZ = require('./AZ.jsx')
var SearchBox = require('./SearchBox.jsx')
var Loading = require('./Loading.jsx')

var utils = require('../utils.js')

// ES6, TODO change rest
const AlbumBrowser = React.createClass({
    componentDidMount: function() {
        console.log(this.props.letter)
        this.props.onReady(this.props.params.letter)
        window.addEventListener('scroll', this.handleScroll)
    },

    componentWillUnmount: function() {
        window.removeEventListener('scroll', this.handleScroll)
    },

    // load the next page if appropriate
    handleScroll: function() {
        if (this.props.loading || this.props.exhausted) {
            return
        }

        // how much remains to scroll, measured in viewport height percent
        // units (vh, like css)
        var Y = window.pageYOffset
        var H = document.body.offsetHeight
        var I = window.innerHeight
        var remaining = (H-Y-I)/I

        // less than 2 vh remaining? Quite eager, but looks great and doesn't
        // waste as much as always loading on scroll
        if (remaining > 2.0)
            return

        this.props.onNewPageRequest()
    },

    categorise: function(album) {
        var character = album.name.toUpperCase().charAt(0)

        if (!character.match('[A-Z]'))
            return ''

        return character
    },

    render: function() {
        // I wish I could use a generator
        var items = []
        var current_category = ''

        this.props.albums.map((props) => {
            var category = this.categorise(props)

            if (category != current_category)
                items.push(
                    <div className="category pure-u-1" key={category}>
                        <h1>{category}</h1>
                    </div>
                )

            items.push( <Album {...props} onClick={this.props.onSelect.bind(this,props.id)} key={props.id} /> )
            current_category = category
        })

        return (
            <div className="albums">
                <AZ onCharChange={this.props.filter_by_letter} selected={this.props.letter} parent={this} />
                { !this.props.albums.length && !this.props.loading ? 'No results.' : ''}
                <div className="pure-g">{items}</div>
                { this.props.loading? <Loading /> :''}
            </div>
        )
    },
})

export default AlbumBrowser
