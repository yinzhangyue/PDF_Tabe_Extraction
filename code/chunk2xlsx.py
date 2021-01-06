from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import os


def processSpecial(chunks):
    rcs = []
    r = None
    for chunk in chunks:
        if chunk['text'] == '千港元':
            rcs.append((chunk['start_row'], chunk['start_col']))
            r = chunk['start_row']
            chunks.remove(chunk)
    for chunk in chunks:
        if (chunk['start_row'] + 1, chunk['start_col']) in rcs:
            chunk['text'] += ' ' + '千港元'
    if r is not None:
        for chunk in chunks:
            if chunk['start_row'] < r:
                chunk['start_row'] += 1
                chunk['end_row'] += 1
        for chunk in chunks:
            if chunk['start_row'] >= r:
                chunk['start_row'] -= 1
                chunk['end_row'] -= 1
    return chunks


def boxCenter(chkp):
    return [(chkp[0] + chkp[2]) / 2, (chkp[1] + chkp[3]) / 2]


def ifSameRow(si, ti):
    c1 = boxCenter(si)
    c2 = boxCenter(ti)
    ss, se = si[1], si[3]
    ts, te = ti[1], ti[3]
    if te >= c1[1] >= ts:
        return 1
    if se >= c2[1] >= ss:
        return 1
    return 0


def ifSameCol(si, ti):
    c1 = boxCenter(si)
    c2 = boxCenter(ti)
    ss, se = si[0], si[2]
    ts, te = ti[0], ti[2]
    if te >= c1[0] >= ts:
        return 1
    if se >= c2[0] >= ss:
        return 1
    return 0


def cal_chk_limits(chunks):
    x_min = min(chunks, key=lambda p: p["pos"][0])["pos"][0]
    x_max = max(chunks, key=lambda p: p["pos"][1])["pos"][1]
    y_min = min(chunks, key=lambda p: p["pos"][2])["pos"][2]
    y_max = max(chunks, key=lambda p: p["pos"][3])["pos"][3]
    return [x_min, x_max, y_min, y_max, x_max - x_min, y_max - y_min]


def findUpChunk(chunks):
    up, minL = 0, 100000
    for i in range(len(chunks)):
        if chunks[i]['pos'][1] < minL:
            up = i
            minL = chunks[i]['pos'][1]
    return up


def findLeftChunk(chunks):
    left, minL = 0, 100000
    for i in range(len(chunks)):
        if chunks[i]['pos'][0] < minL:
            left = i
            minL = chunks[i]['pos'][0]
    return left


def chunk2Structure(chunks):
    rows = []
    r = 0
    while len(chunks) != 0:
        upId = findUpChunk(chunks)
        row = []
        # print(chunks[upId]['pos'])
        for chunk in chunks:
            if ifSameRow(chunks[upId]['pos'], chunk['pos']):
                chunk['start_row'] = r
                chunk['end_row'] = r
                row.append(chunk.copy())
                # print(row)
        row = sorted(row, key=lambda x: x['pos'][0])
        for i in row:
            chunks.remove(i)
        rows.append(row)
        r += 1
    chunks = []
    n_row = len(rows)
    for i in range(n_row):
        chunks.extend(rows[i])
    cols = []
    c = 0
    while len(chunks) != 0:
        leftid = findLeftChunk(chunks)
        # print('left:',chunks[leftid])
        col = []
        for chunk in chunks:
            if ifSameCol(chunks[leftid]['pos'], chunk['pos']):
                chunk['start_col'] = c
                chunk['end_col'] = c
                col.append(chunk.copy())
        col = sorted(col, key=lambda x: x['pos'][2])
        for i in col:
            chunks.remove(i)
        cols.append(col)
        c += 1
    chunks = []
    n_col = len(cols)
    for i in range(n_col):
        chunks.extend(cols[i])
    # chunks = processSpecial(chunks)
    return chunks


def transformStructureToTable(data, filename, savePath='./output'):
    xlsxBook = Workbook()
    workSheet = xlsxBook.active
    for cell in data:
        sr = cell['start_row'] + 1
        er = cell['end_row'] + 1
        sc = cell['start_col'] + 1
        ec = cell['end_col'] + 1
        sc_t = get_column_letter(sc)
        ec_t = get_column_letter(ec)
        pos1 = sc_t + str(sr)
        pos2 = ec_t + str(er)
        workSheet.merge_cells('{}:{}'.format(pos1, pos2))
        content = cell['text']
        workSheet.cell(sr, sc).value = content

    saveXlsx = os.path.join(savePath, filename + '.xlsx')
    xlsxBook.save(saveXlsx)


def dataInput(tuple):
    return {"pos": [tuple[0], tuple[1], tuple[2], tuple[3]], "text": tuple[4]}
