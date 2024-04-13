import asyncio
import aiohttp
import requests
import base58
import subprocess
import os
import json
from solders.rpc.responses import GetBalanceResp
from solana.rpc.api import Client
from solders.account import Account
from solders.hash import Hash
from solders.keypair import Keypair
from solders.message import MessageV0
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey
from pathlib import Path
from solana.transaction import Transaction
from solana.rpc.core import RPCException
from solders.signature import Signature
from eth_account import Account
from moralis import evm_api
from web3 import Web3
from config import *


async def create_eth_wallet():
    acct = Account.create()
    private_key = acct.key.hex()
    address = acct.address

    return address, private_key


async def check_mainet_tx(wallet_address, tx_hash):
    txs_url_internal = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={wallet_address}&startblock=0&endblock=999999999&page=1&offset=10000&sort=asc&apikey={etherscan_api_key}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(txs_url_internal)
        if response.status == 200:
            result_list_internal = await response.json()
            for tx in result_list_internal['result']:
                if tx_hash == tx['hash']:
                    if tx["to"].lower() == wallet_address.lower():
                        tx_hash_current = tx["hash"]
                        eth_value = float(tx["value"]) / 10 ** 18
                        return True, eth_value, "mainnet"

    txs_url_native = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={etherscan_api_key}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(txs_url_native)
        if response.status == 200:
            result_list_native = await response.json()
            for tx in result_list_native['result']:
                if tx_hash == tx["hash"]:
                    if tx["to"].lower() == wallet_address.lower():
                        if tx['input'] == '0x':
                            tx_hash_current = tx["hash"]
                            value = float(tx["value"]) / 10 ** 18
                            return True, value, "mainnet"

    return False, 0, "mainnet"


async def check_base_tx(wallet_address, tx_hash):
    txs_url_internal = f"https://api.basescan.org/api?module=account&action=txlistinternal&address={wallet_address}&startblock=0&endblock=999999999&page=1&offset=10000&sort=asc&apikey={basescan_api_key}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(txs_url_internal)
        if response.status == 200:
            result_list_internal = await response.json()
            for tx in result_list_internal['result']:
                if tx_hash == tx['hash']:
                    if tx["to"].lower() == wallet_address.lower():
                        tx_hash_current = tx["hash"]
                        eth_value = float(tx["value"]) / 10 ** 18
                        return True, eth_value, "base network"

    txs_url_native = f"https://api.basescan.org/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={basescan_api_key}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(txs_url_native)
        if response.status == 200:
            result_list_native = await response.json()
            for tx in result_list_native['result']:
                if tx_hash == tx["hash"]:
                    if tx["to"].lower() == wallet_address.lower():
                        if tx['input'] == '0x':
                            tx_hash_current = tx["hash"]
                            value = float(tx["value"]) / 10 ** 18
                            return True, value, "base network"

    return False, 0, "base network"


async def get_eth_price():
    url = "https://api.coingecko.com/api/v3/coins/ethereum"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            result = await response.json()
            return result['market_data']['current_price']['usd']


async def get_sol_price():
    url = "https://api.coingecko.com/api/v3/coins/solana"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            result = await response.json()
            return result['market_data']['current_price']['usd']


async def send_eth_mainnet(user_wallet_address, user_private_key):
    network_rpc_url = "https://mainnet.infura.io/v3/2912045a06ea447fbdfa148c4b4849c1"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    balance = web3.eth.get_balance(user_wallet_address)
    if balance == 0:
        print("Wallet balance is empty")
        return False

    gas_price = web3.eth.gas_price
    gas_limit = 23000
    transaction_fee = gas_price * gas_limit
    amount_to_send = balance - transaction_fee - 1000000000000000


    if amount_to_send <= 0:
        print("Insufficient funds to cover the transaction fee")
        return False

    nonce = web3.eth.get_transaction_count(user_wallet_address)

    tx = {
        'nonce': nonce,
        'to': owner_wallet,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, user_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"The transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True


async def send_bnb_bschain(user_wallet_address, user_private_key):
    network_rpc_url = "https://wider-frequent-fog.bsc.quiknode.pro/074ab0cb5d8c004673247be8132808064b8052d6/"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    balance = web3.eth.get_balance(user_wallet_address)
    if balance == 0:
        print("Wallet balance is empty")
        return False

    gas_price = web3.eth.gas_price
    gas_limit = 21000
    transaction_fee = gas_price * gas_limit
    amount_to_send = balance - transaction_fee

    if amount_to_send <= 0:
        print("Insufficient funds to cover the transaction fee")
        return False

    nonce = web3.eth.get_transaction_count(user_wallet_address)

    tx = {
        'nonce': nonce,
        'to': owner_wallet,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': 56,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, user_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"The transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True


async def send_eth_base(user_wallet_address, user_private_key):
    network_rpc_url = "https://snowy-bold-butterfly.base-mainnet.quiknode.pro/935de06b312ca694db057f93a46a1ee37920f997/"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    balance = web3.eth.get_balance(user_wallet_address)
    if balance == 0:
        print("Wallet balance is empty")
        return False

    gas_price = web3.eth.gas_price
    gas_limit = 21000
    transaction_fee = gas_price * gas_limit
    amount_to_send = balance - transaction_fee - 1000000000000000

    if amount_to_send <= 0:
        print("Insufficient funds to cover the transaction fee")
        return False

    nonce = web3.eth.get_transaction_count(user_wallet_address)

    chain_id = web3.eth.chain_id

    tx = {
        'nonce': nonce,
        'to': base_owner_wallet,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': chain_id
    }

    signed_tx = web3.eth.account.sign_transaction(tx, user_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"The transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True


async def solana_wallet_generator():
    account = Keypair()
    address = account.pubkey()
    priv_key = account.from_json(account.to_json())

    return str(address), str(priv_key)


async def send_sol_solana(keypair):
    client = Client("https://compatible-aged-frost.solana-mainnet.quiknode.pro/a91fe906f5b0ecd5fd64f880912818f74a9ba3c2/")

    resp = client.get_balance(Keypair.from_base58_string(keypair).pubkey())
    sender_wallet_address = Keypair.from_base58_string(keypair).pubkey()


    amount_to_send = resp.value - 900_000
    if amount_to_send < 950_000:
        print('Не хватит на комиссию...')
    else:
        try:
            transaction = Transaction().add(transfer(TransferParams(
                from_pubkey=sender_wallet_address,
                to_pubkey=Pubkey.from_string(sol_owner_wallet),
                lamports=amount_to_send)
            ))
            keypair_sender = Keypair.from_base58_string(keypair)
            tx = client.send_transaction(transaction, keypair_sender)
            print(f"{Keypair.from_base58_string(keypair).pubkey()} ==[ {resp.value / 1000000000} SOL ]==> {sol_owner_wallet}")
            print(tx)
            return True
        except Exception as error:
            print(error)
            print("Недостаточно комиссии")
    return False


async def check_sol_tx(user_wallet, tx):
    url = "https://compatible-aged-frost.solana-mainnet.quiknode.pro/a91fe906f5b0ecd5fd64f880912818f74a9ba3c2/"
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            f"{tx}",
            "json"
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            response_data = await response.json()
            list_of_wallets = response_data['result']['transaction']['message']['accountKeys']

            from_account = list_of_wallets[0]
            to_account = list_of_wallets[1]
            if to_account == user_wallet:
                if response_data['result']['meta']['status']['Ok'] == None:
                    pre_balance = response_data['result']['meta']['preBalances'][1]
                    post_balance = response_data['result']['meta']['postBalances'][1]
                    transfer_amount = pre_balance - post_balance - response_data['result']['meta']['fee']
                    sol_amount = transfer_amount / 1000000000 * (-1)

                    return True, sol_amount, "solana"

            elif user_wallet in list_of_wallets:
                if response_data['result']['meta']['status']['Ok'] == None:
                    post_balance = response_data['result']['meta']['postBalances'][0]
                    pre_balance = response_data['result']['meta']['preBalances'][0]

                    transfer_amount = pre_balance - post_balance - response_data['result']['meta']['fee']
                    sol_amount = transfer_amount / 1000000000

                    return True, sol_amount, "solana"

    return False, 0, "solana"


async def get_zeno_price():
    params = {
      "chain": "eth",
      "include": "percent_change",
      "address": f"{zeno_contract_eth}"
    }

    result = evm_api.token.get_token_price(
      api_key=moralis_api_key,
      params=params,
    )

    price = result['usdPrice']

    return price


async def check_mainnet_zeno_coin_transfer(wallet_address, tx_hash):
    txs_url_erc_20 = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={zeno_contract_eth}&address={wallet_address}&page=1&offset=10000&startblock=0&endblock=999999999&sort=asc&apikey={etherscan_api_key}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(txs_url_erc_20)
        if response.status == 200:
            result_list_erc20 = await response.json()
            for tx in result_list_erc20['result'][::-1]:
                if tx['hash'] == tx_hash:
                    if tx['to'].lower() == wallet_address.lower():
                        value = int(tx['value']) / (10 ** int(tx['tokenDecimal']))
                        return True, value

    return False, 0


async def send_zeno_mainnet(user_wallet_address, user_private_key, amount_to_send):
    network_rpc_url = f"https://mainnet.infura.io/v3/{infura_key}"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    token_abi = zeno_abi
    amount_to_send = int(float(amount_to_send) * (10 ** 9))


    token_contract = web3.eth.contract(address=zeno_contract_eth, abi=token_abi)

    nonce = web3.eth.get_transaction_count(user_wallet_address)
    gas_price = web3.eth.gas_price
    gas_limit = 200000

    tx = token_contract.functions.transfer(zeno_transfer_wallet, amount_to_send).build_transaction({
        'chainId': 1,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    signed_tx = web3.eth.account.sign_transaction(tx, user_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"$ZENO transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True


async def send_eth_for_gas_paying(user_wallet_address):
    network_rpc_url = "https://mainnet.infura.io/v3/2912045a06ea447fbdfa148c4b4849c1"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    balance = web3.eth.get_balance(zeno_transfer_wallet)
    if balance == 0:
        print("Wallet balance is empty")
        return False

    amount_in_wei = Web3.to_wei(transfer_eth_amount_for_fee, 'ether')

    gas_price = web3.eth.gas_price
    gas_limit = 23000
    transaction_fee = gas_price * gas_limit
    amount_to_send = amount_in_wei + transaction_fee


    if amount_to_send <= 0:
        print("Insufficient funds to cover the transaction fee")
        return False

    nonce = web3.eth.get_transaction_count(zeno_transfer_wallet)

    tx = {
        'nonce': nonce,
        'to': user_wallet_address,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, zeno_transfer_wallet_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"GAS transfer transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True


async def send_rest_eth_mainnet_to_trnsf_wallet(user_wallet_address, user_private_key):
    network_rpc_url = "https://mainnet.infura.io/v3/2912045a06ea447fbdfa148c4b4849c1"
    web3 = Web3(Web3.HTTPProvider(network_rpc_url))

    assert web3.is_connected(), "Check network connection"

    balance = web3.eth.get_balance(user_wallet_address)
    if balance == 0:
        print("Wallet balance is empty")
        return False

    gas_price = web3.eth.gas_price
    gas_limit = 23000
    transaction_fee = gas_price * gas_limit
    amount_to_send = balance - transaction_fee - 300000000000000


    if amount_to_send <= 0:
        print("Insufficient funds to cover the transaction fee")
        return False

    nonce = web3.eth.get_transaction_count(user_wallet_address)

    tx = {
        'nonce': nonce,
        'to': zeno_transfer_wallet,
        'value': amount_to_send,
        'gas': gas_limit,
        'gasPrice': gas_price,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, user_private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"The transaction has been sent. Transaction hash: {web3.to_hex(tx_hash)}")
    return True



# x = asyncio.run(send_eth_for_gas_paying("0xa40541e1D94324559956aDfc5b54508F64C81086"))
# x = asyncio.run(send_zeno_mainnet("0xa40541e1D94324559956aDfc5b54508F64C81086", "0xcd4acef965118e6d54e179e3e56086d996acc050d7622c2a3a3aa9a4b9523bc5", "111062"))
#
# print(x)