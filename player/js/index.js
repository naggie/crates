var React = require("react")
var Dispatcher = require('flux').Dispatcher


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
        }

        xhr.send()
    })
}

window.onload = function() {
    //get('/albums').then(alert)
    setInterval(function(){
        //get('/albums')
        get('/albums').then(function(a){console.log('s',a)},function(a,b){console.log(a,b)})
    },1000)
    //get('/albums').then(function(a){console.log('s',a)},function(){})
}
