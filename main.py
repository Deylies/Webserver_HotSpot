# encoding:utf-8
# __author__:DeyLies,WangYu
from flask import Flask, render_template, url_for
import xlrd, datetime, pickle as pkl

app = Flask(__name__)


def get_order():
    ff = 'F:/projects/ext_project/test.xlsx'
    workbook = xlrd.open_workbook(ff)
    sheet = workbook.sheet_by_name('汇总')
    for c in range(1, sheet.ncols):
        date = sheet.cell(1, c).value
        date = datetime.datetime(*xlrd.xldate_as_tuple(date, 0))
        date = datetime.datetime.strftime(date, '%m-%d')
        for r in range(2, 32):
            product = sheet.cell(r, c).value
            if isinstance(product, float):
                continue
            print(r - 1, date, product)
            # print(r-1,date,len(product))


def get_weight():
    with open('resource/order.pkl', 'rb') as ff:
        return pkl.load(ff)


@app.route('/')
def index():
    return render_template('line-stack.html')


if __name__ == '__main__':
    print(get_weight())
    get_order()
    app.run()
