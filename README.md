# recog-telebot
Deep learning telegram bot that recognizes Russian words and responds in Russian

A Python script calls the Telegram bot and the Python Speech Recognition module is used for transforming voice input into a string. 

The deep learning model then classifies the string by iterating through a JSON file which includes key value pairs. 

If the string matches a key in the dictionary, the Python script will return a value which is a response.

https://www.youtube.com/watch?v=Zgl9s_vVMBE
