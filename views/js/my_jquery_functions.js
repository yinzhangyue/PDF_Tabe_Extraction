//////////////////////////////////////////////////////////前后端数据交互///////////////////////////////////////////////////
// const request = require('request');
// var fs = require('fs');


async function get_data(pdfID) {
    //数据格式: pdfID ——> [[(pagenum, tableID)], [(pagenunm, tableID),(pagenum, tableID)]...] 即每页上表格数为&  [1,2,...]
}

function generate_List(Info) {
    //在html动态地插入<>
    var PAGE = "<template slot='title' id='pageX'><i class='el-icon-s-data'></i>第x页</template>";
    var TABLE = "<el-menu-item index='1-1' id='tableX' class='table'>选项x</el-menu-item>";
    var FRONTTAG = "<el-menu-item-group>";
    var ENDTAG = "</el-menu-item-group>";

    var Segment = "";
    for (var i = 0; i < Info.length(); i++) {

        for (var j = 0; j < Info[i].length; j++) {

        }
    }


}

var buildHTML = function(tag, html, attrs) {

    // you can skip html param

    if (typeof(html) != 'string') {
        attrs = html;
        html = null;
    }
    varh = '<' + tag;
    for (attr in attrs) {
        if (attrs[attr] === false) continue;
        h += ' ' + attr + '="' + attrs[attr] + '"';
    }
    return h += html ? ">" + html + "</" + tag + ">" : "/>";
};

function download_exl() {

}


//////////////////////////////////////////////////////////渲染pdf页面///////////////////////////////////////////////////

function check_support() {
    if (PDFObject.supportsPDFs) {
        console.log("Yay, this browser supports inline PDFs.");
    } else {
        console.log("Boo, inline PDFs are not supported by this browser");
    }
}


let test_url = "http://localhost:8080/views/test.pdf";
let test_divID = "pdf"
let test_pdfID = "user00+filename+create_time";

function get_pdf(url = test_url, divID = test_divID, pdfID = test_pdfID, page_num = '1') {
    var options = {
        //If browser doesn't support inline PDFs
        // fallbackLink: "<p>This is a <a href='[url]'>fallback link</a></p>";
        // id: pdfID,
        height: "800px",
        id: divID,
        page: page_num,
        pdfOpenParams: {
            view: 'FitV',
            // page: page_num,
            // comment: "452fde0e-fd22-457c-84aa2cf5bed5a349"
        }
    };
    window.onload = function() {
        // console.log(url);
        // console.log("#" + divID);
        console.log(options);
        PDFObject.embed(url, "#" + divID, options);
        //TODO: 加载页面时动态地生成sidebar list
        // generate_List();
        // $("#1-1").text("Hellooo");
    }
}

function jump_pdf(url = test_url, divID = test_divID, pdfID = test_pdfID, page_num = '1') {
    var options = {
        //If browser doesn't support inline PDFs
        // fallbackLink: "<p>This is a <a href='[url]'>fallback link</a></p>";
        // id: pdfID,
        height: "800px",
        id: divID,
        page: page_num,
        pdfOpenParams: {
            view: 'FitV',
            // page: page_num,
            // comment: "452fde0e-fd22-457c-84aa2cf5bed5a349"
        }
    };
    // console.log(url);
    // console.log("#" + divID);
    console.log(options);
    PDFObject.embed(url, "#" + divID, options);

}

function version() {
    console.log(PDFObject.pdfobjectversion);
}