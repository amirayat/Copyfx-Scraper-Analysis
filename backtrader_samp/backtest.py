import os
import datetime
import backtrader as bt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
# from data import dataPrepration


starttime    = datetime.datetime.now()
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
# AUDCADDATA_DIR = os.path.join(BASE_DIR, "Gamma_data.csv")
AUDCAD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/AUDCAD.positions.csv"
AUDNZD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/AUDNZD.positions.csv"
EURCAD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/EURCAD.positions.csv"
EURGBP_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/EURGBP.positions.csv"
EURUSD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/EURUSD.positions.csv"
GBPUSD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/GBPUSD.positions.csv"
USDCAD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/USDCAD.positions.csv"
GBPCAD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/GBPCAD.positions.csv"
NZDCAD_DATA_DIR = "/home/amir/Desktop/good algo/MultiWay/pos-data/NZDCAD.positions.csv"
plot_DIR        = os.path.join(BASE_DIR, "Gamma_plot.html")

bokehPlot   = False
matPlotLib  = True
printlog    = True
cash        = 100000
commission  = 0.0004
size        = (True ,1)
percent     = (False,100)

class GenericCSV_XARF(bt.feeds.GenericCSVData):
    lines = ('Side','Size','Price',)
    params =(   ('datetime'     , 0),
                ('open'         , 1),
                ('high'         , 2),
                ('low'          , 3),
                ('close'        , 4),
                ('volume'       , -1),
                ('openinterest' , -1),
                ('Side'         , 5),
                ('Size'         , 6),
                ('Price'        , 7))

class Arbitrage(bt.Strategy):
    params = (  ('sl_coef' , 0.2),                                                            
                ('printlog', printlog),)

    def log(self, txt, dt=None, doprint=False):
        dt = dt or self.data.datetime[0]
        if self.params.printlog or doprint:
            if isinstance(dt, float):
                dt = bt.num2date(dt)
            print('%s, %s' % (dt.isoformat(), txt))                                                   

    def __init__(self):
        self.open       = self.datas[0].open
        self.high       = self.datas[0].high
        self.low        = self.datas[0].low
        self.clos       = self.datas[0].close
        self.Side       = self.datas[0].Side
        self.Size       = self.datas[0].Size  
        self.Price      = self.datas[0].Price

    def cancel_open_orders(self):
        [self.cancel(order) for order in self.broker.orders if order.status < 4]

    def notify_order(self, order):
        side  = lambda order:   "BUY " if order.size==1 else "SELL"
        otype = lambda order:   "  MARKET    " if order.exectype==0 else \
                                "  CLOSE     " if order.exectype==1 else \
                                "  LIMIT     " if order.exectype==2 else \
                                "  STOP      " if order.exectype==3 else \
                                "  STOPLIMIT "  
        def statement(order):
            txt=side(order)+ \
                otype(order)+ \
                f' {order.Status[order.status]}'\
                f' Size: {order.executed.size}' \
                f' Price: {order.executed.price:.2f}' \
                f' Commission: {order.executed.comm:.2f}' 
            return txt
        if order.status is order.Completed:
            if order.exectype==0:          
                self.broker.setcommission(0.0002)
            else: 
                self.broker.setcommission(0.0004)
            if order.exectype==2:           ### limit -> tp
                self.cancel_open_orders()
            elif order.exectype==3:         ### stop  -> sl
                self.cancel_open_orders()
        if order.status not in [order.Submitted, order.Accepted]:
            txt = statement(order)
            self.log(txt)

    def notify_trade(self, trade):
        if trade.isclosed:
            txt = 'TRADE PNL        Gross {}, Net {}'.format(
                                    round(trade.pnl,2),
                                    round(trade.pnlcomm,2))
            self.log(txt)

    def next(self):
        
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name

            if d.Side>0:
                self.buy(
                    data=d, 
                    exectype=bt.Order.Market,
                    # exectype=bt.Order.Limit,
                    # price=d.Price,
                    size=d.Size
                    )

            elif d.Side<0:
                self.sell(
                    data=d, 
                    exectype=bt.Order.Market,
                    # exectype=bt.Order.Limit,
                    # price=d.Price,
                    size=d.Size
                    )

        # gain_long  = abs(self.Hp-self.open)
        # gain_short = abs(self.open-self.Lp)
        # delta      = self.Hp-self.Lp
        # sl_buy     = self.open-(self.p.sl_coef*delta)
        # sl_short   = self.open+(self.p.sl_coef*delta)
        # if bt.num2date(self.data.datetime[0]).timetuple().tm_min==0:
        #     self.cancel_open_orders()
        #     if not self.position:
        #         if gain_long>=gain_short:
        #             self.buy_bracket(limitprice = self.Hp, 
        #                             stopprice   = sl_buy, 
        #                             exectype    = bt.Order.Market,
        #                             valid       = datetime.timedelta(minutes=60-len(self)%60))
        #         else:
        #             self.sell_bracket(limitprice= self.Lp, 
        #                             stopprice   = sl_short, 
        #                             exectype    = bt.Order.Market,
        #                             valid       = datetime.timedelta(minutes=60-len(self)%60))
        #     else:
        #         if self.getposition(self.data).size>0:
        #             if gain_long>=gain_short:
        #                 tpBuyMarket = self.sell(price   = self.Hp,
        #                                         exectype= bt.Order.Limit,
        #                                         valid   = datetime.timedelta(minutes=60-len(self)%60))
        #                 slBuyMarket = self.sell(price   = sl_buy,
        #                                         exectype= bt.Order.Stop,
        #                                         valid   = datetime.timedelta(minutes=60-len(self)%60))
        #             else:
        #                 self.close()
        #                 self.sell_bracket(limitprice= self.Lp, 
        #                             stopprice   = sl_short, 
        #                             exectype    = bt.Order.Market,
        #                             valid       = datetime.timedelta(minutes=60-len(self)%60))
        #         elif self.getposition(self.data).size<0:
        #             if gain_long<gain_short:
        #                 tpSellMarket = self.buy(price   = self.Lp,
        #                                         exectype= bt.Order.Limit,
        #                                         valid   = datetime.timedelta(minutes=60-len(self)%60))
        #                 slSellMarket = self.buy(price   = sl_short,
        #                                         exectype= bt.Order.Stop,
        #                                         valid   = datetime.timedelta(minutes=60-len(self)%60))
        #             else:
        #                 self.close()
        #                 self.buy_bracket(limitprice = self.Hp, 
        #                                 stopprice   = sl_buy, 
        #                                 exectype    = bt.Order.Market,
        #                                 valid       = datetime.timedelta(minutes=60-len(self)%60))

    def stop(self):                                                                                
        txt =   f'Initial cash:{self.broker.startingcash} '\
                f'Final cash:{self.broker.getvalue()}'
        print(txt)

cerebro = bt.Cerebro()
cerebro.broker.setcash(cash)                                                                        
cerebro.broker.setcommission(commission)                                                 

audcad_data = GenericCSV_XARF(dataname=AUDCAD_DATA_DIR)

audnzd_data = GenericCSV_XARF(dataname=AUDNZD_DATA_DIR)

eurcad_data = GenericCSV_XARF(dataname=EURCAD_DATA_DIR)

eurgbp_data = GenericCSV_XARF(dataname=EURGBP_DATA_DIR)

eurusd_data = GenericCSV_XARF(dataname=EURUSD_DATA_DIR)

gbpusd_data = GenericCSV_XARF(dataname=GBPUSD_DATA_DIR)

usdcad_data = GenericCSV_XARF(dataname=USDCAD_DATA_DIR)

gbpcad_data = GenericCSV_XARF(dataname=GBPCAD_DATA_DIR)

nzdcad_data = GenericCSV_XARF(dataname=NZDCAD_DATA_DIR)

cerebro.adddata(audcad_data, name="audcad")
cerebro.adddata(audnzd_data, name="audnzd")
cerebro.adddata(eurcad_data, name="eurcad")
cerebro.adddata(eurgbp_data, name="eurgbp")
cerebro.adddata(eurusd_data, name="eurusd")
cerebro.adddata(gbpusd_data, name="gbpusd")
cerebro.adddata(usdcad_data, name="usdcad")
cerebro.adddata(gbpcad_data, name="gbpcad")
cerebro.adddata(nzdcad_data, name="nzdcad")

cerebro.addstrategy(Arbitrage)
if size[0]:
    cerebro.addsizer(bt.sizers.FixedSize,   stake    = size[1])  
elif percent[0]: 
    cerebro.addsizer(bt.sizers.PercentSizer,percents = percent[1])  
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
cerebro.addanalyzer(bt.analyzers.SharpeRatio, 
                    timeframe       = bt.TimeFrame.Days, 
                    compression     = 1, 
                    riskfreerate    = 0.05,
                    convertrate     = True, 
                    annualize       = True, 
                    factor          = 365)
cerebro.addanalyzer(bt.analyzers.DrawDown)                                  
cerebro.run()

endtime = datetime.datetime.now()
print('Process time duration:',endtime-starttime)

if matPlotLib:
    cerebro.plot(style              = 'candlestick',
                barup               = 'green',
                volume              = False)
if bokehPlot:
    b = Bokeh(  style               = 'bar', 
                plot_mode           = 'single', 
                scheme              = Tradimo(), 
                legend_text_color   = '#000000', 
                filename            = plot_DIR,
                volume              = False)
    cerebro.plot(b)
