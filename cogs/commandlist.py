import discord

from discord.ext import commands

from discord import app_commands

import math

# Emojis für bekannte Kategorien (du kannst beliebig erweitern)

CATEGORY_EMOJIS = {

    "AutoAnswer": "🤖",

    "AutoReaction": "⚡",

    "Avatar": "🖼️",

    "BotInfo": "ℹ️",

    "Bump": "📢",

    "Chatbot": "💬",

    "Clear": "🧹",

    "CommandList": "📋",

    "Joke": "😂",

    "Level": "📈",

    "Meme": "🐸",

    "Owner": "👑",

    "Quiz": "❓",

    "Restart": "🔄",

    "Roast": "🔥",

    "RoleMenu": "🎭",

    "RPS": "✊",

    "Rules": "📜",

    "ServerInfo": "📊",

    "Snipes": "👀",

    "Ticket": "🎫",

    "Welcome": "👋",

    "WYR": "🤔",

    "Logging": "📝",

    "Warn": "⚠️",

    "Image": "🎨",

    "BotEvents": "📡",

    "Changelog": "📜",

    "Other": "📁"

}

class CommandListView(discord.ui.View):

    def __init__(self, categories, bot, items_per_page=6):

        super().__init__(timeout=60)

        self.categories = categories          # Liste von (Kategorie-Name, [commands])

        self.bot = bot

        self.items_per_page = items_per_page

        self.current_page = 0

        self.total_pages = math.ceil(len(categories) / items_per_page)

        self.update_buttons()

    def update_buttons(self):

        self.clear_items()

        if self.total_pages > 1:

            prev_button = discord.ui.Button(

                label="◀️ Vorherige Seite",

                style=discord.ButtonStyle.secondary,

                disabled=(self.current_page == 0)

            )

            next_button = discord.ui.Button(

                label="Nächste Seite ▶️",

                style=discord.ButtonStyle.secondary,

                disabled=(self.current_page == self.total_pages - 1)

            )

            prev_button.callback = self.prev_page

            next_button.callback = self.next_page

            self.add_item(prev_button)

            self.add_item(next_button)

    async def prev_page(self, interaction: discord.Interaction):

        self.current_page -= 1

        self.update_buttons()

        embed = self.build_embed()

        await interaction.response.edit_message(embed=embed, view=self)

    async def next_page(self, interaction: discord.Interaction):

        self.current_page += 1

        self.update_buttons()

        embed = self.build_embed()

        await interaction.response.edit_message(embed=embed, view=self)

    def build_embed(self):

        start = self.current_page * self.items_per_page

        end = start + self.items_per_page

        page_categories = self.categories[start:end]

        embed = discord.Embed(

            title="📜 Befehlsübersicht",

            description=f"**{len(self.categories)}** Kategorien | Seite {self.current_page+1}/{self.total_pages}",

            color=discord.Color.blue()

        )

        for cat_name, cmds in page_categories:

            emoji = CATEGORY_EMOJIS.get(cat_name, "📌")

            cmds_sorted = sorted(cmds, key=lambda x: x["name"])

            value = "\n".join(

                f"`/{cmd['name']}` – {cmd['description']}"

                for cmd in cmds_sorted

            )

            # Falls die Beschreibung zu lang wird (max. 1024 Zeichen pro Feld)

            if len(value) > 1024:

                value = value[:1021] + "..."

            embed.add_field(

                name=f"{emoji} {cat_name} ({len(cmds_sorted)})",

                value=value,

                inline=False

            )

        # Bot-Avatar als Thumbnail (optional)

        if self.bot.user.avatar:

            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(text="Klicke auf die Buttons, um durch die Seiten zu blättern.")

        return embed

class CommandList(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    def get_categories(self):

        """Ermittelt alle Kategorien (Cogs) und ihre Slash-Commands"""

        categories = {}

        for cog_name, cog in self.bot.cogs.items():

            commands_in_cog = []

            for cmd in self.bot.tree.get_commands():

                if isinstance(cmd, app_commands.Command):

                    if cmd.module and cmd.module.endswith(cog_name.lower()):

                        commands_in_cog.append({"name": cmd.name, "description": cmd.description or "Keine Beschreibung"})

            if commands_in_cog:

                categories[cog_name] = commands_in_cog

        # Nicht zugeordnete Befehle in "Sonstige"

        all_assigned = set()

        for cmds in categories.values():

            for cmd in cmds:

                all_assigned.add(cmd["name"])

        leftover = []

        for cmd in self.bot.tree.get_commands():

            if isinstance(cmd, app_commands.Command) and cmd.name not in all_assigned:

                leftover.append({"name": cmd.name, "description": cmd.description or "Keine Beschreibung"})

        if leftover:

            categories["Sonstige"] = leftover

        # Nach Kategoriename sortieren

        return sorted(categories.items(), key=lambda x: x[0])

    @app_commands.command(name="commandlist", description="Zeigt alle verfügbaren Slash-Commands an")

    async def commandlist(self, interaction: discord.Interaction):

        categories = self.get_categories()

        if not categories:

            return await interaction.response.send_message("❌ Keine Befehle gefunden.", ephemeral=True)

        items_per_page = 6   # 6 Kategorien pro Seite (bleibt weit unter 25 Feldern)

        total_pages = math.ceil(len(categories) / items_per_page)

        if total_pages == 1:

            # Nur eine Seite – einfaches Embed ohne Buttons

            embed = discord.Embed(

                title="📜 Befehlsübersicht",

                description=f"**{len(categories)}** Kategorien",

                color=discord.Color.blue()

            )

            for cat_name, cmds in categories:

                emoji = CATEGORY_EMOJIS.get(cat_name, "📌")

                cmds_sorted = sorted(cmds, key=lambda x: x["name"])

                value = "\n".join(

                    f"`/{cmd['name']}` – {cmd['description']}"

                    for cmd in cmds_sorted

                )

                if len(value) > 1024:

                    value = value[:1021] + "..."

                embed.add_field(

                    name=f"{emoji} {cat_name} ({len(cmds_sorted)})",

                    value=value,

                    inline=False

                )

            if self.bot.user.avatar:

                embed.set_thumbnail(url=self.bot.user.avatar.url)

            await interaction.response.send_message(embed=embed)

        else:

            view = CommandListView(categories, self.bot, items_per_page=items_per_page)

            embed = view.build_embed()

            await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):

    await bot.add_cog(CommandList(bot))