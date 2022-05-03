import discord 
import random
import ccxt
import time
from datetime import datetime

TOKEN = 'OTY5Mjk5NjUwMTkwMzc2OTYw.YmrYpQ.U5f5YBi7O5Xicjwzs1wZfIfTf-w'

client = discord.Client()

binance_usd = ccxt.binanceusdm()
binance_coin = ccxt.binancecoinm()
bybit_futures = ccxt.bybit()
ftx_futures = ccxt.ftx()

markets = coinbase_pro.load_markets()
markets = coinbase_pro.symbols

markets_binance_usd = ['BTC/USDT', 'ETH/USDT']
markets_binance_coin = ['BTC/USD', 'ETH/USD']
markets_bybit = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'BTC/USD:BTC', 'ETH/USD:ETH']
markets_ftx = ['BTC/USD:USD', 'ETH/USD:USD'] # funding_rate * 8 * 100 for ftx
# markets_bitfinex = ['BTC/USDT:FUSTF0', 'ETH/USDT:FUSTF0'] ccxt.base.errors.NotSupported: fetch_funding_fee() not supported yet

# Keep relative order of items in both keys.
data = {
        'exchanges': [binance_usd, binance_coin, bybit_futures, ftx_futures],
        'markets': [markets_binance_usd, markets_binance_coin, markets_bybit, markets_ftx]
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Starting funding rate data streaming on channel funding-rates.')
    binance_channel = client.get_channel(967148792384208976)
    bybit_channel = client.get_channel(968943984275767376)
    ftx_channel = client.get_channel(968944116346003476)

    while True:
        for pos in range(len(data['exchanges'])):
            for market in data['markets'][pos]:
                funding_rate = data['exchanges'][pos].fetch