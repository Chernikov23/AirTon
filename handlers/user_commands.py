from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from keyboards import inline
import json
from handlers.bot_messages import *
from utils.updata import *

router = Router()


async def process_referral(user_id: str, referral_code: str) -> int:
    try:
        with open('referral_codes.json', 'r') as file:
            try:
                referral_codes = json.load(file)
            except json.JSONDecodeError:
                # Файл существует, но пуст или содержит некорректные данные
                referral_codes = {}
    except FileNotFoundError:
        # Файл не существует, создаем новый словарь реферальных кодов
        referral_codes = {}

    num_referrals_sent = 0

    if referral_code in referral_codes and user_id != referral_codes[referral_code]:
        num_referrals_sent = update_balances(user_id, referral_codes[referral_code])
        save_used_code(user_id, referral_code)
    elif referral_code not in referral_codes:
        pass  # Реферальный код не найден или неверен.
    else:
        pass  # Невозможно использовать этот реферальный код.

    return num_referrals_sent




@router.message(CommandStart())
async def start(msg: Message):
    user_id = str(msg.from_user.id)
    # Извлекаем аргументы из команды /start, если они есть
    args = msg.text.partition(' ')[2]  # Разделяем текст сообщения и берем часть после /start

    user_data_local = load_user_data()

    if user_id not in user_data_local:
        user_data_local[user_id] = user_data_template
        save_user_data(user_data_local)
        print(f"Пользователь {msg.from_user.username} зарегистрирован")

    if args:
        referral_code = args.strip()
        num_referrals_sent = await process_referral(user_id, referral_code)
        await msg.answer(f"Добро пожаловать в нашего бота! Вы успешно присоединились по реферальной программе! Реферат был разослан {num_referrals_sent} пользователям.", reply_markup=inline.main)
    else:
        await msg.answer("Добро пожаловать в нашего бота! Если у вас есть реферальный код, отправьте его.", reply_markup=inline.main)


@router.message(Command("numofusers"))
async def numus(msg: Message):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
        num_users = len(user_data)
        await msg.answer(f"Количество пользователей: {num_users}")
    except Exception as e:
        await msg.answer("Ошибка при подсчете пользователей: " + str(e))   
        
        
        
@router.message(Command('tops'))
async def show_tops(msg: Message):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        await msg.answer("Произошла ошибка при загрузке данных пользователей.")
        return

    # Сортировка пользователей по балансу (от меньшего к большему) и выбор первых пяти
    top_users = sorted(user_data.items(), key=lambda x: x[1]['yourBal'])[:10]

    # Формирование сообщения с топ-5 пользователей
    top_message = "Топ 10 пользователей с наименьшим балансом:\n"
    for index, (user_id, user_info) in enumerate(top_users, start=1):
        # Для получения username, вам может потребоваться запрос к API Telegram или хранить username в user_data
        top_message += f"{index} - user_id: {user_id}, баланс: {user_info['yourBal']}\n"

    await msg.answer(top_message)        
        

@router.message(Command('chat_id'))
async def proc_chat_id(msg: Message):
    await msg.answer(f"Your chat id: {msg.chat.id}")

def update_balances(user_id, referrer_id):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    num_referrals_sent = 0

    for uid in [user_id, referrer_id]:
        if uid in user_data:
            if user_data[uid]['yourBal'] > 1:
                user_data[uid]['yourBal'] /= 2
            else:
                user_data[uid]['yourBal'] = 1  # Ограничение баланса до 1, если меньше
            num_referrals_sent += 1
        else:
            user_data[uid] = {'yourBal': 8000000000 / 2}
    
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)
    
    return num_referrals_sent



def save_referral_code(user_id, code):
    try:
        with open('referral_codes.json', 'r') as file:
            try:
                referral_codes = json.load(file)
            except json.JSONDecodeError:
                referral_codes = {}  # Файл пуст, создаем новый словарь
    except FileNotFoundError:
        referral_codes = {}  # Файл не найден, создаем новый словарь

    referral_codes[code] = user_id
    with open('referral_codes.json', 'w') as file:
        json.dump(referral_codes, file)


def save_used_code(user_id, code):
    try:
        with open('used_codes.json', 'r') as file:
            try:
                used_codes = json.load(file)
            except json.JSONDecodeError:
                used_codes = {}  # Файл пуст, создаем новый словарь
    except FileNotFoundError:
        used_codes = {}  # Файл не найден, создаем новый словарь

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
                return False  # Файл пуст, следовательно код не мог быть использован
    except FileNotFoundError:
        return False  # Файл не найден, следовательно код не мог быть использован
    return False

