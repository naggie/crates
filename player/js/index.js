var React = require("react")
var Dispatcher = require('flux').Dispatcher

// TODO: split these POC components into separate modules


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
                            return document.location.href = '/accounts/login/'
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


class Album extends React.Component {
    render() {
        return (
            <div className="album pure-u-1 pure-u-md-1-3 pure-u-lg-1-6 pure-u-xl-1-7" key={this.props.id}>
                <img className="pure-img-responsive" src={'/cas/'+this.props.cover_art_ref} />
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

    render() {
        return <div className="alphabet">
            {
                this.alphabet.map((char,i) => {
                    return <div
                        className="char"
                        key={i}
                        onClick={this.props.onClick.bind(this,char)} // WOW!
                    >{char}</div>
                })
            }
        </div>
    }

}

class Albums extends React.Component {
    // NOTE passing props directly to API. May cause problems later, maybe not. It's convenient.
    constructor(props) {
        super(props)
        this.state = {
            albums: [],
        }
    }

    componentDidMount() {
        // what's that fat arrow?
        // for lexical this
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
        get('/albums',this.props).then((albums) => {
            this.setState({
                albums: albums,
            })
        })
    }

    render() {
        return (
            <div className="albums">
                <div className="pure-g">
                    {
                        this.state.albums.map((props) => {
                            return <Album {...props} key={props.id} />
                        })
                    }
                </div>
            </div>
        )
    }
}

class Browser extends React.Component {
    constructor(props) {
        this.state = {char:''}
    }

    updateChar(char) {
        console.log(char)
        this.setState({
            char: char,
        })
    }

    render() {
        return <div>
            <AZ onClick={this.updateChar} />
            <Albums name__startswith={this.state.char} />
        </div>

    }
}

React.render(
    //<Albums name__startswith="B" />,
    //<AZ onClick={(char)=>{console.log(char)}}/>,
    <Browser />,
    document.getElementById('main')
)

//window.onload = function() {
//    return
//    get('/albums').then(function(albums) {
//        console.log(albums)
//    })
//}
