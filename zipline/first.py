from zipline.api import order, record, symbol

# %pylab inline
# figsize(12,12)
# import matplotlib.pyplot as pyplot
# ax1 = plt.subplot(211)
# perf.portfolio_value.plot(ax=ax1)
# ax1.setylabel('Portfolio Value')
# ax2 = plt.subplot(212, sharex=ax1)
# perf.AAPL.plot(ax=ax2)
# ax2.set_ylabel('AAPL Stock Price')

def initialize(context):
    pass

def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))

