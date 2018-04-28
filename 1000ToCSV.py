# 1000バイトファイルをCSVファイルに変換してやるプログラム
# 相当めんどくさいことが想定されるので、適当なところで切り上げよう
import struct
import sys
import os
import configparser
import csv
 
args = sys.argv
argc = len(args)

# print (argc)

# if argc == 2:
#     # 引数あり
#     fName = args[1]
#     if os.path.isfile(fName):
#         print ("OK!")

#     else:
#         print ("不正なファイル名です： " + fName)
#         pass

# else:
#     print ("引数の数が不正です")
#     pass

fName = r".\92800_1804180002.txt"

# ファイルオープン
fobj = open(fName,mode='rb',buffering=-1,encoding=None,errors=None)
py_datas = []
record_format1 = '2s5s9s2s1s2s3s8s8s8s15s2s5s15s4s20s4s20s20s4s30s5s2s1s60s15s5s5s10s20s10s20s15s1s10s10s15s15s40s40s40s40s40s10s15s40s40s3s3s3s9s9s11s11s8s2s216s8s6s2s'
record_format2 = '2s5s9s2s1s2s3s8s8s8s15s10s30s5s30s4s30s4s30s1s10s60s15s1s15s15s40s40s40s5s2s1s10s40s40s40s15s15s40s40s40s15s40s40s40s15s40s40s30s2s2s2s3s2s'
record_format3 = '2s5s9s2s1s2s3s8s8s8s15s2s22s15s2s18s40s10s20s2s2s3s3s2s796s2s'
record_formatBD = '2s5s9s2s1s2s3s8s8s8s15s3s2s18s19s20s50s80s30s40s1s20s1s1s9s9s9s9s15s15s4s4s6s20s6s20s9s1s20s1s2s2s4s5s5s2s1s1s1s10s9s9s7s7s7s10s2s1s2s2s2s5s5s5s9s11s9s9s15s20s20s10s5s1s1s1s2s2s2s1s1s1s2s2s2s40s60s2s2s2s8s6s2s2s2s1s1s1s5s5s5s2s117s2s'
record_size = 1002
assert record_size == struct.calcsize(record_format1)
assert record_size == struct.calcsize(record_format2)
assert record_size == struct.calcsize(record_format3)
assert record_size == struct.calcsize(record_formatBD)
# for line in fobj:

try:
    while True:
        # buf = fobj.read(record_size)
        buf = fobj.read(record_size)
        if not buf:
            break
        
        # 判定用に分解する
        py_data = struct.unpack(record_format1, buf)
        if py_data[0] == b'H1':
            # ヘッダ１レコード
            print ('Ｈ１読込')
            py_data_list = [i.decode('cp932') for i in list(struct.unpack(record_format1, buf))]

        elif py_data[0] == b'H2':
            # ヘッダ２レコード
            py_data_list = [i.decode('cp932') for i in list(struct.unpack(record_format2, buf))]
            
        elif py_data[0] == b'H3':
            # ヘッダ３レコード
            py_data_list = [i.decode('cp932') for i in list(struct.unpack(record_format3, buf))]

        elif py_data[0] == b'BD':
            # ボディレコード
            py_data_list = [i.decode('cp932') for i in list(struct.unpack(record_formatBD, buf))]

        else:
            pass
        py_data_list.pop()          # さいごのようそをさくじょ
        py_datas.append(py_data_list)

finally:
    fobj.close()
    # CSV書き出し
    with open('some.csv', 'w') as f:
        # writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer = csv.writer(f, lineterminator='\n',dialect='excel') # 改行コード（\n）を指定しておく
        # writer.writerow(fbuf)     # list（1次元配列）の場合
        # py_csv = list(py_datas)
        writer.writerows(py_datas) # 2次元配列も書き込める
