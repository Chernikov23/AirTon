
from aiogram import Router, Bot, F
from aiogram.types import Message, LabeledPrice, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, PreCheckoutQuery
from aiogram.filters import Command
from keyboards import reply, inline
from utils.usdata import *
from handlers.user_commands import *
import secrets
import re
from handlers.user_commands import update_balances


router = Router()
code_pattern = re.compile(r'^[A-Za-z0-9_-]{10}$')
def is_referral_code(message_text):
    return code_pattern.match(message_text) is not None

@router.message()
async def join_referral(message: Message):
    code = message.text
    user_id = str(message.from_user.id)
    if has_used_code(user_id, code):
        await message.answer("Вы уже использовали этот реферальный код.")
        return
    
    try:
        with open('referral_codes.json', 'r') as file:
            referral_codes = json.load(file)
        referrer_id = referral_codes.get(code)
        if referrer_id and user_id != referrer_id:
            update_balances(user_id, referrer_id)
            save_used_code(user_id, code)
            await message.answer("Вы успешно присоединились по реферальной программе!")
        else:
            await message.answer("Невозможно использовать этот реферальный код.")
    except FileNotFoundError:
        await message.answer("Произошла ошибка при обработке вашего запроса.")



@router.callback_query()
async def bal(call: CallbackQuery):
    chat_id = str(call.message.chat.id)
    callback_data = call.data
    user_data_local = load_user_data()
    if callback_data == 'balance': 
        await call.message.answer(f"Ваш баланс: {user_data_local[chat_id]['yourBal']}")
    elif callback_data == 'send':
        code = secrets.token_urlsafe(5)  # Генерация уникального кода
        save_referral_code(chat_id, code)
        await call.message.answer(f"Ваш реферальный код:\nОтправьте этот код другу, чтобы он мог его использовать.")
        await call.message.answer(f"{code}\n@Air_tonbot")
    
def save_referral_code(user_id, code):
    try:
        with open('referral_codes.json', 'r') as file:
            referral_codes = json.load(file)
    except FileNotFoundError:
        referral_codes = {}

    referral_codes[code] = user_id
    with open('referral_codes.json', 'w') as file:
        json.dump(referral_codes, file)

def save_used_code(user_id, code):
    try:
        with open('used_codes.json', 'r') as file:
            used_codes = json.load(file)
    except FileNotFoundError:
        used_codes = {}
    
    if user_id in used_codes:
        used_codes[user_id].append(code)
    else:
        used_codes[user_id] = [code]
    
    with open('used_codes.json', 'w') as file:
        json.dump(used_codes, file)

def has_used_code(user_id, code):
    try:
        with open('used_codes.json', 'r') as file:
            used_codes = json.load(file)
        if user_id in used_codes and code in used_codes[user_id]:
            return True
    except FileNotFoundError:
        pass
    return False
