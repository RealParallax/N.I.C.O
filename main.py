import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI and Discord clients
client = OpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name}")


# 1. /ask command to speak directly with the AI
@bot.tree.command(name="ask", description="Speak directly to the AI assistant")
async def ask(interaction: discord.Interaction, prompt: str):
  await interaction.response.defer()  # Acknowledge command while AI generates response

  try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": (
                "You are a helpful assistant integrated into a Discord server."
            ),
        }, {"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    await interaction.followup.send(f"**Q: {prompt}**\n{answer}")
  except Exception as e:
    await interaction.followup.send(
        "Sorry, something went wrong while reaching the AI."
    )


# Sync slash commands when the bot starts
@bot.event
async def setup_hook():
  await bot.tree.sync()


bot.run(DISCORD_TOKEN)
