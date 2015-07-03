#!/usr/bin/env node
// I'm going to trial bundling programatically, as then a global install of
// browserify is not necessary in addition to local dependencies such as react
// itself.
//
// We might want a watch mode. Maybe the answer is watchify or something gulp
// powered such as @jimjibone's https://gitlab.com/snippets/5920 . I suspect
// the latter will be useful if we end up using scss as well.
//
// We should switch on NODE_ENV=production|debug which already tells react to
// remove debug messages or not.
//
// Alternatively, browserify supports full configuration in package.json.
// Perhaps we should use that -- I've added the equivalent.
var browserify = require('browserify')
var fs = require('fs')
var path = require('path')

var base_dir = path.join(__dirname,'/../../')

var b = browserify()
b.add(__dirname+'/index.js')

if (process.env.NODE_ENV == 'production') {
    b.transform({
        global: true,
    },'uglifyify')
}

b.transform({es6:true},'reactify')

var dest = fs.createWriteStream(base_dir+'/static/crates/bundle.js')

b.bundle().pipe(dest)
