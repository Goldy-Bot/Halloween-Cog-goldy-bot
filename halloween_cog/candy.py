import nextcord
from nextcord.ext import commands
import asyncio
import datetime

from goldy_func import *
from goldy_utility import *
import config.msg as goldy_msg

#Importing utilits
from . import msg

cog_name = "candy"

class candy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['balence', 'bank', 'candy'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bal(self, ctx, target_member: nextcord.Member = None):
        if await can_the_command_run(ctx, cog_name) == True:
            if target_member == None:
                member_candy = await candy.member.get(ctx, self.client)
                
                description_message = ((msg.bal.embed.main_context).format(ctx.author.mention, msg.candy_emoji, member_candy))
                title_message = f"🎃 Your Candy!"
                embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.AKI_RED)
                embed.set_footer(text=msg.bal.embed.footer_context)

                user_avatar = ctx.author.avatar.url
                embed.set_thumbnail(url=user_avatar)

                await ctx.send(embed=embed)

            if not target_member == None:
                await ctx.send(goldy_msg.error.not_available_yet)

    @bal.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(goldy_msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "candy.bal")

    class member():
        
        @staticmethod
        async def get(ctx, client): #Returns number of candy the member has.
            database = client.get_cog('database')

            member_data = await database.member.pull(ctx)
            try:
                member_candy = member_data.candy
            except AttributeError as e:
                member_candy = None

            return member_candy

        @staticmethod
        async def add(ctx, client, amount): #Adds currency to member.
            database = client.get_cog('database')
            member_data = await database.member.pull(ctx) #Pull member data.

            member_candy = member_data.candy
            new_candy_bal = member_candy + amount
            member_data.candy = new_candy_bal

            await database.member.push(ctx, member_data) #Push member data back.
            print_and_log(None, f"[{cog_name.upper()}] Added {amount} candy to {ctx.author}'s bank.")

            return new_candy_bal

        @staticmethod
        async def subtract(ctx, client, amount): #Subtracts currency from member.
            database = client.get_cog('database')
            member_data = await database.member.pull(ctx) #Pull member data.

            member_candy = member_data.candy
            new_candy_bal = member_candy - amount

            if new_candy_bal < -1:
                return False

            if not new_candy_bal < -1:
                member_data.goldCoins = new_candy_bal
                await database.member.push(ctx, member_data) #Push member data back.
                print_and_log(None, f"[{cog_name.upper()}] Removed {amount} candy from {ctx.author}'s bank.")

            return new_candy_bal

def setup(client):
    client.add_cog(candy(client))

#Need Help? Check out this: {youtube playlist}