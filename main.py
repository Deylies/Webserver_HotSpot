# encoding:utf-8
# __author__:DeyLies,WangYu
from flask import Flask, render_template, url_for, request, redirect
import xlrd, datetime, pickle as pkl
import pandas as pd
import os
app = Flask(__name__)


def get_fpath():
    with open('resource/file.pkl', 'rb') as f:
        ff = pkl.load(f)
    return ff


def get_order():
    ff = get_fpath()
    workbook = xlrd.open_workbook(ff)
    total = []
    sheet = workbook.sheet_by_name('汇总')
    for c in range(1, sheet.ncols):
        date = sheet.cell(1, c).value
        date = datetime.datetime(*xlrd.xldate_as_tuple(date, 0))
        date = datetime.datetime.strftime(date, '%m-%d')
        for r in range(2, 32):
            product = sheet.cell(r, c).value
            if product==0:
                continue
            total.append([r - 1, date, product])
    total = pd.DataFrame(total, columns=['rank', 'date', 'product'])
    Xdate = list(total['date'].sort_values().drop_duplicates())
    weight = get_weight()
    all_product_diff = []
    all_product_rank = []
    for pro in total.groupby('product'):
        # 不同产品分析差分
        product = pro[0]
        ranks = []
        for day in Xdate:
            rank = pro[1][pro[1]['date'] == day]['rank'].min()
            if pd.isna(rank):
                rank = 31
            ranks.append(int(rank))
        scores = []
        for i in range(len(ranks) - 1):
            start = ranks[i] - 1
            end = ranks[i + 1] - 1
            score = sum(weight[min([start, end]):max([start, end])])
            score = score if end < start else -score
            scores.append(score)
            # print(r-1,date,len(product))
        all_product_diff.append([product, scores])
        all_product_rank.append([product, ranks])
    num = int(get_num())
    # print(num,type(get_num()))
    top_products_diff = sorted(all_product_diff, key=lambda x: sum(x[-1]), reverse=True)[:num]
    top_products_names = [i[0] for i in top_products_diff]
    top_products_ranks = []
    for i in all_product_rank:
        if i[0] in top_products_names:
            top_products_ranks.append(i)
    top_products = [[i[0], i[1], Xdate[1:]] for i in top_products_diff]

    top_products_ranks = [[i[0], i[1], Xdate] for i in top_products_ranks]
    return top_products_names, Xdate[1:], top_products, top_products_names, Xdate, top_products_ranks


def get_weight():
    with open('resource/order.pkl', 'rb') as ff:
        return pkl.load(ff)

def get_num():
    with open('resource/num.pkl', 'rb') as ff:
        return pkl.load(ff)

@app.route('/update_num', methods=['GET', 'POST'])
def update_num():
    req = request.form.get('num')
    try:
        with open('resource/num.pkl','wb') as ff:
            pkl.dump(int(req),ff)
        return redirect(url_for('index'))
    except Exception as e:
        print('update_num', e)
        return redirect(url_for('index',warn='请输入整数！'))

@app.route('/update_location', methods=['GET', 'POST'])
def update_location():
    req = request.form.get('path')
    with open('resource/file.pkl','wb') as ff:
        pkl.dump(req,ff)
    return redirect(url_for('index'))


@app.route('/update_weight', methods=['GET', 'POST'])
def update_weight():
    req = request.form.getlist('weight[]')
    try:
        weights = [int(w) for w in req]
        with open('resource/order.pkl', 'wb') as ff:
            pkl.dump(weights, ff)
        return redirect(url_for('index'))
    except Exception as e:
        print('update_weight',e)
        return redirect(url_for('index', warn='请输入数字'))


@app.route('/')
def index():
    msg = request.args.get('msg')
    warn = request.args.get('warn')
    f_path = os.path.join(os.getcwd(),'test.xlsx')
    f_path = f_path.replace('\\','/')
    weight = get_weight()
    current = get_fpath()
    headers = [i + 1 for i in range(30)]
    try:
        legend, xAxis, lines, legend2, xAxis2, lines2 = get_order()
        num = get_num()

        return render_template('home.html', headers=headers, weight=weight, ff=current, msg=msg,warn=warn,f_path=f_path,
                               char_name='Top%d商品变化'%num, legend=legend, xAxis=xAxis, lines=lines,chart=True,
                               char_name2='Top%d商品排名'%num, legend2=legend2, xAxis2=xAxis, lines2=lines2)
    except Exception as e:
        print('get_order', e)
        warn = '文件路径有误或者文件格式不正确,参考文件：'+f_path
        return render_template('home.html', headers=headers, weight=weight, ff=current, msg=msg,warn=warn,f_path=f_path)


# legend=['a','b','c'],
# xAxis=['1','2','3'],
# lines=[['a',['1','2','3'],[1,2,3]],['b',['1','2','3'],[1,2,3]],['c',['1','2','3'],[1,2,3]]])


if __name__ == '__main__':
    app.run()
