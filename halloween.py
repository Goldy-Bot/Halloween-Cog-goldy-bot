from logging import disable
import nextcord
from nextcord.ext import commands
import asyncio
import random
import datetime
import time
import importlib
import numpy as np

from src.goldy_func import *
from src.goldy_utility import *
from utility import msg as goldy_msg
import src.goldy_cache as goldy_cache

from cogs.database import database

#Importing extenstion packs.
import cogs.halloween_cog.msg as msg
from cogs.halloween_cog.candy import candy
import cogs.halloween_cog.bats as bats

#Importing other extentions.
from cogs.giphy import giphy
from cogs.giphy_cog.api import gif

cog_name = "halloween"
version = 1.00

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

        #Adding additional give/take options.
        goldy_cache.give_cmd_additional_options += '''
from cogs.halloween_cog.candy import candy
loop = asyncio.get_event_loop()

if option.lower() == "candy":
    try:
        arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
        new_bal = loop.create_task(candy.member.add(target_member_ctx, self.client, arg1))
        loop.create_task(ctx.send((msg.admin.give.main_layout).format(admin.mention, target_member.mention, f"🍬``{arg1}``")))

    except ValueError as e:
        loop.create_task(help(admin))
        
    done = True
        '''

        goldy_cache.take_cmd_additional_options += '''
from cogs.halloween_cog.candy import candy
loop = asyncio.get_event_loop()

if option.lower() == "candy":
    try:
        arg1 = int(arg1) #This is here to stop IDIOTS from breaking someone's member data.
        new_bal = loop.create_task(candy.member.subtract(target_member_ctx, self.client, arg1))
        loop.create_task(ctx.send((msg.admin.take.main_layout).format(admin.mention, f"🍬``{arg1}``", target_member.mention)))

    except ValueError as e:
        loop.create_task(help(admin))
        
    done = True
        '''

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
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.boo")
    
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=["trick-or-treat", "trick"], description="A command for gaining candy with a 30% chance of getting tricked and losing a lot of candy.")
    async def treat(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!treat"):
                random_num = np.random.randint(low=1, high=3)

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
                    description=msg.treat.embed.steal_context.format(ctx.author.mention, msg.candy_emoji, f"-{amount}"), 
                    colour=settings.RED)

                    embed.set_footer(text=msg.embed.footer_1)
                    embed.set_thumbnail(url=msg.treat.embed.steal_gif)
                    await ctx.send(embed=embed)
                
                else: #Give candy to the member.
                    amount = random.randint(6, 11)
                    await candy.member.add(ctx, self.client, amount)
                    
                    embed = nextcord.Embed(title="🎃You've been 🤩TREATED!", 
                    description=(msg.treat.embed.won_context).format(ctx.author.mention, msg.candy_emoji, amount), 
                    colour=settings.AKI_ORANGE)

                    embed.set_footer(text=msg.embed.footer_1)
                    embed.set_thumbnail(url=msg.treat.embed.candy_kid_gif)
                    await ctx.send(embed=embed)

            else:
                await ctx.send(goldy_msg.error.do_not_have_item.format(ctx.author.mention))

    @treat.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.boo.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.treat")

    @commands.command(aliases=["creepy"], description="Sends you a random spooky image.")
    async def spooky(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!spooky"):
                url = await gif.random(ctx, self.client, "creepy", (5, 30))
                embed = nextcord.Embed(title="🕯️ Creeeepy...", colour=settings.GREY)
                embed.set_image(url=url)
                embed.set_footer(text=goldy_msg.footer.giphy)
                await ctx.send(embed=embed)

            else:
                await ctx.send(goldy_msg.error.do_not_have_item.format(ctx.author.mention))

    @spooky.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.boo.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.spooky")

    '''
    @commands.command(aliases=["scary"], description="Desolves 1 candy and gives you a horro story.")
    async def story(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass
    '''

    @commands.command(aliases=["skele", "skull", "skeletons"], description="💀Sends skeletons.")
    async def skeleton(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            url = await gif.random(ctx, self.client, "anime skeleton", (2, 30))
            embed = nextcord.Embed(title="💀", colour=settings.WHITE)
            embed.set_image(url=url)
            embed.set_footer(text=msg.embed.footer_1)
            await ctx.send(embed=embed)
            await ctx.send("**💀☠️**")

    @skeleton.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.boo.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.skeleton")

    @commands.cooldown(1, 180, commands.BucketType.user)
    @commands.command(aliases=["bats"], description="Sends a bat to a member's dm.")
    async def bat(self, ctx, member:nextcord.Member=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if await database.member.checks.has_item(ctx, "!bat"):
                if member == None:
                    await ctx.send(goldy_msg.help.command_usage.format(ctx.author.mention, "!bat {member}"))
                    ctx.command.reset_cooldown(ctx)
                else:
                    (ctx, member_ctx) = await goldy_methods.ctx_merger.merge(ctx, member)

                    #Check if member mentioned is battable first.
                    member_data = await database.member.pull(member_ctx)
                    if await bats.member.checks.is_battable(ctx, member_data):
                        #Payment
                        candy_taken = await candy.member.subtract(ctx, self.client, 10)
                        if candy_taken == False:
                            await ctx.send(msg.error.no_candy.format(ctx.author.mention))
                            ctx.command.reset_cooldown(ctx)
                            return False
                    
                        #Get random image.
                        random_image = await bats.random_bat_image.get()

                        #Send embeds
                        dm_embed = await bats.embed.create(member_ctx.author)
                        dm_embed.set_image(url=random_image.url)
                        await member_ctx.author.send(embed=dm_embed)

                        #Bat sent message
                        embed = await bats.embed.sent.create(ctx, 10)
                        await ctx.send(embed=embed)

                        return True

                    else:
                        await ctx.send(msg.bat.failed.not_battable.format(ctx.author.mention))
                        ctx.command.reset_cooldown(ctx)
            else:
                await ctx.send(goldy_msg.error.do_not_have_item.format(ctx.author.mention))
                ctx.command.reset_cooldown(ctx)

    @bat.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.bat")

    @commands.command(aliases=["batable"], description="Allows you to toggle bat blocking on or off.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def battable(self, ctx, option=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if not option == None:
                is_done = await bats.member.toggle(ctx, option.lower())

                if is_done[0] == True:
                    if is_done[1] == "on":
                        await ctx.send(msg.battable.toggle_on.format(ctx.author.mention))
                    if is_done[1] == "off":
                        await ctx.send(msg.battable.toggle_off.format(ctx.author.mention))

                if is_done[0] == False:
                    await ctx.send(msg.help.command_usage.format(ctx.author.mention, "!battable {on/off}"))
                    
            else:
                member_data = await database.member.pull(ctx)

                if await bats.member.checks.is_battable(ctx, member_data):
                    await ctx.send(msg.battable.your_battable.format(ctx.author.mention))
                else:
                    await ctx.send(msg.battable.your_not_battable.format(ctx.author.mention))

    @battable.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, f"{cog_name}.battable")

    @commands.command()
    async def cram(self, ctx):
        if await can_the_command_run(ctx, cog_name) == True:
            pass

    class embed():
        @staticmethod
        async def create(description="Happy Halloween!"):
            embed=nextcord.Embed(title="**__🎃Halloween (2021)__**", description=description, color=settings.AKI_ORANGE)
            return embed

class buttons():
    class yes_no(nextcord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx
            self.value = None

        @nextcord.ui.button(label="💚Yes", style=nextcord.ButtonStyle.green)
        async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            if interaction.user == self.ctx.author:
                self.value = True
                self.stop()

        @nextcord.ui.button(label="❤️No", style=nextcord.ButtonStyle.red)
        async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            if interaction.user == self.ctx.author:
                self.value = False
                self.stop()

def setup(client):
    client.add_cog(halloween(client))

#Need Help? Check out this: {youtube playlist}