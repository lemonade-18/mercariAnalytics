import math


def graphdata(list):

    # スタージェスの公式
    frequency = round(1 + math.log2(len(list)))

    data = [0] * frequency
    hierarchy = [0] * frequency

    price = [y[1] for y in list]
    sold = [x[2] for x in list]

    # 最大値と最小値を求める
    max_price = 0
    min_price = 0
    sold_elements = 0
    for money in price:
        if sold[sold_elements] == 'sold':
            if max_price <= money:
                max_price = money
            if min_price >= money:
                min_price = money
        sold_elements += 1

    # print(max_price)
    # print(sold)

    # 階層の数を求める
    sold_elements = 0
    average = int((max_price - min_price)/frequency/10000)
    sold_count = 0
    average = int((average+1)*10000)
    # print(average)
    print(frequency)
    print(data)
    print(hierarchy)
    for i in range(frequency-1):
        hierarchy[i+1] = hierarchy[i]+average

    for money in price:
        if sold[sold_elements] == 'sold':
            sold_count += 1
            dataElements = int(money / average)
            print(dataElements)
            if dataElements < frequency:
                data[dataElements] += 1
            else:
                data[frequency - 1] += 1
        sold_elements += 1

    # data_textの整形
    data_text = ""
    for val in data:
        data_text += str(val)
        data_text += ","
    data_text = data_text[:-1]
    # print(data_text)

    # labelsTextの整形
    labelsText = ""
    for val in hierarchy:
        labelsText += "'"
        labelsText += "\xA5"
        labelsText += str("{:,d}".format(val))
        labelsText += "~"
        labelsText += "'"
        labelsText += ","
    labelsText = labelsText[:-1]
    # print(labelsText)

    # maxsoldnum
    maxSoldNum = int((max(data)/10 + 1)) * 10

    step_size = 5

    if maxSoldNum >= 100:
        step_size = 10
    elif maxSoldNum < 30:
        step_size = 1

    result = [data_text, labelsText, maxSoldNum, step_size]
    return result
