var React = require("react")
var Dispatcher = require('flux').Dispatcher

// TODO: split these POC components into separate modules


function get(url) {
    return new Promise(function(resolve,reject){
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

class Albums extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            albums: [],
        }
    }

    componentDidMount() {
        // what's fat arrow?
        // for lexical this
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
        get('/albums').then((albums) => {
            this.setState({
                albums: albums,
            })
        })
    }

    render() {
        var albums = []

        this.state.albums.forEach((props) => {
            albums.push(<Album {...props} />)
        })

        return (
            <div className="albums">
                <div className="pure-g">
                    {albums}
                </div>
            </div>
        )
    }
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

React.render(
    <Albums />,
    document.getElementById('main')
)

window.onload = function() {
    return
    get('/albums').then(function(albums) {
        console.log(albums)
    })
}
