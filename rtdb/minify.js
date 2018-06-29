var fs = require('fs');
var minify = require('html-minifier').minify;

// get the html contents
var fileContents = fs.readFileSync('temp.html', 'utf8');

// pass the html to the minifier
var result = minify(fileContents, {
    minifyCSS: true,
    removeComments: true
});

console.log(result);
