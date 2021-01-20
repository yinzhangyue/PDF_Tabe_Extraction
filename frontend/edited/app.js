////////////////////////////////////////////////global Variable///////////////////////////////////////////
var PORT = 3000;
// var SERVER = "113.31.124.254";
var SERVER = "106.75.237.104";

////////////////////////////////////////////////Dependency////////////////////////////////////////////////
var path = require('path');
const request = require('request');
var http = require('http');
var fs = require('fs');
var url = require('url');
var bodyParser = require('body-parser');
var ejs = require('ejs');
var express = require('express');
var multiparty = require('multiparty');
var formidable = require("formidable");
const { type } = require('jquery');
var app = express();


////////////////////////////////////////////////Settings//////////////////////////////////////////////////
app.set('port', 3000);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.engine('html', ejs.renderFile);
app.set('view engine', 'html');
// app.set("engine", "ejs");


////////////////////////////////////////////////Midware///////////////////////////////////////////////////
app.use(function(req, res, next) {
    res.locals.showTests = app.get('env') != 'production' && req.query.showTests === '1';
    next();
});
app.use(express.static(__dirname + '/views'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));




////////////////////////////////////////////////Request///////////////////////////////////////////////////
/////////////////////////////////////////////////params///////////////////////////////////////////////////




//////////////////////////////////////////////////rout////////////////////////////////////////////////////
//服务器主页输出
app.get('/', function(req, res) {
    console.log(req.body);
    // Request.title = req.query.title;
    // Request.kw = req.query.kw;
    // Request.content = req.query.content;
    // console.log(Request.title);
    // console.log(Request.kw);
    // console.log(Request.content);
    // if (Request.title == undefined) {
    //     res.render('home');
    // } else if (Request.title == undefined) {
    //     res.render('home');
    // } else {
    //     res.redirect('/news?title=' + Request.title + '&kw=' + Request.kw + '&content=' + Request.content);
    // }
    // res.render('browsePDF');
    res.render('index.html', { title: 'HTML' });
    // res.redirect('/news');
    // res.send(req.body);
});


async function upload(pdfPATH, pdfName) {
    return new Promise(function(resolve, reject) {

        var Info = {
            name: '',
            pages: undefined,
            pageNum: undefined,
            dist: undefined,
            pdfURL: undefined,
            status: undefined,
            message: ''
        }

        try {
            var uploadURL = "http://" + SERVER + ":5000/pdf/upload";
            var options = {
                formData: {
                    "file": fs.createReadStream(pdfPATH)
                }
            };
            request.post(uploadURL, options, function(err, res, body) {
                var result = JSON.parse(body);
                if (!err && result.status == 1) {
                    console.log(result);
                    resolve(result);
                } else {
                    console.log(err);
                    return;
                }
            });

        } catch (error) {
            console.log(error.response.body);
        }
        //从后端传回的Info中解析数据
        Info.name = pdfName;
        Info.dist = JSON.parse(result.info);
        Info.pages = Object.keys(Info.dist);
        Info.pageNum = Info.pages.length;
        Info.status = result.status;
        Info.message = result.message;

        var storeDict = path.basename(pdfPATH, '.pdf');
        // console.log(storeDict);
        Info.pdfURL = "http://" + SERVER + ":8080/" + storeDict + "/" + storeDict + "_.pdf";

        console.log(Info);
        return Info;
    });
    //生成pdf文件编号
    //传输到服务端
    //await get_data()后端数据的返回
    //最后return chunk

}

app.post('/upload', function(req, res) {
    console.log("===========================收到一个上传请求===========================");
    let form = new multiparty.Form();
    form.parse(req, function(err, fields, files) {
        console.log(files);
        // console.log("$$$" + typeof files);
        var filePath = files.file[0].path;
        var name = files.file[0].originalFilename;

        // console.log(filePath);
        var Info = upload(filePath, name);
    });
});

app.get('/pdf', function(req, res) {
    res.render('browsePDF.html', { title: 'HTML' });
});


app.get('/try', function(req, res) {
    res.render('try.html', { title: 'HTML' });
    // var readFile = "views/try.html";
    // var fileContents = fs.readFileSync(readFile);

    // res.send(fileContents.toString())
});


//////////////////////////////////////////////////error///////////////////////////////////////////////////
app.use(function(req, res) {
    res.type('text/plain');
    res.status(404);
    res.send('404 - Not Found');
});
app.use(function(err, req, res, next) {
    console.error(err.stack);
    res.type('text/plain');
    res.status(500);
    res.write('500 - Server Error');
    res.end();
});



//////////////////////////////////////////////////Server//////////////////////////////////////////////////
var server = app.listen(app.get('port'), "0.0.0.0", function() { //指跑在哪个端口

    var host = server.address().address
    var port = server.address().port
    console.log(host);
    console.log(port);

    console.log("访问地址为 http://%s:%s", host, port)

})