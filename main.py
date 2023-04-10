# importing packages
import os
import array as arr
from uuid import uuid4
from decouple import config
from pytube import YouTube
from aiogram import Bot, Dispatcher, executor, types


def downloadMp3( url ):
    # url input from user
    yt = YouTube( url )
    
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    

    # replace destination with the path where you want to save the downloaded file
    destination = "./"
    
    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    #new_file = base + '.mp3'
    new_file = str(uuid4()) + '.mp3'
    os.rename(out_file, new_file)
    return [new_file, yt.title]
    # result of success
    #print(yt.title + " has been successfully downloaded.")

def extractYoutubeLink( message ):
    messageSplit = str(message).split(" ")
    for i in range(len(messageSplit)):
        indexWithLink = messageSplit[i].startswith(('https://www.you', 'http://www.you', 'www.you','https://youtu.be'))
        if indexWithLink == True:
            return messageSplit[i]
    return ""


bot = Bot(config('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','ayuda'])
async def welcome(message: types.Message):
    await message.reply("Envia el url del video de youtube que deseas convertir a mp3")

@dp.message_handler(commands=['juan'])
async def welcome(message: types.Message):
    await message.reply("Mensaje personal para el master")
    await message.reply("Aprecio total padrino <3")

@dp.message_handler()
async def echo(message: types.Message):
    youtubeLink = extractYoutubeLink( message.text )
    if youtubeLink == "" : 
        await message.answer("No es un link de youtube valido, envia /ayuda para obtener mas informacion")
    else:
        await message.answer('Descargando video')
        nameFile, nameSong = downloadMp3( youtubeLink )
        await message.answer("Enviando archivo")
        file = open( nameFile , "rb")
        try:
            await bot.send_audio(chat_id = message.from_user.id, audio= file, performer = "ManuelOct", title = nameSong)
            await message.answer("Proceso terminado, recomienda este bot con tus amigos")
        except Exception as e:
            print(e)
            await message.answer("Ocurrio un error y no se ha podido enviar el archivo")
        finally:
            file.close()
            os.remove(nameFile)
    

executor.start_polling(dp)
