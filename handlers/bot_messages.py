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


async def process_referral(user_id: str, referral_code: str) -> str:
    try:
        with open('referral_codes.json', 'r') as file:
            try:
                referral_codes = json.load(file)
            except json.JSONDecodeError:
                referral_codes = {}
    except FileNotFoundError:
        referral_codes = {}

    if referral_code in referral_codes and user_id != referral_codes[referral_code]:
        update_balances(user_id, referral_codes[referral_code])
        save_used_code(user_id, referral_code)
        return "Вы успешно присоединились по реферальной программе!"
    elif referral_code not in referral_codes:
        return "Реферальный код не найден или неверен."
    else:
        return "Невозможно использовать этот реферальный код."


@router.message()
async def join_referral(message: Message):
    if is_referral_code(message.text):
        user_id = str(message.from_user.id)
        code = message.text
        if has_used_code(user_id, code):
            await message.answer("Вы уже использовали этот реферальный код.")
            return
        
        response_message = await process_referral(user_id, code)
        await message.answer(response_message)



@router.callback_query()
async def bal(call: CallbackQuery):
    chat_id = str(call.message.chat.id)
    callback_data = call.data
    user_data_local = load_user_data()
    if callback_data == 'balance': 
        await call.message.answer(f"Ваш баланс: {user_data_local[chat_id]['yourBal']}")
    elif callback_data == 'send':
        code = secrets.token_urlsafe(10)  # Adjusted to generate a 10-character code to match the pattern
        save_referral_code(chat_id, code)
        bot_username = 'testbardbot'  # Ensure this is your bot's username
        referral_link = f"https://t.me/{bot_username}?start={code}"  # Generating the referral link
        await call.message.answer(f"Ваша реферальная ссылка:\nОтправьте эту ссылку другу, чтобы он мог присоединиться.\n{referral_link}")



def save_referral_code(user_id, code):
    try:
        with open('referral_codes.json', 'r') as file:
            try:
                referral_codes = json.load(file)
            except json.JSONDecodeError:
                referral_codes = {} 
    except FileNotFoundError:
        referral_codes = {}  

    referral_codes[code] = user_id
    with open('referral_codes.json', 'w') as file:
        json.dump(referral_codes, file)


def save_used_code(user_id, code):
    try:
        with open('used_codes.json', 'r') as file:
            try:
                used_codes = json.load(file)
            except json.JSONDecodeError:
                used_codes = {}  
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
            try:
                used_codes = json.load(file)
                if user_id in used_codes and code in used_codes[user_id]:
                    return True
            except json.JSONDecodeError:
                return False  
    except FileNotFoundError:
        return False  
    return False

