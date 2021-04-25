import logging
import json
from datetime import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from db import DB
from config import Config

# ЛОГГЕР
# logging.basicConfig(filename="bot_log.log", level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
TOKEN = Config.get_config()['bot']['token']
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

### надо состояния для юзеров куда-то писать 
### и сами состояния чтобы считывать сначала состояние юзера, выполнять действия по этому состоянию , менять состояние
### 



class BotMethods:
    map_state = {
        'start': {
            'keys':{
                'appeal': 'Создать обращение',
                'todo': 'Список дел',
                'dinner': 'Сегодня в меню',
            },
            'message': 'Добрый день! Бот оказывает различную помощь студентам и преподавателям'
        },
        'appeal':{
            'keys':{
                'start':'Назад', 
            },
            'message': 'Выберите подразделения в которые вы хотите отправить обращение'
        },        
    }


    def __init__(self):
        self.db = DB().connect(Config.get_config()) 

    def get_map_state(self):
        query = 'SELECT * from hackinhome.departaments'
        result = self.db.select(query)
        if result:
            for item in result:
                key = 'appeal_'+str(item['id'])
                name = item['departament_name']
                self.map_state['appeal']['keys'][key] = name

                key_type_anon = 'appeal_'+str(item['id']) +'_anon' 
                name_anon = 'Анонимное обращение'
                key_type_dis = 'appeal_'+str(item['id']) +'_dis' 
                name_dis = 'Обращение требующие ответа'
                self.map_state[key] = {
                    'keys':{
                        'appeal':'Назад',
                        key_type_anon: name_anon,
                        key_type_dis: name_dis
                    },
                    'message': 'Выберите тип обращения:'
                }

                self.map_state[key_type_anon] = {
                    'keys':{
                        'appeal':'Назад',
                    },
                    'message': 'Введите и отправьте ваше обращение'
                }
                self.map_state[key_type_dis] = {
                    'keys':{
                        'appeal':'Назад',
                    },
                    'message': 'Введите и отправьте ваше обращение'
                }




        return self.map_state


    def set_state(self, chat_id, state='start'):
        user_exist = self.db.select(f'SELECT state FROM hackinhome.users WHERE chat_id = {chat_id}')
        if user_exist:
            query = f"update hackinhome.users set state = '{state}' where chat_id = {chat_id}"
            self.db.update(query)
        else:
            query = f"insert into hackinhome.users(chat_id, state) values ({chat.id},'start')"
            self.db.insert(query)

    def get_state(self, chat_id):
        user_exist = self.db.select(f'SELECT state FROM hackinhome.users WHERE chat_id = {chat_id}')
        if user_exist:
            print(user_exist)
            return user_exist


    #### КОМАНДА СТАРТ
    def start(self,update, context):
        print(update)
        query = f'SELECT * FROM hackinhome.users WHERE chat_id = {update.effective_chat.id}'
        db_result = self.db.select(query)
        if not db_result:
            query = f"insert into hackinhome.users(chat_id, stud_id, full_name, user_name, type) values ({update.effective_chat.id},{update.effective_chat.id}, 'Абдулов Рамир Ринатович', '{update.effective_user.username}', 1)"
            self.db.insert(query)
            self.set_state(update.effective_chat.id, 'start')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Добрый день! Бот оказывает различную помощь студентам и преподавателям", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Обращение', callback_data='appeal')]]))

    def get_keyboard(self, map):
        keyboard = []
        for key, value in map.items():
            keyboard.append([InlineKeyboardButton(text=value, callback_data=key)])
        return InlineKeyboardMarkup( keyboard)


    #ОБРАБАТЫВАЕТ ЗАПРОСЫ ОТ ВСЕХ КНОПОК
    def callback_button_handler(self,update, context):
        query = update.callback_query
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
        
        if query.data in self.map_state.keys():
            print(query.data)
            query.edit_message_text(text=self.map_state[query.data]['message'], reply_markup= self.get_keyboard(self.map_state[query.data]['keys']))
            self.set_state(update.effective_chat.id, query.data)
       
    #ЕСЛИ не распознал команду /команда
    def unknown(self,update, context):
        state = self.get_state(update.effective_chat.id)
        if state:
            print(state)
        if 'appeal' in state[0]['state'] and ('anon' in state[0]['state'] or 'dis' in state[0]['state']):
            chat_id = update.effective_chat.id
            message_id = update.message.message_id
            text = update.message.text
            departament_id = int(str(state[0]['state']).replace('appeal_', '')[0])
            state = 1

            print(chat_id, message_id,text,departament_id,state)
            query = f"insert into hackinhome.appeal (chat_id, message_id, text, departament_id, state) values \
                ({chat_id},{message_id},'{text}',{departament_id},{state})"
            appeal_number = str(self.db.insert(query))
            context.bot.send_message(chat_id=update.effective_chat.id, text="Обращение зарегистрировано. Номер обращения: "+appeal_number,reply_markup= self.get_keyboard(self.map_state['start']['keys']))
            self.set_state(chat_id)
    

botMethods = BotMethods()
botMethods.get_map_state()

print(botMethods.get_map_state())

##ДОБАВЛЕНИЕ ХЕНДЛЕРОВ
dispatcher.add_handler(CallbackQueryHandler(botMethods.callback_button_handler))
start_handler = CommandHandler('start', botMethods.start)
dispatcher.add_handler(start_handler)



    
unknown_handler = MessageHandler(Filters.text, botMethods.unknown)
dispatcher.add_handler(unknown_handler)



updater.start_polling()