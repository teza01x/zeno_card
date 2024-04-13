import os


telegram_token = "6962541096:AAHHJURq-dXOYqLSBU2RyQ-4_WWckC75eFI"
infura_key = "2912045a06ea447fbdfa148c4b4849c1"
etherscan_api_key = "95SQXNXDUZA8QGARK2DZBY44UTW28XA7GE"
basescan_api_key = "RNYPIDDHRTTIRBYZ36ECQKK8GZ93QIJCJE"
pst_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5wc3QubmV0L3VzZXIvYXBpLWtleSIsImlhdCI6MTcxMTEyMjkxMCwibmJmIjoxNzExMTIyOTEwLCJqdGkiOiJRTzVDalFvZHR3ZmhONzdVIiwic3ViIjoiNzIzNDk3IiwicHJ2IjoiYjkxMjc5OTc4ZjExYWE3YmM1NjcwNDg3ZmZmMDFlMjI4MjUzZmU0OCIsImFiaWxpdGllcyI6WyJmdWxsX2FjY2VzcyJdfQ.3c-0ZK_rq6hiu-FD1D52-9gvW4pgJlqy747WL2Czr10"
moralis_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImJhZGIzYWViLTVjOTEtNDRiZC1iODY5LTM2NTBlMWJmNTVjMiIsIm9yZ0lkIjoiMzg3Mjk3IiwidXNlcklkIjoiMzk3OTQ3IiwidHlwZUlkIjoiOGYyNWE3ODQtN2QzZi00NmJjLTljODYtNzAzZjA2MGFjZjc1IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTI3NDA1MzUsImV4cCI6NDg2ODUwMDUzNX0.Y0cMwfLySxYpdAUkYHpcvsVDtPVmDnc75JDaqdZ7mf8"

data_base = os.path.join(os.path.dirname(__file__), 'database.db')

owner_wallet = "0xC00b814eacab5ac72B3D3A99CfdB21a550e740fb"
base_owner_wallet = "0x29c5cCB005B1cF89D45622c9b6B1F4DfA6c0aDAc"
sol_owner_wallet = "5msLtWffEg17wWaxKykzrBebUx7RLaLNdzjKWTUjoj8g"

transfer_eth_amount_for_fee = 0.003
zeno_transfer_wallet = "0x22A0451aFa604573A1E32a09EE411eE1118be7F3"
zeno_transfer_wallet_private_key = "def57f5191627831ba1b4391519c51d0ae1195f2dba00f28b479200ce9be4031"

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

zeno_contract_eth = "0xD51e4965ad973e8C1E1f22369Bb884E6914B012C"
zeno_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_maxTxAmount","type":"uint256"}],"name":"MaxTxAmountUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_maxTaxSwap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxWalletSize","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxSwapThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"a","type":"address"}],"name":"isBot","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"manualSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"openTrading","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_newFee","type":"uint256"}],"name":"reduceFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"removeUnclogLimits","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferDelayEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
