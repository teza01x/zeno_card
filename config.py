import os


telegram_token = "6501432731:AAEpwpqGhEE_GR4vin8npDWJzNeLuYGD114"
infura_key = "2912045a06ea447fbdfa148c4b4849c1"
etherscan_api_key = "95SQXNXDUZA8QGARK2DZBY44UTW28XA7GE"
basescan_api_key = "RNYPIDDHRTTIRBYZ36ECQKK8GZ93QIJCJE"
bscscan_api_key = "QTKZZAB5TM9U38WDR73G38SDDAMCSPNUJ6"
polygon_api_key = "9S51NGWVNA6Z3ZFFVZN7TNB9PZ49B1T6MC"
tron_api_key = "b1780134-9524-4e89-9232-e1d2709450fd"

pst_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5wc3QubmV0L3VzZXIvYXBpLWtleSIsImlhdCI6MTcxMTEyMjkxMCwibmJmIjoxNzExMTIyOTEwLCJqdGkiOiJRTzVDalFvZHR3ZmhONzdVIiwic3ViIjoiNzIzNDk3IiwicHJ2IjoiYjkxMjc5OTc4ZjExYWE3YmM1NjcwNDg3ZmZmMDFlMjI4MjUzZmU0OCIsImFiaWxpdGllcyI6WyJmdWxsX2FjY2VzcyJdfQ.3c-0ZK_rq6hiu-FD1D52-9gvW4pgJlqy747WL2Czr10"
moralis_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImJhZGIzYWViLTVjOTEtNDRiZC1iODY5LTM2NTBlMWJmNTVjMiIsIm9yZ0lkIjoiMzg3Mjk3IiwidXNlcklkIjoiMzk3OTQ3IiwidHlwZUlkIjoiOGYyNWE3ODQtN2QzZi00NmJjLTljODYtNzAzZjA2MGFjZjc1IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTI3NDA1MzUsImV4cCI6NDg2ODUwMDUzNX0.Y0cMwfLySxYpdAUkYHpcvsVDtPVmDnc75JDaqdZ7mf8"

data_base = os.path.join(os.path.dirname(__file__), 'database.db')

#uncomment
owner_wallet = "0xC00b814eacab5ac72B3D3A99CfdB21a550e740fb"
base_owner_wallet = "0x29c5cCB005B1cF89D45622c9b6B1F4DfA6c0aDAc"
sol_owner_wallet = "AhtawdbMvCAcEwuCJxhc9gvwpjjsT8vuhUyhFTSsNDCk"

tron_owner_wallet = "TWQgw3bvd8DsJj8Dtn3kvsV5VxKxLbT1sY"
tron_owner_private_key = ""

transfer_eth_amount_for_fee = 0.003
transfer_bnb_amount_for_fee = 0.003
transfer_trx_amount_for_fee = 40


zeno_transfer_wallet = "0x22A0451aFa604573A1E32a09EE411eE1118be7F3"
zeno_transfer_wallet_private_key = ""


start_menu_status = 0
amount_for_creating_card = 1
amount_for_deposit_card = 2

first_stage_transfer = 0
second_stage_transfer = 1
third_stage_transfer = 2
final_stage_transfer = 3

cards_limit_per_user = 3
minimum_deposit_card_creation = 10
max_deposit_card_creation = 1002

zeno_amount_to_upgrade = 113258
zeno_amount_to_upgrade_accept = 107851.6
usdt_amount_to_upgrade = 200
new_increased_card_limit = 2002

deposit_fee = 0.06
card_creation_fee = 1.09

minimal_deposit_value_in_dollars = 10

# new one
usdt_contract_eth = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
usdt_contract_bnb = "0x55d398326f99059fF775485246999027B3197955"
usdt_contract_tron = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
false = False
true = True

zeno_contract_eth = "0xD51e4965ad973e8C1E1f22369Bb884E6914B012C"
zeno_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_maxTxAmount","type":"uint256"}],"name":"MaxTxAmountUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_maxTaxSwap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxWalletSize","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxSwapThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"isBot","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"manualSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"openTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_newFee","type":"uint256"}],"name":"reduceFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeUnclogLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferDelayEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
