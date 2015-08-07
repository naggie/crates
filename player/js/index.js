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

                        return resolve(xhr)
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

class Browser extends React.Component {
    render() {
        return (
            <div class="albums">
                <div class="pure-g">
                    {this.albums}
                </div>
            </div>
        )
    }
}

class Album extends React.Component {
    render() {
        return (
            <div class="album pure-u-1 pure-u-md-1-3 pure-u-lg-1-6 pure-u-xl-1-7">
                <img class="pure-img-responsive" src={'/cas/'+this.props.cover_art_ref} />
                <div class="title">{this.props.name}</div>
                <div class="artist">{this.props.artist}</div>
            </div>
        )
    }
}


window.onload = function() {
    //get('/albums').then(alert)
    setInterval(function(){
        //get('/albums')
        get('/albums').then(function(a){console.log('s',a)},function(a,b){console.log(a,b)})
    },1000)
    //get('/albums').then(function(a){console.log('s',a)},function(){})
}
