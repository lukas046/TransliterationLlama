# This example requires the 'message_content' intent.

import discord
import emojify
import generateImage
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
global right_answer


@client.event
async def on_ready():
    global right_answer
    right_answer = ""
    print(f'We have logged in as {client.user}')

prefix = '$'

playwords = ["play", "start", "game"]
drawwords = ["draw"]
leaderwords = ["leaderboard"]


@client.event
async def on_message(message):
    global right_answer
    global attemptNum
    global emojiSave
    global leaderBoard
    if message.author == client.user:
        return
    
    if message.content.startswith("$help"):
      await message.channel.send('Commands: \n  `$play` \n   `$draw {prompt}`')

    if message.content.startswith(prefix):
        message.content = message.content[len(prefix):]
        arguments = message.content.split(" ")
        prompt = arguments
        if arguments[0] in playwords:
            await message.channel.send('Starting game!')
            right_answer = emojify.parseJSON(
                emojify.generatePhrase(), 0).lower().strip(".?,<>!@#$%^&*()")
            emojiSave = emojify.parseJSON(emojify.emojiTrans(
                right_answer), 1)
            await message.channel.send(
                f"Guess the phrase from the given emojis: {emojiSave}")
            attemptNum = 0
            # Setup leaderboard if it dosnt exist
            try:
                leaderBoard
            except NameError:
                leaderBoard = {}

        elif prompt[0] in drawwords:
            if len(prompt) == 1:
                await message.channel.send('please enter an image to be drawn')
            else:
                await message.channel.send('Drawing')
                msg = message.content[len(prompt[0]):].strip(" ")
                generateImage.generateImage(msg)
                await message.channel.send(file=discord.File("1.png"))
        elif prompt[0] in leaderwords:
            try:
                leaderBoard
            except NameError:
                await message.channel.send('No winners have been recorded yet!')
            else:
                await message.channel.send('Current Leaderboard:')
                for key, val in leaderBoard.items():
                    await message.channel.send(f"   <@{key}>: {val}")
    else:
        try:
            right_answer
        except NameError:
            print()
        else:
            if right_answer != "":
                if message.content.lower().strip() == right_answer.strip():
                    await message.channel.send('Correct')
                    right_answer = ""
                    attemptNum = -1
                    # Get username of user that guessed it correct
                    # winnerName = f"{message.author.name}#{message.author.discriminator}"
                    winnerName = message.author.id
                    if winnerName in leaderBoard:
                        leaderBoard.update(
                            {winnerName: leaderBoard[winnerName]})
                    else:
                        leaderBoard.update({winnerName: 1})

                elif attemptNum == 5:
                    await message.channel.send(f"You ran out of guesses! The correct answer was: {right_answer.strip()}")
                    right_answer = ""
                    attemptNum = -1
                else:
                    await message.channel.send('Wrong')
                    # Generate a hint?
                    tmpHint = emojify.parseJSON(
                        emojify.generateHint(right_answer), 0).strip("!").strip()
                    await message.channel.send(f"Emojis: {emojiSave}")
                    await message.channel.send(f"Hint: {tmpHint}")
                    attemptNum += 1


with open('token.txt') as f:
    lines = f.readlines()

TOKEN = lines[0].strip()
client.run(TOKEN)
