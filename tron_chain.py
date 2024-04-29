import aiohttp
import json
import asyncio
import requests
from tronpy import Tron, Contract
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from async_sql_scripts import *
from config import *


async def tron_usdt_check_tx(wallet_address, tx):
    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            result = await response.json()
            tx_status = result['confirmed']
            if tx_status == True:
                tx_data = result['trc20TransferInfo'][0]
                to_address = tx_data['to_address']
                if to_address.lower() == wallet_address.lower():
                    contract_address = tx_data['contract_address']
                    if contract_address.lower() == usdt_contract_tron.lower():
                        decimals = tx_data['decimals']
                        usdt_amount = int(tx_data['amount_str']) / (10 ** decimals)
                        return True, int(usdt_amount), "tron chain"
        return False, 0, "tron chain"


async def tron_trx_check_tx(wallet_address, tx):
    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            result = await response.json()
            tx_status = result['confirmed']
            if tx_status == True:
                tx_data = result['contractData']
                to_address = tx_data['to_address']
                if to_address.lower() == wallet_address.lower():
                    trx_amount = tx_data['amount'] / (10 ** 6)
                    return True, int(trx_amount), "tron chain"
        return False, 0, "tron chain"


async def create_tron_wallet():
    try:
        tron = Tron(network="https://api.trongrid.io")
        account = tron.generate_address()
        wallet_address = account['base58check_address']
        private_key = account['private_key']

        return wallet_address, private_key
    except Exception as e:
        print(f"Error creating tron wallet: {e}")


async def send_trx_for_gas_paying_transaction(user_wallet_address):
    try:
        provider = HTTPProvider(api_key=tron_api_key)
        client = Tron(provider)


        priv_key = PrivateKey(bytes.fromhex(tron_owner_private_key))

        txn = (
            client.trx.transfer(
                tron_owner_wallet,  # from
                user_wallet_address,  # to
                int(transfer_trx_amount_for_fee) * (10 ** 6)  # Amount in Sun (1 TRX = 1_000_000 Sun)
            )
            .memo("Sending TRX for gas pay")
            .build()
            .sign(priv_key)
        )

        result = txn.broadcast()
        print(f"TRC-20 Transaction send. Status: {result['result']}. TX: {result['txid']}")
        if result['result'] == True:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in sending trx to owner wallet: {e}")


async def send_trx_transaction(user_wallet_address, user_private_key):
    try:
        provider = HTTPProvider(api_key=tron_api_key)
        client = Tron(provider)

        priv_key = PrivateKey(bytes.fromhex(user_private_key))
        balance = client.get_account_balance(user_wallet_address)
        amount = int(balance) * (10 ** 6) - 3_000_000

        txn = (
            client.trx.transfer(
                user_wallet_address,
                tron_owner_wallet,
                amount
            )
            .memo("Sending TRX")
            .build()
            .sign(priv_key)
        )

        result = txn.broadcast()
        print(f"TRC-20 Transaction send. Status: {result['result']}. TX: {result['txid']}")
        if result['result'] == True:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in sending trx to owner wallet: {e}")


async def send_usdt_tron_transaction(usdt_amount, user_wallet_address, user_private_key):
    try:
        provider = HTTPProvider(api_key=tron_api_key)
        client = Tron(provider)

        priv_key = PrivateKey(bytes.fromhex(user_private_key))

        usdt_contract = client.get_contract(usdt_contract_tron)
        usdt_contract_abi = client.get_contract(usdt_contract_tron)

        usdt_format = int(usdt_amount) * 1_000_000

        txn = (
            usdt_contract.functions.transfer(
                tron_owner_wallet,
                usdt_format
            )
            .with_owner(user_wallet_address)
            .fee_limit(35_000_000)
            .build()
            .sign(priv_key)
        )

        result = txn.broadcast()
        print(f"TRC-20 USDT Transaction send. Status: {result['result']}. TX: {result['txid']}")
        if result['result'] == True:
            return True
        else:
            return False
    except Exception as error:
        print(f"Error in sending usdt tron to owner wallet: {error}")


async def send_rest_trx_to_trnsf_wallet(user_wallet_address, user_private_key):
    try:
        provider = HTTPProvider(api_key=tron_api_key)
        client = Tron(provider)

        priv_key = PrivateKey(bytes.fromhex(user_private_key))

        balance = client.get_account_balance(user_wallet_address)
        amount = int(balance) * (10 ** 6) - 3_000_000

        txn = (
            client.trx.transfer(
                user_wallet_address,
                tron_owner_wallet,
                amount
            )
            .memo("Sending TRX")
            .build()
            .sign(priv_key)
        )

        result = txn.broadcast()
        print(f"TRC-20 Transaction send. Status: {result['result']}. TX: {result['txid']}")
        if result['result'] == True:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in sending trx to owner wallet: {e}")
