const request = require('request');
var fs = require('fs');
// const http = require("http");
// const { Http2ServerRequest } = require('http2');

request.post("http://113.31.124.254:5000/pdf/upload", {
    formData: {
        // "name": "testPDF-cvpr2015",
        "file": fs.createReadStream("D:/cvpr2015.pdf")
    }
}, function(err, res, body) {
    if (body) {
        console.log(body);
    }

    if (err) {
        console.log("ERROR! " + err);
    }
});