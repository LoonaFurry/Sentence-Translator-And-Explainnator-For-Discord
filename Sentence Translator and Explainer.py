import discord
import requests
import asyncio
from discord.ext import commands
import random

# Discord Bot Token
TOKEN = 'your-discord-token-here'

# Define intents
intents = discord.Intents.all()
intents.messages = True  # Enable message events

# Gemini API endpoint
GEMINI_API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

# Your Gemini API key
GEMINI_API_KEY = 'your-gemini-api-key'

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Generate a response using the Gemini API
    response = await generate_response(message.content)

    # Send the response to the channel
    await message.channel.send(f"{message.author.mention}, {response}")

async def generate_response(prompt):
    # Prepend the desired text to the user's input
    prompt = "translate this sentence and explain in turkish input " + prompt

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    try:
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, params={'key': GEMINI_API_KEY}))
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                print("API Response:", data)
        else:
            print("API Error:", response.text)
    except Exception as e:
        print("API Exception:", e)
    return "I'm sorry, I couldn't generate a response."

if __name__ == "__main__":
    bot.run(TOKEN)