import asyncio
import os

from pydub import AudioSegment

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from constants.bot_cons import TOKEN, COMMANDS, MP3, AAC, WELCOME


async def start_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)


async def aac_to_mp3(update, context):
    file_name = update.message.document.file_name
    file_name = file_name.replace(" ", "_").lower()
    print(f"{file_name} is received.")
    new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive(file_name)
    await update.message.reply_text(f"{file_name} saved successfully")
    mp3_file_path = f"{file_name[:-4]}.{MP3}"
    await asyncio.sleep(15)
    convert_to_mp3(file_name, mp3_file_path)
    with open(mp3_file_path, "rb") as mp3_file:
        await update.message.reply_audio(mp3_file)
    os.remove(file_name)
    os.remove(mp3_file_path)


def convert_to_mp3(input_file, output_file):
    audio = AudioSegment.from_file(input_file, format=AAC)
    audio.export(output_file, format=MP3)
    return output_file


if __name__ == "__main__":
    print("Starting the bot ...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler(COMMANDS[0], start_command))
    app.add_handler(MessageHandler(filters.ATTACHMENT, aac_to_mp3))
    print("Polling ...")
    app.run_polling(3)