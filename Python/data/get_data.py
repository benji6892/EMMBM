import os
import sys
sys.path.append("..")
from requests import get
from sqlite3 import connect, OperationalError
from requests import get
from json import *
import time
from datetime import datetime
from math import floor
from xlwt import Workbook

class APINotWorkingError(Exception):
    pass

def timestamp_to_string(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def as_datetime(day):
    return datetime.strptime(day, '%Y-%m-%d')


HALVINGS = [as_datetime('2012-11-28'),
            as_datetime('2016-07-09'),
            as_datetime('2020-05-11')]


def get_blocks(beginning=None, end=None, latest=False):
    
    BASE_URL_BTC_COM = 'https://chain.api.btc.com/v3/block/'
    
    def make_btc_api_call_until_it_works(api_call):
        response = get(api_call)
        failures = 0
        while response.status_code != 200:
            failures += 1
            response = get(api_call)
            if failures == 10:
                raise APINotWorkingError
        return response.json()['data']
    
    if latest:
        return make_btc_api_call_until_it_works(BASE_URL_BTC_COM + 'latest')
    else:
        blocks_to_request = range(beginning, end + 1)
        api_call = BASE_URL_BTC_COM + ','.join([str(i) for i in blocks_to_request])
        blocks = make_btc_api_call_until_it_works(api_call)
        if isinstance(blocks, dict):
            blocks = [blocks]
        return blocks

def make_api_call_exchange_rate(to_timestamp=None, limit=1):

    api_key = '2aa8589235dcf557b78fec8085b4e02b84a3b8f2aba9e07989cb6e8f42262459'
    main_url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD'
    if limit > 1:
        if to_timestamp is not None:
            api_call = f'{main_url}&toTs={to_timestamp}&limit={limit - 1}&api_key={api_key}'
        else:
            api_call = f'{main_url}&limit={limit - 1}&api_key={api_key}'

        response = get(api_call)
        return [(timestamp_to_string(int(day['time'])), int(day['time']), day['close'])\
                for day in response.json()['Data']['Data']]

    else:
        if to_timestamp is not None:
            api_call = f'{main_url}&toTs={to_timestamp}&limit=1&api_key={api_key}'
        else:
            api_call = f'{main_url}&limit={limit}&api_key={api_key}'

        response = get(api_call)
        return [(timestamp_to_string(int(day['time'])), int(day['time']), day['close'])\
                for day in [response.json()['Data']['Data'][1]]]


def get_data_path():
    return 'database.db' if os.getcwd().endswith('data') else 'data/database.db'


class DataUpdater():

    def __init__(self):
        self.connection = connect(get_data_path())
        self.cursor = self.connection.cursor()        

    
    def table_exists(self, table_name):
        self.cursor.execute('''SELECT count(*)
                               FROM sqlite_master
                               WHERE type='table' AND name=? ''', (table_name,))
        return self.cursor.fetchone()[0] == 1


    def get_raw_blockchain_data(self):           

        REQUEST_SIZE_BTC_COM = 1000
        
        def parse_btc_api_response(blocks):
            return [(block['height'], block['timestamp'], block['reward_block'],\
              block['reward_fees'], block['difficulty']) for block in blocks]
        
        try:
            self.cursor.execute('SELECT max(height) FROM blocks')
            max_height = self.cursor.fetchone()[0]

        except OperationalError:
            self.cursor.execute('''CREATE TABLE blocks
                                   (height int, timestamp real, reward real, fees real,
                                    difficulty real)''')
            max_height = -1
        last_block_available = get_blocks(latest=True)['height']
        print(last_block_available)
        while max_height < last_block_available:
            last_block_to_request = min(max_height + REQUEST_SIZE_BTC_COM, last_block_available)
            blocks = get_blocks(max_height + 1, last_block_to_request)
            parsed_response = parse_btc_api_response(blocks)
            self.cursor.executemany('INSERT INTO blocks VALUES (?,?,?,?,?)', parsed_response)
            max_height = parsed_response[-1][0]
            print('last block saved: ',max_height)  



    def get_exchange_rate(self):
        try:
            self.cursor.execute('''SELECT max(timestamp) FROM exchange_rate''')
            max_timestamp_in_database = self.cursor.fetchone()[0]
        except OperationalError:
            self.cursor.execute('''CREATE TABLE exchange_rate
                                   (day str, timestamp real, usd_btc real)''')
            max_timestamp_in_database = 1293753600 # 2010-12-31
        to_timestamp = make_api_call_exchange_rate()[0][1]
        number_day_to_get = int((to_timestamp - max_timestamp_in_database) / (3600 * 24))
        data = []
        while number_day_to_get > 0:
            limit = min(2001, number_day_to_get)
            data += make_api_call_exchange_rate(to_timestamp, limit)
            number_day_to_get -= limit
            to_timestamp -= limit * 3600 * 24
        self.cursor.executemany('INSERT INTO exchange_rate VALUES (?,?,?)', data)


    def cluster_data_by_day(self):
        self.connection.create_function('day', 1, timestamp_to_string, deterministic=True)
        if not self.table_exists('daily_data'):
            self.cursor.execute('''CREATE TABLE daily_data
                                    (day str PRIMARY KEY, number_blocks int, full_reward real,
                                     difficulty real, exchange_rate real)''')
            
        self.cursor.execute('''INSERT INTO daily_data
                               SELECT daily_blockchain_data.day,
                                      daily_blockchain_data.number_blocks,
                                      daily_blockchain_data.full_reward,
                                      daily_blockchain_data.difficulty,
                                      exchange_rate.usd_btc
                               FROM
                               (
                                   SELECT day(timestamp) AS day,
                                          count(*) AS number_blocks,
                                          sum(reward + fees) / 1e8 AS full_reward,
                                          sum(difficulty) AS difficulty
                                   FROM blocks
                                   GROUP BY day(timestamp)
                                ) AS daily_blockchain_data
                                LEFT JOIN exchange_rate AS exchange_rate
                                    ON daily_blockchain_data.day = exchange_rate.day
                                WHERE daily_blockchain_data.day NOT IN (SELECT day FROM daily_data)
                            ''')

        # Last day incomplete because we do not have all blocks yet for that day.
        self.cursor.execute(''' DELETE FROM daily_data
                                WHERE day IN (SELECT day FROM daily_data ORDER BY day DESC LIMIT 1)''')




    def create_R_Q_P(self):
        
        def six_months_ago(date_str):
            if date_str is None:
                return '0000-00-00'
            else:
                months = 12 * int(date_str[:4]) + int(date_str[5:7]) - 7
                return str(months // 12) + '-' + ('0' + str(months % 12 + 1))[-2:] + date_str[7:]
            
        self.connection.create_function('six_months_ago', 1, six_months_ago, deterministic=True)
        
        def local_linear_regression(y,h):
            print('local linear regression...')
            import numpy as np
            k = lambda x: [np.exp(-a**2/2)/np.sqrt(2*np.pi) for a in x]
            res=[]
            x=np.array(range(len(y)))
            y=np.array(y)
            for a in x:
                d=a-x
                z=k(d/h)
                s1=d*z
                s2=sum(d*s1)
                s1=sum(s1)
                res.append(sum((s2-s1*d)*z*y)/(s2*sum(z)-s1*s1))
            return res
        
        if not self.table_exists('article_data'):
            self.cursor.execute(''' CREATE TABLE article_data
                                    (day str PRIMARY KEY, r real, q real, p real)''')
        days = []
        Q_hat = []
        R = []
        P = []
        for row in self.cursor.execute(''' SELECT day,
                                                  difficulty,
                                                  full_reward * exchange_rate,
                                                  number_blocks
                                           FROM daily_data
                                           WHERE exchange_rate IS NOT NULL
                                             AND day > (SELECT six_months_ago(max(day)) FROM article_data)
                                           ORDER BY day '''):
            days.append(row[0])
            q_hat = row[1] * 2**32 / (3600 * 24 * 1e12)
            Q_hat.append(q_hat)
            R.append(144 * row[2] / row[3])
            P.append(row[2] / q_hat)
        Q = local_linear_regression(Q_hat, 15)
        self.cursor.execute(''' DELETE FROM article_data
                                WHERE day > (SELECT six_months_ago(max(day)) FROM article_data)
                            ''')
        
        self.cursor.executemany(''' INSERT INTO article_data (day, r, q, p)
                                    VALUES (?,?,?,?) ''', [(day, r, q, p) for day, r, q, p in zip(days, R, Q, P)])


    def export_excel(self):
        workbook = Workbook()
        worksheet = workbook.add_sheet('data')
        worksheet.write(0, 0, 'day')
        worksheet.write(0, 1, 'average daily network revenue (R)')
        worksheet.write(0, 2, 'daily payoff for 1 Th/s (P)')
        worksheet.write(0, 3, 'hashrate (Th/s) (Q)')
        worksheet.write(0, 4, 'number blocks found during day')
        worksheet.write(0, 5, 'cummulated difficulty')
        worksheet.write(0, 6, 'daily reward in bitcoin')
        worksheet.write(0, 7, 'bitcoin / dollar exchange rate')

        row_index = 1
        for row in self.cursor.execute(''' SELECT article.day,
                                                  article.r,
                                                  article.p,
                                                  article.q,
                                                  daily.number_blocks,
                                                  daily.difficulty,
                                                  daily.full_reward,
                                                  daily.exchange_rate
                                           FROM article_data AS article
                                           LEFT JOIN daily_data as daily
                                               ON article.day = daily.day
                                       '''):
            for colunm in range(8):
                worksheet.write(row_index, colunm, row[colunm])
            row_index += 1
        workbook.save('database.xls')
        

def update_data():
    data_updater = DataUpdater()
    try:
        data_updater.get_raw_blockchain_data()
        data_updater.get_exchange_rate()
        data_updater.cluster_data_by_day()
        data_updater.create_R_Q_P()
        print('database up to date!')
    except APINotWorkingError:
        print('Sorry, btc.com API unavailable. Please try again later.')
    data_updater.connection.commit()
    data_updater.export_excel()
    data_updater.connection.close()
    
    
def load_data(date_from=None, date_to=None):
    """
    BE CAREFUL!! The study period belongs to the interval ]date_from, date_to]. "date_from" excluded!
    The rational for this is that we need the day "date_from" for the inital value for Q
    """
    
    date_from = '2011-01-02' if date_from is None else date_from
    date_to = '9999-99-99' if date_to is None else date_to
    
    connection = connect(get_data_path())
    c = connection.cursor()
    days = []
    R = []
    Q = []
    P = []
    for row in c.execute(''' SELECT day, r, q, p
                             FROM article_data
                             WHERE day > ? AND day <= ?
                             ORDER BY day ''', (date_from, date_to)):
        days.append(row[0])
        R.append(row[1])
        Q.append(row[2])
        P.append(row[3])

    c.execute(''' SELECT q FROM article_data WHERE day = ? ''', (date_from,))
    Q_initial = c.fetchone()[0]
    connection.close()  
    return [as_datetime(day) for day in days], R, Q, P, Q_initial


def load_exchange_rate(date_from=None, date_to=None):

    date_from = '0000-01-01' if date_from is None else date_from
    date_to = '9999-99-99' if date_to is None else date_to

    connection = connect(get_data_path())
    c = connection.cursor()

    days = []
    exchange_rate = []
    for row in c.execute(''' SELECT day, usd_btc
                             FROM exchange_rate
                             WHERE day >= ? AND day <= ?
                             ORDER BY day ''', (date_from, date_to)):
        days.append(as_datetime(row[0]))
        exchange_rate.append(row[1])
    connection.close()
    return days, exchange_rate


def load_number_blocks():
    connection = connect(get_data_path())
    connection.create_function('day', 1, timestamp_to_string, deterministic=True)
    c = connection.cursor()

    days = []
    number_blocks = []
    for row in c.execute(''' SELECT day(timestamp), count(*)
                             FROM blocks
                             GROUP BY day(timestamp)
                             ORDER BY day(timestamp) '''):
        days.append(as_datetime(row[0]))
        number_blocks.append(row[1])
    connection.close()
    return days, number_blocks


def load_q_data(date_from=None, date_to=None):

    date_from = '0000-01-01' if date_from is None else date_from
    date_to = '9999-99-99' if date_to is None else date_to

    connection = connect(get_data_path())
    c = connection.cursor()

    days = []
    Q_hat = []
    probability_find_block = []
    Q = []
    for row in c.execute(''' SELECT daily.day,
                                    daily.difficulty,
                                    daily.number_blocks,
                                    article.Q
                             FROM daily_data AS daily
                             LEFT JOIN article_data as article
                                 ON daily.day = article.day
                             WHERE daily.day >= ? AND daily.day <= ?
                             ORDER BY daily.day ''', (date_from, date_to)):
        days.append(as_datetime(row[0]))
        Q_hat.append(row[1] * 2**32 / (3600 * 24 * 1e12))
        probability_find_block.append(row[2] / (row[1] * 2**32))
        Q.append(row[3])
    connection.close()
    return days, Q_hat, probability_find_block, Q


if __name__=='__main__':
    
    update_data()

    
    


    


