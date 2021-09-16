import nextcord
from nextcord.ext import commands
import asyncio
import random
import datetime

from goldy_func import *
from goldy_utility import *
from config import msg as goldy_msg

#Importing extenstion pack.
import cogs.halloween_cog.msg as msg

#Importing other extentions.
from cogs.giphy import giphy
from cogs.giphy_cog.api import gif

from cogs.halloween_cog.candy import candy

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "halloween"

class halloween(commands.Cog):
    def __init__(self, client):
        self.client = client

        #Unload cogs that halloween cog will override.
        settings.ignore_cogs.append(["shop", "economy"])

        #Loading halloween's extentions.
        goldy.cogs.load(self.client, "cogs.halloween_cog.candy")
        goldy.cogs.load(self.client, "cogs.halloween_cog.shop")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(description="Has a 50% chance of being a jumpscare or giving you some candy.")
    async def boo(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            random_num = random.randint(1, 7)

            if random_num in [1, 2, 3]: #Send random scary image.
                embed = nextcord.Embed(title="🎃Oh no, you've been spooked!", description="Opps better luck next time.", colour=settings.AKI_RED)
                url = await gif.random(ctx, self.client, "scary game jumpscare", (0, 10))
                embed.set_image(url=url)
                embed.set_footer(text=msg.embed.footer_1)
                await ctx.send(embed=embed)
            
            else: #Give some candy to the member.
                amount = random.randint(2, 8)
                await candy.member.add(ctx, self.client, amount)
                
                description_message = ((msg.embed.prize_context).format(ctx.author.mention, msg.candy_emoji, amount))
                title_message = f"🍬 You Won Candy!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.AKI_RED)
                embed.set_footer(text=msg.embed.footer_1)

                embed.set_thumbnail(url=msg.boo.embed.gif_url)

                await ctx.send(embed=embed)

            pass

    @boo.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.boo.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "halloween.boo")

    @commands.command(aliases=["trick-or-treat", "trick"])
    async def treat(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(description="Sends you a random spooky image.")
    async def spooky(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["scary"])
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