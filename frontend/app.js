////////////////////////////////////////////////global Variable///////////////////////////////////////////
var PORT = 3000;
var SERVER = "localhost";
var HOST_IP = "113.31.124.87"//TODO: 改成当前服务器的ip地址
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
var cors = require('cors');
var app = express();


////////////////////////////////////////////////Settings//////////////////////////////////////////////////
app.set('port', 3000);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.engine('html', ejs.renderFile);
app.set('view engine', 'html');
// app.set("engine", "ejs");


////////////////////////////////////////////////Midware///////////////////////////////////////////////////
app.use(cors());
// app.use(function(req, res, next) {
//     res.setHeader("Access-Control-Allow-Origin", "*");
//     res.setHeader("Access-Control-Allow-Credentials", "true");
//     res.setHeader(
//     "Access-Control-Allow-Methods",
//     "GET,HEAD,OPTIONS,POST,PUT,DELETE"
//     );
//     res.setHeader(
//     "Access-Control-Allow-Headers",
//     "Origin,Cache-Control,Accept,X-Access-Token ,X-Requested-With, Content-Type, Access-Control-Request-Method"
//     );
//     if (req.method === "OPTIONS") {
//     return res.status(200).end();
//     }
//     next();
//     });
app.use(function(req, res, next) {
    res.locals.showTests = app.get('env') != 'production' && req.query.showTests === '1';
    next();
});
app.use(express.static(__dirname + '/views'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


//////////////////////////////////////////////////rout////////////////////////////////////////////////////
//服务器主页输出
app.get('/', function(req, res) {
    res.render('index.html', { title: 'HTML' });
    if (!req) {
        res.render('index.html', { title: 'HTML' });
    } else if (Info == undefined) {
        console.log('####################### go to loading');
        res.render('loading.html', { title: 'HTML' });
    } else {
        res.redirect('/pdf');
    }
    // res.redirect('/news');
    // res.send(req.body);
});


app.post('/upload', async function(req, res) {
    console.log("===========================收到一个上传请求===========================");

    var name = undefined,
        filePath = undefined,
        Info = undefined;

    let form = new multiparty.Form();
    form.parse(req, async function(err, fields, files) {
        console.log(files);
        // console.log("$$$" + typeof files);
        filePath = files.file[0].path;
        name = files.file[0].originalFilename;

        // console.log(filePath);
        Info = await upload(filePath, name);
        res.send(Info);
    });


});

app.get('/loading', function(req, res) {
    res.render('loading.html', { title: 'HTML' });
});

app.get('/pdf*', function(req, res) {
    res.render('browsePDF.html', { title: 'HTML' });
    // console.log(typeof req.Info);
    // var Info = JSON.parse(req.Info);
    // console.log("**************", Info);

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
    // res.render('404.html', { title: 'HTML' });
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



async function upload(pdfPATH, pdfName) {
    return new Promise(function(resolve, reject) {

        var Info = {
            name: '',
            saveName: '',
            pages: undefined,
            pageNum: undefined,
            dist: undefined,
            pdfURL: undefined,
            status: undefined,
            message: ''
        }
        var result;
        try {
            var uploadURL = "http://" + SERVER + ":5000/pdf/upload";
            var options = {
                formData: {
                    "file": fs.createReadStream(pdfPATH)
                }
            };
            request.post(uploadURL, options, function(err, res, body) {
                result = JSON.parse(body);
                if (!err && result.status == 1) {
                    console.log(result);
                    // resolve(result);
                    //从后端传回的Info中解析数据
                    Info.name = pdfName;
                    Info.dist = JSON.parse(result.info);
                    Info.pages = Object.keys(Info.dist);
                    Info.pageNum = Info.pages.length;
                    Info.status = result.status;
                    Info.message = result.message;

                    Info.saveName = path.basename(pdfPATH, '.pdf');
                    Info.pdfURL = 'http://' + HOST_IP + ':8080/' + Info.saveName + '/' + Info.saveName + '_.pdf';

                    console.log(Info);
                    resolve(Info);
                } else {
                    console.log(err);
                    return;
                }
            });

        } catch (error) {
            console.log(error);
        }

    });

}