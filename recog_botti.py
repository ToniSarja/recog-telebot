import telebot
import speech_recognition as sr
import os
from os import path
from pydub import AudioSegment
import soundfile
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from random import choice
import pickle
import numpy as np
import json
import telegram_upload
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
bot = telebot.TeleBot("", parse_mode=None)

with open("intents.json",encoding="utf8") as file:
    data = json.load(file)

with open("quiz.json",encoding="utf8") as f:
    visa = json.load(f)
    
#load the model
model = keras.models.load_model('chat_model')
max_len = 20
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

#This handles user input, voice
@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    path = "zvuk/"
    for file_name in os.listdir(path):
        user_audio_file = None
        # construct full file path
        file = path + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

    #voice input happens here
    r = sr.Recognizer()
    file_info = bot.get_file(message.voice.file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)

    #Voice input saved into a file, transformed into .wav file
    with open(f'zvuk/{message.voice.file_id}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    src_filename = f'zvuk/{message.voice.file_id}.ogg'
    dest_filename = f'zvuk/{message.voice.file_id}_output.wav'

    sound = AudioSegment.from_ogg(src_filename)
    sound.export(dest_filename, format="wav")

    #Speech recognition happens here, speech_recogniser turns file into a string
    user_audio_file = sr.AudioFile(f"zvuk/{message.voice.file_id}_output.wav")
    with user_audio_file as source:
        user_audio = r.record(source)
        text = r.recognize_google(user_audio, language='uk-UA')
        #the model tries to classify user input according the JSON data
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]),truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                bot.send_voice(message.from_user.id, np.random.choice(i['responses']))

bot.infinity_polling()
