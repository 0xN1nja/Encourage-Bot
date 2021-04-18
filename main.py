import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client=discord.Client()
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=["encouraging_message"]
def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements
sad_words=["sad","unhappy","depressed","miserable","depressing","angry"]
starter_encouragements=[
  "Cheer Up !",
  "Hang In There.",
  "You Are A Great Person !"
]
if "responding" not in db.keys():
  db["responding"]=True
def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=f"{json_data[0]['q']} -{json_data[0]['a']}"
  return quote
@client.event
async def on_ready():
  print(f"Bot Has Successfully Logged In As {client.user}")
@client.event
async def on_message(message):
  if message.author==client.user:
    return
  msg=message.content
  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options=options+list(db["encouragements"])
    if any([word in msg for word in sad_words]):
      await message.channel.send(random.choice(options))
  if message.content.startswith("$hello"):
    await message.channel.send("Hello !")
  if message.content.startswith("$hi"):
    await message.channel.send("Hello !")
  if message.content.startswith("$inspire"):
    quote=get_quote()
    await message.channel.send(quote)
  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New Encouraging Message Added.")
  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
      await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  if msg.startswith("$responding"):
    value=msg.split("$responding ",1)[1]
    if value.lower()=="true":
      db["responding"]=True
      await message.channel.send("Responding Is On")
    else:
      db["responding"]=False
      await message.channel.send("Responding Is Off")
  if msg.startswith("$who created you"):
    await message.channel.send("I Was Created By Abhimanyu Sharma...")
  if msg.startswith("$commands") or msg.startswith("$help"):
    commands_dict={"$hello":"Bot Will Say Hello !","$hi":"Bot Will Say Hi !","$inspire":"Bot Will Return A Random Inspirational Quote","$new":"Bot Will Add Provided Encouraging Message","$del":"Bot Will Delete Provided Encouraging Message","$list":"Bot Will Return An Array Of Encouraging Messages","$help/$commands":"Bot Will Return Dict Of Commands","$responding true":"Bot Will Turn On Responding; Like If You Typed I'm Sad, Bot Will React To It.","$responding false":"Bot Will Turn Off Responding; Like If You Typed I'm Sad, Bot Will Not React To It.","$code":"Bot Will Return Source Code Of Bot On GitHub"}
    await message.channel.send(commands_dict)
  if msg.startswith("$code"):
    await message.channel.send("https://github.com/N1nja0p/Encourage-Bot")
keep_alive()
client.run(os.getenv("TOKEN"))
