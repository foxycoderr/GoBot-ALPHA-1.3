from flask import Flask
import os
from threading import Thread



app = Flask('')



@app.route('/')

def home():

    return "<h> Bot is online and working. <\h>"



def run():
  os.system("clear")
  app.run(host='0.0.0.0',port=8080)
  os.system("clear")



def keep_alive():  

    t = Thread(target=run)

    t.start()
    os.system("clear")

