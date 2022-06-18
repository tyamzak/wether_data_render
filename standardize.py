import glob
import pandas as pd
import json
import decimal


try:
    with open('conf.json', encoding='utf8') as cf:
        param = json.load(cf)
except:
    with open('conf.json', encoding='ansi') as cf:
        param = json.load(cf)



columns = ['temp','humi','time','weather']

files = glob.glob("CSV/*.csv")

#csv2フォルダに入るファイル
csv2 = []

with open(files[0], 'r', encoding='ansi') as f:
    while True:
        line = f.readline()
        if not line:
            break
        items = line.replace('\n','').split(',')
        csv2.append([
            f'{(decimal.Decimal(items[2]) - decimal.Decimal(param["TempMin"])) / (decimal.Decimal(param["TempMax"]) - decimal.Decimal(param["TempMin"])):.6f}',
            f'{decimal.Decimal(items[3]) * decimal.Decimal(param["Humid2Ratio"]):.6f}',
            items[0],
            f'{decimal.Decimal(param["Weather"][items[1]]) :.6f}'
        ])
        
df = pd.DataFrame(csv2, columns =columns)
df.to_csv(f'{files[0]}'.replace('CSV','CSV2'))