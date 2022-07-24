import discord 
from discord.ext import commands
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import yfinance as yf

spx = yf.Ticker('^SPX')

botStatus = True
def getData():
       return yf.download(tickers='^SPX', period='3d', interval='1m')
      
     #   data.head()
      # data[['Close','EMA-8', 'EMA-13', 'EMA-21', 'EMA-55']].plot(figsize=(12,10))
      #   ## plt.show()
##
async def main():
    sentSignal = False
    signal = 0
    last_ema_8 = None
    last_ema_13 = None
    last_ema_21= 0
    last_ema_55 = 0
 
    #1 is = call
    #2 is = puts
    while botStatus:
        data = getData()
        data['EMA-8'] = ta.EMA(data['Close'], timeperiod=8)
        data['EMA-13'] = ta.EMA(data['Close'], timeperiod=13)
        data['EMA-21'] = ta.EMA(data['Close'], timeperiod=21)
        data['EMA-55'] = ta.EMA(data['Close'], timeperiod=55)

        ema_21 = data['EMA-21'][-1]
        ema_55 = data['EMA-55'][-1]

    

        if(ema_21 > ema_55):
            if(ema_21 > last_ema_21):
                if(signal != 1 or 2):
                    signal = 1
                    await calculateCalls()
        if(ema_55 > ema_21):
            if(ema_55 > last_ema_55):
                if(signal != 1 or 2):
                    signal = 2
                    await calculatePuts()

        last_ema_8 = data['EMA-8'][-1]
        last_ema_13 = data['EMA-13'][-1]
        last_ema_21= data['EMA-21'][-1]
        last_ema_55 = data['EMA-55'][-1]




bot = commands.Bot(command_prefix='$', description="This is a Helper Bot")

# Events  
@bot.event
async def on_ready():
    print('Launched')

@bot.listen()
async def on_message(message):
    if "tate" in message.content.lower():
        await message.channel.send('my topg')
        await bot.process_commands(message)


# Commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def start(ctx):
    await main()
    await ctx.send('Bot Started')



@bot.command()
async def stop(ctx):
    botStatus = False
    await ctx.send('Bot Stopped')


@bot.command()
async def testBotOne(ctx):
   await calculateCalls()
   await ctx.send('done')
  

async def calculateCalls():
    choiceList = []
    optionsContracts = spx.option_chain('2022-07-25')
    df = pd.DataFrame(optionsContracts.calls)
    bidPrice = df['bid'] > 0.8
    cheapestBid = df[bidPrice]
    bidIndex = cheapestBid.min()
    contractType = 'C'
    contractStrike = bidIndex['strike']
    contractDate = '07/25'
    contractBid = bidIndex['bid']
    await sendMessage(contractType, contractStrike, contractDate, contractBid)
    print('The calculation for Calls went through')

async def calculatePuts():
    choiceList = []
    optionsContracts = spx.option_chain('2022-07-25')
    df = pd.DataFrame(optionsContracts.puts)
    bidPrice = df['bid'] > 0.8
    cheapestBid = df[bidPrice]
    bidIndex = cheapestBid.min()
    contractType = 'P'
    contractStrike = bidIndex['strike']
    contractDate = '07/25'
    contractBid = bidIndex['bid']
    await sendMessage(contractType, contractStrike, contractDate, contractBid)
    print('The calculation for Puts went through')

async def sendMessage(contractType, contractStrike, contractDate, contractBid):
        channel = bot.get_channel(996827256091590736)
        await channel.send("<@&995033007184416778> BTO SPX " + str(contractStrike) + str(contractType) + " 07/25" + " @ " + str(contractBid))

  
bot.run('OTk2ODQwMDc2MDgyNDI1OTY2.GiFr94.mLdGErEoaLMTyu25tiYGTinKbCiQ5ZtCGTQFcU')
