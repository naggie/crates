#!/usr/bin/env node
// TODO Use gulp for this, mainly for watching and possibly speed


// JS
var browserify = require('browserify')
var fs = require('fs')
var path = require('path')
var sass = require('node-sass')
var babelify = require("babelify")


var base_dir = path.join(__dirname,'/../../')
var production = process.env.NODE_ENV == 'production'

var b = browserify({
    debug:!production,
})

b.add(__dirname+'/index.js')
//b.require(__dirname+'/index.js', { entry: true })

b.on("error", function (err) {
    console.log("Error: " + err.message)
})

.transform(babelify)

if (production) {
    b.transform({
        global: true,
    },'uglifyify')
}


var js_dest = b.bundle().pipe(fs.createWriteStream(base_dir+'/static/crates/bundle.js'))



// SCSS
// TODO: move to player/static or something
var css_file = base_dir+'/static/crates/bundle.css'
var result = sass.renderSync({
    file : base_dir+'/static/crates/index.scss', // does not write -- required for sourcemap
    outFile : css_file,
    outputStyle : production ? 'compressed' : 'nested',
    sourceMap : !production,
})

fs.writeFileSync(css_file,result.css)

if (!production)
    fs.writeFileSync(css_file+'.map',result.map)
