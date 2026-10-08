import discord

from discord import app_commands

from discord.ext import commands

import aiohttp

class AnimeCommands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.API_URL = "https://graphql.anilist.co"

        self.QUERY = """
            query ($search: String!) {
                Media(search: $search, type: ANIME) {
                    title { english romaji }
                    siteUrl
                    coverImage { extraLarge large }
                    format
                    status
                    episodes
                    averageScore
                    startDate { year }
                    description(asHtml: false)
                }
            }
        """

    @app_commands.command(name="anime", description="🔍 Get anime info with cover image")

    async def anime_search(self, interaction: discord.Interaction, name: str):

        """Simple anime search with English description only"""

        try:

            name = name.strip()

            if not name:
                return await interaction.response.send_message(
                    "Gib bitte einen Anime-Namen ein.",
                    ephemeral=True,
                )

            await interaction.response.defer(thinking=True)

            

            timeout = aiohttp.ClientTimeout(total=12, connect=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    self.API_URL,
                    json={"query": self.QUERY, "variables": {"search": name}},
                    headers={"Accept": "application/json"},
                ) as response:
                    if response.status == 429:
                        return await interaction.followup.send(
                            "Die Anime-Suche ist gerade ausgelastet. Bitte versuche es gleich erneut.",
                            ephemeral=True,
                        )

                    if response.status != 200:
                        return await interaction.followup.send(
                            "Die Anime-Datenbank ist gerade nicht erreichbar. Bitte versuche es später erneut.",
                            ephemeral=True,
                        )

                    data = await response.json()
                    if data.get("errors"):
                        raise RuntimeError("AniList returned a GraphQL error")

                    anime = (data.get("data") or {}).get("Media")
                    if not anime:
                        return await interaction.followup.send(
                            f"🔍 Keine Ergebnisse für „{discord.utils.escape_markdown(name)}“ gefunden."
                        )

                    

                    # Create embed

                    title = anime.get("title") or {}
                    title_text = title.get("english") or title.get("romaji") or name
                    embed = discord.Embed(
                        title=f"🎌 {title_text[:250]}",
                        url=anime.get("siteUrl"),
                        color=0x2e51a2,
                    )

                    

                    # Add cover image

                    cover = anime.get("coverImage") or {}
                    cover_url = cover.get("extraLarge") or cover.get("large")
                    if cover_url:
                        embed.set_image(url=cover_url)

                    

                    # Add metadata

                    anime_format = (anime.get("format") or "N/A").replace("_", " ")
                    status = (anime.get("status") or "N/A").replace("_", " ").title()
                    score = anime.get("averageScore")
                    year = (anime.get("startDate") or {}).get("year") or "N/A"
                    embed.add_field(
                        name="📊 Info",
                        value=(
                            f"**Format:** {anime_format}\n"
                            f"**Status:** {status}\n"
                            f"**Score:** ⭐ {f'{score}/100' if score is not None else 'N/A'}\n"
                            f"**Episodes:** {anime.get('episodes') or 'N/A'}\n"
                            f"**Year:** {year}"
                        ),
                        inline=False,
                    )

                    

                    # Add English description

                    description = (anime.get("description") or "Keine Beschreibung verfügbar.")
                    description = description.replace("```", "'''").strip()
                    description = discord.utils.escape_mentions(description)

                    embed.add_field(

                        name="📝 Description",

                        value=description[:1000] + ("…" if len(description) > 1000 else ""),

                        inline=False

                    )

                    

                    await interaction.followup.send(embed=embed)

                    

        except Exception as e:

            error_message = "❌ Die Anime-Suche ist fehlgeschlagen. Bitte versuche es später erneut."
            if interaction.response.is_done():
                await interaction.followup.send(error_message, ephemeral=True)
            else:
                await interaction.response.send_message(error_message, ephemeral=True)

            print(f"[Anime Error] {type(e).__name__}: {e}")

async def setup(bot):

    await bot.add_cog(AnimeCommands(bot))