#from http import client
from email import message
from re import I
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from collections import defaultdict
load_dotenv()
intents = discord.Intents().default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print('beep bop i am {0.user}'.format(client))

dic = {}
with open('wordle_scores.txt', 'r') as f:
    dic = eval(f.read())
dic = defaultdict(lambda: {'1/6':0,'2/6':0,'3/6':0,'4/6':0,'5/6':0,'6/6':0, 'X/6':0},dic)
@client.event
async def on_message(message):
    print(message)
    if message.content.startswith('Wordle'):
        message_arr = message.content.split()
        if(len(message_arr) > 2):
            if(message_arr[1].isdigit()):
                if(len(message_arr[2]) == 3 and (message_arr[2][0].isdigit() or message_arr[2][0] == 'X') and message_arr[2][1] == '/' and message_arr[2][2].isdigit() and message_arr[2][2] == '6'):
                    dic[message.author.name][message_arr[2]] += 1
                    open("wordle_scores.txt", "w").close()
                    with open('wordle_scores.txt', 'w') as f:
                        print(dict(dic),file=f)
                    if (message_arr[2][0] == 'X'):
                        await message.channel.send("lawrd have mercy")
                    elif int(message_arr[2][0]) < 4:
                        await message.channel.send("hey, thats not bad")
                    elif int(message_arr[2][0]) >= 4:
                        await message.channel.send("yikers my dude")
                    
    if message.content.startswith('$bruh'):
        await message.channel.send('BrUh')
    if 'coni' in message.content:
        await message.channel.send('coooniiiii')
    if message.content.startswith('$praise'):
        await message.channel.send("yesus")
    if message.content.startswith('$hi'):
        await message.channel.send('wasap')
    if message.content.startswith("$$Read"):
        count = 0
        
        for channel in message.guild.text_channels:
            async for messages in channel.history(limit = None):
                message_arr = messages.content.split()
                if(len(message_arr) > 2):
                    if(message_arr[0] == 'Wordle'):
                        if(message_arr[1].isdigit()):
                            if(len(message_arr[2]) == 3 and message_arr[2][0].isdigit() and message_arr[2][1] == '/' and message_arr[2][2].isdigit() and message_arr[2][2] == '6'):
                                dic[messages.author.name][message_arr[2]] += 1
        print(dic)
    if message.content.startswith('$wordle_score '):
        mes = message.content.split(' ',1)
        #await message.channel.send(mes[1], " scores:")
        #print(mes[1])
        if mes[1] in dic:
            output_score = "\n".join(f'{key} : {value}' for key,value in dic[mes[1]].items())
            output_text = f'{mes[1]} wordle score: \n' + output_score
            await message.channel.send(output_text)
        else:
            await message.channel.send(f'user "{mes[1]}" could not be found')

       
client.run(os.getenv('TOKEN'))
