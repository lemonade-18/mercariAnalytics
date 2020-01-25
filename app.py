# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
import scraping
import graph

# Flaskオブジェクトの生成
app = Flask(__name__)

# 「/」へアクセスがあった場合
@app.route('/')
def main():
    return render_template('condition.html', title="mercari analytics")

# 「/help/」へアクセスがあった場合
@app.route('/help/')
def help():
    return render_template('help.html', title="mercari analytics")

# 「/search/」へアクセスがあった場合
@app.route('/search/', methods=["GET", "POST"])
def search():
    # GETの受け取り
    keyword = request.args.get('keyword')
    category_root = request.args.get('category_root')
    category_child = request.args.get('category_child')

    # category_grand_childチェックボックスの受け取り
    category_grand_child = ""
    cnt = 0
    while cnt < 3000:
        if None is not request.args.get("category_grand_child[{0}]".format(cnt)):
            category_grand_child += "&category_grand_child[{0}]=1".format(cnt)
        cnt += 1

    # item_conditionチェックボックスの受け取り
    item_condition = ""
    if None is not request.args.get("condition_all"):
        item_condition += "&condition_all=1"
    cnt = 0
    while cnt <= 6:
        if None is not request.args.get("item_condition_id[{0}]".format(cnt)):
            item_condition += "&item_condition[{0}]=1".format(cnt)
        cnt += 1

    # 受け取り確認
    print("keyword: ", keyword)
    print("category_root: ", category_root)
    print("category_child: ", category_child)
    print("category_grand_child: ", category_grand_child)
    print("item_condition: ", item_condition)

    # 売り切れ商品の取得
    sold_itemlist = scraping.mercariSearch(keyword, category_root,
                                           category_child, category_grand_child, item_condition, 1, 1)
    # 販売中の商品の取得
    unsold_itemlist = scraping.mercariSearch(keyword, category_root,

                                             category_child, category_grand_child, item_condition, 0, 1)
    # 該当商品の存在チェック
    if sold_itemlist is None:
        # 存在しなければ専用のページに遷移
        return render_template("nonitem.html",
                               title=keyword+"の分析結果",
                               keyword=keyword)

    # 取得内容の並び替え
    sold_itemlist = sorted(sold_itemlist, key=lambda x: x[1])
    unsold_itemlist = sorted(unsold_itemlist, key=lambda x: x[1])

    # 取得内容確認
    print("------------------------------------------------------------------")
    print("sold_itemlist件数: ", len(sold_itemlist))
    print(*sold_itemlist, sep='\n')
    print("------------------------------------------------------------------")
    print("unsold_itemlist件数: ", len(unsold_itemlist))
    print(*unsold_itemlist, sep='\n')
    print("------------------------------------------------------------------")

    # graph.pyを呼び出し及び戻り値の受け取り
    graph_data = graph.graphdata(sold_itemlist)
    data_text = graph_data[0]
    labels_text = graph_data[1]
    suggested_max = graph_data[2]
    step_size = graph_data[3]
    data = graph_data[4]
    labels = graph_data[5]
    binwidth = graph_data[6]

    # 購入件数の多い価格帯のインデックス
    popular_price_index = data.index(max(data))
    print("popular_price: ", popular_price_index)

    # 分析結果画面表示
    return render_template('graph.html',
                           title=keyword+"の分析結果",
                           keyword=keyword,
                           sold_itemlist=sold_itemlist,
                           unsold_itemlist=unsold_itemlist,
                           labels=labels,
                           binwidth=binwidth,
                           graph_data=data_text,
                           graph_labels=labels_text,
                           graph_max=suggested_max,
                           graph_stepsize=step_size,
                           popular_price_index=popular_price_index)

# ユーザー定義例外のスーパークラスのハンドラを登録しておく
@app.errorhandler(Exception)
def error_handler(ex):
    return render_template("exception.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888, threaded=True)
