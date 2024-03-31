from aiohttp import web
import json

async def handle_referral(request):
    token = request.match_info.get('token', "")
    success = process_referral_link(token)
    if success:
        return web.Response(text="Баланс уменьшен вдвое")
    else:
        return web.Response(text="Невозможно обработать ссылку")

def process_referral_link(token):
    try:
        with open('referral_links.json', 'r') as file:
            referral_links = json.load(file)
        user_id = referral_links.get(token)
        if user_id:
            half_balance(user_id)
            return True
    except FileNotFoundError:
        pass
    return False

def half_balance(user_id):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    if user_id in user_data:
        user_data[user_id]['yourBal'] /= 2
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file)
    else:
        # Создание нового пользователя с начальным балансом, если он не существует
        user_data[user_id] = {'yourBal': 8000000000 / 2}
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file)

app = web.Application()
app.add_routes([web.get('/referral/{token}', handle_referral)])

if __name__ == '__main__':
    web.run_app(app, port=8080)
