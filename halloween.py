import nextcord
from nextcord.ext import commands
import asyncio

from goldy_func import *
from goldy_utility import *
import config.msg as msg

#Change 'your_cog' to the name you wish to call your cog. ('your_cog' is just a placeholder.)
cog_name = "halloween"

class halloween(commands.Cog):
    def __init__(self, client):
        self.client = client

        client.load_extension(f'cogs.halloween_cog.candy')
        client.load_extension(f'cogs.halloween_cog.shop')
        print("🍬candy loaded! ")

    @commands.command(description="Has a 50% chance of being a jumpscare or giving you some candy.")
    async def boo(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["trick-or-treat", "trick"])
    async def treat(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(description="Sends you a random spooky image.")
    async def spooky (self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["scary"])
    async def story(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    @commands.command(aliases=["skele", "skull"])
    async def skeletons(self, ctx):
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

def setup(client):
    client.add_cog(halloween(client))

#Need Help? Check out this: {youtube playlist}