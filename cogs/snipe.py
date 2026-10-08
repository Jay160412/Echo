import discord

from discord.ext import commands

from discord import app_commands

class SnipeCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.deleted_messages = {}  # {channel_id: message}

    @commands.Cog.listener()

    async def on_message_delete(self, message):

        # Ignoriere Bot-Nachrichten und leere Nachrichten

        if message.author.bot or not message.content:

            return

            

        # Speichere die gelöschte Nachricht

        self.deleted_messages[message.channel.id] = {

            "content": message.content,

            "author": message.author,

            "created_at": message.created_at,

            "attachments": [a.url for a in message.attachments]

        }

    @app_commands.command(name="snipe", description="Zeigt die letzte gelöschte Nachricht an")

    async def snipe(self, interaction: discord.Interaction):

        """Einfacher Snipe-Befehl ohne Admin-Beschränkung zum Testen"""

        try:

            # Hole die gespeicherte Nachricht

            if interaction.channel.id not in self.deleted_messages:

                await interaction.response.send_message("❌ Keine gelöschten Nachrichten gefunden!", ephemeral=True)

                return

            message = self.deleted_messages[interaction.channel.id]

            # Erstelle das Embed

            embed = discord.Embed(

                description=message["content"],

                color=discord.Color.red(),

                timestamp=message["created_at"]

            )

            embed.set_author(

                name=str(message["author"]),

                icon_url=message["author"].avatar.url

            )

            # Füge Anhänge hinzu falls vorhanden

            if message["attachments"]:

                embed.add_field(

                    name="Anhänge",

                    value="\n".join(message["attachments"]),

                    inline=False

                )

            await interaction.response.send_message(embed=embed)

        except Exception as e:

            print(f"Fehler in snipe: {e}")

            await interaction.response.send_message(

                "❌ Es ist ein Fehler aufgetreten!",

                ephemeral=True

            )

async def setup(bot):

    await bot.add_cog(SnipeCog(bot))