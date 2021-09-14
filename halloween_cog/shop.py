import nextcord
from nextcord import guild
from nextcord.ext import commands
import asyncio
import datetime
import traceback

from goldy_func import *
from goldy_utility import *
import config.msg as msg

from . import msg as hallo_msg

cog_name = "shop"

max_pages = 2

class shop(commands.Cog):
    def __init__(self, client):
        self.client = client

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

            database = self.client.get_cog('database')
            items_data = await self.items.find(ctx)
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
                items_data = await self.items.find_one(ctx, item)

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

            commands_context = await shop.embeded.get_context(ctx, commands_context, page)
            roles_context = await shop.embeded.get_context(ctx, roles_context, page)
            colours_context = await shop.embeded.get_context(ctx, colours_context, page)

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

        @staticmethod
        async def get_context(ctx, context, page): #Grabs the correct number of items to view in page. (Used to only grab a certain amount of items for the shop page)
            try:
                last_item = page * 5
                first_item = last_item - 5

                list_of_items = (context.splitlines()[first_item:last_item])
                context = ""
                for command in list_of_items:
                    context += command + "\n"

                if context == "":
                    return "***There's no more items on this page.***"

                return context

            except Exception as e:
                goldy.log_error(ctx, f"Failed to grab items!!! {msg.error.contact_dev}\n" + e) #Fix this function thing...
                return "***Failed to grab items!!! Contact a Dev.***"

    class items():
        class role():
            class bundle:
                @staticmethod
                async def find(ctx, bundle_code_name): #Finds the role bundle data.
                    try:
                        server_info = servers.get(ctx.guild.id)
                        server_code_name = server_info.names.code_name

                        code_name = bundle_code_name
                        
                        f = open (f'config\\{server_code_name}\\items.json', "r")
                        bundles_json = json.loads(f.read())

                        async def found_bundle(bundle_json):
                            bundle_json = json.dumps(bundle_json)
                            bundle_info = json.loads(bundle_json, object_hook=lambda d: SimpleNamespace(**d))
                            
                            return bundle_info #Returns the json but as python class so you can easily pick the data.

                        #Find the bundles.
                        for bundle in bundles_json["roles"]:
                            if bundle == code_name:
                                if str(bundle)[0] == "@":
                                    bundle_json = bundles_json["roles"][code_name]
                                    bundle_json["type"] = "role_bundle"
                                    bundle_info = await found_bundle(bundle_json)
                                    return bundle_info

                        #If bundle not found.
                        return False

                    except Exception as e:
                        print_and_log("error", f"Exception in shop.items.role.bundle.find method. {e}")

            @staticmethod
            async def is_merging(ctx, item_data): #Checks if there's any role confilct going on.
                #Check if item has 'do_not_merge_with' object in config.
                try:
                    #Find 'do_not_merge_with' object.
                    try:
                        merging = item_data.config.do_not_merge_with
                    except AttributeError as e:
                        return (False, None)

                    #If 'do_not_merge_with' object exist find the role bundle.
                    role_bundle_info = await shop.items.role.bundle.find(ctx, merging)

                    #Check if member has any roles in list.
                    for role_id in role_bundle_info.ids:
                        role = nextcord.utils.get(ctx.guild.roles, id=role_id)

                        if role in ctx.author.roles: #If member does, return True immediately.
                            return (True, role)

                    #If member has none of the roles return False.
                    return (False, None)

                except Exception as e:
                    print_and_log("error", f"Exception in shop.items.role.is_merging method. {e}")

            @staticmethod
            async def give(ctx, item_data): #Give a member a role safely.
                role = nextcord.utils.get(ctx.guild.roles, id=item_data.id)

                has_role = None
                #Check if member has role.
                if role in ctx.author.roles:
                    has_role = True
                else:
                    has_role = False

                if has_role == True:
                    return False
                if has_role == False:
                    await ctx.author.add_roles(role)
                    print_and_log(None, f"[{cog_name.upper()}] Gave '{role.name}' to '{ctx.author.name}'.")
                    return True

            @staticmethod
            async def take(ctx, item_data): #Remove a role from a member safely.
                role = nextcord.utils.get(ctx.guild.roles, id=item_data.id)

                has_role = None
                #Check if member has role.
                if role in ctx.author.roles:
                    has_role = True
                else:
                    has_role = False

                if has_role == True:
                    await ctx.author.remove_roles(role)
                    print_and_log(None, f"[{cog_name.upper()}] Removed '{role.name}' from '{ctx.author.name}''.")
                    return True
                if has_role == False:
                    return False

        class checks():
            @staticmethod
            async def item_type(item_data): #Tells you what type the item is, a command(cmd), a role or a colour.(Used in buy function.)
                item_type = item_data.type
                return item_type

            @staticmethod
            async def is_sellable(item_data):  
                try:
                    #Find sellable object
                    try:
                        sellable = item_data.config.sellable
                    except AttributeError as e:
                        sellable = None

                    if sellable == None: #If not specified, it will default to True.
                        return True
                    else:
                        return sellable

                except Exception as e:
                    print_and_log("error", f"Exception in shop.items.checks.is_sellable method. {e}")

        @staticmethod
        async def find(ctx): #Grabs data/info of all items. (Used in commands like the shop command but this method is slower if finding percific item's data.)
            server_info = servers.get(ctx.guild.id)
            server_code_name = server_info.names.code_name
            
            async def run():
                #Guild items.json.
                f = open (f'config\\{server_code_name}\\items.json', "r")
                guild_items_json_normal = json.loads(f.read())

                #Global items.json.
                f = open (f'config\\global\\items.json', "r")
                global_items_json_normal = json.loads(f.read())

                #Combind items data.
                items_json_normal = await shop.items.merge(guild_items_json_normal, global_items_json_normal)
                
                #Format data.
                items_json = json.dumps(items_json_normal)
                items_info_formatted = json.loads(items_json, object_hook=lambda d: SimpleNamespace(**d))
                
                return items_info_formatted, items_json_normal #Returns the json but as python class so you can easily pick the data.

            try:
                return await run()

            except FileNotFoundError as e:
                print_and_log("warn", f"'items.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()
                return await run()

            except Exception as e:
                print_and_log("error_cog", cog_name.upper(), "items.find", e)

        @staticmethod
        async def find_one(ctx, code_name): #Grabs data/info of an item. (Used for getting info for a percific item only and is also faster than the normal get method.)
            server_info = servers.get(ctx.guild.id)
            server_code_name = server_info.names.code_name

            code_name = code_name.lower()
            
            async def run():
                #Guild items.json.
                f = open (f'config\\{server_code_name}\\items.json', "r")
                guild_items_json = json.loads(f.read())

                #Global items.json.
                f = open (f'config\\global\\items.json', "r")
                global_items_json = json.loads(f.read())

                items_json = (guild_items_json, global_items_json)

                async def found_item(item_json):
                    item_json = json.dumps(item_json)
                    item_info = json.loads(item_json, object_hook=lambda d: SimpleNamespace(**d))
                    
                    return item_info #Returns the json but as python class so you can easily pick the data.
                
                #Find the guild items and global items.
                for i in range(len(items_json)):

                    for command in items_json[i]["commands"]["list"]:
                        if not (code_name[0]) == "!": #Allows function to still find the command even if there's no '!' at the start.
                            new_code_name = "!" + code_name
                        else:
                            new_code_name = code_name

                        if command == new_code_name:
                            item_json = items_json[i]["commands"][new_code_name]
                            item_json["type"] = "cmd"
                            item_info = await found_item(item_json)
                            return item_info

                    for role in items_json[i]["roles"]["list"]:
                        if role == code_name:
                            item_json = items_json[i]["roles"][code_name]
                            item_json["type"] = "role"
                            item_info = await found_item(item_json)
                            return item_info

                    for colour in items_json[i]["colours"]["list"]:
                        if colour == code_name.replace(" ", "_"):
                            item_json = items_json[i]["colours"][code_name]
                            item_json["type"] = "colour"
                            item_info = await found_item(item_json)
                            return item_info

                #If item not found.
                return False

            try:
                return await run()

            except FileNotFoundError as e:
                print_and_log("warn", f"'items.json' was not found. Running update function and trying again. >>> {e}")
                await servers.update()

                return await run()

            except Exception as e:
                print_and_log("error_cog", cog_name.upper(), "items.find_one", e)

        @staticmethod
        async def get_name(ctx, item_data): #Get's actually name of item.
            
            try:
                #Find display name
                try:
                    display_name = item_data.display_name
                except AttributeError as e:
                    display_name = None

                if display_name == None:
                    #If the item is a role, change item name to role mention.
                    if await shop.items.checks.item_type(item_data) == "role":
                        role_mention = (nextcord.utils.get(ctx.guild.roles, id=item_data.id)).mention
                        item_name = role_mention
                        return item_name
                    else:
                        item_name = item_data.names.code_name
                        return item_name

                if not display_name == None:
                    return item_data.display_name

            except Exception as e:
                print_and_log("error", f"Exception in database shop.items.get_name method. {e}")

        @staticmethod
        async def merge(guild_items_json_normal, global_items_json_normal): #Merges global items with guild items.
            merged_items_json_normal = {}

            #Commands
            merged_items_json_normal["commands"] = await guild_func.dict.merge(guild_items_json_normal["commands"], global_items_json_normal["commands"])
            merged_items_json_normal["commands"]["list"] = guild_items_json_normal["commands"]["list"] + global_items_json_normal["commands"]["list"] #Alter the list.
            
            #Roles
            merged_items_json_normal["roles"] = guild_items_json_normal["roles"]
            
            #Colours
            merged_items_json_normal["colours"] = await guild_func.dict.merge(guild_items_json_normal["colours"], global_items_json_normal["colours"])
            merged_items_json_normal["colours"]["list"] = guild_items_json_normal["colours"]["list"] + global_items_json_normal["colours"]["list"] #Alter the list.

            return merged_items_json_normal

        @staticmethod
        async def buy(ctx, client, item_data): #This buy function handels purchusing the item and sending Purchased embeded.
            item = await shop.items.get_name(ctx, item_data)

            economy = client.get_cog('candy')
            database = client.get_cog('database')

            #Check if member has item.
            has_item = await database.member.checks.has_item(ctx, item_data.names.code_name)
            if has_item == True:
                await ctx.send((msg.buy.failed.already_own).format(ctx.author.mention))
                return False

            #If the item is a role add the role, update member's prefix and check if it merges with any other roles.
            if await shop.items.checks.item_type(item_data) == "role":
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
                await shop.items.role.give(ctx, item_data)
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
            item = await shop.items.get_name(ctx, item_data) #Replace this with 'shop.item.get_name' when done with coding it OR ELSE BUYING ROLES WON'T WORK!

            economy = client.get_cog('candy')
            database = client.get_cog('database')

            #Check if member has item.
            has_item = await database.member.checks.has_item(ctx, item_data.names.code_name)
            if has_item == False:
                await ctx.send((msg.sell.failed.do_not_have_item).format(ctx.author.mention))
                return False

            #Check if item is sellable.
            sellable = await shop.items.checks.is_sellable(item_data)
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
            if await shop.items.checks.item_type(item_data) == "role":
                #Remove role from member.
                await shop.items.role.take(ctx, item_data)

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