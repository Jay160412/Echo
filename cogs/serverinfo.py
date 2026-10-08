import discord

from discord.ext import commands

from discord import app_commands

import datetime

from typing import Optional

# Versuche humanize zu importieren (optional)

try:

    import humanize

    HAS_HUMANIZE = True

except ImportError:

    HAS_HUMANIZE = False

class ServerInfo(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(name="serverinfo", description="Zeigt detaillierte Serverinformationen an")

    async def serverinfo(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None:
            return await interaction.response.send_message(
                "Dieser Befehl funktioniert nur auf einem Server.",
                ephemeral=True,
            )

        

        # Embed erstellen

        embed = discord.Embed(

            title=f"📊 Server-Info: {guild.name}",

            color=guild.owner.color if guild.owner else discord.Color.blurple()

        )

        # Server Icon (Thumbnail)

        if guild.icon:

            embed.set_thumbnail(url=guild.icon.url)

        # Server Banner (Image)

        if guild.banner:

            embed.set_image(url=guild.banner.url)

        # Erstellungsdatum

        created = guild.created_at

        if HAS_HUMANIZE:

            created_str = f"{created.strftime('%d.%m.%Y %H:%M')}\n({humanize.naturaltime(created)})"

        else:

            days = (discord.utils.utcnow() - created).days

            created_str = f"{created.strftime('%d.%m.%Y %H:%M')}\n(vor {days} Tagen)"

        # Besitzer

        owner = guild.owner

        owner_mention = owner.mention if owner else f"<@{guild.owner_id}>"

        owner_name = str(owner) if owner else "Serverbesitzer"

        # Basis-Informationen

        embed.add_field(

            name="👑 Besitzer",

            value=f"{owner_mention}\n`{owner_name}`",

            inline=True

        )

        embed.add_field(

            name="🆔 Server-ID",

            value=f"`{guild.id}`",

            inline=True

        )

        embed.add_field(

            name="📅 Erstellt",

            value=created_str,

            inline=False

        )

        # Mitglieder

        total_members = guild.member_count if guild.member_count is not None else len(guild.members)

        humans = sum(not member.bot for member in guild.members)

        bots = max(0, total_members - humans)

        online = (
            sum(
                member.status not in (discord.Status.offline, discord.Status.invisible)
                for member in guild.members
            )
            if self.bot.intents.presences
            else None
        )

        embed.add_field(

            name="👥 Mitglieder",

            value=(
                f"**Insgesamt:** {total_members}\n👤 Menschen: {humans}\n🤖 Bots: {bots}"
                + (f"\n🟢 Online: {online}" if online is not None else "")
            ),

            inline=True

        )

        # Kanäle

        text_channels = len(guild.text_channels)

        voice_channels = len(guild.voice_channels)

        categories = len(guild.categories)

        embed.add_field(

            name="💬 Kanäle",

            value=f"📝 Text: {text_channels}\n🔊 Sprach: {voice_channels}\n📁 Kategorien: {categories}",

            inline=True

        )

        # Rollen

        roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)

        role_count = len(roles)

        highest_role = roles[0].mention if roles else "Keine"

        embed.add_field(

            name="🎭 Rollen",

            value=f"**Anzahl:** {role_count}\n**Höchste:** {highest_role}",

            inline=True

        )

        # Boosts

        if (guild.premium_subscription_count or 0) > 0:

            boost_count = guild.premium_subscription_count or 0

            boost_level = guild.premium_tier

            embed.add_field(

                name="💎 Boosts",

                value=f"**Level:** {boost_level}\n**Anzahl:** {boost_count}\n**Booster:** {len(guild.premium_subscribers)}",

                inline=True

            )

        # Sicherheitseinstellungen

        verification_levels = {

            discord.VerificationLevel.none: "❌ Keine",

            discord.VerificationLevel.low: "📧 E-Mail bestätigt",

            discord.VerificationLevel.medium: "🕒 5 Minuten im Server",

            discord.VerificationLevel.high: "📱 Handy bestätigt",

            discord.VerificationLevel.highest: "🔒 Höchste (Handy + 5 Min)"

        }

        explicit_filter = {

            discord.ContentFilter.disabled: "❌ Deaktiviert",

            discord.ContentFilter.no_role: "👥 Nur Mitglieder ohne Rolle",

            discord.ContentFilter.all_members: "🔞 Alle Mitglieder"

        }

        embed.add_field(

            name="🔒 Sicherheit",

            value=f"**Verifikation:** {verification_levels.get(guild.verification_level, 'Unbekannt')}\n"

                  f"**Filter:** {explicit_filter.get(guild.explicit_content_filter, 'Unbekannt')}",

            inline=False

        )

        # Features (Server-Funktionen)

        if guild.features:

            feature_map = {

                "ANIMATED_ICON": "🎨 Animiertes Icon",

                "BANNER": "🏞️ Banner",

                "COMMUNITY": "👥 Community",

                "DISCOVERABLE": "🔍 Entdeckbar",

                "INVITE_SPLASH": "💧 Einladungs-Splash",

                "MEMBER_VERIFICATION_GATE_ENABLED": "🛡️ Mitgliederverifikation",

                "NEWS": "📰 Nachrichtenkanäle",

                "PARTNERED": "⭐ Partner",

                "PREVIEW_ENABLED": "👁️ Vorschau",

                "ROLE_ICONS": "🎭 Rollenicons",

                "SEVEN_DAY_THREAD_ARCHIVE": "📌 7-Tage-Thread-Archiv",

                "THREE_DAY_THREAD_ARCHIVE": "📌 3-Tage-Thread-Archiv",

                "VANITY_URL": "🔗 Vanity-URL",

                "VERIFIED": "✅ Verifiziert",

                "VIP_REGIONS": "🌟 VIP-Sprachkanäle",

                "WELCOME_SCREEN_ENABLED": "👋 Willkommensbildschirm"

            }

            features = [feature_map.get(f, f.replace("_", " ").title()) for f in guild.features if f in feature_map]

            if features:

                embed.add_field(

                    name="🌟 Server-Features",

                    value=", ".join(features[:10]) + (" …" if len(features) > 10 else ""),

                    inline=False

                )

        # Footer

        embed.set_footer(

            text=f"Angefordert von {interaction.user.display_name} • {len(guild.members)} Mitglieder",

            icon_url=interaction.user.display_avatar.url

        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):

    await bot.add_cog(ServerInfo(bot))