import os

import discord
from discord.ext import commands

import questions_core.bot_helper as bh
import questions_core.questions as q
import questions_core.util as util


""" The file that the api token is stored in. """
TOKEN_FILE = str(util.get_project_root() / "data/discord_token.txt")
MEME_FILE = str(util.get_project_root() / "data/balloon_ritchie.jpg")
DISCORD_VAR = 'DISCORDTOKEN'


def create_bot():
    # bot = commands.Bot(command_prefix=commands.when_mentioned)
    bot = commands.Bot(command_prefix='.')
    rqg = bh.RandomQuestionGenerator(q.QuestionsList())     # lol closures

    @bot.command()
    async def ask(ctx):
        await ctx.send(rqg.random_question())

    @bot.command()
    async def mascot(ctx):
        await ctx.send(file=discord.File(MEME_FILE))

    print("Bot created.")
    return bot


if __name__ == '__main__':
    bot = create_bot()
    try:
        with open(TOKEN_FILE) as fd:
            token = fd.read()
    except FileNotFoundError:
        token = os.environ[DISCORD_VAR]
    print("Bot ready.")
    bot.run(token)
