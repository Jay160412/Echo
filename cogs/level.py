import discord

from discord.ext import commands

from discord import app_commands

import json

import os

import random

from typing import Optional

import datetime

class LevelSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.data_dir = os.path.join(os.path.dirname(__file__), "data")

        self.users_file = os.path.join(self.data_dir, "users.json")

        self.shop_file = os.path.join(self.data_dir, "shop.json")

        self.quests_file = os.path.join(self.data_dir, "quests.json")

        self.setup_files()

        

        self.level_roles = {

            1: {"name": "🎉 Level 1", "color": discord.Colour.green(), "coins": 50},

            5: {"name": "💰 Level 5", "color": discord.Colour.blue(), "coins": 100},

            10: {"name": "🎁 Level 10", "color": discord.Colour.gold(), "coins": 200},

            20: {"name": "💎 Level 20", "color": discord.Colour.purple(), "coins": 500}

        }

        self.daily_quests = {

            "messages": {"target": 10, "reward": 50, "description": "Sende 10 Nachrichten"},

            "reactions": {"target": 5, "reward": 30, "description": "Reagiere 5 mal auf Nachrichten"},

            "voice": {"target": 30, "reward": 100, "description": "Verbringe 30 Minuten im Voice"}

        }

    def setup_files(self):

        """Initialisiert alle benötigten Dateien sicher"""

        try:

            os.makedirs(self.data_dir, exist_ok=True)

            

            if not os.path.exists(self.users_file):

                with open(self.users_file, "w") as f:

                    json.dump({}, f)

            

            if not os.path.exists(self.shop_file):

                default_shop = {

                    "1": {

                        "name": "🌟 VIP-Badge",

                        "price": 500,

                        "type": "role",

                        "description": "Exklusives Abzeichen neben deinem Namen"

                    },

                    "2": {

                        "name": "🎨 Custom Color",

                        "price": 300,

                        "type": "role",

                        "description": "Persönliche Farbrolle"

                    },

                    "3": {

                        "name": "👑 Legendary Title",

                        "price": 1000,

                        "type": "role",

                        "description": "Spezieller Titel unter deinem Namen"

                    }

                }

                with open(self.shop_file, "w") as f:

                    json.dump(default_shop, f, indent=4)

            

            if not os.path.exists(self.quests_file):

                with open(self.quests_file, "w") as f:

                    json.dump({}, f)

        except Exception as e:

            print(f"FEHLER beim Datei-Setup: {e}")

    def get_user_data(self, user_id: int) -> dict:

        """Lädt Benutzerdaten mit Fehlerbehandlung"""

        try:

            with open(self.users_file, "r") as f:

                users = json.load(f)

                return users.get(str(user_id), {

                    "xp": 0, 

                    "level": 1, 

                    "coins": 0,

                    "last_daily": None,

                    "quests": {

                        "messages": 0,

                        "reactions": 0,

                        "voice": 0

                    }

                })

        except (json.JSONDecodeError, FileNotFoundError):

            return {

                "xp": 0, 

                "level": 1, 

                "coins": 0,

                "last_daily": None,

                "quests": {

                    "messages": 0,

                    "reactions": 0,

                    "voice": 0

                }

            }

    def save_user_data(self, user_id: int, data: dict):

        """Speichert Benutzerdaten sicher"""

        try:

            with open(self.users_file, "r") as f:

                users = json.load(f)

            

            users[str(user_id)] = data

            

            with open(self.users_file, "w") as f:

                json.dump(users, f, indent=4)

        except Exception as e:

            print(f"FEHLER beim Speichern der User-Daten: {e}")

    async def create_level_roles(self, guild: discord.Guild):

        """Erstellt Level-Rollen falls nicht vorhanden"""

        for level, role_data in self.level_roles.items():

            try:

                if not discord.utils.get(guild.roles, name=role_data["name"]):

                    await guild.create_role(

                        name=role_data["name"],

                        color=role_data["color"],

                        mentionable=True

                    )

            except discord.Forbidden:

                print(f"Keine Berechtigung zum Erstellen von Rollen in {guild.name}")

            except Exception as e:

                print(f"FEHLER beim Rollen-Erstellen: {e}")

    @commands.Cog.listener()

    async def on_ready(self):

        print(f"LevelSystem Cog geladen für {len(self.bot.guilds)} Server")

        for guild in self.bot.guilds:

            await self.create_level_roles(guild)

    @commands.Cog.listener()

    async def on_guild_join(self, guild: discord.Guild):

        await self.create_level_roles(guild)

    @commands.Cog.listener()

    async def on_message(self, message: discord.Message):

        if message.author.bot or not message.guild:

            return

            

        try:

            user_id = message.author.id

            user_data = self.get_user_data(user_id)

            

            # XP vergeben

            xp_gain = random.randint(5, 15)

            user_data["xp"] += xp_gain

            

            # Quest-Progress

            user_data["quests"]["messages"] += 1

            

            # Level-Berechnung

            new_level = int((user_data["xp"] / 100) ** 0.5) + 1

            

            if new_level > user_data["level"]:

                user_data["level"] = new_level

                

                if new_level in self.level_roles:

                    reward = self.level_roles[new_level]

                    user_data["coins"] += reward["coins"]

                    

                    role = discord.utils.get(message.guild.roles, name=reward["name"])

                    if role:

                        try:

                            await message.author.add_roles(role)

                            await message.channel.send(

                                f"🎉 {message.author.mention} ist jetzt Level {new_level}! "

                                f"Belohnung: {reward['coins']} Coins und Rolle {reward['name']}!"

                            )

                        except discord.Forbidden:

                            print(f"Keine Berechtigung für Rollenvergabe in {message.guild.name}")

            

            self.save_user_data(user_id, user_data)

        except Exception as e:

            print(f"FEHLER in on_message: {e}")

    @app_commands.command(name="level", description="Zeigt dein Level an")

    async def level_cmd(self, interaction: discord.Interaction):

        try:

            user_data = self.get_user_data(interaction.user.id)

            

            embed = discord.Embed(

                title=f"📊 {interaction.user.display_name}",

                color=discord.Colour.blurple()

            )

            embed.add_field(name="Level", value=f"`{user_data['level']}`", inline=True)

            embed.add_field(name="XP", value=f"`{user_data['xp']}`", inline=True)

            embed.add_field(name="Coins", value=f"`{user_data['coins']}`", inline=True)

            

            next_level_xp = (user_data['level']**2) * 100

            current_level_xp = ((user_data['level'] - 1)**2) * 100

            progress = min(100, int(((user_data['xp'] - current_level_xp) / (next_level_xp - current_level_xp)) * 100))

            

            embed.add_field(

                name="Fortschritt",

                value=f"`{progress}%` zum nächsten Level (XP: {user_data['xp']}/{next_level_xp})",

                inline=False

            )

            

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            print(f"FEHLER in /level: {e}")

            await interaction.response.send_message(

                "❌ Fehler beim Laden der Level-Daten!",

                ephemeral=True

            )

    @app_commands.command(name="shop", description="Zeigt den Shop an")

    async def shop(self, interaction: discord.Interaction):

        try:

            with open(self.shop_file, "r") as f:

                shop_items = json.load(f)

            

            embed = discord.Embed(title="🛒 Shop", color=discord.Colour.gold())

            

            for item_id, item in shop_items.items():

                embed.add_field(

                    name=f"{item['name']} - {item['price']} Coins",

                    value=f"{item['description']}\n`ID: {item_id}`",

                    inline=False

                )

            

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            print(f"FEHLER in /shop: {e}")

            await interaction.response.send_message(

                "❌ Shop konnte nicht geladen werden!",

                ephemeral=True

            )

    @app_commands.command(name="buy", description="Kaufe ein Item")

    @app_commands.describe(item_id="Die ID des Items aus /shop")

    async def buy(self, interaction: discord.Interaction, item_id: str):

        try:

            with open(self.shop_file, "r") as f:

                shop_items = json.load(f)

            

            if item_id not in shop_items:

                return await interaction.response.send_message("❌ Ungültige Item-ID!", ephemeral=True)

                

            user_data = self.get_user_data(interaction.user.id)

            item = shop_items[item_id]

            

            if user_data["coins"] < item["price"]:

                return await interaction.response.send_message("❌ Nicht genug Coins!", ephemeral=True)

                

            user_data["coins"] -= item["price"]

            self.save_user_data(interaction.user.id, user_data)

            

            if item["type"] == "role":

                role = discord.utils.get(interaction.guild.roles, name=item["name"])

                if not role:

                    role = await interaction.guild.create_role(

                        name=item["name"],

                        color=discord.Colour.random(),

                        hoist=True

                    )

                await interaction.user.add_roles(role)

            

            await interaction.response.send_message(

                f"✅ Erfolgreich gekauft: **{item['name']}**!",

                ephemeral=True

            )

        except Exception as e:

            print(f"FEHLER in /buy: {e}")

            await interaction.response.send_message(

                "❌ Fehler beim Kauf!",

                ephemeral=True

            )

    @app_commands.command(name="leaderboard", description="Top 10 Spieler")

    async def leaderboard(self, interaction: discord.Interaction):

        try:

            with open(self.users_file, "r") as f:

                users = json.load(f)

            

            sorted_users = sorted(

                users.items(),

                key=lambda x: (-x[1].get("level", 0), -x[1].get("xp", 0))

            )[:10]

            

            embed = discord.Embed(title="🏆 Leaderboard", color=discord.Colour.green())

            description = []

            

            for rank, (user_id, data) in enumerate(sorted_users, 1):

                try:

                    user = await self.bot.fetch_user(int(user_id))

                    description.append(

                        f"{rank}. **{user.display_name}** - "

                        f"Level {data.get('level', 0)} | "

                        f"{data.get('xp', 0)} XP | "

                        f"💰 {data.get('coins', 0)}"

                    )

                except:

                    continue

            

            embed.description = "\n".join(description)

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            print(f"FEHLER in /leaderboard: {e}")

            await interaction.response.send_message(

                "❌ Leaderboard konnte nicht geladen werden!",

                ephemeral=True

            )

    @app_commands.command(name="daily", description="Tägliche Belohnungen abholen")

    async def daily(self, interaction: discord.Interaction):

        try:

            user_data = self.get_user_data(interaction.user.id)

            today = datetime.datetime.now().date()

            

            if user_data["last_daily"] and datetime.datetime.strptime(user_data["last_daily"], "%Y-%m-%d").date() == today:

                return await interaction.response.send_message(

                    "❌ Du hast deine tägliche Belohnung heute schon abgeholt!",

                    ephemeral=True

                )

            

            # Quest-Überprüfung

            completed_quests = []

            reward = 0

            

            for quest_id, quest in self.daily_quests.items():

                if user_data["quests"].get(quest_id, 0) >= quest["target"]:

                    completed_quests.append(f"✅ {quest['description']} (+{quest['reward']} Coins)")

                    reward += quest["reward"]

                    user_data["quests"][quest_id] = 0

            

            # Basisbelohnung

            base_reward = 100

            reward += base_reward

            

            user_data["coins"] += reward

            user_data["last_daily"] = today.strftime("%Y-%m-%d")

            self.save_user_data(interaction.user.id, user_data)

            

            embed = discord.Embed(

                title="🎁 Tägliche Belohnung",

                description=f"Du hast **{reward} Coins** erhalten!",

                color=discord.Colour.green()

            )

            

            if completed_quests:

                embed.add_field(

                    name="Abgeschlossene Quests",

                    value="\n".join(completed_quests),

                    inline=False

                )

            

            embed.set_footer(text="Komm morgen wieder für weitere Belohnungen!")

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            print(f"FEHLER in /daily: {e}")

            await interaction.response.send_message(

                "❌ Fehler beim Abholen der täglichen Belohnung!",

                ephemeral=True

            )

async def setup(bot):

    await bot.add_cog(LevelSystem(bot))