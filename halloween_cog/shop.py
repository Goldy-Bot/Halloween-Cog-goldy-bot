import nextcord
from nextcord import guild
from nextcord.ext import commands
import asyncio
import datetime
import traceback

from src.goldy_func import *
from src.goldy_utility import *
import utility.msg as msg

from . import msg as hallo_msg

from cogs.database import database
from cogs.shop import shop as core_shop

cog_name = "shop"

max_pages = config.max_pages

class shop(commands.Cog, name="🛒Shop"):
    def __init__(self, client):
        self.client = client
        self.cog_name = cog_name
        self.help_command_index = 3

    #Main shop command.
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, ctx, page=None):
        if await can_the_command_run(ctx, cog_name) == True:

            try:
                page = int(page)
            except TypeError as e:
                pass

            if page == None:
                page = 1
            if page > max_pages:
                await ctx.send(msg.shop.page_out_of_range.format(ctx.author.mention))
                return

            
            items_data = await core_shop.items.find(ctx)
            server_info = servers.get(ctx.guild.id)

            commands_context = ""

            #Grab all commands.
            for command in items_data[0].commands.list:
                #Picking the item data.
                name = (items_data[1]["commands"][command]["names"]["display_name"])
                price = (items_data[1]["commands"][command]["price"])

                #Check if member has item.
                if await database.member.checks.has_item(ctx, command) == True:
                    possession_status = "✅"
                else:
                    possession_status = "❌"

                commands_context += f"**• {name} (CMD): **{hallo_msg.candy_emoji}``{price}`` **{possession_status}**\n"

            roles_context = ""

            #Grab all roles.
            for role in items_data[0].roles.list:
                #Picking the item data.
                rank_mention = (nextcord.utils.get(ctx.guild.roles, id=items_data[1]["roles"][role]["id"])).mention
                price = (items_data[1]["roles"][role]["price"])

                #Check if member has item.
                if await database.member.checks.has_item(ctx, role) == True:
                    possession_status = "✅"
                else:
                    possession_status = "❌"

                roles_context += f"**• {rank_mention} (RANK): **{hallo_msg.candy_emoji}``{price}`` **{possession_status}**\n"

            colours_context = "***• Type !colour to view the  🍭Colour Shop.***"

            if page == 1:
                await self.shop_pages.page_1(self.client, ctx, commands_context, roles_context, colours_context)

            if page == 2:
                await self.shop_pages.page_2(self.client, ctx, commands_context, roles_context, colours_context)
            
            pass

    @shop.error
    async def shop_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "shop.shop")

    class shop_pages():
        
        @staticmethod
        async def page_1(client, ctx, commands_context, roles_context, colours_context):
            page = 1

            embed = await shop.embeded.create(ctx, client, commands_context, roles_context, colours_context, page)

            embed.set_image(url="https://media.discordapp.net/attachments/876976105335177286/887428868208742410/wp7608576_1.png")
            embed.set_footer(text=f"[PAGE {page}/{max_pages}] " + msg.footer.type_2)
            await ctx.send(embed=embed)

            del embed

        @staticmethod
        async def page_2(client, ctx, commands_context, roles_context, colours_context):
            page = 2

            embed = await shop.embeded.create(ctx, client, commands_context, roles_context, colours_context, page)

            embed.set_image(url="https://media.discordapp.net/attachments/876976105335177286/887428868191965204/devushka-prazdnik-anime-art-khellouin.png")
            embed.set_footer(text=f"[PAGE {page}/{max_pages}] " + msg.footer.type_2)
            await ctx.send(embed=embed)

            del embed



    #Buy Command
    @commands.command()
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    async def buy(self, ctx, *, item=None): #Work in progress.
        if await can_the_command_run(ctx, cog_name) == True:
            if not item == None:
                items_data = await core_shop.items.find_one(ctx, item)

                if not items_data == False:
                    #Buy item
                    await shop.items.buy(ctx, self.client, items_data)

                if items_data == False:
                    await ctx.send((msg.buy.failed.no_exist).format(ctx.author.mention))

            if item == None:
                await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!buy {item}"))

    @buy.error
    async def buy_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "shop.buy")



    #Sell Command
    @commands.command()
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    async def sell(self, ctx, *, item=None):
        if await can_the_command_run(ctx, cog_name) == True:
            if not item == None:
                items_data = await self.items.find_one(ctx, item)

                if not items_data == False:
                    #Sell item
                    await shop.items.sell(ctx, self.client, items_data)

                if items_data == False:
                    await ctx.send((msg.sell.failed.no_exist).format(ctx.author.mention))

            if item == None:
                await ctx.send((msg.help.command_usage).format(ctx.author.mention, "!sell {item}"))

    @sell.error
    async def sell_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(msg.error.cooldown.format(datetime.timedelta(seconds=round(error.retry_after))))
        else:
            await goldy.log_error(ctx, self.client, error, "shop.sell")

    class embeded():

        @staticmethod
        async def create(ctx, client, commands_context, roles_context, colours_context, page):
            embed=nextcord.Embed(title="**🎃🛒 __Halloween Shop__**", description="Welcome to Goldy's halloween shop.", color=settings.AKI_ORANGE)

            commands_context = await core_shop.embeded.get_context(ctx, commands_context, page)
            roles_context = await core_shop.embeded.get_context(ctx, roles_context, page)
            colours_context = await core_shop.embeded.get_context(ctx, colours_context, page)

            try:
                server_icon = ctx.guild.icon.url
            except AttributeError as e:
                try:
                    server_icon = client.user.display_avatar.url
                except AttributeError as e:
                    server_icon = "https://htmlcolors.com/color-image/2f3136.png"
                    pass

            server_name = await servers.get_name(ctx)
            embed.set_author(name=f"{server_name} - 🎃{ctx.author.name}", url=settings.github_page, icon_url=server_icon)

            embed.add_field(name="__🏷️Ranks__", value=roles_context, inline=False)
            embed.add_field(name="__❗Commands__", value=commands_context, inline=False)
            embed.add_field(name="__🍭Colours__", value=colours_context, inline=False)

            return embed

    class items():

        @staticmethod
        async def buy(ctx, client, item_data): #This buy function handels purchusing the item and sending Purchased embeded.
            item = await core_shop.items.get_name(ctx, item_data)

            economy = client.get_cog('candy')

            #Check if member has item.
            has_item = await database.member.checks.has_item(ctx, item_data.names.code_name)
            if has_item == True:
                await ctx.send((msg.buy.failed.already_own).format(ctx.author.mention))
                return False

            #If the item is a role add the role, update member's prefix and check if it merges with any other roles.
            if await core_shop.items.checks.item_type(item_data) == "role":
                is_it_merging = await shop.items.role.is_merging(ctx, item_data)
                if is_it_merging[0] == True:
                    role_that_is_causing_it = is_it_merging[1]
                    
                    description_message = ((msg.buy.failed.role_conflict).format(ctx.author.mention, role_that_is_causing_it.mention, item))
                    title_message = "❌ __PURCHASE FAILED!__"
                    embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.RED)
                    embed.set_footer(text=msg.footer.type_2)
                    embed.set_thumbnail(url="https://c.tenor.com/t3Vqq1DiC0YAAAAM/obama-cool-kids-club.gif")
                    await ctx.send(embed=embed)
                    return False

                #Add role to member.
                await core_shop.items.role.give(ctx, item_data)
                #Update member's prefix.

            #Payment process.
            user_bal = await economy.member.subtract(ctx, client, item_data.price)
            if user_bal == False: #Get's exacuted if member doesn't have enough money.
                await ctx.send((msg.buy.failed.no_money).format(ctx.author.mention))
                return False

            user_bal = '{:.2f}'.format(round(user_bal, 2))


            #Give user item.
            member_data = await database.member.pull(ctx) #Pull member data.

            member_items = member_data.items #Create copy of list.
            member_items.append(item_data.names.code_name) #Append item to the list.
            member_data.items = member_items #Update the original list with modified list.

            await database.member.push(ctx, member_data) #Push member data back to whatever hole it came from. 😏
            
            #Embeded message
            description_message = ((msg.buy.embed.item_context).format(ctx.author.mention, item, item_data.embed.msg, hallo_msg.candy_emoji, item_data.price, hallo_msg.candy_emoji, user_bal))
            title_message = "🎃 __Purchase Complete!__"
            embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.GREEN)
            embed.set_footer(text=msg.footer.type_2)
            if not item_data.embed.image in ["", None]: #yes ThIs iS tHe LAzY MEtHod
                embed.set_thumbnail(url=item_data.embed.image)
            await ctx.send(embed=embed)

            #You horny?

            return True #Tells buy command purchase was complete and it can progress.

        @staticmethod
        async def sell(ctx, client, item_data):
            item = await core_shop.items.get_name(ctx, item_data) #Replace this with 'shop.item.get_name' when done with coding it OR ELSE BUYING ROLES WON'T WORK!

            economy = client.get_cog('candy')
            database = client.get_cog('database')

            #Check if member has item.
            has_item = await database.member.checks.has_item(ctx, item_data.names.code_name)
            if has_item == False:
                await ctx.send((msg.sell.failed.do_not_have_item).format(ctx.author.mention))
                return False

            #Check if item is sellable.
            sellable = await core_shop.items.checks.is_sellable(item_data)
            if sellable == False:
                await ctx.send((msg.sell.failed.not_sellable).format(ctx.author.mention))
                return False

            a = settings.sell_tax*0.01
            x = item_data.price*a #Applying Sell Tax
            amount = item_data.price - x

            #Payment process.
            user_bal = await economy.member.add(ctx, client, amount)
            user_bal = '{:.2f}'.format(round(user_bal, 2))
            amount = '{:.2f}'.format(round(amount, 2))

            #Remove item from user.
            member_data = await database.member.pull(ctx) #Pull member data.

            member_items = member_data.items #Create copy of list.
            try:
                member_items.remove(item_data.names.code_name) #Remove item from the list.
            except ValueError as e:
                pass
            member_data.items = member_items #Update the original list with modified list.

            await database.member.push(ctx, member_data) #Push member data back up.

            #If the item is a role update member's prefix and remove role from member.
            if await core_shop.items.checks.item_type(item_data) == "role":
                #Remove role from member.
                await core_shop.items.role.take(ctx, item_data)

                #Update member's prefix.

            #Get money emoji.
            money_emoji = hallo_msg.candy_emoji
            
            #Embeded message
            description_message = ((msg.sell.embed.main_context).format(ctx.author.mention, item, money_emoji, amount, money_emoji, user_bal, money_emoji, settings.sell_tax))
            title_message = "🤝 __ITEM SOLD!__"
            embed = nextcord.Embed(title=title_message, description=description_message, colour=settings.YELLOW)
            embed.set_footer(text=msg.footer.type_2)
            if not item_data.embed.image in ["", None]:
                embed.set_thumbnail(url=item_data.embed.image)
            await ctx.send(embed=embed)

            #You still horny?

            return True #Tells buy command purchase was complete and it can progress.

def setup(client):
    client.add_cog(shop(client))