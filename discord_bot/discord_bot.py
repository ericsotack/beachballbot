import os

import discord
from discord.ext import commands

import questions_core.bot_helper as bh
import questions_core.questions as q
import questions_core.util as util


""" The file that the api token is stored in. """
TOKEN_FILE = str(util.get_project_root() / "data/discord_token.txt")

""" Environment variable key that the token is stored in """
DISCORD_VAR = 'DISCORDTOKEN'

""" The file that the funny mascot photo is stored in """
MEME_FILE = str(util.get_project_root() / "data/balloon_ritchie.jpg")


def create_bot():
    """
    Creates the bot so it will respond to commands prefixed with a period.
    Commands available: .ask and .mascot
    :return: The discord bot.
    """
    # bot = commands.Bot(command_prefix=commands.when_mentioned)
    bot = commands.Bot(command_prefix='.')
    rqg = bh.RandomQuestionGenerator(q.QuestionsList())     # lol closures

    @bot.command()
    async def ask(ctx):
        """
        Command to get and send back a question from the database of questions.
        :param ctx:
        :return: n/a
        """
        await ctx.send(rqg.random_question())

    @bot.command()
    async def mascot(ctx):
        """
        Command to send back the funny mascot photo.
        :param ctx: Context for the message
        :return: n/a
        """
        await ctx.send(file=discord.File(MEME_FILE))

    print("Bot created.")
    return bot


# run the bot
if __name__ == '__main__':
    bot = create_bot()
    try:
        with open(TOKEN_FILE) as fd:
            token = fd.read()
    except FileNotFoundError:
        token = os.environ[DISCORD_VAR]
    print("Bot ready.")
    bot.run(token)
