import discord 
import random
import ccxt
import time
from datetime import datetime

TOKEN = 'OTY3MTM0NDM5NTcyNDAyMjE2.YmL4Ig.Br3rgaF6WpgsWhtJWa0JChuYW9M'
TOKEN_oi = 'OTY5Mjk5NjUwMTkwMzc2OTYw.YmrYpQ.U5f5YBi7O5Xicjwzs1wZfIfTf-w'
client = discord.Client()

binance_usd = ccxt.binanceusdm()
binance_coin = ccxt.binancecoinm()
bybit_futures = ccxt.bybit()
ftx_futures = ccxt.ftx()

# coinbase_pro = ccxt.coinbasepro()
# bitfinex_futures = ccxt.bitfinex()


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
    # bitfinex_channel = client.get_channel(968944212122943538)

    while True:
        for pos in range(len(data['exchanges'])):
            for market in data['markets'][pos]:
                funding_rate = data['exchanges'][pos].fetch_funding_rate(market)#['info']['nextFundingRate']

                if 'e' in str(funding_rate['fundingRate']):
                    message = f'Funding rate for {market} is: {"%.08f" % funding_rate["fundingRate"]}.'
                else:
                    message = f'Funding rate for {market} is: {funding_rate["fundingRate"]}.'
                
                print(message)
                
                if data['exchanges'][pos] in [binance_usd, binance_coin]:
                    await binance_channel.send(message)
                    now = datetime.fromtimestamp(int(funding_rate['info']['time'])/1000)
                    next_funding_rate = datetime.fromtimestamp(int(funding_rate['info']['nextFundingTime'])/1000)
                elif data['exchanges'][pos] == bybit_futures:
                    await bybit_channel.send(message)
                elif data['exchanges'][pos] == ftx_futures:
                    await ftx_channel.send(message)

                # elif data['exchanges'][pos] == bitfinex_futures:
                #     await bitfinex_channel.send(message)

        
        difference = next_funding_rate - now
        print(f'Sleeping for {difference}')
        time.sleep(difference.total_seconds())
                

# @client.event
# async def on_message(message):
#     # user_message = str(message.content).split()
#     user_message = 'get BTC/USDT funding_rate'.split()
#     message_type = user_message[0] # e.g. GET
#     market = user_message[1]
#     requested_data = user_message[2]
#     channel = str(message.channel.name)

#     if message.author == client.user:
#         return
    
#     # Ask for specific funding rate: get BTC/USDT funding_rate
#     if channel == 'general' and message_type == 'get' and requested_data == 'funding_rate':
#         if market in markets:
#             funding_rate = binance_futures.fetch_funding_rate(market)['info']['lastFundingRate']
#             print(f'Funding rate for {market} is: {funding_rate}.')
#             await message.channel.send(f'Funding rate for {market} is: {funding_rate}.')
#     return

# @client.event
# async def on_error():


if __name__ == "__main__":
    client.run(TOKEN)



# Concurrent Threads Example
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     future_to_market = {await executor.submit(get_funding_rate, market, channel): market for market in markets}
#     for future in concurrent.futures.as_completed(future_to_market):
#         market = future_to_market[future]
#         try:
#             data = future.result()
#             print(data)
#         except Exception as e:
#             print('%r generated an exception: %s' % (market, e))