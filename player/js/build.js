#!/usr/bin/env node

// handles JSX, commonjs, bundling, uglifyjs2, SCSS
//
// No longer ES6 for use with react, because:
//   * No auto 'this' binding
//   * exporting didn't work
//   * no mixins
//
// See https://facebook.github.io/react/blog/2015/01/27/react-v0.13.0-beta-1.html
// May be viable one day. Without commonjs.

// TODO Use gulp for this, mainly for watching and possibly speed


// JS

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

b.transform({},'reactify')

var js_dest = fs.createWriteStream(base_dir+'/static/crates/bundle.js')

b.bundle().pipe(js_dest)

// SCSS

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
