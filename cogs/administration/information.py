from typing import List

import discord
from discord.ext import commands

import aoi
from utils import conversions


class Information(commands.Cog):
    def __init__(self, bot: aoi.AoiBot):
        self.bot = bot

    @commands.command(brief="Shows info on a user", aliases=["uinfo"])
    async def userinfo(self, ctx: aoi.AoiContext, member: discord.Member = None):
        if not member:
            member = ctx.author
        joined_at = member.joined_at.strftime("%c")
        created_at = member.created_at.strftime("%c")
        r: discord.Role
        hoisted_roles = [r for r in member.roles if r.hoist]
        normal_roles = member.roles
        await ctx.embed(
            title=f"Info for {member}",
            fields=[
                ("ID", member.id),
                ("Joined Server", joined_at),
                ("Joined Discord", created_at),
                (f"Hoisted Roles ({len(hoisted_roles)}) ",
                 " ".join([r.mention for r in hoisted_roles[0:5]]) if hoisted_roles
                 else "None"),
                (f"Normal Roles ({len(normal_roles) - 1})",
                 " ".join([r.mention for r in normal_roles[1:5] if r.id not in
                           [x.id for x in hoisted_roles]]) if len(normal_roles) > 1
                 else "None"),
                ("Top Role", member.roles[-1].mention),
                ("Ansura Profile", f"https://www.ansura.xyz/profile/{member.id}")
            ],
            clr=member.color,
            thumbnail=member.avatar_url
        )

    @commands.command(brief="Shows info on the current server", aliases=["sinfo"])
    async def serverinfo(self, ctx: aoi.AoiContext):
        guild: discord.Guild = ctx.guild
        created = guild.created_at.strftime("%c")
        voice_channels = len(guild.voice_channels)
        text_channels = len(guild.text_channels)
        roles = len(guild.roles) - 1
        statuses = {
            "dnd": 0,
            "idle": 0,
            "online": 0,
            "bot": 0,
            "offline": 0
        }
        m: discord.Member
        for m in guild.members:
            if m.bot:
                statuses["bot"] += 1
            else:
                statuses[str(m.status)] += 1
        await ctx.embed(
            title=f"Info for {guild}",
            fields=[
                ("ID", guild.id),
                ("Created at", created),
                ("Channels", f"{voice_channels} Voice, {text_channels} Text"),
                ("System Channel", (guild.system_channel.mention if guild.system_channel else "None")),
                ("Members", guild.member_count),
                ("Roles", roles),
                ("Region", guild.region),
                ("Features", "\n".join(guild.features) if guild.features else "None"),
                ("Breakdown", f":green_circle: {statuses['online']} online\n"
                              f":yellow_circle: {statuses['idle']} idle\n"
                              f":red_circle: {statuses['dnd']} dnd\n"
                              f":white_circle: {statuses['offline']} offline\n"
                              f":robot: {statuses['bot']} bots\n")
            ],
            thumbnail=guild.icon_url
        )

    @commands.command(brief="Shows info on a role", aliases=["rinfo"])
    async def roleinfo(self, ctx: aoi.AoiContext, role: discord.Role):
        await ctx.embed(
            clr=role.colour,
            title=f"Info for {role}",
            fields=[
                ("ID", role.id),
                ("Members", len(role.members)),
                ("Color", conversions.color_to_string(role.colour)),
                ("Hoisted", role.hoist),
                ("Mentionable", role.mentionable),
                ("Position", role.position),
                ("Created at", role.created_at.strftime("%c"))
            ]
        )

    @commands.has_permissions(manage_guild=True)
    @commands.command(brief="Shows mentionable roles")
    async def menroles(self, ctx: aoi.AoiContext):
        r: discord.Role
        roles: List[discord.Role] = [r for r in ctx.guild.roles if r.mentionable]
        await ctx.send_info(" ".join(r.mention for r in roles)
                            if roles else "None", title="Mentionable Roles")


def setup(bot: aoi.AoiBot) -> None:
    bot.add_cog(Information(bot))
