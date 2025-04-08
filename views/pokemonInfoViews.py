import discord

min_max_text = "Min and Max values are calculated for level 100 with hindering/beneficial nature, 0 IVs, and 0 EVs (Min) or 31 IVs and 252 EVs (Max)."

class InfoView(discord.ui.View):
    def __init__(self, pokemon, file=None, user_id=None):
        super().__init__(timeout=300)
        self.pokemon = pokemon
        self.file = file
        self.embed = self.build_info_embed()
        self.user_id = user_id

    def build_info_embed(self):
        p = self.pokemon
        embed = discord.Embed(
            title=f"#{p['id']} - {p['name']}",
            url=f"https://pokemondb.net/pokedex/{p['base_id']}",
            color=discord.Color.red(),
        )
        embed.add_field(name="Generation", value=f"Gen {p['generation']}", inline=True)
        embed.add_field(name="Types", value=", ".join(p["types"]), inline=True)
        embed.add_field(name="Height", value=f"{p['height']} m", inline=True)
        embed.add_field(name="Weight", value=f"{p['weight']} kg", inline=True)
        embed.add_field(name="Abilities", value=", ".join(p["abilities"]), inline=True)

        if p["hidden_abilities"]:
            embed.add_field(name="Hidden Abilities", value=", ".join(p["hidden_abilities"]), inline=True)

        if p["varieties"]:
            embed.add_field(name="Varieties", value=", ".join(p["varieties"][:10]) + "...", inline=False)

        embed.add_field(name="Moves (Sample)", value=", ".join(p["moves"][:10]) + "...", inline=False)

        if self.file:
            embed.set_image(url="attachment://sprite.png")

        embed.add_field(name="More Info", value=f"[Pokemon Database](https://pokemondb.net/pokedex/{p['base_id']})", inline=False)

        return embed

    def build_stats_embed(self):
        p = self.pokemon
        embed = discord.Embed(
            title=f"#{p['id']} - {p['name']} - Base Stats",
            color=discord.Color.red(),
        )

        stats_text = ""
        for stat_name, stat_data in p["stats"].items():
            stats_text += (
                f"**{stat_name.replace('-', ' ').title()}** - "
                f"{stat_data['value']}\n"
                f"{stat_data['bar']}\n"
                f"**Min/Max:** {stat_data['min-100']}/{stat_data['max-100']}\n\n"
            )

        embed.add_field(name="", value=stats_text, inline=False)
        embed.add_field(name="", value=f"*{min_max_text}*", inline=False)

        if self.file:
            embed.set_image(url="attachment://sprite.png")

        return embed
    
    @discord.ui.button(label="Show Info", style=discord.ButtonStyle.primary)
    async def show_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This button is not for you!", ephemeral=True)
            return
        else:
            await interaction.response.edit_message(embed=self.build_info_embed(), view=self)

    @discord.ui.button(label="Show Stats", style=discord.ButtonStyle.primary)
    async def show_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This button is not for you!", ephemeral=True)
            return
        else:
            await interaction.response.edit_message(embed=self.build_stats_embed(), view=self)