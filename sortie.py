import datetime
from functools import reduce
from discord.ext import commands

TOKEN = ''
PREFIX = '>>'
REQUIRE_ADMIN = True
MESSAGE_LIMIT = 10000
FROM_DATE = datetime.datetime.today() - datetime.timedelta(days=7) #one week ago

count = lambda iterable: reduce((lambda x, y: x + 1), iterable, 0)

bot = commands.Bot(command_prefix=PREFIX)

BUSY = False
@bot.command()
async def sort(ctx):

    if BUSY:
        await ctx.send(f"```Channels are already being processed```")
        return

    BUSY = True
    await ctx.send(f"```Sorting channels```")
    print('\n== RECIEVED SORT COMMAND ==')

    if REQUIRE_ADMIN and not dict(iter(ctx.message.author.guild_permissions))['administrator']:
        print(f"<exiting> {ctx.message.author} is not an administrator")
        BUSY = False
        return

    print('>> reading channels <<')
    channels = []
    for channel in ctx.guild.text_channels:
        if channel.category == None:
            try: 
                history = await channel.history(after=FROM_DATE, limit=MESSAGE_LIMIT)
                message_count = count(history)
                channels.append({'ref': channel, 'count': message_count})
            except:
                print(f'<error> cannot read {channel.name}')

    print('>> sorting channels <<')
    channels.sort(key=lambda channel: channel['count'])
    for index, channel in enumerate(channels):
        try:
            await channel['ref'].edit(position=index)
            print(f'Sent {channel['ref'].name} with {channel['count']} messages to position {index}')
        except:
            print(f'<error> cannot move {channel.name}')

    print('<exiting> success')
    await ctx.send(f"```Sorting channels complete :)```")
    BUSY = False

bot.run(TOKEN)
