from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.db import *

router = Router()


@router.callback_query(F.data == 'send')
async def send_ref(callback: CallbackQuery):
    await callback.message.answer(f"Your tgid:\n`https://t.me/testbardbot?start={callback.from_user.id}`")


@router.callback_query(F.data == 'balance')
async def show_balance(callback: CallbackQuery):
    user_balance = get_user_by_tgid(callback.from_user.id)[4]
    total_balance = get_balance()
    await callback.message.answer(f"Ваш баланс: *{user_balance}* AirTon\nОбщий баланс системы: *{total_balance}* AirTon")




# def is_referral_code(message_text):
#     return code_pattern.match(message_text) is not None


# async def process_referral(user_id: str, referral_code: str) -> str:
#     try:
#         with open('referral_codes.json', 'r') as file:
#             try:
#                 referral_codes = json.load(file)
#             except json.JSONDecodeError:
#                 referral_codes = {}
#     except FileNotFoundError:
#         referral_codes = {}

#     if referral_code in referral_codes and user_id != referral_codes[referral_code]:
#         update_balances(user_id, referral_codes[referral_code])
#         save_used_code(user_id, referral_code)
#         return "Вы успешно присоединились по реферальной программе!"
#     elif referral_code not in referral_codes:
#         return "Реферальный код не найден или неверен."
#     else:
#         return "Невозможно использовать этот реферальный код."


# @router.message()
# async def join_referral(message: Message):
#     if is_referral_code(message.text):
#         user_id = str(message.from_user.id)
#         code = message.text
#         if has_used_code(user_id, code):
#             await message.answer("Вы уже использовали этот реферальный код.")
#             return
        
#         response_message = await process_referral(user_id, code)
#         await message.answer(response_message)



# @router.callback_query()
# async def bal(call: CallbackQuery):
#     chat_id = str(call.message.chat.id)
#     callback_data = call.data
#     user_data_local = load_user_data()
#     if callback_data == 'balance': 
#         await call.message.answer(f"Ваш баланс: **{user_data_local[chat_id]['yourBal']}**")
#     elif callback_data == 'send':
#         code = call.from_user.username  
#         save_referral_code(chat_id, code)
#         bot_username = 'testbardbot'  # Ensure this is your bot's username
#         referral_link = f"https://t.me/{bot_username}?start={code}"  # Generating the referral link
#         await call.message.answer(f"Ваша реферальная ссылка:\nОтправьте эту ссылку другу, чтобы он мог присоединиться.\n`{referral_link}`")



# def save_referral_code(user_id, code):
#     try:
#         with open('referral_codes.json', 'r') as file:
#             try:
#                 referral_codes = json.load(file)
#             except json.JSONDecodeError:
#                 referral_codes = {} 
#     except FileNotFoundError:
#         referral_codes = {}  

#     referral_codes[code] = user_id
#     with open('referral_codes.json', 'w') as file:
#         json.dump(referral_codes, file)


# def save_used_code(user_id, code):
#     try:
#         with open('used_codes.json', 'r') as file:
#             try:
#                 used_codes = json.load(file)
#             except json.JSONDecodeError:
#                 used_codes = {}  
#     except FileNotFoundError:
#         used_codes = {} 

#     if user_id in used_codes:
#         used_codes[user_id].append(code)
#     else:
#         used_codes[user_id] = [code]
    
#     with open('used_codes.json', 'w') as file:
#         json.dump(used_codes, file)


# def has_used_code(user_id, code):
#     try:
#         with open('used_codes.json', 'r') as file:
#             try:
#                 used_codes = json.load(file)
#                 if user_id in used_codes and code in used_codes[user_id]:
#                     return True
#             except json.JSONDecodeError:
#                 return False  
#     except FileNotFoundError:
#         return False  
#     return False

