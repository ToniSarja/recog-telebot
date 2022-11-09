import telebot
import speech_recognition as sr
from os import path
from pydub import AudioSegment
import soundfile
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from random import choice
import pickle
import numpy as np
import json

with open("intents.json",encoding="utf8") as file:
    data = json.load(file)


bot = telebot.TeleBot("TOKEN_GOES_HERE", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Placeholder text")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Placeholder text")

@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    #load the model
    model = keras.models.load_model('chat_model')
    max_len = 20
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    #bot graps the audio file
    bot.reply_to(message, "Pieni hetki")
    r = sr.Recognizer()
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('user_voice.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
    src_filename = 'user_voice.ogg'
    dest_filename = 'user_voice_output.wav'
    
    #change of format
    sound = AudioSegment.from_ogg(src_filename)
    sound.export(dest_filename, format="wav")

    user_audio_file = sr.AudioFile("user_voice_output.wav")
    with user_audio_file as source:
        #speech recognition happens here
        user_audio = r.record(source)
        text = r.recognize_google(user_audio, language='ru')
        #classification and iterating thru the JSON dataset
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([text]),truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data['intents']:
            if i['tag'] == tag:
                bot.send_message(message.from_user.id, np.random.choice(i['responses']))


bot.infinity_polling()
