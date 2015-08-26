var React = require("react")

var Album = require('./Album.jsx')
var AZ = require('./AZ.jsx')
var SearchBox = require('./SearchBox.jsx')
var Loading = require('./Loading.jsx')

var utils = require('../utils.js')

var AlbumBrowser = React.createClass({
    getInitialState: function() {
        return {
            albums:[],
            loading:true,
            exhausted:false,
            current_query:{},
            current_page:0,
        }
    },

    componentDidMount: function() {
        this.loadFromAPI({order_by:'name'})
        window.addEventListener('scroll', this.handleScroll)
    },

    componentWillUnmount: function() {
        // ahhh... It makes sense!
        window.removeEventListener('scroll', this.handleScroll)
    },

    updateChar: function(char) {
        this.setState({
            char:char,
            albums:[],
        })
        this.loadFromAPI({
            name__istartswith : char,
            order_by : 'name',
            //artist_istartswith=A,
            //order_by=artist
        })
    },

    // load the next page if appropriate
    handleScroll: function() {
        if (this.state.loading || this.state.exhausted) {
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

        // build new query (I don't like to mutate
        // -- especially component state without setState)
        var query = utils.clone(this.state.current_query)
        query.page = this.state.current_page + 1
        this.setState({current_page:query.page})
        this.loadFromAPI(query)
    },

    loadFromAPI: function(query) {
        // what's that fat arrow?
        // for lexical this
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
        this.setState({
            loading:true,
            current_query: query,
        })
        utils.get('/albums',query).then((albums) => {
            this.setState({
                albums: this.state.albums.concat(albums),
                loading: false,
                exhausted: !albums.length,
            })
        })
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

        this.state.albums.map((props) => {
            var category = this.categorise(props)

            if (category != current_category)
                items.push(
                    <div className="category pure-u-1" key={category}>
                        <h1>{category}</h1>
                    </div>
                )

            items.push( <Album {...props} key={props.id} /> )
            current_category = category
        })

        return (
            <div className="albums">
                <AZ onCharChange={this.updateChar} selected={this.state.char} parent={this} />
                { !this.state.albums.length && !this.state.loading ? 'No results.' : ''}
                <div className="pure-g">{items}</div>
                { this.state.loading? <Loading /> :''}
            </div>
        )
    },
})

module.exports = AlbumBrowser
