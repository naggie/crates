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
                    case 403:
                        return document.location.href = '/accounts/login/'
                    case 200:
                        return resolve(xhr.response)
                    case 500:
                        alert('Internal server error')
                        console.log(xhr.status,xhr.response)
                    default:
                        console.log(xhr.status,xhr.response)
                        reject(xhr.status)
                }
        }

        xhr.send()
    })
}

window.onload = function() {
    //get('/albums').then(alert)
    setTimeout(function(){
        //get('/albums')
        get('/albums').then(function(a){console.log('s',a)},function(){})
    },4000)
    //get('/albums').then(function(a){console.log('s',a)},function(){})
}
