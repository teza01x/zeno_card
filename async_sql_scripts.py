import aiosqlite
import asyncio
from config import *


async def check_user_exists(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
            user = await result.fetchall()
        return bool(len(user))


async def add_user_to_db(user_id, username, eth_address, eth_private_key, solana_adr, solana_private_key):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO user (user_id, username, menu_status, wallet_address, private_wallet_key, cards_id, account_balance, mask, secure_code, code_status, solana_wallet_address, solana_private_key, card_limit) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, username, 0, eth_address, eth_private_key, "", 0, "", "", 0, solana_adr, solana_private_key, 1002))
            await conn.commit()


async def update_username(user_id, username):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET username = ? WHERE user_id = ?", (username, user_id,))
            await conn.commit()


async def user_wallet_address_from_db(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT wallet_address FROM user WHERE user_id = ?", (user_id,))
            wallet = await result.fetchone()
            return wallet[0]


async def user_solana_wallet_address_from_db(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT solana_wallet_address FROM user WHERE user_id = ?", (user_id,))
            wallet = await result.fetchone()
            return wallet[0]


async def update_eth_price_in_db(price):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE eth_price SET eth = ? WHERE status = ?", (price, "current_price",))
            await conn.commit()


async def update_sol_price_in_db(price):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE eth_price SET eth = ? WHERE status = ?", (price, "solana_current_price",))
            await conn.commit()


async def update_zeno_price_in_db(price):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE eth_price SET eth = ? WHERE status = ?", (price, "zeno_current_price",))
            await conn.commit()


async def get_fresh_eth_price():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT eth FROM eth_price WHERE status = ?", ("current_price",))
            price = await result.fetchone()
            return float(price[0])


async def get_fresh_sol_price():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT eth FROM eth_price WHERE status = ?", ("solana_current_price",))
            price = await result.fetchone()
            return float(price[0])


async def get_fresh_zeno_price():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT eth FROM eth_price WHERE status = ?", ("zeno_current_price",))
            price = await result.fetchone()
            return float(price[0])


async def add_tx_in_db(user_id, username, tx_hash, eth_value, network):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO paid_hash (user_id, username, hash, sum_eth, network) VALUES(?, ?, ?, ?, ?)",
                (user_id, username, tx_hash, eth_value, network,))
            await conn.commit()


async def update_user_balance(user_id, value):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET account_balance = ? WHERE user_id = ?", (float(value), user_id,))
            await conn.commit()


async def get_user_balance(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT account_balance FROM user WHERE user_id = ?", (user_id,))
            balance = await result.fetchone()
            return float(balance[0])


async def get_user_blockchain_info(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT wallet_address, private_wallet_key FROM user WHERE user_id = ?", (user_id,))
            info_list = await result.fetchall()
            info = info_list[0]
            return info[0], info[1]


async def get_user_solana_chain_info(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT solana_wallet_address, solana_private_key FROM user WHERE user_id = ?", (user_id,))
            info_list = await result.fetchall()
            info = info_list[0]
            return info[0], info[1]


async def change_menu_status(user_id, status):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET menu_status = ? WHERE user_id = ?", (status, user_id,))
            await conn.commit()


async def get_user_status(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT menu_status FROM user WHERE user_id = ?", (user_id,))
            user_status = await result.fetchone()
            return user_status[0]


async def get_user_cards_list(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT cards_id FROM user WHERE user_id = ?", (user_id,))
            card_list = await result.fetchone()
            result_list = [i for i in card_list[0].split(":") if len(i) > 0]
            return result_list


async def get_user_cards_masks(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT mask FROM user WHERE user_id = ?", (user_id,))
            card_list = await result.fetchone()
            result_list = [i for i in card_list[0].split(":") if len(i) > 0]
            return result_list


async def add_new_card_to_user(user_id, card_id, mask):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            user_card_list = await get_user_cards_list(user_id)
            card_id = str(card_id) + ":"
            user_card_list.append(card_id)
            cards_list_to_update = ":".join(user_card_list)

            user_card_mask = await get_user_cards_masks(user_id)
            card_mask = str(mask) + ":"
            user_card_mask.append(card_mask)
            cards_mask_to_update = ":".join(user_card_mask)

            await cursor.execute("UPDATE user SET cards_id = ?, mask = ? WHERE user_id = ?", (cards_list_to_update, cards_mask_to_update, user_id,))
            await conn.commit()


async def add_new_top_up_process(card_id, card_iban, user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO top_up (card_id, user_id, amount, status, card_iban) VALUES(?, ?, ?, ?, ?)",
                (card_id, user_id, "0", 0, card_iban,))
            await conn.commit()


async def get_top_up_active_order(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT card_id, card_iban FROM top_up WHERE user_id = ? AND status = ?", (user_id, 0,))
            card_info = await result.fetchone()
            return card_info[0], card_info[1]


async def change_top_up_status_for_current_user(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE top_up SET status = ? WHERE user_id = ?", (1, user_id,))
            await conn.commit()


async def get_all_cards_from_db():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            result = await cursor.execute("SELECT user_id, cards_id FROM user")
            card_list = await result.fetchall()
            return card_list


async def add_new_mask_to_user(user_id, mask):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            user_card_mask = await get_user_cards_masks(user_id)
            card_mask = str(mask) + ":"
            user_card_mask.append(card_mask)
            cards_mask_to_update = ":".join(user_card_mask)

            await cursor.execute("UPDATE user SET mask = ? WHERE user_id = ?", (cards_mask_to_update, user_id,))
            await conn.commit()


async def add_new_secure_code(mask, secure_code):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            mask_object = await cursor.execute("SELECT user_id, mask FROM user")
            mask_list = await mask_object.fetchall()
            mask_list = [i for i in mask_list if len(i[1]) > 0]
            for user_info in mask_list:
                if mask in user_info[1]:
                    user_id = user_info[0]
                    break
            await cursor.execute("UPDATE user SET secure_code = ?, code_status = ? WHERE user_id = ?", (secure_code, 1, user_id,))
            await conn.commit()


async def get_all_users_with_active_secure_code():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            list_of_users = await cursor.execute("SELECT user_id FROM user WHERE code_status = ?", (1,))
            users = await list_of_users.fetchall()
            return [i[0] for i in users]


async def get_secure_code_by_user_id(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            fetch_secure_code = await cursor.execute("SELECT secure_code FROM user WHERE user_id = ?", (user_id,))
            secure_info = await fetch_secure_code.fetchone()
            secure_info = secure_info[0].split(":")
            return secure_info[0], secure_info[1]


async def update_secure_code_status(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET code_status = ? WHERE user_id = ?", (0, user_id,))
            await conn.commit()


async def get_all_users():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            fetch_secure_code = await cursor.execute("SELECT user_id FROM user")
            secure_info = await fetch_secure_code.fetchall()
            return [i[0] for i in secure_info]


async def insert_solana_data(user_id, solana_wallet, solana_pkey):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET solana_wallet_address = ?, solana_private_key = ? WHERE user_id = ?", (solana_wallet, solana_pkey, user_id,))
            await conn.commit()


async def get_card_limit(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            card_limit_fetch = await cursor.execute("SELECT card_limit FROM user WHERE user_id = ?", (user_id,))
            card_limit = await card_limit_fetch.fetchone()
            return card_limit[0]


async def increase_top_up_card_limit(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE user SET card_limit = ? WHERE user_id = ?", (new_increased_card_limit, user_id,))
            await conn.commit()


async def add_new_tx_increase_limit(user_id, tx, usdt_value, zeno_value):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO increase_limit_txs (user_id, tx, usdt_value, zeno_value, status) VALUES(?, ?, ?, ?, ?)",
                (user_id, tx, usdt_value, zeno_value, first_stage_transfer))
            await conn.commit()


async def get_tx_transfer_statuses():
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            fetch_user_data = await cursor.execute("SELECT user_id, status FROM increase_limit_txs")
            user_data = await fetch_user_data.fetchall()
            return user_data


async def update_tx_limit_status(user_id, status):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE increase_limit_txs SET status = ? WHERE user_id = ?", (status, user_id,))
            await conn.commit()


async def get_zeno_amount_for_transfer(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            fetch_zeno_value = await cursor.execute("SELECT zeno_value FROM increase_limit_txs WHERE user_id = ?", (user_id,))
            zn_val = await fetch_zeno_value.fetchone()
            return zn_val[0]


async def get_user_card_limit(user_id):
    async with aiosqlite.connect(data_base) as conn:
        async with conn.cursor() as cursor:
            fetch_card_limit = await cursor.execute("SELECT card_limit FROM user WHERE user_id = ?", (user_id,))
            card_limit = await fetch_card_limit.fetchone()
            return card_limit[0]
