import random
from discord.ext import commands


class Games:
    """Some fun games."""

    __slots__ = 'bot'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rps(self, ctx, choice: str):
        """Play rock paper scissors."""
        choice = choice.lower()
        options = [
            "rock",
            "paper",
            "scissors",
        ]
        if choice not in options:
            await ctx.channel.send("Please choose from: rock, paper, scissors")
            return
        bot_choice = random.choice(options)

        if choice == bot_choice:
            message = "Tie!"
        elif choice == "rock":
            if bot_choice == "Paper":
                message = f"You lose!{bot_choice} covers {choice}"
            else:
                message = f"You win! {choice} smashes {bot_choice}"
        elif choice == "paper":
            if bot_choice == "Scissors":
                message = f"You lose! {bot_choice} cut {choice}"
            else:
                message = f"You win! {choice} covers {bot_choice}"
        elif choice == "scissors":
            if bot_choice == "Rock":
                message = f"You lose... {bot_choice} smashes {choice}"
            else:
                message = f"You win! {choice} cut {bot_choice}"
        else:
            message = "Oops something went wrong"

        await ctx.channel.send(message)


def setup(bot):
    bot.add_cog(Games(bot))
