import datetime
from functools import reduce
from discord.ext import commands

TOKEN = ''
PREFIX = '>>'
REQUIRE_ADMIN = True
MESSAGE_LIMIT = 10000
FROM_DATE = datetime.datetime.today() - datetime.timedelta(days=7) #one week ago

bot = commands.Bot(command_prefix=PREFIX)
bot.busy = False

@bot.command()
async def sort(ctx):

    if bot.busy:
        await ctx.send(f"```Channels are already being processed```")
        return

    bot.busy = True
    await ctx.send(f"```Sorting channels```")
    print('\n== RECIEVED SORT COMMAND ==')

    if REQUIRE_ADMIN and not dict(iter(ctx.message.author.guild_permissions))['administrator']:
        print(f"<exiting> {ctx.message.author} is not an administrator")
        bot.busy = False
        return

    print('>> reading channels <<')
    channels = []
    for channel in ctx.guild.text_channels:
        if channel.category == None:
            try: 
                count = 0
                async for message in channel.history(after=FROM_DATE, limit=MESSAGE_LIMIT):
                    count += 1
                channels.append({'ref': channel, 'count': count})
            except:
                print(f'<error> cannot read {channel.name}')

    print('>> sorting channels <<')
    channels.sort(key=lambda channel: channel['count'])
    for index, channel in enumerate(channels):
        try:
            await channel['ref'].edit(position=index)
            print(f'Sent {channel["ref"].name} with {channel["count"]} messages to position {index}')
        except:
            print(f'<error> cannot move {channel.name}')

    print('<exiting> success')
    await ctx.send(f"```Sorting channels complete :)```")
    bot.busy = False

bot.run(TOKEN)
