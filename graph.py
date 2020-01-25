from statistics import stdev


def graphdata(list):
    # 価格リストを作成
    prices = [row[1] for row in list]
    # データの数
    price_num = len(prices)
    # データの標準偏差を算出
    if price_num == 1:
        prices.append(0)
    price_sd = stdev(prices)

    # Scottの公式
    binwidth = 3.49 * price_sd/price_num ** (1/3)
    binwidth = int(round(binwidth, -1))
    print("binwidth", binwidth)

    # priceの最大値, 最小値を取得
    price_min = min(prices)
    price_max = max(prices)
    print("price_min", price_min)
    print("price_max", price_max)

    # labelsの生成
    labels = []
    label = price_min
    while label < price_max:
        labels.append(label)
        label += binwidth
    print("labels: ", labels)

    # dataの生成
    data = []
    cnt = 0
    for label in labels:
        for price in prices:
            if price >= label and price < label+binwidth:
                cnt += 1
        data.append(cnt)
        cnt = 0
    print("data: ", data)

    # labals及びdataの要素数を最大8件になるように切り出す
    # 要素数と最大値の要素番号を取得
    data_len = len(data)
    data_max_index = data.index(max(data))

    # 切り出しはじめと切り出し終わりを算出
    index_a = 0
    index_b = 0
    if data_len > 8:
        if data_len-4 < data_max_index:
            index_b = data_len-1
            index_a = data_len - 8
        elif 3 > data_max_index:
            index_a = 0
            index_b = 7
        else:
            index_a = data_max_index - 4
            index_b = data_max_index + 3
    else:
        index_b = data_len-1
    print("index_a: ", index_a)
    print("index_b: ", index_b)

    # 切り出し
    labels8 = []
    data8 = []
    while index_a <= index_b:
        labels8.append(labels[index_a])
        data8.append(data[index_a])
        index_a += 1
    print("labels8: ", labels8)
    print("data8: ", data8)

    # 整形
    # data_textの整形
    data_text = ""
    for val in data8:
        data_text += str(val)
        data_text += ","
    data_text = data_text[:-1]
    print("data_text: ", data_text)

    # labels_textの整形
    labels_text = ""
    for label in labels8:
        labels_text += "'"
        labels_text += "\xA5"
        labels_text += str("{:,d}".format(label))
        labels_text += "~"
        labels_text += "'"
        labels_text += ","
    labels_text = labels_text[:-1]
    print("labels_text: ", labels_text)

    # 縦軸の最大値を求める
    suggested_max = int((max(data8)/10 + 1)) * 10

    # 刻み幅の設定
    step_size = suggested_max / (suggested_max / 10)

    result = [data_text, labels_text, suggested_max,
              step_size, data8, labels8, binwidth]
    return result
