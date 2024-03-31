from aiogram import Router, F, Bot
from aiogram.types import Message, LabeledPrice, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards import reply, inline
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_reader import config
import asyncio
import json
import secrets
from handlers.bot_messages import *
from utils.usdata import *

router = Router()


@router.message(CommandStart())
async def start(msg: Message):
    chat_id = str(msg.chat.id)
    user_data_local = load_user_data()
    if chat_id not in user_data_local:
        user_data_local[chat_id] = user_data_template
        save_user_data(user_data_local)
    await msg.answer("Мы хотим вас инфицировать Вселенной", reply_markup=inline.main)
        

@router.message(Command("numofusers"))
async def numus(msg: Message):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
        num_users = len(user_data)
        await msg.answer(f"Количество пользователей: {num_users}")
    except Exception as e:
        await msg.answer("Ошибка при подсчете пользователей: " + str(e))
        

@router.message(Command('join_referal'))
async def join_referral(message: Message):
    args = message.text.split(maxsplit=1)  # Разделение сообщения на части
    if len(args) > 1:
        code = args[1]  # Второй элемент — это наш код
        try:
            with open('referral_codes.json', 'r') as file:
                referral_codes = json.load(file)
            referrer_id = referral_codes.get(code)
            if referrer_id:
                user_id = str(message.from_user.id)
                if user_id != referrer_id:  # Проверка, чтобы пользователь не использовал свой же код
                    update_balances(user_id, referrer_id)
                    await message.answer("Вы успешно присоединились по реферальной программе!")
                else:
                    await message.answer("Вы не можете использовать свой собственный реферальный код.")
        except FileNotFoundError:
            await message.answer("Произошла ошибка при обработке вашего запроса.")
    else:
        await message.answer("Пожалуйста, укажите реферальный код после команды. Например, /join_referral XYZ123")
        
def update_balances(user_id, referrer_id):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    for uid in [user_id, referrer_id]:
        if uid in user_data:
            user_data[uid]['yourBal'] /= 2
        else:
            user_data[uid] = {'yourBal': 8000000000 / 2}
    
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)
