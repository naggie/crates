var React = require("react")
var Dispatcher = require('flux').Dispatcher

var classNames = require('classnames')

var utils = require('./utils')

// TODO: split these POC components into separate modules like the flux todomvc example


function get(url,params) {
    return new Promise(function(resolve,reject){
        if (params) {
            url += '?' + Object.keys(params).map((key) => {
                return key + "="+params[key]
            }) .join("&")
        }

        var xhr =  new XMLHttpRequest()
        xhr.open("GET",url,true)
        xhr.responseType = 'json'

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4)

                switch (xhr.status) {
                    case 200:
                        // hack to detect if session has expired
                        if (xhr.responseURL.match('/accounts/login/')) {
                            return document.location.href = '/accounts/login/?next='+document.location.pathname
                        }

                        return resolve(xhr.response)
                    case 500:
                        alert('Internal server error')
                        // fall...
                    default:
                        console.log(xhr.status,xhr)
                        reject(xhr.status)
                }
        }

        xhr.onerror = function(error) {
            console.log(error)
            reject(error)
        }

        xhr.send()
    })
}


class Loading extends React.Component {
    render() {
        return (
            <div className="loading pure-u-1">
                <i className="fa fa-spin fa-3x fa-circle-o-notch" />
            </div>
        )
    }
}

class SearchBox extends React.Component {
    componentDidMount() {
        this.refs.search.getDOMNode.focus()
    }
    render() {
        return
            <form>
                <input ref="search" type="text" placeholder="Search..."/>
            </form>

    }
}

class Album extends React.Component {
    // square placeholder is used for non-deterministic height -- stops many reflows on load.
    constructor() {
        this.state = {'loaded':false}
        // automate this: http://www.newmediacampaigns.com/blog/refactoring-react-components-to-es6-classes
        this.swapImg = this.swapImg.bind(this) // TODO this elsewhere instead of passing parent this
    }

    swapImg() {
        this.setState({loaded:true})
    }

    render() {
        var imgstyle = {display:this.state.loaded?'block':'none'}
        var plcstyle = {display:this.state.loaded?'none':'block'}

        return (
            <div className="album pure-u-1 pure-u-md-1-3 pure-u-lg-1-6 pure-u-xl-1-7" key={this.props.id}>
                <img
                    className="pure-img-responsive"
                    onLoad={this.swapImg}
                    style={imgstyle}
                    src={'/cas/'+this.props.cover_art_ref}
                />
                <img style={plcstyle} className="pure-img-responsive" src="/static/crates/placeholder.png" />

                <div className="title">{this.props.name}</div>
                <div className="artist">{this.props.artist}</div>
            </div>
        )
    }
}

class AZ extends React.Component {
    // TODO use purecss.io primitives for this
    constructor(props) {
        this.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')
    }

    updateChar(char) {
        this.props.onCharChange(char)
    }

    render() {
        return (
            <div className="pure-menu alphabet">
                 <ul className="pure-menu-list">
                    {
                        this.alphabet.map((char,i) => {
                            var classes = classNames('pure-menu-item',{
                                'pure-menu-selected' : char == this.props.selected,
                            })
                            return <li
                                className={classes}
                                key={i}
                                onClick={this.updateChar.bind(this,char)}>
                                <a href="#" className="pure-menu-link">{char}</a>
                            </li>
                        })
                    }
                </ul>
            </div>
        )
    }

}

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
        get('/albums',query).then((albums) => {
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

React.render(
    //<Albums name__startswith="B" />,
    //<AZ onClick={(char)=>{console.log(char)}}/>,
    <AlbumBrowser />,
    document.getElementById('main')
)

//window.onload = function() {
//    return
//    get('/albums').then(function(albums) {
//        console.log(albums)
//    })
//}
