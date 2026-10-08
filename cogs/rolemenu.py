import discord
from discord.ext import commands
from discord import app_commands, ui
import json
import os
import re
from typing import List


def split_role_references(value: str) -> list[str]:
    """Accept role mentions/IDs separated by spaces and names separated by commas."""
    refs = []
    id_pattern = re.compile(r"<@&(\d+)>|(?<!\d)\d{15,22}(?!\d)")
    for match in id_pattern.finditer(value):
        refs.append(match.group(1) or match.group(0))

    remainder = id_pattern.sub(",", value)
    refs.extend(
        part.strip().lstrip("@").strip()
        for part in re.split(r"[,;\n]+", remainder)
        if part.strip()
    )
    return refs


class RoleMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data_file = "data/role_menus.json"
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.persistent_views = self.load_menus()
        self._restored_messages = set()

    def load_menus(self) -> dict:
        """Lädt gespeicherte Menüs aus JSON"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_menus(self):
        """Speichert Menüs in JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.persistent_views, f, indent=2)

    class RoleView(ui.View):
        def __init__(self, roles: List[discord.Role], menu_id: str):
            super().__init__(timeout=None)
            self.menu_id = menu_id
            self.role_ids = {str(role.id) for role in roles}
            self.add_item(RoleMenu.RoleDropdown(roles))

    class RoleDropdown(ui.Select):
        def __init__(self, roles: List[discord.Role]):
            valid_roles = [r for r in roles if isinstance(r, discord.Role)][:25]
            options = [
                discord.SelectOption(
                    label=role.name[:25],
                    value=str(role.id),
                    description=f"Aktiviert @{role.name[:50]}" if role.name else "Rolle",
                    emoji="🔔"
                ) for role in valid_roles
            ] or [discord.SelectOption(label="Keine Rollen", value="0", description="Konfiguriere /rolemenu")]

            super().__init__(
                placeholder="Wähle deine Rollen..."[:100],
                min_values=0,
                max_values=min(25, max(1, len(valid_roles))),
                options=options[:25],
                custom_id="role_dropdown"
            )

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                added, removed = [], []
                guild, member = interaction.guild, interaction.user
                if guild is None or not isinstance(member, discord.Member):
                    return await interaction.followup.send(
                        "Dieses Rollen-Menü funktioniert nur auf einem Server.",
                        ephemeral=True,
                    )

                bot_member = guild.me
                if bot_member is None or not bot_member.guild_permissions.manage_roles:
                    return await interaction.followup.send(
                        "Der Bot benötigt die Berechtigung „Rollen verwalten“.",
                        ephemeral=True,
                    )

                selected_ids = {int(id) for id in self.values if id != "0"}
                current_ids = {r.id for r in member.roles}

                # Rollen hinzufügen
                for role_id in selected_ids - current_ids:
                    if role := guild.get_role(role_id):
                        if role < bot_member.top_role:
                            await member.add_roles(role)
                            added.append(role.name)

                # Rollen entfernen
                for role in member.roles:
                    if str(role.id) in self.view.role_ids and role.id not in selected_ids:
                        if role < bot_member.top_role:
                            await member.remove_roles(role)
                            removed.append(role.name)

                # Antwort senden
                message = []
                if added: message.append(f"✅ Hinzugefügt: {', '.join(added)}")
                if removed: message.append(f"❌ Entfernt: {', '.join(removed)}")
                await interaction.followup.send("\n".join(message) or "Keine Änderungen", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send(
                    "Discord hat die Rollenänderung abgelehnt. Prüfe „Rollen verwalten“ und die Position der Bot-Rolle.",
                    ephemeral=True,
                )
            except Exception as e:
                await interaction.followup.send(f"⚠️ Fehler: {type(e).__name__}", ephemeral=True)

    @app_commands.command(name="rolemenu", description="Erstellt ein anpassbares Rollen-Menü")
    @app_commands.describe(
        channel="Zielkanal für das Menü",
        roles="Rollen (@Erwähnungen oder IDs, kommagetrennt)",
        title="Embed-Titel (max. 256 Zeichen)",
        description="Embed-Beschreibung (max. 4096 Zeichen)",
        footer="Footer-Text (max. 2048 Zeichen)",
        color="Embed-Farbe (Hex-Code, z.B. FF5733)",
        thumbnail_url="Thumbnail-URL (optional)"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def create_role_menu(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        roles: str,
        title: str = "🔔 Rollen-Verwaltung",
        description: str = "Wähle deine gewünschten Rollen aus:",
        footer: str = "Jederzeit änderbar",
        color: str = "3498db",
        thumbnail_url: str = None
    ):
        try:
            await interaction.response.defer(ephemeral=True)

            guild = interaction.guild
            bot_member = guild.me if guild else None
            if bot_member is None or not bot_member.guild_permissions.manage_roles:
                return await interaction.followup.send(
                    "Der Bot benötigt auf diesem Server die Berechtigung „Rollen verwalten“.",
                    ephemeral=True,
                )
            
            # Mentions and IDs may be space-separated; role names are comma-separated.
            role_objects, invalid, unavailable = [], [], []
            seen_role_ids = set()
            for ref in split_role_references(roles):
                if ref.isdigit():
                    role = guild.get_role(int(ref))
                else:
                    role = next(
                        (candidate for candidate in guild.roles
                         if candidate.name.casefold() == ref.casefold()),
                        None,
                    )

                if role is None:
                    invalid.append(ref)
                    continue
                if role.id in seen_role_ids:
                    continue
                seen_role_ids.add(role.id)

                if role.is_default():
                    unavailable.append(f"{role.name} (Standardrolle)")
                elif role.managed:
                    unavailable.append(f"{role.name} (verwaltete Rolle)")
                elif role >= bot_member.top_role:
                    unavailable.append(f"{role.name} (Bot-Rolle muss darüber stehen)")
                else:
                    role_objects.append(role)

            if not role_objects:
                reasons = []
                if unavailable:
                    reasons.append("Nicht zuweisbar: " + ", ".join(unavailable))
                if invalid:
                    reasons.append("Nicht gefunden: " + ", ".join(invalid))
                if not reasons:
                    reasons.append("Keine Rollenangaben erkannt.")
                return await interaction.followup.send(
                    "❌ Keine gültigen Rollen gefunden.\n"
                    + "\n".join(reasons)
                    + "\nErwähne Rollen, füge Rollen-IDs ein oder trenne exakte Rollennamen mit Kommas.",
                    ephemeral=True
                )

            too_many = len(role_objects) > 25
            role_objects = role_objects[:25]
            if too_many:
                unavailable.append("Weitere Rollen ausgelassen (Discord erlaubt höchstens 25 Optionen).")

            # Embed-Farbe parsen
            try:
                embed_color = int(color.strip("#"), 16)
            except:
                embed_color = 0x3498db

            # Embed erstellen
            embed = discord.Embed(
                title=title[:256],
                description=description[:4096],
                color=embed_color
            )

            embed.add_field(
                name="Verfügbare Rollen",
                value="\n".join(f"• {r.mention}" for r in role_objects)[:1024],
                inline=False
            )

            embed.set_footer(text=footer[:2048])
            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)

            # View erstellen
            menu_id = f"{channel.id}-{interaction.id}"
            view = self.RoleView(role_objects, menu_id)
            # Nachricht senden und speichern
            message = await channel.send(embed=embed, view=view)

            self.persistent_views[menu_id] = {
                "channel_id": channel.id,
                "message_id": message.id,
                "role_ids": [r.id for r in role_objects],
                "embed_data": {
                    "title": title,
                    "description": description,
                    "color": color,
                    "footer": footer,
                    "thumbnail_url": thumbnail_url
                }
            }

            self.save_menus()

            ignored = invalid + unavailable
            ignored_text = f"Ignoriert: {', '.join(ignored)}" if ignored else ""
            await interaction.followup.send(
                f"✅ Menü in {channel.mention} erstellt!\n{ignored_text}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Kritischer Fehler: {type(e).__name__}\n{str(e)}",
                ephemeral=True
            )

    @create_role_menu.error
    async def create_role_menu_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            message = "Du brauchst die Berechtigung „Rollen verwalten“, um ein Rollen-Menü zu erstellen."
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)

    async def restore_menus(self):
        """Stellt alle Menüs nach Neustart wieder her"""
        for menu_id, data in list(self.persistent_views.items()):
            try:
                channel = self.bot.get_channel(data["channel_id"])
                if not channel:
                    continue

                roles = []
                for role_id in data["role_ids"]:
                    if role := channel.guild.get_role(role_id):
                        if role.is_assignable():
                            roles.append(role)

                if not roles:
                    print(
                        f"Rollenmenü {menu_id} bleibt gespeichert, weil aktuell keine der Rollen "
                        "durch die Bot-Rollenhierarchie zuweisbar ist."
                    )
                    continue

                embed_data = data.get("embed_data", {})
                embed = discord.Embed(
                    title=embed_data.get("title", "🔔 Rollen-Verwaltung")[:256],
                    description=embed_data.get("description", "Wiederhergestelltes Menü")[:4096],
                    color=int(embed_data.get("color", "3498db").strip("#"), 16) if embed_data.get("color") else 0x3498db
                )

                embed.add_field(
                    name="Verfügbare Rollen",
                    value="\n".join(f"• {r.mention}" for r in roles)[:1024],
                    inline=False
                )

                embed.set_footer(text=embed_data.get("footer", "Wiederhergestellt")[:2048])
                if thumbnail_url := embed_data.get("thumbnail_url"):
                    embed.set_thumbnail(url=thumbnail_url)

                view = self.RoleView(roles, menu_id)

                try:
                    message = await channel.fetch_message(data["message_id"])
                    if message.id not in self._restored_messages:
                        self.bot.add_view(view, message_id=message.id)
                        self._restored_messages.add(message.id)
                    await message.edit(embed=embed, view=view)
                except discord.NotFound:
                    del self.persistent_views[menu_id]
                    self.save_menus()
                except Exception as e:
                    print(f"Fehler beim Bearbeiten der Nachricht {menu_id}: {e}")

            except Exception as e:
                print(f"Fehler beim Wiederherstellen von Menü {menu_id}: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.restore_menus()

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleMenu(bot))