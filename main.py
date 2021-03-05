import discord
from discord.ext import commands, menus

bot = commands.Bot(command_prefix="YOUR_PREFIX")

# Creating custom error! :)
class LolException(Exception):
    pass

# load json file!
def loading():
    global balance
    with open("data.json","r") as fr:
        balance = json.loads(fr.read())
        
# saving in an python var!        
loading()
balance = balance

# saver for json file
def save():
    with open("data.json","w") as fw:
        fw.write(json.dumps(balance))
        
# Account creating function!
def create_account(name:str):
    balance[name] = 0
    save()

# Main Part
class Economy(commands.Cog):
    '''Economy Commands and it is halal! :)'''
    @commands.command(aliases=['bal','balance'])
    async def wallet(self, ctx, *kwargs:discord.Member):
        '''Get Wallet!'''
        if kwargs:
            if kwargs[0].name not in balance.keys():
                create_account(kwargs[0].name)
                save()
            embed = discord.Embed(title = f"{kwargs[0].name}'s Balance:", description=f"Wallet: {balance[kwargs[0].name]}", color=0x00ff00)
            await ctx.send(embed=embed)
            return
            
        if not ctx.author.name in balance.keys():
            create_account(ctx.author.name)
            save()
        await ctx.send(embed =  discord.Embed(title = f"{ctx.author.name}'s Balance:", description=f"Wallet: {balance[ctx.author.name]}", color=0x00ff00))
    @commands.command(aliases=['Work'])
    @commands.cooldown(1,4)
    async def work(self, ctx):
        '''Work and earn!'''
        if not ctx.author.name in balance.keys():
            create_account(ctx.author.name)
            save()
        c =random.randint(1,100000)
        balance[ctx.author.name] += c
        await ctx.send(f"Congrats You got {c}$")
        save()
    @commands.command()
    async def give(self, ctx, member:discord.Member,limit):
        '''Share with your kindness!'''
        if limit == "all":
            limit = balance[ctx.author.name]
        else:
            limit = int(limit)
        if limit > int(balance[ctx.author.name]):
            raise LolException("You can't share more than you have in your wallet")
            return
        balance[member.name] += limit
        balance[ctx.author.name] -= limit
        save()
        await ctx.send(f"You gave {member.mention} {limit}")
        save()




bot.add_cog(Economy())
bot.run("YOUR_BOT_TOKEN")
