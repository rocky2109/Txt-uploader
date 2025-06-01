# 🚀 Full Upgraded helper.py with Enhanced Features
# 🔒 Smart m3u8 downloader + AES decryption + Telegram upload + PDF watermarking + more!
# All previous logic remains the same...

# >>> Injected New Function <<<
import os
import subprocess
import mmap
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import logging
import datetime
import asyncio
import requests
import time
from p_bar import progress_bar
import aiohttp
import aiofiles
import tgcrypto
import concurrent.futures
from pyrogram.types import Message
from pyrogram import Client
from pathlib import Path
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

KEY = b'^#^#&@*HDU@&@*()'
IV = b'^@%#&*NSHUE&$*#)'

EMOJIS = ["🔥", "💥", "👨‍❤️‍💋‍👨", "👱🏻", "👻", "⚡", "💫", "🐟", "🦅", "🌹", "🦋"]
emoji_counter = 0

def get_next_emoji():
    global emoji_counter
    emoji = EMOJIS[emoji_counter]
    emoji_counter = (emoji_counter + 1) % len(EMOJIS)
    return emoji

def dec_url(enc_url):
    enc_url = enc_url.replace("helper://", "")
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(b64decode(enc_url)), AES.block_size)
    return decrypted.decode('utf-8')

def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date}_{current_time}.mp4"

def decrypt_file(file_path, key):
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r+b") as f:
        num_bytes = min(28, os.path.getsize(file_path))
        with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
            for i in range(num_bytes):
                mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
    return True

async def handle_m3u8_download_and_upload(bot: Client, m: Message, url: str, key: str = None):
    name = time_name().replace(' ', '_').replace(':', '-')
    temp_path = f"{name}.mp4"
    emoji = get_next_emoji()
    status = await m.reply_text(f"{emoji} 𝗦𝘁𝗮𝗿𝘁𝗶𝗻𝗴 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗳𝗼𝗿:\n`{url}`")

    try:
        cmd = ["yt-dlp", "--no-check-certificate", "--allow-unplayable-formats", "-N", "8", "-o", temp_path, url]
        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            await status.edit(f"❌ Download failed:\n```{stderr.decode()}```")
            return

        if key:
            await status.edit("🔐 Decrypting video...")
            success = decrypt_file(temp_path, key)
            if not success:
                await status.edit("❌ Decryption failed.")
                return

        await status.edit("📤 Uploading to Telegram...")
        await send_vid(bot, m, cc=f"Downloaded from link:\n{url}", filename=temp_path, thumb="no", name=name, prog=status)

    except Exception as e:
        await m.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_path + ".jpg"):
            os.remove(temp_path + ".jpg")

# >>> End of upgrade <<<

# Your original functions like decrypt_and_merge_video, watermark_pdf, send_vid etc. remain intact.
