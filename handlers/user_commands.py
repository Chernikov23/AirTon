from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import inline
from utils.db import *
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config_reader import config


router = Router()
bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))


init_db()

@router.message(CommandStart())
async def start(msg: Message):
    tgid = msg.from_user.id
    username = msg.from_user.username or f"user_{tgid}"
    referral_link = f"https://t.me/testbardbot?start={tgid}"

    is_new_user = not user_exists(tgid)
    if is_new_user:
        add_user(username, tgid, referral_link)
        await msg.answer("Вы успешно зарегистрировались в системе!", reply_markup=inline.main)
    else:
        await msg.answer("Вы уже зарегистрированы в системе!", reply_markup=inline.main)

    args = msg.text.split()[1:]  # Извлекаем аргументы из команды /start

    if args and is_new_user:
        referrer_id = int(args[0].strip())
        if referrer_id == tgid:
            await msg.answer("Вы не можете использовать свою собственную реферальную ссылку.", reply_markup=inline.main)
        elif referral_exists(referrer_id, tgid):
            await msg.answer("Вы уже использовали эту реферальную ссылку.", reply_markup=inline.main)
        elif user_exists(referrer_id):
            add_referral(referrer_id, tgid)
            increase_user_invites(referrer_id)
            decrease_balance()
            await msg.answer("Вы успешно присоединились по реферальной ссылке!", reply_markup=inline.main)
            referrer = get_user_by_tgid(referrer_id)
            await bot.send_message(referrer[2], f"Пользователь @{username} перешел по вашей реферальной ссылке и вам был начислен 1 AirTon.", reply_markup=inline.main)
        else:
            await msg.answer("Недействительная реферальная ссылка.", reply_markup=inline.main)
            
@router.message(Command('top'))
async def top(msg: Message):
    top_referrers = get_top_referrers()
    if top_referrers:
        response = "Топ 10 пользователей по количеству приглашенных:\n"
        for i, (username, invited_count) in enumerate(top_referrers, 1):
            response += f"{i}. @{username}: *{invited_count}* приглашенных\n"
    else:
        response = "Нет данных о пользователях."
    await msg.answer(response)
    
@router.message(Command('users'))
async def show_users(msg: Message):
    total_users = get_total_users()
    await msg.answer(f"Общее количество пользователей: *{total_users}*")