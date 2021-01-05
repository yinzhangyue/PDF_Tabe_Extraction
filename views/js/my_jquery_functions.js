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

function upload(pdfID) {
    //生成pdf文件编号
    //传输到服务端
    //await get_data()后端数据的返回
    //最后return ok
}

async function get_date(pdfID) {
    //数据格式: pdfID ——> [[(pagenum, tableID)], [(pagenunm, tableID),(pagenum, tableID)]...] 即每页上表格数为&  [1,2,...]
}

function generate_List() {
    //在html动态地插入<>
}

function download_exl() {

}

function get_pdf(url = test_url, divID = test_divID, pdfID = test_pdfID, page_num = 1) {
    var options = {
        //If browser doesn't support inline PDFs
        // fallbackLink: "<p>This is a <a href='[url]'>fallback link</a></p>";
        height: "800px",
        id: divID,
        page: page_num.toString(),
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
        generate_List();
    }
}

function jump_pdf(url = test_url, divID = test_divID, pdfID = test_pdfID, page_num = 1) {
    var options = {
        //If browser doesn't support inline PDFs
        // fallbackLink: "<p>This is a <a href='[url]'>fallback link</a></p>";
        height: "800px",
        id: divID,
        page: page_num.toString(),
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