import discord


def color_to_string(color: discord.Color) -> str:
    return "".join(hex(n)[2:] for n in color.to_rgb())


def hex_color_to_string(color: int) -> str:
    return hex(color)[2:].rjust(6, "0")