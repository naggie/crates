#!/usr/bin/env node

// handles JSX, ES6, commonjs, bundling, uglifyjs2, SCSS

// TODO Use gulp for this, mainly for watching and possibly speed


// JS
//
//
// TODO: need sourcemap for browserify

var browserify = require('browserify')
var fs = require('fs')
var path = require('path')
var sass = require('node-sass')


var base_dir = path.join(__dirname,'/../../')
var production = process.env.NODE_ENV == 'production'

var b = browserify({
    debug:!production,
})

b.add(__dirname+'/index.js')

if (production) {
    b.transform({
        global: true,
    },'uglifyify')
}

b.transform({es6:true},'reactify')

var js_dest = fs.createWriteStream(base_dir+'/static/crates/bundle.js')

b.bundle().pipe(js_dest)

// SCSS
//
// TODO link in external libs with main.scss (renamed from main.css) and link from index.html

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
