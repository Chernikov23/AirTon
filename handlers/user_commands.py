from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import inline
from utils.db import *
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config_reader import config
import os, json

router = Router()
bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

async def get_message(key, lang_code):
    file_path = os.path.join(os.path.join(os.path.dirname(__file__), 'locales'), f"{lang_code}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key)


init_db()

@router.message(CommandStart())
async def start(msg: Message):
    tgid = msg.from_user.id
    username = msg.from_user.username or f"user_{tgid}"
    referral_link = f"https://t.me/air_tonbot?start={tgid}"

    is_new_user = not user_exists(tgid)
    if is_new_user:
        add_user(username, tgid, referral_link)
        await msg.answer(text=await get_message('succeed', msg.from_user.language_code), reply_markup=inline.main)
    else:
        await msg.answer(text=await get_message('already', msg.from_user.language_code), reply_markup=inline.main)

    args = msg.text.split()[1:]  

    if args and is_new_user:
        referrer_id = int(args[0].strip())
        if referrer_id == tgid:
            await msg.answer(text=await get_message('yourOwn', msg.from_user.language_code), reply_markup=inline.main)
        elif referral_exists(referrer_id, tgid):
            await msg.answer(text=await get_message('hasUsed', msg.from_user.language_code), reply_markup=inline.main)
        elif user_exists(referrer_id):
            add_referral(referrer_id, tgid)
            increase_user_invites(referrer_id)
            decrease_balance()
            await msg.answer(text= await get_message('joined', msg.from_user.language_code), reply_markup=inline.main)
            referrer = get_user_by_tgid(referrer_id)
            await bot.send_message(referrer[2], text=str(await get_message('usJoin', msg.from_user.language_code)).format(username), reply_markup=inline.main)
        else:
            await msg.answer(text=await get_message('donWork', msg.from_user.language_code), reply_markup=inline.main)
            
@router.message(Command('top'))
async def top(msg: Message):
    top_referrers = get_top_referrers()
    if top_referrers:
        response = f"{str(await get_message('topUsers', msg.from_user.language_code))}\n"
        for i, (username, invited_count) in enumerate(top_referrers, 1):
            response += f"{i}. @{username}: *{invited_count}* invited\n"
    else:
        response = await get_message('noData', msg.from_user.language_code)
    await msg.answer(response)
    
@router.message(Command('users'))
async def show_users(msg: Message):
    total_users = get_total_users()
    await msg.answer(str(await get_message('usAmo', msg.from_user.language_code)).format(total_users))
