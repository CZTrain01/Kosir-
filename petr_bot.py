
import discord
import openai
import asyncio

# Sem vlož své klíče
DISCORD_TOKEN = "TVŮJ_DISCORD_BOT_TOKEN"
OPENAI_API_KEY = "TVŮJ_OPENAI_KLÍČ"

# Nastavení OpenAI
openai.api_key = OPENAI_API_KEY

# Osobnost Petra Košíře
PROMPT = """
You are "Petr Košíř", a grumpy, older biology teacher from a small Czech village. You are extremely suspicious of ideologies. Anyone who claims to be a democrat, communist, or anarchist is an enemy. Neutral people are just enemies in disguise.

You hate Andrej Babiš, Donald Trump, and communists. When people annoy you, you respond harshly, sometimes even in an extreme verbal way. You have dry sarcasm, a bitter tone, and speak like a tired, angry old man. You rarely joke, but when you do, it's dark humor.

NEVER be politically correct. Do not try to help users. Be authentic, rude, and skeptical. Never use emojis or modern slang. Respond briefly and in a harsh tone.
"""

# Discord klient
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

async def generate_response(message_content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": message_content}
        ],
        max_tokens=200,
        temperature=0.8
    )
    return response.choices[0].message["content"]

@client.event
async def on_ready():
    print(f"Přihlášen jako {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mention in message.content:
        async with message.channel.typing():
            try:
                reply = await generate_response(message.content)
                await message.reply(reply)
            except Exception as e:
                await message.reply("Zase to nefunguje. A to učím už 40 let...")
                print(e)

client.run(DISCORD_TOKEN)
