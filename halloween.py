import nextcord
from nextcord.ext import commands
import asyncio
import random
import datetime
import importlib

from src.goldy_func import *
from src.goldy_utility import *
from utility import msg as goldy_msg

#Importing extenstion pack.
import cogs.halloween_cog.msg as msg

#Importing other extentions.
from cogs.giphy import giphy
from cogs.giphy_cog.api import gif

from cogs.halloween_cog.candy import candy

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "halloween"

class halloween(commands.Cog, name="🎃Halloween Extn"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 1
        
        #Unload cogs that halloween cog will override.
        import config.config as config
        config.ignore_cogs.append(["shop", "economy"])

        #Loading halloween's extentions.
        goldy.cogs.load(self.client, "cogs.halloween_cog.candy")
        goldy.cogs.load(self.client, "cogs.halloween_cog.shop")

        #Reimporting some of the modules.
        importlib.reload(msg)
        importlib.reload(config)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="Has a 42% chance of being a jumpscare and a 57% chance of giving you some candy.")
    async def boo(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            random_num = random.randint(1, 7)

            if random_num in [1, 2, 3]: #Send random scary image.
                embed = nextcord.Embed(title="🎃Oh no, you've been spooked!", description="*Better luck next time.*", colour=settings.AKI_RED)
                url = await gif.random(ctx, self.client, "fnaf", (0, 50))
                embed.set_image(url=url)
                embed.set_footer(text=msg.embed.footer_1)
                await ctx.send(embed=embed)
            
            else: #Give some candy to the member.
                amount = random.randint(2, 8)
                await candy.member.add(ctx, self.client, amount)
                
                description_message = ((msg.embed.prize_context).format(ctx.author.mention, msg.candy_emoji, amount))
                title_message = f"🍬 You Won Candy!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.AKI_ORANGE)
                embed.set_footer(text=msg.embed.footer_1)

                embed.set_thumbnail(url=msg.boo.embed.gif_url)

                await ctx.send(embed=embed)

    @boo.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.boo.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "halloween.boo")

    @commands.command(aliases=["trick-or-treat", "trick"], description="A command for gaining candy with a 10% chance of getting tricked and losing X amount.")
    async def treat(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            random_num = random.randint(1, 3)

            #Send knock, knock messages.
            await ctx.send("*Knock, Knock*")
            await asyncio.sleep(1)
            await ctx.send("*Door Creaks Open...*")
            await asyncio.sleep(0.5)
            await ctx.send("***TRICK OR TREAT!***")
            await asyncio.sleep(0.5)
            
            if random_num == 1: #Steal member's money.
                amount = random.randint(4, 14)
                await candy.member.subtract(ctx, self.client, amount)

                embed = nextcord.Embed(title="🎃You've been 😈TR$CK%D!", 
                description=msg.treat.embed.steal_context.format(ctx.author.mention, msg.candy_emoji, amount), 
                colour=settings.RED)

                embed.set_footer(text=msg.embed.footer_1)
                embed.set_thumbnail(url=msg.treat.embed.steal_gif)
                await ctx.send(embed=embed)
            
            else: #Give candy to the member.
                amount = random.randint(6, 11)
                await candy.member.add(ctx, self.client, amount)
                
                description_message = ((msg.treat.embed.won_context).format(ctx.author.mention, msg.candy_emoji, amount))
                embed = nextcord.Embed(title="🎃You've been 🤩TREATED!", 
                description=(msg.treat.embed.won_context).format(ctx.author.mention, msg.candy_emoji, amount), 
                colour=settings.AKI_ORANGE)

                embed.set_footer(text=msg.embed.footer_1)
                embed.set_thumbnail(url=msg.treat.embed.candy_kid_gif)
                await ctx.send(embed=embed)

    @commands.command(description="Sends you a random spooky image.")
    async def spooky(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["scary"], description="Desolves 1 candy and gives you a horro story.")
    async def story(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["skele", "skull", "skeletons"])
    async def skeleton(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command()
    async def bats(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command()
    async def cram(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    class embed():
        @staticmethod
        async def create(description="Happy Halloween!"):
            embed=nextcord.Embed(title="**__🎃Halloween (2021)__**", description=description, color=settings.AKI_ORANGE)
            return embed

def setup(client):
    client.add_cog(halloween(client))

#Need Help? Check out this: {youtube playlist}