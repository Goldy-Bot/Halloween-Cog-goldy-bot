from types import SimpleNamespace
import nextcord
import os
import json
import random

from src.goldy_func import print_and_log
import settings

import cogs.giphy_cog.api as giphy_api

from cogs.database import database

class member():
        class checks():
            @staticmethod
            async def is_battable(ctx, member_data): #Checks if member is battable or not.
                battable = await member.get(ctx, member_data)

                if battable == True:
                    return True
                else:
                    return False

        @staticmethod
        async def toggle(ctx, on_off:str): #Toggles battable on or off.
            member_data = await database.member.pull(ctx)
            
            if on_off.lower() == "on":
                try:
                    member_data.battable = True
                    await database.member.push(ctx, member_data)
                    return (True, "on")
                except AttributeError as e:
                    await database.member.add_object(ctx, "battable", True)
                    return (True, "on")

            if on_off.lower() == "off":
                try:
                    member_data.battable = False
                    await database.member.push(ctx, member_data)
                    return (True, "off")
                except AttributeError as e:
                    await database.member.add_object(ctx, "battable", False)
                    return (True, "off")

            return (False, None)

        @staticmethod
        async def get(ctx, member_data): #Get's the "battable" object from the member data.
            try:
                battable = member_data.battable #The new object name.
                return battable
            except AttributeError as e:
                await database.member.add_object(ctx, "battable", True)
                return False

class random_bat_image():
    @staticmethod
    async def update(): #Checks if "simp_images.json" is in config.
        json_file_name = "bat_images.json"

        if not json_file_name in os.listdir("config/"):
            #Create and write to level_up_msgs.json
            simp_images_file = open(f"config/{json_file_name}", "x")
            simp_images_file = open(f"config/{json_file_name}", "w")
            
            json.dump({"1" : {"name": "Bat 1", 
            "url" : "https://cdn.dribbble.com/users/47268/screenshots/6224451/bat.gif"}}, simp_images_file) #Dumping the example layout in the json file.

    @staticmethod
    async def get(): #Get's random simp image from "simp_images.json".
        json_file_name = "bat_images.json"

        try:
            f = open (f'config/{json_file_name}', "r", encoding="utf8")
            simp_images_normal = json.loads(f.read())

        except FileNotFoundError as e:
            print_and_log("warn", f"'{json_file_name}' was not found. Running update function and trying again. >>> {e}")
            await random_bat_image.update()

            f = open (f'config/{json_file_name}', "r", encoding="utf8")
            simp_images_normal = json.loads(f.read())


        max_images_num = len(simp_images_normal.keys())
        random_num = random.randint(1, max_images_num) #Test to see what happends if max num is also 1.

        level_up_message = json.dumps(simp_images_normal[str(random_num)])
        level_up_message_formatted = json.loads(level_up_message, object_hook=lambda d: SimpleNamespace(**d))

        return level_up_message_formatted

class embed():
    @staticmethod
    async def create(member_sent_by):
        embed = nextcord.Embed(title="**🦇 Someone sent you a bat.**", colour=settings.AKI_ORANGE)
        embed.set_footer(text=f"Sent by {member_sent_by.name}", icon_url=member_sent_by.avatar.url)
        return embed