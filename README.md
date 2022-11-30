# recog-telebot
Deep learning telegram bot that recognizes Russian words and responds in Russian

A Python script calls the Telegram bot and the Python Speech Recognition module is used for transforming voice input into a string. I use Google Speech Recognition for voice recognition

The deep learning model then classifies the string by iterating through a JSON file which includes key value pairs. 

If the string matches a key in the dictionary, the Python script will return a value which is a response.

Here's a video demonstration

[![Alt text](https://img.youtube.com/vi/Zgl9s_vVMBE/0.jpg)](https://www.youtube.com/watch?v=Zgl9s_vVMBE)

Planned features
-
A SQL database that collects user responses so that I could build a better dataset for classification

Some nice visualizations for users to view their progress
