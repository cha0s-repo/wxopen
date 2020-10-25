import sqlite3
import logging

log_path = './run.log'
log_level = logging.DEBUG
logging.basicConfig(filename=log_path, level=log_level)

database = './stock/data/stockdata.db'

class StockData:
    tab = ''
    date = ''
    def __init__(self,date, target='002028'):
        self.tab = 'tab'+target
        self.date = date

    def get_data(self):
        collect_data = []
        c_max = 20
        try:
            date = int(self.date)
            conn = sqlite3.connect(database)
            cr = conn.cursor()
            cmd = "SELECT date, close from " + self.tab
            sel = cr.execute(cmd)

            count = 0
            for row in sel:
                if int(row[0]) < date:
                    collect_data.insert(0, float(row[1]))
                    count += 1
                if count >= c_max:
                    break
        except:
            logging.error('get data failed')

        return collect_data

    def calc_ma_sine(self, collect_data, sine):
        ma=[]
        data_len = len(collect_data)
        if data_len < sine:
            return

        for i in range(0, data_len):
            if i+sine > data_len:
                break
            else:
                av = sum(collect_data[i:i+sine]) * 1.0 / sine
                ma.insert(0, av)

        return ma

    def S1(self):
        coll_data = self.get_data()
        ma5 = self.calc_ma_sine(coll_data, 5)
        ma10 = self.calc_ma_sine(coll_data,10)

        alen = min(len(ma5), len(ma10), 5)

        ma5a = sum(ma5[0:alen]) * 1.0 / alen
        ma10a = sum(ma10[0:alen]) * 1.0 / alen

        t1 = ((ma5[alen-1] - ma5a) + (ma10[0] - ma5[0])) * 1.0 / (abs(ma5[0] - ma5a) + 0.1)

        return str(t1)

if __name__ == "__main__":
    sd = StockData('002028', '20200804')
    sd.S1()


