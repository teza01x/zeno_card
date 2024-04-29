import asyncio
import aiohttp
import requests
import re
import telebot
import json
import base58
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from async_sql_scripts import *
from blockchain import *


async def is_valid_ethereum_tx_hash(tx_hash):
    pattern = r'^0x[a-fA-F0-9]{64}$'
    match = re.match(pattern, tx_hash)
    return bool(match)


async def is_valid_solana_address(tx_hash):
    if 80 < len(tx_hash) < 100:
        return True
    else:
        return False


async def is_valid_tron_tx_hash(tx_hash):
    pattern = r'^(0x)?[a-fA-F0-9]{64}$'
    match = re.match(pattern, tx_hash)
    return bool(match)


async def top_up_card_balance(card_iban, topup_amount):
    url = "https://api.pst.net/integration/transfer/transfer"
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {pst_api_key}",
        'X-CSRF-TOKEN': ''
    }

    data = {
        "from_account_id": 3051867,
        "to_account_iban": f"{card_iban}",
        "amount": f"{topup_amount}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                print(response_data)
            else:
                print(f"Error top up card balance: {response.status}, {await response.text()}")


async def get_full_list_of_cards():
    url = 'https://api.pst.net/integration/user/card'
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {pst_api_key}",
        'X-CSRF-TOKEN': ''
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                data = response_data['data']
                return data
            else:
                print(f"Error get list of cards: {response.status}, {await response.text()}")


async def create_new_card(user_id, username, start_balance):
    url = 'https://api.pst.net/integration/user/card/buy'
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {pst_api_key}",
        'X-CSRF-TOKEN': ''
    }

    data = {
            "account_id": 3051867,
            "start_balance": f"{start_balance}",
            "description": f"user_id: {user_id}, username: {username}",
            "system": 4,
            "type": "ultima"
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                data = response_data['data']
                card_id = data['id']
                mask = data['mask'][-4::]
                return card_id, mask
            else:
                print(f"Error creating card: {response.status}, {await response.text()}")


async def card_info(list_of_cards):
    result_info_list = list()
    for card_id in list_of_cards:
        url = f'https://api.pst.net/integration/user/card/{card_id}'
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {pst_api_key}",
            'X-CSRF-TOKEN': ''
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    card_data = response_data['data']
                    card_id = card_data['id']
                    card_name = card_data['holder_name']
                    card_address = card_data['holder_address']
                    card_balance = card_data['account']['balance']
                else:
                    print(f"Error creating card: {response.status}, {await response.text()}")

        url_showpan = f"https://api.pst.net/integration/user/card/{card_id}/showpan"
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {pst_api_key}",
            'X-CSRF-TOKEN': ''
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url_showpan, headers=headers) as response:
                if response.status == 200:
                    response_data_showpan = await response.json()
                    card_showpan = response_data_showpan['data']
                    card_number = card_showpan['number']
                    card_cvv = card_showpan['cvx2']
                    card_exp_month = card_showpan['exp_month']
                    card_exp_year = card_showpan['exp_year']
                else:
                    print(f"Error card info: {response.status}, {await response.text()}")


        card_full_info = (f"**Card: {card_id}**\n\n"
             f"**Name:** `{card_name}`\n"
             f"**Address:** `{card_address}`\n"
             f"**Balance:** `{card_balance}` **USD**\n\n"
             "**Card Info:**⬇️\n\n"
             f"**Card Number:** `{card_number}`\n"
             f"**CVV:** `{card_cvv}`\n"
             f"**Expiration (MMYY):** `{card_exp_month}{card_exp_year}`")


        result_info_list.append(card_full_info)

    result_text = "**Your Zeno Cards**\n\n**=================================**\n\n" + "\n\n**=================================**\n\n".join(result_info_list)
    return result_text


async def card_balance(card_id):
    url = f'https://api.pst.net/integration/user/card/{card_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {pst_api_key}",
        'X-CSRF-TOKEN': ''
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                card_data = response_data['data']
                current_card_balance = card_data['account']['balance']
                iban = card_data['account']['iban']
            else:
                print(f"Error creating card: {response.status}, {await response.text()}")

    return current_card_balance, iban


async def create_buttons_list(ids_list):
    markup = InlineKeyboardMarkup()
    for id in ids_list:
        button = InlineKeyboardButton(text=f"Card ID: {id}", callback_data=f"id_{id}")
        markup.add(button)
    back_button = InlineKeyboardButton(text="Back", callback_data="start_menu")
    markup.add(back_button)

    return markup


# async def add_mask_to_db():
#     data = await get_full_list_of_cards()
#     user_data = await get_all_cards_from_db()
#     for card in data:
#         for user in user_data:
#             if len(user[1]) > 0:
#                 if str(card['id']) in user[1]:
#                     mask = card['mask'][-4::]
#                     await add_new_mask_to_user(user[0], mask)


async def webhook_check():
    url = 'https://api.pst.net/integration/user/webhook'

    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {pst_api_key}",
        'X-CSRF-TOKEN': ''
    }


    data = {
        "url": "http://65.21.58.198/pst",
        "auth_username": "securecodes",
        "auth_password": "securecodes3d",
        "active": True,
        "events": ["transaction.created", "3ds.received", "card.blocked", "card.overdraft", "card.reordered"]
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                print(response_data)
            else:
                print(f"error: {response.status}, {await response.text()}")


async def webhook_send_request():
    url = 'http://65.21.58.198/pst'

    data = json.dumps({'event': '3ds.received', 'data': {'card': {'id': 165417, 'user_account_id': 4000017, 'holder_name': 'Lowell Nader', 'holder_address': '129 Brynhurst Dr, Chelsea, AL 35043, US', 'mask': '485932******1472', 'description': 'user_id: 1789796842, username: cryptobeo', 'favorite': 0, 'status': 1, 'ordered_at': '2024-04-01T00:25:55.000000Z', 'ordered_until': '2024-05-01T00:25:55.000000Z', 'created_at': '2024-03-28T05:33:12.000000Z', 'simple_status': 'active', 'has_waiting_transactions': False, 'account': {'id': 4000017, 'type': 2, 'currency_id': 2, 'iban': '0202488345392412', 'balance': '20.00', 'balance_default': '20.00', 'created_at': '2024-04-01T00:25:55.000000Z', 'updated_at': '2024-04-01T00:25:56.000000Z', 'addresses': [], 'summary': {'positive_transactions_sum': '19.00000000000000000000', 'negative_transactions_sum': '0', 'positive_transactions_count': 1, 'negative_transactions_count': 0}}, 'tariff_id': 11, 'need_amount': False, 'limits_equals': True, 'auto_refill': None, 'tags': [], 'subscription_tariff': {'id': 11, 'renewal': 10, 'type': 10, 'status': 10, 'name': 'Large', 'currency_id': 2, 'amount': '479.00000000000000000000', 'amount_first': '399.00000000000000000000', 'cards_limit': 100, 'cashback_percent': '3.00000000000000000000', 'cashback_limit': '3000.00', 'cashback_spend_limit': '100000.00000000000000000000', 'fee_topup': '3.00', 'allow_api_access': False, 'transaction_fee': '0.00000000000000000000', 'renewal_name': 'MONTHLY', 'type_name': 'MAIN', 'status_name': 'ACTIVE'}}, 'code': 'testcode001'}})

    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                resp = await response.json()
                print("ok")
            else:
                resp = await response.json()
                print(resp)
                print(response.status)


# async def add_solana_wallets():
#     users = await get_all_users()
#
#     for user_id in users:
#         address, private_key = await solana_wallet_generator()
#         print(address, private_key)
#
#         await insert_solana_data(user_id, address, private_key)



