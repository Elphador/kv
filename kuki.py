import os

from pyrogram import Client, filters, enums 

from pyrogram.errors import UserNotParticipant , FloodWait,InputUserDeactivated , UserIsBlocked , PeerIdInvalid

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle 

from  pymongo import MongoClient

import asyncio ,time

import requests,  json

from time import sleep 

import datetime 

HELP = """**--Help--\n Kuki is your AI chat Bot friend Just Start conversation \n\n the premium Version of Kuki chatbot is Available for purchase ,it can include more features like Kuki learns from your everyday activity 

,she will never miss you(bot can have memory) , and you can train her well. \n\nCommands & their Usage \n/start Restarts the Bot \n/bots to get list of our bots made by Neural programmes team\n

/broadcast to Broadcast message for bot users , you should have to be an admin to use this feature you can require this in our group or using feedback command and promote your products via our bot \n

/users to get how many users we have\n

/sms send message for one specified user \n

/adminstrators to get list of admins of this bot \nN.B : Some commands doesn't work for free users\n**"""

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-M135FU) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',

'Referer': 'https://chat.kuki.ai/chat'}

api_id =18802415 ; api_hash = "a8993f96404fd9a67de867586b3ddc92" ; bot_token = "5759372798:AAHB655HjNY-77raQYplIzNKZcKORvjZAt4"

mongodb = "mongodb+srv://elphador69:59TDtNdq532MQAk4@cluster0.aqze07b.mongodb.net/?retryWrites=true&w=majority"

"buttons"

channel = InlineKeyboardButton("Channel🌴",url='https://t.me/neuralp')

group = InlineKeyboardButton("Group🪺",url='https://t.me/neuralg')

developer = InlineKeyboardButton("Developer🦭",url="https://t.me/e_phador")

premium = InlineKeyboardButton("Subscribe Premium🍿",url='https://t.me/the_ep')

help = InlineKeyboardButton("Help📃",callback_data='help')

mark = InlineKeyboardMarkup([[InlineKeyboardButton("🥬team Neural 🌽",url = "https://t.me/neuralp")]])   

app = Client ("grabber",api_id=api_id,api_hash=api_hash, bot_token=bot_token)

cli = MongoClient(mongodb); db = cli.database; cuser = db.cuser ; cadmin = db.cadmin ; force = db.force ; newbots = db.newbots

    

@app.on_message(filters.command("cast"))

async def cast_mesg(bot,msg):

    txt = msg.text

    blocked = " "

    idinvalid  = " "

    deactive = " "

    cast_text = txt.replace('/cast',"")

    for user in cuser.find():

        try :

            await bot.send_message(user['userid'],f" Hey {user['name']}🤗\n{cast_text}", reply_markup=mark)

        except UserIsBlocked:

            blocked+=f"{user['userid']} : {user['name']} :  @{user['username']}\n"

        except InputUserDeactivated:

            deactive+=f"{user['userid']} : {user['name']} : {user['username']}\n"

        except PeerIdInvalid:

            idinvalid+=f" {user['userid']} : {user['name']} : {user['username']}\n"

        except FloodWait as e:

            await asyncio.sleep(e.x)     

        except Exception as error:

          await msg.reply(error)

    await msg.reply(f"**Cast Logs**\n\n**Blocked Users**\n{blocked}\n**Invalid Ids**\n{idinvalid}**Deactivated**\n{deactive}")  

    

@app.on_message( filters.command("msg"))    

async def single_msg(bot,msg):

  try :

    text_ = msg.text

    

        

    user_id = text_.split(" ")[1]

    msg_text = text_.replace('/msg',"").replace(user_id,'')

    getting_name = cuser.find_one({"userid":int(user_id)})

    

    

    await bot.send_message(int(user_id), f"Hey {getting_name['name']}😊\n{msg_text}\n\n\n**Neural Programmers CEO**",reply_markup=mark) 

    await msg.reply("your message sent successfully")

  except Exception as error:

        await msg.reply(f"not sent\n{error}")   

        

@app.on_message( filters.command("admins"))

async def admins_list(bot, msg):

    list_ = " "

    for x in cadmin.find({}):

        admins_id= x['admins']

        promoter = x['promoted']

        list_+= f"ID {admins_id} : promoted by {promoter} \n"

    await msg.reply(list_)

    

@app.on_message(filters.command("force"))       

def channel_force(bot , msg):

    stats = force.find_one({"frc":"frc"})

    if stats :

      editing = force.update_one({"frc":"frc"},{"$set" : {"status":msg.text.split(' ')[1]}})

    else :

      status = force.insert_one({"status":msg.text.split(' ')[1],'frc':"frc"})

    stats = force.find_one({"frc":"frc"})

    current = msg.reply(f"**Current Force Join Status {stats['status']}🦊**")

    time.sleep(3)

    current.edit(f"**Current Force Join Set to {stats['status']}🦊.**")

    

    

@app.on_message(filters.command("set") )

def set_admin(bot, msg):

    new_id = msg.text.split(" ")[-1]

    promoter = msg.from_user.first_name 

    vals = {"admins":int(new_id),"promoted":promoter}

    cadmin.insert_one(vals)

    cut = cadmin.find_one({"admins":int(new_id)})

    bot.send_message(int(new_id),f"you have promoted to admin by {promoter}")

    msg.reply("Promoting New Admin Done🦊")

    

    

@app.on_message(filters.private & filters.command("newbot"))

def newbot(bot, msg):

    # name | type | language | Description | Status | payment

    bot_info = msg.text.replace('/newbot','').split('|')

    print(bot_info)

    name = bot_info[0] ; srname= bot_info[2] ; type = bot_info[1] ; lang= bot_info[3]

    description = bot_info[4] ; stats = bot_info[5] ; pay = bot_info[6] 

    adding = newbots.insert_one({"name":name,"username":srname,"type":type,"language":lang,"description":description, "status":stats,"payment":pay})

    norm_msg = msg.reply("`Organising your bot information....`")

    time.sleep(2)

    show = newbots.find_one({"name":name})

    norm_msg.edit(f"`your bots text looks like ..... `\n\n**Name : **{show['name']}\nType :{show['type']}\n**Username :**{show['username']} \n**Languages : **{show['language']}\n**Description : **{show['description']}\n**Status : **{show['status']}\n**Payment : **{show['payment']}")

@app.on_message(filters.private & filters.command("editbot"))

def newbot(bot, msg):

    # name | type | language | Description | Status | payment

    bot_info = msg.text.replace('/editbot','').split('|')

    print(bot_info)

    name = bot_info[0] ; type= bot_info[2] ; srname = bot_info[1] ; lang= bot_info[3]

    description = bot_info[4] ; stats = bot_info[5] ; pay = bot_info[6] 

    adding = newbots.update_one({"username":srname},{"$set":{"name":name,"username":srname,"type":type,"language":lang,"description":description, "status":stats,"payment":pay}})

    norm_msg = msg.reply("`Organising your bot information....`")

    time.sleep(2)

    show = newbots.find_one({"username":srname})

    norm_msg.edit(f"`your bots text looks like ..... `\n\n**Name : **{show['name']}\nType :{show['type']}\n**Username :**{show['username']} \n**Languages : **{show['language']}\n**Description : **{show['description']}\n**Status : **{show['status']}\n**Payment : **{show['payment']}")

  

@app.on_message(filters.private & filters.command("bots"))

def bots(bot, msg):

    text = ""

    dynamising = msg.reply("`Remembering ......Laoding ......`")

    for show in newbots.find() :

        text+=f"\n\n**Name : **{show['name']}\nType : {show['type']}\n**Username :**{show['username']} \n**Languages : **{show['language']}\n**Description : **{show['description']}\n**Status : **{show['status']}\n**Payment : **{show['payment']}"

    dynamising.edit(f"**🧑‍🌾Our Bots👩‍🌾**\n\n\n\n{text}")

@app.on_message(filters.private & filters.command("delbot"))

def newbot(bot, msg):

    # name | type | language | Description | Status | payment

    bot_info = msg.text.replace('/delbot','').split('|')

    print(bot_info)

    name = bot_info[0] #; srname= bot_info[1] #; type = bot_info[2] ; lang= bot_info[3]

 #   description = bot_info[4] ; stats = bot_info[5] ; pay = bot_info[6] 

    newbots.delete_many({"name":name})

    norm_msg = msg.reply("`Organising your bot information....`")

    time.sleep(2)

    show = newbots.find_one({"name":name})

    print(show)

    

    norm_msg.edit(f"`your bots deleted text ..... `\n\n**Name : **{show['name']}\nType :{show['type']}\n**Username :**{show['username']} \n**Languages : **{show['language']}\n**Description : **{show['description']}\n**Status : **{show['status']}\n**Payment : **{show['payment']}")

  

    

@app.on_message( filters.command("start"))

async def start(bot, msg):

  

    name = msg.from_user.first_name 

    userid = msg.from_user.id

    username = msg.from_user.username  

    check = cuser.find_one({'userid':userid})

    user = {"name":name,"userid":userid,"username":username, "date":datetime.datetime.now()}

    if not check :

      cuser.insert_one(user)

    else:

      pass

    markup = InlineKeyboardMarkup([[channel, group], [developer,premium],[help]])

    await msg.reply(f"**Hello {username} My name Is Kuki I'm an Ai Chat Bot , I'm here to waste my time talking with you**",

    reply_markup= markup )

@app.on_message( filters.command("feedback"))

async def feeback (bot , msg):

    cool_text = msg.text.replace('/feedback','')

    feedbacker = msg.from_user.id 

    name = msg.from_user.first_name 

    for each in cadmin.find():

        await bot.send_message(int(each['admins']),f"feedback from {name}, ID  : {feedbacker}\n\n{cool_text}")   

    

@app.on_message( filters.private & filters.command("users")) 

def users_count (bot, msg):

     count = cuser.find()

     counting = len(list(count))

     msg.reply(f"**we have {counting} users at this moment🦝**")

    

@app.on_message(filters.command("userlist")) 

async def userslist(bot,msg):

    names =""

    load = await msg.reply("`Loading .......`")

    for usr in cuser.find():

        names+=f"{usr['name']} => @{usr['username']} => {usr['userid']} => Joined in {usr['date']}\n"

        await load.edit(names)    

    

#always we change the codes down here for different bots just we copy and paste the above code to implement all functions on each of our bots , you can take some actions if it's needed, aka , if you need 

@app.on_message( filters.text)

async def kuki(bot, msg):

    stats = force.find_one({"frc":"frc"})

    if stats['status'] == 'on' :

        try :

            await bot.get_chat_member(-1001776406696 ,msg.from_user.id)

        except UserNotParticipant:

            await msg.reply("**Sorry i can't help you a lot on this ,Join the channel before our meeting**",

            reply_markup = InlineKeyboardMarkup([[channel]]))

            return

    else :

        pass
    await msg.reply_chat_action(enums.ChatAction.TYPING)
     

    try :

      data = {
    'uid': '4e937c67cc0880db',
    'input': msg.text,
    'sessionid': '483819942',
}

      resp = requests.post('https://kuli.kuki.ai/cptalk', headers=headers, data=data)

      print(resp.text)

      aqe = json.loads(resp.text);lst = aqe['responses'][0] 

      await msg.reply(lst)

    except KeyError :

        header = {'Content-Type': 'application/x-www-form-urlencoded',}

        data = f'botkey=97c170abd89a58faed88f4f2546dbb145ec856ffcd0b2221443bbf033b3e6e8e&input={msg.text}&client_name=foo'

        resp = requests.post('https://devman.kuki.ai/talk', headers=header, data=data)

        print(resp.text)

        aqe = json.loads(resp.text);lst = aqe['responses'][0]

        await msg.reply(lst)

    #except Exception as e:

     #await msg.reply(e)

      

    

    

    

@app.on_callback_query() 

async def calls(bot,update):

    name = update.message.from_user.first_name

    chat_id = update.message.chat.id; call = update.data

    if call == "help":

        await update.message.reply(HELP)

    else :

        await update.message.reply("oh forgotten button report bug ")            

            

            

print(app.run())            

app.run() 
