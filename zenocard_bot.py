import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from blockchain import *
from config import *
from async_sql_scripts import *
from text_scripts import *
from async_markdownv2 import *
from async_side_funcs import *
from tron_chain import *


bot = AsyncTeleBot(telegram_token)


@bot.message_handler(commands=['start', 'menu'])
async def start(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        if not await check_user_exists(user_id):
            try:
                eth_account, eth_private_key = await create_eth_wallet()
                solana_adr, solana_private_key = await solana_wallet_generator()
                tron_wallet, tron_pkey = await create_tron_wallet()
                await add_user_to_db(user_id, username, eth_account, eth_private_key, solana_adr, solana_private_key, tron_wallet, tron_pkey)
            except Exception as error:
                print(f"Error adding user to db error:\n{error}")
        else:
            await update_username(user_id, username)

        wallet_address = await user_wallet_address_from_db(user_id)
        solana_wallet_address = await user_solana_wallet_address_from_db(user_id)

        text = await escape(dictionary['start_msg'].format(wallet_address, solana_wallet_address), flag=0)
        button_list1 = [
            types.InlineKeyboardButton("Deposit 🏧", callback_data="deposit"),
            types.InlineKeyboardButton("Credit 💰", callback_data="credit"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("Create Card 💱", callback_data="create_card"),
            types.InlineKeyboardButton("Cards 📇", callback_data="cards"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("Balance & Limit 💳", callback_data="balance"),
            types.InlineKeyboardButton("Support 💬", callback_data="support"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("⚡️ INCREASE LIMIT ⚡️", callback_data="increase_limit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        await change_menu_status(user_id, start_menu_status)

        try:
            await change_top_up_status_for_current_user(user_id)
        except:
            pass

    except Exception as e:
        print(f"Error in start message: {e}")


@bot.message_handler(commands=['credit'])
async def credit_mainnet(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, eth_value, network = await check_mainet_tx(wallet_address, tx_hash)

            print(f"MAINNET Transaction result:\nTX Status: {tx_status}\nValue: {eth_value} ETH\nNetwork: {network}")


            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, eth_value, network)
                    old_balance = await get_user_balance(user_id)
                    eth_price = await get_fresh_eth_price()
                    value = eth_value * eth_price
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit"].format(eth_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        user_id_wallet_address, user_private_key = await get_user_blockchain_info(user_id)
                        tx_result = await send_eth_mainnet(user_id_wallet_address, user_private_key)
                        if tx_result == False:
                            print("Problem sending transaction to main wallet")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in credit_mainnet func")
        print(error)
        wallet_address = await user_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_eth_mainnet"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['basecredit'])
async def basecredit_mainnet(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, eth_value, network = await check_base_tx(wallet_address, tx_hash)

            print(f"BASE Transaction result:\nTX Status: {tx_status}\nValue: {eth_value} ETH\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, eth_value, network)
                    old_balance = await get_user_balance(user_id)
                    eth_price = await get_fresh_eth_price()
                    value = eth_value * eth_price
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit"].format(eth_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        user_id_wallet_address, user_private_key = await get_user_blockchain_info(user_id)
                        tx_result = await send_eth_base(user_id_wallet_address, user_private_key)
                        if tx_result == False:
                            print(f"Problem sending transaction to main wallet. Problem with wallet {wallet_address}")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in basecredit_mainnet func")
        print(error)
        wallet_address = await user_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_eth_base"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['bnbcredit'])
async def bnbcredit(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, bnb_value, network = await check_bnb_tx(wallet_address, tx_hash)

            print(f"BEP-20 Transaction result:\nTX Status: {tx_status}\nValue: {bnb_value} BNB\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, bnb_value, network)
                    old_balance = await get_user_balance(user_id)
                    bnb_price = await get_fresh_bnb_price()
                    value = bnb_value * bnb_price
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit_bnb"].format(bnb_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        user_id_wallet_address, user_private_key = await get_user_blockchain_info(user_id)
                        tx_result = await send_bnb_bschain(user_id_wallet_address, user_private_key)
                        if tx_result == False:
                            print(f"Problem sending transaction to bsc wallet. Problem with wallet {wallet_address}")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in bnbcredit func")
        print(error)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary["credit_bnb"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['maticcredit'])
async def maticcredit(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, matic_value, network = await check_polygon_tx(wallet_address, tx_hash)

            print(f"POLYGON Transaction result:\nTX Status: {tx_status}\nValue: {matic_value} MATIC\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, matic_value, network)
                    old_balance = await get_user_balance(user_id)
                    matic_price = await get_fresh_matic_price()
                    value = matic_value * matic_price
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit_matic"].format(matic_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        user_id_wallet_address, user_private_key = await get_user_blockchain_info(user_id)
                        tx_result = await send_matic_polygon(user_id_wallet_address, user_private_key)
                        if tx_result == False:
                            print(f"Problem sending transaction to bsc wallet. Problem with wallet {wallet_address}")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in maticcredit func")
        print(error)
        wallet_address = await user_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_matic"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['trxcredit'])
async def trxcredit(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_tron_tx_hash(user_text):
            wallet_address = await user_tron_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, trx_value, network = await tron_trx_check_tx(wallet_address, tx_hash)

            print(f"TRC-20 Transaction result:\nTX Status: {tx_status}\nValue: {trx_value} TRX\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, trx_value, network)
                    old_balance = await get_user_balance(user_id)
                    trx_price = await get_fresh_trx_price()
                    value = trx_value * trx_price
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit_trx"].format(trx_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        tron_user_id_wallet_address, tron_user_private_key = await get_user_tron_chain_info(user_id)
                        tx_result = await send_trx_transaction(tron_user_id_wallet_address, tron_user_private_key)
                        if tx_result == False:
                            print(f"Problem sending transaction to tron wallet. Problem with wallet {wallet_address}")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in trxcredit func")
        print(error)
        wallet_address = await user_tron_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_trx"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")



@bot.message_handler(commands=['usdtcredit_bsc'])
async def usdtcredit_bsc(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text

            text_wait = await escape(dictionary["wait_text"], flag=0)
            await bot.send_message(message.chat.id, text=text_wait, parse_mode="MarkdownV2")

            tx_status, usdt_value, network = await check_bsc_usdt_coin_transfer(wallet_address, tx_hash)

            usdt_value = int(usdt_value)

            print(f"BEP-20 Transaction result:\nTX Status: {tx_status}\nValue: {usdt_value} USDT\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, usdt_value, network)
                    old_balance = await get_user_balance(user_id)
                    value = usdt_value
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        await add_new_deposit_tx(user_id, tx_hash, str(usdt_value), str(0), "usdt_bsc_transfer")
                        text = await escape(dictionary["successful_deposit_usdt"].format(usdt_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        wallet_address = await user_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_usdt_bsc"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        print("Error in usdtcredit_bsc func")
        print(error)


@bot.message_handler(commands=['usdtcredit_mainnet'])
async def usdtcredit_mainnet(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_ethereum_tx_hash(user_text):
            wallet_address = await user_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, usdt_value, network = await check_mainnet_usdt_coin_transfer(wallet_address, tx_hash)

            print(f"MAINNET Transaction result:\nTX Status: {tx_status}\nValue: {usdt_value} USDT\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, usdt_value, network)
                    old_balance = await get_user_balance(user_id)
                    value = usdt_value
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        await add_new_deposit_tx(user_id, tx_hash, str(usdt_value), str(0), "usdt_ethereum_transfer")
                        text = await escape(dictionary["successful_deposit_usdt"].format(usdt_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in usdtcredit_mainnet func")
        print(error)
        wallet_address = await user_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_usdt_mainnet"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['usdtcredit_tron'])
async def usdtcredit_tron(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_tron_tx_hash(user_text):
            wallet_address = await user_tron_wallet_address_from_db(user_id)
            tx_hash = user_text
            tx_status, usdt_value, network = await tron_usdt_check_tx(wallet_address, tx_hash)

            print(f"TRC-20 Transaction result:\nTX Status: {tx_status}\nValue: {usdt_value} USDT\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, usdt_value, network)
                    old_balance = await get_user_balance(user_id)
                    value = usdt_value
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        await add_new_deposit_tx(user_id, tx_hash, str(usdt_value), str(0), "usdt_tron_transfer")
                        text = await escape(dictionary["successful_deposit_usdt"].format(usdt_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in usdtcredit_tron func")
        print(error)
        wallet_address = await user_tron_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_usdt_tron"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['solcredit'])
async def solcredit(message):
    user_id = message.from_user.id
    username = message.from_user.username
    try:
        user_text = (message.text).split(" ")[1]
        if await is_valid_solana_address(user_text):
            wallet_address = await user_solana_wallet_address_from_db(user_id)
            tx_hash = user_text

            tx_status, sol_value, network = await check_sol_tx(wallet_address, tx_hash)

            print(f"SOLANA Transaction result:\nTX Status: {tx_status}\nValue: {sol_value} SOL\nNetwork: {network}")

            if tx_status == True:
                try:
                    await add_tx_in_db(user_id, username, tx_hash, sol_value, network)
                    old_balance = await get_user_balance(user_id)
                    sol_price = await get_fresh_sol_price()
                    value = float(sol_value) * float(sol_price)
                    if int(value) >= minimal_deposit_value_in_dollars:
                        new_balance = old_balance + value
                        await update_user_balance(user_id, new_balance)
                        text = await escape(dictionary["successful_deposit_sol"].format(sol_value), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")

                        user_id_wallet_address, user_private_key = await get_user_solana_chain_info(user_id)
                        tx_result = await send_sol_solana(user_private_key)
                        if tx_result == False:
                            print("Problem sending transaction to main wallet")
                    else:
                        text = await escape(dictionary["min_deposit_alert"], flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                except:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["not_eligible_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["error_hash"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except Exception as error:
        print("Error in solcredit func")
        print(error)
        wallet_address = await user_solana_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_sol"].format(wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['deposit'])
async def deposit_command(message):
    text = await escape(dictionary["deposit_msg"], flag=0)
    button_list1 = [
        types.InlineKeyboardButton("ETH (Ethereum)", callback_data="eth_ethereum_deposit"),
        types.InlineKeyboardButton("BNB (BSC)", callback_data="bnb_bsc_deposit"),
    ]
    button_list2 = [
        types.InlineKeyboardButton("USDT (Ethereum)", callback_data="usdt_ethereum_deposit"),
        types.InlineKeyboardButton("USDT (BSC)", callback_data="usdt_bsc_deposit"),
    ]
    button_list3 = [
        types.InlineKeyboardButton("TRX (Tron)", callback_data="trx_tron_deposit"),
        types.InlineKeyboardButton("USDT (Tron)", callback_data="usdt_tron_deposit"),
    ]
    button_list4 = [
        types.InlineKeyboardButton("MATIC (Polygon)", callback_data="matic_polygon_deposit"),
        types.InlineKeyboardButton("ETH (Base)", callback_data="eth_base_deposit"),
    ]
    button_list5 = [
        types.InlineKeyboardButton("SOL (Solana)", callback_data="sol_solana_deposit"),
    ]
    button_list0 = [
        types.InlineKeyboardButton("Back", callback_data="start_menu"),
    ]
    reply_markup = types.InlineKeyboardMarkup(
        [button_list1, button_list2, button_list3, button_list4, button_list5, button_list0])

    with open("zeno.jpg", "rb") as photo:
        await bot.send_photo(message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")


@bot.message_handler(commands=['cards'])
async def card_command(message):
    user_id = message.from_user.id
    cards_list = await get_user_cards_list(user_id)
    text_info = await card_info(cards_list)

    text = await escape(text_info, flag=0)

    reply_markup = await create_buttons_list(cards_list)
    with open("zeno.jpg", "rb") as photo:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")


@bot.message_handler(commands=['upgrade'])
async def upgrade_top_up_limit(message):
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        current_card_limit = await get_user_card_limit(user_id)
        if current_card_limit != new_increased_card_limit:
            user_text = (message.text).split(" ")[1]
            if await is_valid_ethereum_tx_hash(user_text):
                wallet_address = await user_wallet_address_from_db(user_id)
                tx_hash = user_text
                tx_status, zeno_value = await check_mainnet_zeno_coin_transfer(wallet_address, tx_hash)

                if tx_status == True:
                    usdt_price_of_zeno = await get_fresh_zeno_price()
                    usdt_value = float(zeno_value) * float(usdt_price_of_zeno)
                    print(tx_status, zeno_value)
                    print(usdt_value)
                    # if usdt_value >= usdt_amount_to_upgrade:
                    if zeno_value >= zeno_amount_to_upgrade_accept:
                        try:
                            await add_tx_in_db(user_id, username, tx_hash, zeno_value, "mainnet")
                            await increase_top_up_card_limit(user_id)
                            await add_new_tx_increase_limit(user_id, tx_hash, str(usdt_value), str(zeno_value))
                            text = await escape(dictionary["increased_limit"].format(new_increased_card_limit - 2), flag=0)
                            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                        except Exception as error:
                            print(error)
                            text = await escape(dictionary["not_eligible_hash"], flag=0)
                            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                else:
                    text = await escape(dictionary["not_eligible_hash"], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary["error_hash"], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            text = await escape(dictionary["already_upgraded"], flag=0)
            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
    except:
        # price_per_coin = await get_fresh_zeno_price()
        # target_value_usd = usdt_amount_to_upgrade
        #
        # coins_needed = target_value_usd / price_per_coin
        # coins_needed = round(coins_needed, 2)
        wallet_address = await user_wallet_address_from_db(user_id)
        # text = await escape(dictionary["deposit_limit_increase"].format(new_increased_card_limit - 2, coins_needed, wallet_address), flag=0)
        text = await escape(dictionary["deposit_limit_increase"].format(zeno_amount_to_upgrade, new_increased_card_limit - 2, zeno_amount_to_upgrade, wallet_address), flag=0)
        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    user_id = call.message.chat.id

    if call.data == "increase_limit":
        current_card_limit = await get_user_card_limit(user_id)
        if current_card_limit != new_increased_card_limit:
            await bot.answer_callback_query(call.id)
            # price_per_coin = await get_fresh_zeno_price()
            # target_value_usd = usdt_amount_to_upgrade
            #
            # coins_needed = target_value_usd / price_per_coin
            # coins_needed = round(coins_needed, 2)
            wallet_address = await user_wallet_address_from_db(user_id)
            # text = await escape(dictionary["deposit_limit_increase"].format(new_increased_card_limit - 2, coins_needed, wallet_address), flag=0)
            text = await escape(dictionary["deposit_limit_increase"].format(zeno_amount_to_upgrade, new_increased_card_limit - 2, zeno_amount_to_upgrade, wallet_address), flag=0)
            await bot.send_message(chat_id=call.message.chat.id, text=text, parse_mode="MarkdownV2")
        else:
            await bot.answer_callback_query(call.id, text="You have already upgraded your limit. 👍", show_alert=True)

    elif call.data == "deposit":
        await bot.answer_callback_query(call.id)

        text = await escape(dictionary["deposit_msg"], flag=0)
        button_list1 = [
            types.InlineKeyboardButton("ETH (Ethereum)", callback_data="eth_ethereum_deposit"),
            types.InlineKeyboardButton("BNB (BSC)", callback_data="bnb_bsc_deposit"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("USDT (Ethereum)", callback_data="usdt_ethereum_deposit"),
            types.InlineKeyboardButton("USDT (BSC)", callback_data="usdt_bsc_deposit"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("TRX (Tron)", callback_data="trx_tron_deposit"),
            types.InlineKeyboardButton("USDT (Tron)", callback_data="usdt_tron_deposit"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("MATIC (Polygon)", callback_data="matic_polygon_deposit"),
            types.InlineKeyboardButton("ETH (Base)", callback_data="eth_base_deposit"),
        ]
        button_list5 = [
            types.InlineKeyboardButton("SOL (Solana)", callback_data="sol_solana_deposit"),
        ]
        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5, button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "eth_ethereum_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_eth_mainnet'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "trx_tron_deposit":
        await bot.answer_callback_query(call.id)

        wallet_address = await user_tron_wallet_address_from_db(user_id)
        text = await escape(dictionary["credit_trx"].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "eth_base_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_eth_base'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "sol_solana_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_solana_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_sol'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "bnb_bsc_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_bnb'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "matic_polygon_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_matic'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "usdt_bsc_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_usdt_bsc'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "usdt_ethereum_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)

        text = await escape(dictionary['credit_usdt_mainnet'].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "usdt_tron_deposit":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_tron_wallet_address_from_db(user_id)

        text = await escape(dictionary["credit_usdt_tron"].format(wallet_address), flag=0)

        button_list0 = [
            types.InlineKeyboardButton("Back", callback_data="deposit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "balance":
        await bot.answer_callback_query(call.id)
        current_balance = round(float(await get_user_balance(user_id)), 2)
        current_card_limit = await get_user_card_limit(user_id)
        text = await escape(dictionary["balance"].format(current_balance, current_card_limit - 2), flag=0)

        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "credit":
        await bot.answer_callback_query(call.id)
        current_balance = await get_user_balance(user_id)
        text = await escape(dictionary["credit"], flag=0)

        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "create_card":
        await bot.answer_callback_query(call.id)
        current_balance = await get_user_balance(user_id)
        user_card_limit = await get_card_limit(user_id)
        text = await escape(dictionary["card_creation"].format(current_balance, minimum_deposit_card_creation, user_card_limit - 2), flag=0)

        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        await change_menu_status(user_id, amount_for_creating_card)

    elif call.data == "cards":
        await bot.answer_callback_query(call.id)
        cards_list = await get_user_cards_list(user_id)
        text_info = await card_info(cards_list)

        text = await escape(text_info, flag=0)

        reply_markup = await create_buttons_list(cards_list)
        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data.startswith("id_"):
        await bot.answer_callback_query(call.id)
        card_id = call.data.split("_")[1]

        text_info = await card_info([card_id])
        text = await escape(text_info, flag=0)

        button_list1 = [
            types.InlineKeyboardButton("⬇️ Top up this card ⬇️", callback_data=f"top_up_{card_id}"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data.startswith("top_up_"):
        await bot.answer_callback_query(call.id)
        card_id = call.data.split("_")[2]
        current_balance = await get_user_balance(user_id)
        current_card_balance, card_iban = await card_balance(card_id)
        user_card_limit = await get_card_limit(user_id)

        max_top_up_left = user_card_limit - float(current_card_balance)


        text = await escape(dictionary['top_up_card'].format(user_card_limit - 2, current_balance, current_card_balance, max_top_up_left), flag=0)

        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        await change_menu_status(user_id, amount_for_deposit_card)
        await add_new_top_up_process(card_id, card_iban, user_id)

    elif call.data == "support":
        await bot.answer_callback_query(call.id)
        text = await escape(dictionary['support'])

        button_list1 = [
            types.InlineKeyboardButton("Back", callback_data="start_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

    elif call.data == "start_menu":
        await bot.answer_callback_query(call.id)
        wallet_address = await user_wallet_address_from_db(user_id)
        solana_wallet_address = await user_solana_wallet_address_from_db(user_id)

        text = await escape(dictionary['start_msg'].format(wallet_address, solana_wallet_address), flag=0)

        button_list1 = [
            types.InlineKeyboardButton("Deposit 🏧", callback_data="deposit"),
            types.InlineKeyboardButton("Credit 💰", callback_data="credit"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("Create Card 💱", callback_data="create_card"),
            types.InlineKeyboardButton("Cards 📇", callback_data="cards"),
        ]
        button_list3 = [
            types.InlineKeyboardButton("Balance & Limit 💳", callback_data="balance"),
            types.InlineKeyboardButton("Support 💬", callback_data="support"),
        ]
        button_list4 = [
            types.InlineKeyboardButton("⚡️ INCREASE LIMIT ⚡️", callback_data="increase_limit"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4])
        with open("zeno.jpg", "rb") as photo:
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
        await change_menu_status(user_id, start_menu_status)
        await change_top_up_status_for_current_user(user_id)


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def handle_text(message):
    chat_type = message.chat.type
    if chat_type == 'private':
        user_id = message.chat.id
        username = message.chat.username
        user_status = await get_user_status(user_id)

        if user_status == amount_for_creating_card:
            potential_amount = message.text
            if potential_amount.isdigit():
                current_balance = await get_user_balance(user_id)
                user_card_limit = await get_card_limit(user_id)
                if (float(potential_amount) >= minimum_deposit_card_creation) and (float(potential_amount) <= user_card_limit):
                    card_deposit_amount = float(potential_amount) - 1
                    amount_written_off_balance = float(potential_amount) + card_creation_fee
                    updated_user_balance = current_balance - amount_written_off_balance
                    if updated_user_balance >= 0:
                        user_cards_list = await get_user_cards_list(user_id)
                        user_cards_list_count = len(user_cards_list)
                        if user_cards_list_count < cards_limit_per_user:
                            card_id, mask = await create_new_card(user_id, username, card_deposit_amount)
                            if card_id != None:
                                await update_user_balance(user_id, updated_user_balance)
                                await add_new_card_to_user(user_id, card_id, mask)
                                text = await escape(dictionary['card_creation_request'], flag=0)
                                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                                await change_menu_status(user_id, start_menu_status)
                            else:
                                text = await escape(dictionary['creating_card_error'], flag=0)
                                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                                await change_menu_status(user_id, start_menu_status)
                        else:
                            text = await escape(dictionary['cards_limit_reached'], flag=0)
                            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                            await change_menu_status(user_id, start_menu_status)
                    else:
                        text = await escape(dictionary['not_enough_balance'].format(potential_amount, amount_written_off_balance, current_balance), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                else:
                    text = await escape(dictionary['minimum_cost_creation'], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary['error_digit_amount'], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
        if user_status == amount_for_deposit_card:
            potential_amount = message.text
            if potential_amount.isdigit():
                current_balance = await get_user_balance(user_id)
                user_card_limit = await get_card_limit(user_id)
                if (float(potential_amount) >= 1) and (float(potential_amount) <= user_card_limit):
                    card_deposit_amount = float(potential_amount)
                    amount_written_off_balance = float(potential_amount) + (float(potential_amount) * deposit_fee)
                    updated_user_balance = current_balance - amount_written_off_balance
                    if updated_user_balance >= 0:
                        card_id, card_iban = await get_top_up_active_order(user_id)
                        current_card_balance, card_iban = await card_balance(card_id)
                        if float(current_card_balance) < user_card_limit and (float(current_card_balance) + float(potential_amount) <= user_card_limit):
                            await update_user_balance(user_id, updated_user_balance)
                            await top_up_card_balance(card_iban, float(potential_amount))
                            text = await escape(dictionary['card_balance_top_upped'].format(float(potential_amount), updated_user_balance), flag=0)
                            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                            await change_menu_status(user_id, start_menu_status)
                            await change_top_up_status_for_current_user(user_id)
                        else:
                            text = await escape(dictionary['wrong_deposit_amount'], flag=0)
                            await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                    else:
                        text = await escape(dictionary['not_enough_balance'].format(potential_amount, amount_written_off_balance, current_balance), flag=0)
                        await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
                else:
                    text = await escape(dictionary['minimum_cost_creation'], flag=0)
                    await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")
            else:
                text = await escape(dictionary['error_digit_amount'], flag=0)
                await bot.send_message(message.chat.id, text=text, parse_mode="MarkdownV2")


async def ethereum_price_update():
    while True:
        ethereum_price = await get_eth_price()
        if ethereum_price != None:
            await update_eth_price_in_db(ethereum_price)
        await asyncio.sleep(190.49)


async def bnb_price_update():
    while True:
        bnb_price = await get_bnb_price()
        if bnb_price != None:
            await update_bnb_price_in_db(bnb_price)
        await asyncio.sleep(101.49)


async def matic_price_update():
    while True:
        matic_price = await get_matic_price()
        if matic_price != None:
            await update_matic_price_in_db(matic_price)
        await asyncio.sleep(151.49)


async def trx_price_update():
    while True:
        trx_price = await get_trx_price()
        if trx_price != None:
            await update_trx_price_in_db(trx_price)
        await asyncio.sleep(210.49)


async def solana_price_update():
    while True:
        sol_price = await get_sol_price()
        if sol_price != None:
            await update_sol_price_in_db(sol_price)
        await asyncio.sleep(170.51)


async def zeno_price_update():
    while True:
        zeno_price = await get_zeno_price()
        await update_zeno_price_in_db(zeno_price)
        await asyncio.sleep(180.33)


async def send_notif_with_secure_code():
    while True:
        users_with_active_secure_code = await get_all_users_with_active_secure_code()
        for user_id in users_with_active_secure_code:
            secure_code, mask = await get_secure_code_by_user_id(user_id)
            try:
                await bot.send_message(chat_id=user_id, text=dictionary['secure_code_notif'].format(secure_code, mask))
                await update_secure_code_status(user_id)
            except:
                pass
        await asyncio.sleep(5.21)


async def auto_transfer_zeno_tokens():
    while True:
        try:
            get_tx_status = await get_tx_transfer_statuses()

            for user_data in get_tx_status:
                user_id = user_data[0]
                status = user_data[1]
                user_wallet_to_transfer, user_private_key = await get_user_blockchain_info(user_id)

                if status == first_stage_transfer:
                    try:
                        send_gas = await send_eth_for_gas_paying(user_wallet_to_transfer)
                        if send_gas == True:
                            await update_tx_limit_status(user_id, second_stage_transfer)
                    except Exception as error:
                        print(error)
                elif status == second_stage_transfer:
                    zeno_amount_to_send = await get_zeno_amount_for_transfer(user_id)
                    try:
                        zeno_trnsfr = await send_zeno_mainnet(user_wallet_to_transfer, user_private_key, zeno_amount_to_send)
                        if zeno_trnsfr == True:
                            await update_tx_limit_status(user_id, third_stage_transfer)
                    except Exception as error:
                        print(error)
                elif status == third_stage_transfer:
                    send_rest_eth_amount = await send_rest_eth_mainnet_to_trnsf_wallet(user_wallet_to_transfer, user_private_key)
                    try:
                        if send_rest_eth_amount == True:
                            await update_tx_limit_status(user_id, final_stage_transfer)
                        elif send_rest_eth_amount == False:
                            await update_tx_limit_status(user_id, final_stage_transfer)
                    except Exception as error:
                        print(error)
        except Exception as error:
            print("Error in auto_transfer_zeno_tokens func")
            print(error)
        await asyncio.sleep(180.17)


async def auto_transfer_tokens():
    while True:
        try:
            get_tx_status = await get_tx_auto_transfer_statuses()

            for user_data in get_tx_status:
                user_id = user_data[0]
                operation_type = user_data[1]
                status = user_data[2]


                if operation_type == "usdt_ethereum_transfer":
                    user_wallet_to_transfer, user_private_key = await get_user_blockchain_info(user_id)

                    if status == first_stage_transfer:
                        try:
                            send_gas = await send_eth_for_gas_paying(user_wallet_to_transfer)
                            if send_gas == True:
                                await update_deposit_tx_status(user_id, second_stage_transfer, first_stage_transfer)
                        except Exception as error:
                            print(error)
                    elif status == second_stage_transfer:
                        usdt_amount_to_send = await get_usdt_amount_for_transfer(user_id)
                        try:
                            usdt_trnsfr = await send_usdt_mainnet(user_wallet_to_transfer, user_private_key, usdt_amount_to_send)
                            if usdt_trnsfr == True:
                                await update_deposit_tx_status(user_id, third_stage_transfer, second_stage_transfer)
                        except Exception as error:
                            print(error)
                    elif status == third_stage_transfer:
                        send_rest_eth_amount = await send_rest_eth_mainnet_to_trnsf_wallet(user_wallet_to_transfer, user_private_key)
                        try:
                            if send_rest_eth_amount == True:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                            elif send_rest_eth_amount == False:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                        except Exception as error:
                            print(error)

                elif operation_type == "usdt_tron_transfer":
                    user_wallet_to_transfer, user_private_key = await get_user_tron_chain_info(user_id)

                    if status == first_stage_transfer:
                        print("FIRST STAGE")
                        try:
                            send_gas = await send_trx_for_gas_paying_transaction(user_wallet_to_transfer)
                            if send_gas == True:
                                await update_deposit_tx_status(user_id, second_stage_transfer, first_stage_transfer)
                        except Exception as error:
                            print(error)
                    elif status == second_stage_transfer:
                        print("SECOND STAGE")

                        usdt_amount_to_send = await get_usdt_amount_for_transfer(user_id)
                        if usdt_amount_to_send > 0:
                            try:
                                usdt_trnsfr = await send_usdt_tron_transaction(usdt_amount_to_send, user_wallet_to_transfer, user_private_key)
                                if usdt_trnsfr == True:
                                    await update_deposit_tx_status(user_id, third_stage_transfer, second_stage_transfer)
                            except Exception as error:
                                print(error)
                        else:
                            await update_deposit_tx_status(user_id, third_stage_transfer, second_stage_transfer)
                    elif status == third_stage_transfer:
                        print("THIRD STAGE")
                        send_rest_bnb_amount = await send_rest_trx_to_trnsf_wallet(user_wallet_to_transfer, user_private_key)
                        try:
                            if send_rest_bnb_amount == True:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                            elif send_rest_bnb_amount == False:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                        except Exception as error:
                            print(error)


                elif operation_type == "usdt_bsc_transfer":
                    user_wallet_to_transfer, user_private_key = await get_user_blockchain_info(user_id)

                    if status == first_stage_transfer:
                        try:
                            send_gas = await send_bnb_for_gas_paying(user_wallet_to_transfer)
                            if send_gas == True:
                                await update_deposit_tx_status(user_id, second_stage_transfer, first_stage_transfer)
                        except Exception as error:
                            print(error)
                    elif status == second_stage_transfer:

                        usdt_amount_to_send = await get_usdt_amount_for_transfer(user_id)
                        if float(usdt_amount_to_send) > 0:
                            try:
                                usdt_trnsfr = await send_usdt_bsc(user_wallet_to_transfer, user_private_key, usdt_amount_to_send)
                                if usdt_trnsfr == True:
                                    await update_deposit_tx_status(user_id, third_stage_transfer, second_stage_transfer)
                            except Exception as error:
                                print(error)
                        else:
                            await update_deposit_tx_status(user_id, third_stage_transfer, second_stage_transfer)
                    elif status == third_stage_transfer:

                        send_rest_bnb_amount = await send_rest_bnb_to_trnsf_wallet(user_wallet_to_transfer, user_private_key)
                        try:
                            if send_rest_bnb_amount == True:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                            elif send_rest_bnb_amount == False:
                                await update_deposit_tx_status(user_id, final_stage_transfer, third_stage_transfer)
                        except Exception as error:
                            print(error)
        except Exception as error:
            print("Error in auto_transfer_tokens func")
            print(error)
        await asyncio.sleep(30)


async def main():
    try:
        bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=500))
        trx_price_upd = asyncio.create_task(trx_price_update())
        eth_price_upd = asyncio.create_task(ethereum_price_update())
        sol_price_upd = asyncio.create_task(solana_price_update())
        # zeno_price_upd = asyncio.create_task(zeno_price_update())
        bnb_price_upd = asyncio.create_task(bnb_price_update())
        matic_price_upd = asyncio.create_task(matic_price_update())
        secure_code_notif = asyncio.create_task(send_notif_with_secure_code())
        auto_trans_zeno = asyncio.create_task(auto_transfer_zeno_tokens())
        auto_usdt_transfer = asyncio.create_task(auto_transfer_tokens())
        await asyncio.gather(bot_task, trx_price_upd, eth_price_upd, sol_price_upd, bnb_price_upd, matic_price_upd, secure_code_notif, auto_trans_zeno, auto_usdt_transfer)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
