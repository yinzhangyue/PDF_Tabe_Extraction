import os
import json
import zipfile


def runModel(filename):
    # status = os.system('python ./hello.py {}'.format(filename))
    status = os.system('sh /root/run.sh {}'.format(filename))
    return status


def formatHtml(pdfName, pageNum):
    rootPath = '/root/pdfTableDetection/Files'
    path = os.path.join(rootPath, str(pdfName), "chunks", str(pageNum)+'.json')
    with open(path) as f:
        data = json.load(f)
    structs = [data[key] for key in data]
    rowcnt = max(structs, key=lambda p: p["end_row"])["end_row"] + 1
    colcnt = max(structs, key=lambda p: p["end_col"])["end_col"] + 1
    print("row , col number:", rowcnt, colcnt)
    mat = [["<td></td>"] * colcnt for i in range(rowcnt)]
    for st in structs:
        mat[st["start_row"]][st["start_col"]] = "<td>" + st["text"] + "</td>"
    html = ""
    for row in mat:
        html += "<tr>" + "".join(row) + "</tr>"
    html = "<table border='1'>{}</table>".format(html)
    return html


def compress_file(zipfilename, dirname):      # zipfilename是压缩包名字，dirname是要打包的目录
    if os.path.isfile(dirname):
        with zipfile.ZipFile(zipfilename, 'w') as z:
            z.write(dirname)
    else:
        with zipfile.ZipFile(zipfilename, 'w') as z:
            for root, dirs, files in os.walk(dirname):
                for single_file in files:
                    if single_file != zipfilename:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath)


# if __name__ == '__main__':
#     print(formatHtml("00067", "18"))