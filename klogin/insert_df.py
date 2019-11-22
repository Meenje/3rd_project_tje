## 2019.11.21 기준 예측

from klogin.db_work.crawling_stock_info import *
import sqlite3
import pandas as pd
from klogin.predict import *
from datetime import datetime

# #infostock에 초기 값들 넣어주기
# conn = sqlite3.connect("C:\\Users\\Administrator\\PycharmProjects\\project_test_kakao_view1\\db.sqlite3")
# cur = conn.cursor()
# sql = "select stock_code from klogin_scode"
# cur.execute(sql)
# rows = cur.fetchall()
# for code in rows:
#     s_code = code[0]
#     df = crawling_info(s_code,2)
#     for i in range(df.__len__()-1):
#         r = df.iloc[i]
#         sql = "insert into klogin_infostock(stock_code, date, open, high, low, close, volume) values(?,?,?,?,?,?,?)"
#         cur.execute(sql, (r.code, r.date, int(r.open), int(r.high), int(r.low), int(r.close), int(r.volume)))
#     print(code[0], "완료")
# conn.commit()
# conn.close()

# 종목코드, 이름 넣기
#conn = sqlite3.connect("C:\\Users\\Administrator\\PycharmProjects\\project_test_kakao_view1\\db.sqlite3")
#cur = conn.cursor()
#codes, names = crawling_KOSPI200()
#for i in range(200):
    #sql = "insert into klogin_scode(stock_code, stock_name) values(?,?)"
    #cur.execute(sql, (codes[i], names[i]))
#conn.commit()
#conn.close()

# 예측값 넣어주기
now = datetime.now()
conn = sqlite3.connect("C:\\Users\\Administrator\\PycharmProjects\\project_test_kakao_view1\\db.sqlite3")
cur = conn.cursor()
get_sql = "select stock_code from klogin_scode"
cur.execute(get_sql)
codes_list = cur.fetchall()
subset_codes = codes_list[:50]
for code in subset_codes:
    sql = "select * from klogin_infostock where stock_code=?"

    cur.execute(sql, (code[0],))
    list = cur.fetchall()
    df = pd.DataFrame(list, columns = ['index' , 'code', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    del df['index']
    del df['code']
    del df['Date']

    if len(df) > 1000:
        df = df.iloc[-1000:]

    print(code[0], "예측 시작합니다")
    p_price = int(foresee(df)[0])
    today = str(now.year) + str(now.month) + str(now.day)

    insert_sql = "insert into klogin_predicted_by_ts(stock_code, date, stock_price) values(?,?,?)"
    cur.execute(insert_sql, (str(code[0]), today, str(p_price)))
print("종료")
conn.commit()
conn.close()

