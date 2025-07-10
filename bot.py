import discord
import json
import asyncio
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from db import init_db, update_score, get_leaderboard, reset_leaderboard

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Load questions from JSON
with open("quiz_data.json", encoding="utf-8") as f:
    quiz_data = json.load(f)

init_db()

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user} ({bot.user.id})")

# Slash command: /kuis
@tree.command(name="kuis", description="Mulai kuis bertema anime")
async def start_quiz(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(
        title="🎮 Anime Quiz Started!",
        description=f"**Started by:** {interaction.user.mention}\n**Questions:** {len(quiz_data)}\n**Time per question:** 20 seconds",
        color=discord.Color.purple()
    ))
    
    for i, q in enumerate(quiz_data):
        await send_question(interaction.channel, i + 1, q)

    await show_leaderboard(interaction.channel)

# Slash command: /leaderboard
@tree.command(name="leaderboard", description="Lihat leaderboard kuis")
async def leaderboard_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    await show_leaderboard(interaction.channel)

# Slash command: /reset
@tree.command(name="reset", description="Reset leaderboard (admin only)")
async def reset_lb(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Kamu bukan admin.", ephemeral=True)
        return
    reset_leaderboard()
    await interaction.response.send_message("✅ Leaderboard berhasil di-reset.")

# Mengirim soal ke channel
async def send_question(channel, qnum, question_data):
    question = question_data["question"]
    choices = question_data["choices"]
    correct = question_data["answer"]

    view = discord.ui.View(timeout=20)
    answered_users = {}

    for i, choice in enumerate(choices):
        label = chr(65 + i)  # A, B, C, D

        async def callback(interaction: discord.Interaction, i=i):
            uid = str(interaction.user.id)
            if uid in answered_users:
                await interaction.response.send_message("Kamu sudah menjawab!", ephemeral=True)
                return
            answered_users[uid] = i
            username = interaction.user.display_name
            if i == correct:
                update_score(uid, username, 900)
            await interaction.response.defer()

        button = discord.ui.Button(label=f"{label}. {choice}", style=discord.ButtonStyle.primary)
        button.callback = callback
        view.add_item(button)

    embed = discord.Embed(
        title=f"❓ Question {qnum}",
        description=question,
        color=discord.Color.blue()
    )
    for i, choice in enumerate(choices):
        embed.add_field(name=f"{chr(65+i)}", value=choice, inline=False)

    await channel.send(embed=embed, view=view)
    await asyncio.sleep(20)

    # Hasil jawaban
    result_embed = discord.Embed(title="🕓 Time's Up!", color=discord.Color.gold())
    for i, choice in enumerate(choices):
        status = "✅" if i == correct else "❌"
        result_embed.add_field(name=f"{status} {chr(65+i)}", value=choice, inline=False)

    await channel.send(embed=result_embed)

# Menampilkan leaderboard
async def show_leaderboard(channel):
    scores = get_leaderboard()
    if not scores:
        await channel.send("📭 Belum ada peserta di leaderboard.")
        return

    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.green())
    for i, (username, score) in enumerate(scores, 1):
        embed.add_field(name=f"#{i}. {username}", value=f"{score} points", inline=False)
    await channel.send(embed=embed)

bot.run(TOKEN)
