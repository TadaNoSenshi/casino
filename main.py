import discord
import os
import asyncio
import time
import json
import datetime as dt
import random
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="~", intents=discord.Intents.all(), case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------------------------')
    print('Bot running.')


async def status_task():
    while True:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"at {len(set(bot.users))} users"))
        await asyncio.sleep(13)
        await bot.change_presence(activity=discord.Game(f'In {len(bot.guilds)} Servers'), status=discord.Status.online)
        await asyncio.sleep(13)


@bot.event
async def on_guild_join(guild):
    members = guild.member_count
    if members <= 1:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="You cant add this Bot now",
                        value="Unfortunately, your server does not have the \nrequired number of members to be able "
                              "\nto add this bot. \nJust try again if you have at least **5 members** \non your "
                              "server: [Invite Link](https://discord.com/oauth2/authorize?client_id=898188257471369217&permissions=8&scope=bot%20applications.commands)")
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/706132176378527755/824707773887021066"
                "/3ad09d4905511990cccc98d904bd1e94_w200.gif")
        embed.set_footer(text="This limit was set to avoid fake invites!")
        await guild.owner.send(embed=embed)
        await guild.leave()
        return
    total_text_channels = len(guild.text_channels)
    total_voice_channels = len(guild.voice_channels)
    total_channels = total_text_channels + total_voice_channels
    guild_owner = bot.get_user(guild.owner.id)
    embed = discord.Embed(title=f"{guild.name} (ID: {guild.id})", color=0x10b6e0)
    embed.add_field(
        name=f"I joined a new Server. Now I am in {len(bot.guilds)} Server. The Owner is``{guild_owner}`` and in his server are {guild.member_count} Member",
        value=f"```All channels: {total_channels}\nText channels: {total_text_channels}\nVoice channels: {total_voice_channels}```")
    channel = bot.get_channel(905815154191650856)
    await channel.send("<@!624317230955626507>")
    await channel.send(embed=embed)
    owner = guild.owner
    embed = discord.Embed(title="Some IMPORTANT stuff",
                          description=f"Thank you for adding me to your Server *{guild.name}*\n{guild.owner}",
                          color=0x10b6e0)
    embed.add_field(name="We recommend a setup:",
                    value="Its a good idea to give this Bot his own channel, because he got a \nlot of "
                          "functures.\n\n**Should I create a channel for this Bot in your Server?**. \nI really "
                          "recommend it for you. You can move the channel where you want. \nReact to the reaction "
                          "below for creating.")
    embed.set_thumbnail(url="https://images8.alphacoders.com/835/thumb-1920-835735.jpg")
    embed.set_footer(text="The reaction will be invalid after 10 days!")
    msg = await owner.send(embed=embed)
    await msg.add_reaction("✅")
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction,
                                                                             user: user == guild.owner and reaction.emoji == "✅",
                                                timeout=864000.0)
        except asyncio.TimeoutError:
            return
        else:
            channel = await guild.create_text_channel(name="🤖--Rich Maker--🤖")
            await channel.edit(
                topic='In here you can use the slash commands for the Bot and manage your settings. Everyone can use this channel!')
            embed = discord.Embed(title=f"Thank You For Adding Me", color=0x7a7aff)
            embed.add_field(name="Lets Get Started",
                            value=f'Use the /help command to get an List of my commands and use **/bug** to report an '
                                  f'bug.')
            embed.set_footer(text='Type /support Into The Chat To Get Support')
            await channel.send(embed=embed)


@slash.slash(name="help", description="Get Command List")
async def hilfe(ctx):
    embed = discord.Embed(title="Hilfe zum Bot", color=0x10b6e0)
    embed.add_field(name="Allgemein:", value="/bank - Look at your money\n/transfer - transfer money to your bank "
                                             "\n/withdraw - withdraw Money to get it bar\n/work - Your "
                                             "daily work\n/luck - If you win, "
                                             "you will get good money\n/give - Give a user money from you\n/clear - "
                                             "Delete a acc of a member\n/leaderboard - See "
                                             "the richest member in this guild\n/shop - Look at the shop\n/buy - Buy some chests"
                                             "\n/bag - See your buyed chests"
                                             "\n/open - Open a chest\n/rob - rob a member\n/roulette - Russian roulett the shoot is your dead\n/bug - report a bug")
    await ctx.send(embed=embed)

    
@slash.slash(name="upvote", description="Upvote the bot on Top.gg")
async def _Upvote(ctx):
    embed=discord.Embed(title="Upvote", description="Click [here](https://top.gg/bot/898188257471369217/vote) to upvote the Bot", color=0x10b6e0)
    await ctx.send(embed=embed)

@slash.slash(name="bank", description="Look at your money")
async def bank(ctx, member: discord.Member = None):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if member == None:
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(ctx.author.id)] = {}
            data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
            data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
            data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
            data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        embed = discord.Embed(title="Bank", description=f"{ctx.author}", color=0x10b6e0)
        embed.add_field(name="Bar:", value=f"{bar} <:moneybag:904819147660218448>", inline=True)
        embed.add_field(name="Bank:", value=f"{bank} <:moneybag:904819147660218448>", inline=True)
        await ctx.send(embed=embed)
    else:
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
        if not str(member.id) in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][str(member.id)] = {}
            data[str(ctx.guild.id)][str(member.id)]['Bar'] = 100
            data[str(ctx.guild.id)][str(member.id)]['Bank'] = 100
            data[str(ctx.guild.id)][str(member.id)]['Kleine Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Normale Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Teure Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Reiche Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Bronze Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Silber Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Gold Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Diamant Kiste'] = 0
            data[str(ctx.guild.id)][str(member.id)]['Platin Kiste'] = 0
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        bar = data[str(ctx.guild.id)][str(member.id)]['Bar']
        bank = data[str(ctx.guild.id)][str(member.id)]['Bank']
        embed = discord.Embed(title="Bank", description=f"{member}", color=0x10b6e0)
        embed.add_field(name="Bar:", value=f"{bar} <:moneybag:904819147660218448>", inline=True)
        embed.add_field(name="Bank:", value=f"{bank} <:moneybag:904819147660218448>", inline=True)
        await ctx.send(embed=embed)


@slash.slash(name="transfer", description="transfer money to your bank")
async def transfer(ctx, money=None):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
    if bar == 0:
        embed = discord.Embed(title="Error", description="You have no money to transfer", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if bar <= 1:
        embed = discord.Embed(title="Error",
                              description="First you must have more money than 1 <:moneybag:904819147660218448>",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    if money==None:
        transfer = bar + bank
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = transfer
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Transfer Successfully",
                          description=f"You transfer {bar} <:moneybag:904819147660218448> on your bank",
                          color=0x10b6e0)
        await ctx.send(embed=embed)
    else:
        transfer = int(money)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] -= transfer
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] += transfer
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Transfer Successfully",
                          description=f"You transfer {transfer} <:moneybag:904819147660218448> on your bank",
                          color=0x10b6e0)
        await ctx.send(embed=embed)


@slash.slash(name="give", description="Give a user money from you")
async def überweisen(ctx, member: discord.Member, arg):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    if not str(member.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(member.id)] = {}
        data[str(ctx.guild.id)][str(member.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(member.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(member.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(member.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
    bankuser = data[str(ctx.guild.id)][str(member.id)]['Bank']
    if bank <= int(arg):
        embed = discord.Embed(title="Error", description="You dont have this much money", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if bank == 0:
        embed = discord.Embed(title="Error", description="You have no money to give", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if bank <= 1:
        embed = discord.Embed(title="Error",
                              description="First you must have more money than 1 <:moneybag:904819147660218448>",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= int(arg)
    data[str(ctx.guild.id)][str(member.id)]['Bank'] += int(arg)
    with open("bank.json", "w") as f:
        json.dump(data, f, indent=4)
    embed = discord.Embed(title="Transfer Successfully",
                          description=f"{ctx.author.mention} gave {member.mention} {arg} <:moneybag:904819147660218448>",
                          color=0x10b6e0)
    await ctx.send(embed=embed)


@slash.slash(name="work", description="Your daily Work")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def arbeit(ctx):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    plus = random.randint(20, 63)
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += plus
    with open("bank.json", "w") as f:
        json.dump(data, f, indent=4)
    bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    embed = discord.Embed(title="Arbeit", description=f"{ctx.author}", color=0x10b6e0)
    embed.add_field(name="Today wages:", value=f"{plus} <:moneybag:904819147660218448>", inline=True)
    embed.add_field(name="Current Bar:", value=f"{bar} <:moneybag:904819147660218448>", inline=True)
    embed.add_field(name="Note", value=f"Come again next day", inline=False)
    await ctx.send(embed=embed)


@arbeit.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown",
                              description='Oh, you wont be able to work again for {:.2f} hour(s)'.format(
                                  error.retry_after / 60 / 60), color=0xff0000)
        await ctx.send(embed=embed)
    else:
        raise error


@slash.slash(name="luck", description="If you have luck you will earn money, otherwise you can loose a lot")
@commands.cooldown(1, 30, commands.BucketType.user)
async def glueck(ctx):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    plus = random.randint(-33, 45)
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += plus
    bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    with open("bank.json", "w") as f:
        json.dump(data, f, indent=4)
    if plus >= 1:
        embed = discord.Embed(title="Luck", description=f"{ctx.author}", color=0x10b6e0)
        embed.add_field(name="You Win:", value=f"{plus} <:moneybag:904819147660218448>", inline=True)
        embed.add_field(name="Current Bar:", value=f"{bar} <:moneybag:904819147660218448>", inline=True)
        await ctx.send(embed=embed)
    if plus <= 0:
        embed = discord.Embed(title="Failed", description=f"{ctx.author}", color=0x10b6e0)
        embed.add_field(name="You loose:", value=f"{plus} <:moneybag:904819147660218448>", inline=True)
        embed.add_field(name="Current Bar:", value=f"{bar} <:moneybag:904819147660218448>", inline=True)
        await ctx.send(embed=embed)


@glueck.error
async def glueck_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown",
                              description='Oh, you wont be able to play again for {:.2f} hour'.format(
                                  error.retry_after), color=0xff0000)
        await ctx.send(embed=embed)
    else:
        raise error


@slash.slash(name="delete", description="Delete a account from a member on this guild")
@commands.has_permissions(administrator=True)
async def delete(ctx, member: discord.Member):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    data[str(ctx.guild.id)][str(member.id)] = {}
    data[str(ctx.guild.id)][str(member.id)]['Bar'] = 100
    data[str(ctx.guild.id)][str(member.id)]['Bank'] = 100
    data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
    data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
    with open("bank.json", "w") as f:
        json.dump(data, f, indent=4)
    embed = discord.Embed(title="Reset Succesfully", description=f"User: {member}", color=0x10b6e0)
    await ctx.send(embed=embed)


@delete.error
async def clear_error(ctx):
    embed = discord.Embed(title="Error", description="This User has no account :shrug:", color=0xff0000)
    await ctx.send(embed=embed)


@slash.slash(name="leaderboard", description="See richest people of this guild")
async def leaderboard(ctx, x=10):
    with open('bank.json', 'r') as f:

        data = json.load(f)

    leaderboard = {}
    total = []

    for user in list(data[str(ctx.guild.id)]):
        name = int(user)
        total_amt = data[str(ctx.guild.id)][str(user)]['Bank']
        leaderboard[total_amt] = name
        total.append(total_amt)

    total = sorted(total, reverse=True)

    em = discord.Embed(
        title=f'Top {x} highest leveled members in Server:\n{ctx.guild.name}',
        description='Congratulations to:', color=0xff00c8
    )
    embed = discord.Embed(title=f'Top {x} richest User in:\n{ctx.guild.name}', color=0x10b6e0)

    index = 1
    for amt in total:
        id_ = leaderboard[amt]
        member = bot.get_user(id_)

        embed.add_field(name=f'{index}: {member}', value=f'╠ {amt} <:moneybag:904819147660218448>', inline=False)
        if index == x:
            break
        else:
            index += 1
    await ctx.send(embed=embed)


@slash.slash(name="withdraw", description="whitedraw money to get it bar")
async def abheben(ctx, money):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
    if bank == 0:
        embed = discord.Embed(title="Error", description="You have no money to whitedraw", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if bank <= 1:
        embed = discord.Embed(title="Error",
                              description="First you must have more money than 1 <:moneybag:904819147660218448>",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    transfer = int(money)
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += transfer
    data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= transfer
    with open("bank.json", "w") as f:
        json.dump(data, f, indent=4)
    embed = discord.Embed(title="Transfer Successfully",
                          description=f"You have whitedraw {transfer} <:moneybag:904819147660218448>", color=0x10b6e0)
    await ctx.send(embed=embed)


@slash.slash(name="shop", description="Look at the shop")
async def shop(ctx):
    embed = discord.Embed(title="Willkommen im Shop", color=0x10b6e0)
    embed.add_field(name="9. Platin Chest", value="75.000 <:moneybag:904819147660218448>")
    embed.add_field(name="8. Diamant Chest", value="50.000 <:moneybag:904819147660218448>")
    embed.add_field(name="7. Gold Chest", value="33.400 <:moneybag:904819147660218448>")
    embed.add_field(name="6. Silber Chest", value="12.520 <:moneybag:904819147660218448>")
    embed.add_field(name="5. Bronze Chest", value="2.990 <:moneybag:904819147660218448>")
    embed.add_field(name="4. Rich Chest", value="2.500 <:moneybag:904819147660218448>")
    embed.add_field(name="3. Expensiv Chest", value="1.300 <:moneybag:904819147660218448>")
    embed.add_field(name="2. Normal Chest", value="900 <:moneybag:904819147660218448>")
    embed.add_field(name="1. Little Chest", value="500 <:moneybag:904819147660218448>")
    embed.set_footer(text="Use /buy (Number) to buy a chest")
    await ctx.send(embed=embed)


@slash.slash(name="buy", description="Buy chests")
async def one(ctx, nummer):
    if int(nummer) == 1:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= 499:
            embed = discord.Embed(title="Error",
                                  description=f"You need {500 - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        kosten = 500
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one little chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** little chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 2:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 899
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {500 - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one normal chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** normal chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 3:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 1299
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one expensiv chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** expensiv chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 4:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 2499
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one rich chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** rich chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 5:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 2989
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one bronze chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** bronze chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 6:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 12519
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one silver chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** silver chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 7:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 33399
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one gold chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** gold chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 8:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 49999
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one diamant chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** diamant chest(s)")
        await ctx.send(embed=embed)
    if int(nummer) == 9:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
        kosten = 54999
        if bank == 0:
            embed = discord.Embed(title="Error", description="You have no money to buy this", color=0xff0000)
            await ctx.send(embed=embed)
            return
        if bank <= kosten:
            embed = discord.Embed(title="Error",
                                  description=f"You need {kosten - bank} <:moneybag:904819147660218448> more money to buy this",
                                  color=0xff0000)
            await ctx.send(embed=embed)
            return
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] -= kosten
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] += 1
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        kiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste']
        embed = discord.Embed(title="Buy Successfully",
                              description=f"You buyed one platin chest", color=0x10b6e0)
        embed.add_field(name="You now have:", value=f"**{kiste}** platin chest(s)")
        await ctx.send(embed=embed)


@slash.slash(name="bag", description="Look at your chests")
async def tasche(ctx):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        embed = discord.Embed(title="Bag", description="Your Bag is empty", color=0x10b6e0)
        await ctx.send(embed=embed)
        return
    bar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    bank = data[str(ctx.guild.id)][str(ctx.author.id)]['Bank']
    klkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste']
    nokiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste']
    tekiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste']
    rekiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste']
    brkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste']
    sikiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste']
    gokiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste']
    dikiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste']
    plkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste']
    embed = discord.Embed(title="Tasche", color=0x10b6e0)
    if klkiste >= 1:
        embed.add_field(name="1. Little Chest:", value=f"```{klkiste} stk.```")
    if nokiste >= 1:
        embed.add_field(name="2. Normal Chest:", value=f"```{nokiste} stk.```")
    if tekiste >= 1:
        embed.add_field(name="3. Expensiv Chest:", value=f"```{tekiste} stk.```")
    if rekiste >= 1:
        embed.add_field(name="4. Rich Chest:", value=f"```{rekiste} stk.```")
    if brkiste >= 1:
        embed.add_field(name="5. Bronze Chest:", value=f"```{brkiste} stk.```")
    if sikiste >= 1:
        embed.add_field(name="6. Silber Chest:", value=f"```{sikiste} stk.```")
    if gokiste >= 1:
        embed.add_field(name="7. Gold Chest:", value=f"```{gokiste} stk.```")
    if dikiste >= 1:
        embed.add_field(name="8. Diamant Chest:", value=f"```{dikiste} stk.```")
    if plkiste >= 1:
        embed.add_field(name="9. Platin Chest:", value=f"```{plkiste} stk.```")
    embed.set_footer(text="To open a chest, use /open (Number)")
    await ctx.send(embed=embed)


@slash.slash(name="open", description="Open a chest")
async def oeffnen(ctx, nummer):
    if int(nummer) == 1:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no little chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        klkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste']
        if klkiste < 1:
            embed = discord.Embed(title="Open", description="You have no little chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 5)
        if auswahl == 5:
            gewinn = 1000
        else:
            gewinn = random.randint(200, 500)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 2:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no normal chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        nokiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste']
        if nokiste < 1:
            embed = discord.Embed(title="Open", description="You have no normal chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 5)
        if auswahl == 5:
            gewinn = 1500
        else:
            gewinn = random.randint(450, 1000)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 3:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no expensive chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        tekiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste']
        if tekiste < 1:
            embed = discord.Embed(title="Open", description="You have no expensive chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 5)
        if auswahl == 5:
            gewinn = 2350
        else:
            gewinn = random.randint(999, 1300)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 4:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no rich chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        rekiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste']
        if rekiste < 1:
            embed = discord.Embed(title="Open", description="You have no rich chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 5)
        if auswahl == 5:
            gewinn = 2800
        else:
            gewinn = random.randint(1300, 2400)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 5:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no bronze chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        brkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste']
        if brkiste < 1:
            embed = discord.Embed(title="Open", description="You have no bronze chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 8)
        if auswahl == 8:
            gewinn = 5000
        else:
            gewinn = random.randint(2000, 3000)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 6:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no silver chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        sikiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste']
        if sikiste < 1:
            embed = discord.Embed(title="Open", description="You have no silver chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 8)
        if auswahl == 8:
            gewinn = 18000
        else:
            gewinn = random.randint(8000, 13520)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 7:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no gold chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        gokiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste']
        if gokiste < 1:
            embed = discord.Embed(title="Open", description="You have no gold chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 9)
        if auswahl == 9:
            gewinn = 40000
        else:
            gewinn = random.randint(20000, 35400)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 8:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no diamant chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        dikiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste']
        if dikiste < 1:
            embed = discord.Embed(title="Open", description="You have no diamant chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 10)
        if auswahl == 9:
            gewinn = 60000
        else:
            gewinn = random.randint(40000, 51000)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    if int(nummer) == 9:
        with open("bank.json", "r") as f:
            data = json.load(f)
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
            with open("bank.json", "w") as f:
                json.dump(data, f, indent=4)
        if not str(ctx.author.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(title="Open", description="You have no platin chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        plkiste = data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste']
        if plkiste < 1:
            embed = discord.Embed(title="Open", description="You have no platin chest", color=0x10b6e0)
            await ctx.send(embed=embed)
            return
        auswahl = random.randint(1, 15)
        if auswahl == 15:
            gewinn = 100000
        else:
            gewinn = random.randint(50000, 85000)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] -= 1
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += gewinn
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Congratulation",
                              description=f"You got {gewinn} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)


@slash.slash(name="rob", description="Rob a member")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def raub(ctx, member: discord.Member):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    if not str(member.id) in data[str(ctx.guild.id)]:
        embed = discord.Embed(title="Error", description=f"You cant rob {member} he got no account",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    if member == ctx.author:
        embed = discord.Embed(title="Error", description=f"You can not rob yourself",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    nummer = random.randint(1, 3)
    if nummer == 3:
        bar = data[str(ctx.guild.id)][str(member.id)]['Bar']
        rob = random.randint(1, bar)
        data[str(ctx.guild.id)][str(member.id)]['Bar'] -= rob
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += rob
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Rob", description=f"You rob {rob} <:moneybag:904819147660218448> from {member}",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    else:
        bankbar = data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
        robber = random.randint(1, bankbar)
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] -= robber
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="Rob",
                              description=f"You got catched. You lost {robber} <:moneybag"
                                          f":904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)


@raub.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown",
                              description='Oh, you wont be able to rob again for {:.2f} minute(s)'.format(
                                  error.retry_after / 60), color=0xff0000)
        await ctx.send(embed=embed)
    else:
        raise error


@slash.slash(name="bug-report", description="Report an bug from the bot")
async def bug(ctx, desc=None, rep=None):
    user = ctx.author
    embed = discord.Embed(title="Welcome To Bug Report!",
                          description="Here you can enter your report and my\nMaster will read this and fix it.",
                          color=0xff00c8)
    embed.add_field(name="What should you do:",
                    value="Still write the bug you found in this Text. \nPlease be detailled, You will not get\nanswered on your bug report but it will be \nread by someone and it will be fix by \nsomeone. If your report is not an bug, then \nan moderator will send you an request and \nyou will be addet to TadaNoSenshi support server\r\nHope you enjoy me :) ",
                    inline=False)
    embed.set_footer(text="Type Exit to exit the Command")
    await ctx.send(embed=embed)
    responseDesc = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300)
    description = responseDesc.content
    if responseDesc.content == "exit":
        embed = discord.Embed(title="Exit", description="You Exit the Command", color=0x7a7aff)
        embed.set_thumbnail(
            url="https://images.unsplash.com/photo-1559284379-46ac083d4028?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTV8fGV4aXR8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80")
        embed.set_footer(text="This is an bug? Report bugs with `bug`")
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(title='Bug Report', color=0xff00c8)
        embed.add_field(name='Description', value=description, inline=False)
        embed.add_field(name='Reported By', value=user, inline=True)
        embed.add_field(name="Server:", value=f"{ctx.guild.name}")
        adminBug = bot.get_channel(905815276015190036)
        await adminBug.send("<@!624317230955626507>")
        await adminBug.send(embed=embed)
        embed = discord.Embed(title="Bug Report",
                              description=f"Bug report successfully requested.", color=0x7a7aff)
        await ctx.send(embed=embed)


@slash.slash(name="roulette", description="Russian Roulett, the shoot is your Dead")
async def roulett(ctx, bet):
    with open("bank.json", "r") as f:
        data = json.load(f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
    if not str(ctx.author.id) in data[str(ctx.guild.id)]:
        data[str(ctx.guild.id)][str(ctx.author.id)] = {}
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bank'] = 100
        data[str(ctx.guild.id)][str(ctx.author.id)]['Kleine Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Normale Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Teure Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Reiche Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bronze Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Silber Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Gold Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Diamant Kiste'] = 0
        data[str(ctx.guild.id)][str(ctx.author.id)]['Platin Kiste'] = 0
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
    bar=data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']
    if bar<int(bet):
        embed = discord.Embed(title="Error", description="You dont have so much money in bar",
                              color=0xff0000)
        await ctx.send(embed=embed)
        return
    if int(bet)<=1:
        embed = discord.Embed(title="Error", description="You must Bet more than 0 <:moneybag:904819147660218448>", color=0xff0000)
        await ctx.send(embed=embed)
        return
    rand=random.randint(1,6)
    if rand==1:
        hi=int(bet)
        luck=random.randint(-hi,0)
        luck=luck*6
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar'] += luck
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title="SHOOT, Slot 1",
                              description=f"You loose {luck} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    else:
        luck=random.randint(0,int(bet))
        data[str(ctx.guild.id)][str(ctx.author.id)]['Bar']+=luck
        with open("bank.json", "w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(title=f"EMPTY, Slot {rand}",
                              description=f"You win {luck} <:moneybag:904819147660218448>",
                              color=0x10b6e0)
        await ctx.send(embed=embed)
    
    
bot.run("TOKEN")
