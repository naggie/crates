#!/usr/bin/env node

// handles JSX, ES6, commonjs, bundling, uglifyjs2, SCSS

// TODO Use gulp for this, mainly for watching and possibly speed


// JS

var browserify = require('browserify')
var fs = require('fs')
var path = require('path')

var base_dir = path.join(__dirname,'/../../')

production = process.env.NODE_ENV == 'production'

var b = browserify()
b.add(__dirname+'/index.js')

if (production) {
    b.transform({
        global: true,
    },'uglifyify')
}

b.transform({es6:true},'reactify')

var dest = fs.createWriteStream(base_dir+'/static/crates/bundle.js')

b.bundle().pipe(dest)

// SCSS

//var sass = require('node-sass');
//var result = sass.renderSync({
//    file : base_dir+'/static/crates/main.css',
//    outFile : base_dir+'/static/crates/bundle.css',
//    outputStyle : production ? 'compressed' : 'nested',
//[, options..]
//});
