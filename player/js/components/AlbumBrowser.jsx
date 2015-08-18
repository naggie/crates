var React = require("react")

var Album = require('./Album.jsx')
var AZ = require('./AZ.jsx')
var SearchBox = require('./SearchBox.jsx')
var Loading = require('./Loading.jsx')

class AlbumBrowser extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            albums:[],
            loading:true,
            exhausted:false,
            current_query:{},
            current_page:0,
        }
        // override 'this' when used as callback fired from child Component
        this.updateChar = this.updateChar.bind(this)
        this.handleScroll = this.handleScroll.bind(this)
    }

    componentDidMount() {
        this.loadFromAPI({order_by:'name'})
        window.addEventListener('scroll', this.handleScroll)
    }

    componentWillUnmount() {
        // ahhh... It makes sense!
        window.removeEventListener('scroll', this.handleScroll)
    }

    updateChar(char) {
        // TODO change query based on property, see comments
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
    }

    // load the next page if appropriate
    handleScroll() {
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
    }

    loadFromAPI(query) {
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
    }

    render() {
        // TODO passing parent 'this' is strange. Flux time?
        return (
            <div className="albums">
                <AZ onCharChange={this.updateChar} selected={this.state.char} parent={this} />
                { !this.state.albums.length && !this.state.loading ? 'No results.' : ''}
                <div className="pure-g">
                    {
                        this.state.albums.map((props) => {
                            return <Album {...props} key={props.id} />
                        })
                    }
                </div>
                { this.state.loading? <Loading /> :''}
            </div>
        )
    }
}

exports = AlbumBrowser
