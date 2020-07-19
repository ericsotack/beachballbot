import discord
from discord.ext import commands

import questions_core.bot_helper as bh
import questions_core.questions as q
import questions_core.util as util


""" The file that the api token is stored in. """
TOKEN_FILE = str(util.get_project_root() / "data/discord_token.txt")
MEME_FILE = str(util.get_project_root() / "data/balloon_ritchie.jpg")


def create_bot():
    bot = commands.Bot(command_prefix=commands.when_mentioned)
    rqg = bh.RandomQuestionGenerator(q.QuestionsList())     # lol closures

    @bot.command()
    async def ask(ctx):
        await ctx.send(rqg.random_question())

    @bot.command()
    async def mascot(ctx):
        await ctx.send(file=discord.File(MEME_FILE))

    return bot


if __name__ == '__main__':
    bot = create_bot()
    with open(TOKEN_FILE) as fd:
        token = fd.read()
    bot.run(token)
