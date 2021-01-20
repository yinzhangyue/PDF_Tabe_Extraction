import os
from flask import jsonify, request
from flask import Blueprint, current_app, send_from_directory
from werkzeug.utils import secure_filename
from controllers.pdf import *


pdf_bp = Blueprint("pdf_bp", __name__, url_prefix="/pdf")


@pdf_bp.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return 'success get'
    elif request.method == 'POST':
        return 'success post'


@pdf_bp.route('/upload', methods=['POST'])
def uploadPdf():
    rootPath = '/root/pdfTableDetection/Files'
    # rootPath = './upload'
    f = request.files['file']
    filename = os.path.splitext(f.filename)[0]
    print(filename)
    if os.path.exists(os.path.join(rootPath, filename)):
        return jsonify({
            "status": -1,
            "message": "已存在同名文件，请重命名后尝试"
        }), 404
    else:
        os.makedirs(os.path.join(rootPath, filename))
        savePath = os.path.join(rootPath, filename, secure_filename(f.filename))
        f.save(savePath)
        # f.save(os.path.join('./upload', secure_filename(f.filename)))
        status = runModel(filename)
        if status != 0:
            return jsonify({
                "status": -1,
                "message": "模型错误"
            }), 403
        infoPath = os.path.join(rootPath, filename, filename+'.json')
        with open(infoPath) as f:
            info = json.load(f)
        return jsonify({
            "status": 1,
            "message": "success",
            "info": info
        }), 200


@pdf_bp.route('/downloadXLSX/<path:filename>/<pageNum>', methods=['GET'])
def downloadXLSX(filename, pageNum):
    # rootPath = './generate'
    rootPath = '/root/pdfTableDetection/Files'
    folderPath = os.path.join(rootPath, filename, "xlsx")
    return send_from_directory(folderPath, '{}.xlsx'.format(pageNum), as_attachment=True)


@pdf_bp.route('/downloadResult/<path:filename>', methods=['GET'])
def downloadResult(filename):
    rootPath = '/root/pdfTableDetection/Files'
    folderPath = os.path.join(rootPath, filename, "xlsx")
    savePath = os.path.join(rootPath, filename, "{}.zip".format(filename))
    compress_file(savePath, folderPath)
    return send_from_directory(os.path.join(rootPath, filename),
                               "{}.zip".format(filename), as_attachment=True)


@pdf_bp.route('/downloadImage/<path:filename>', methods=['GET'])
def downloadImage(filename):
    file = '{}.png'.format(filename)
    dirPath = './download'
    return send_from_directory(dirPath, file, as_attachment=True)


# @pdf_bp.route('/runModel/<path:filename>', methods=['GET'])
# def runModel(filename):
#     file = '{}.png'.format(filename)
#     dirPath = './download'
#     return send_from_directory(dirPath, file, as_attachment=True)


@pdf_bp.route('/getTable/<pdfName>/<pageNum>', methods=['GET'])
def getTableHTML(pdfName, pageNum):
    tableHtml = formatHtml(pdfName, pageNum)
    return jsonify({'table': tableHtml})


