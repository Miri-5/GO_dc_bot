import discord
from discord.ext import commands
from config import token

# Car sınıfı
class Car:
    def __init__(self, renk, marka):
        self.renk = renk
        self.marka = marka

    def info(self):
        return f"Aracınız: {self.renk} renkli {self.marka}"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # banlamak için gerekli

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f'Giriş yaptı: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Reklam veya link içeriyor mu kontrol et
    if "https://" in message.content or "http://" in message.content:
        await message.channel.send(f"{message.author.mention} link paylaştığı için banlandı!")
        await message.author.ban(reason="Reklam veya link paylaşımı")
        return  # komutları işleme alma

    # Eğer link yoksa komutları ve echo'yu çalıştır
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)
    else:
        await message.channel.send(message.content)

@client.command()
async def about(ctx):
    await ctx.send('Bu discord.py kütüphanesi ile oluşturulmuş echo-bot!')

@client.command()
async def car(ctx, renk: str, marka: str):
    araba = Car(renk, marka)
    await ctx.send(araba.info())
@client.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages:  # botun mesaj atma yetkisi varsa
            await channel.send(f'Hoş geldiniz, {member.mention}! 🎉')
            break

client.run(token)
