


dictionary = {
    "start_msg": "**Welcome back to Zeno Card!**\n\n"
                 "Zenocard is an innovative web3 platform enabling users to effortlessly convert their digital crypto assets into versatile virtual credit cards.\n\n"
                 "With Zenocard, users can seamlessly utilize their crypto holdings for real-world transactions, including bill payments, purchasing gift cards, and shopping on e-commerce platforms.\n\n"
                 "To get started, deposit cryptocurrency to your wallet addresses.\n\n"
                 # "**for $ETH:**\n"
                 # "`{}`\n\n"
                 # "**for $SOL:**\n"
                 # "`{}`\n\n"
                 "**We accept:**\n"
                 " **Mainnet, Base** $ETH |\n"
                 " **Solana** $SOL |\n"
                 " **BNB Smart Chain** $BNB |\n"
                 " **Polygon** $MATIC |\n"
                 " **Tron** $TRX |\n"
                 " **ERC-20 / BEP-20 / TRC-20** $USDT |\n\n"
                 " Run the /deposit command for more info.",
    "min_deposit_alert": "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.",
    # "deposit_msg": "**Zeno Deposit Process**\n\n"
    #                 "Send **Mainnet / Base** $ETH to your deposit address:\n"
    #                 "`{}`\n\n"
    #                 "Send **Solana** $SOL to your deposit address:\n"
    #                 "`{}`\n\n"
    #                 "Once your transaction has been made, use the commands below to process your transaction:\n\n"
    #                 "/credit [transaction hash] for **Mainnet** $ETH\n"
    #                 "/basecredit [transaction hash] for **Base** $ETH\n"
    #                 "/solcredit [transaction hash] for **Solana** $SOL",
    "deposit_msg": "**Zeno Deposit Process**\n"
                   "**Choose your payment method below**",
    "error_hash": "You entered an incorrect transaction hash. Try again.",
    "not_eligible_hash": "This transaction cannot be accepted.",
    "successful_deposit": "Transaction successfully processed!\nYou have been credited with {} $ETH.",
    "successful_deposit_usdt": "Transaction successfully processed!\nYou have been credited with {} $USDT.",
    "successful_deposit_sol": "Transaction successfully processed!\nYou have been credited with {} $SOL.",
    "successful_deposit_bnb": "Transaction successfully processed!\nYou have been credited with {} $BNB.",
    "successful_deposit_matic": "Transaction successfully processed!\nYou have been credited with {} $MATIC.",
    "successful_deposit_trx": "Transaction successfully processed!\nYou have been credited with {} $TRX.",
    "balance": "**Zeno Balance**\n\nYour current balance is: **{}** USD.\n\nYour current deposit limit: **{}** USD",
    "credit": "Please provide a transaction hash of your deposit in this format:\n"
              "/credit [hash] - for **Mainnet** $ETH\n"
              "/basecredit [hash] - for **Base** $ETH\n"
              "/solcredit [hash] - for **Solana** $SOL\n"
              "/bnbcredit [hash] - for **BEP-20** $BNB\n"
              "/maticcredit [hash] - for **POLYGON** $MATIC\n"
              "/trxcredit [hash] - for **TRC-20** $TRX\n"
              "/usdtcredit_bsc [hash] - for **BEP-20** `Binance-Peg BSC-USD`\n"
              "/usdtcredit_mainnet [hash] - for **ERC-20** $USDT\n"
              "/usdtcredit_tron [hash] - for **TRC-20** $USDT\n",
    "credit_eth_mainnet": "Send **Mainnet** $ETH to your deposit address:\n"
                          "`{}`\n\n"
                          "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                          "Please provide a transaction hash of your deposit in this format:\n"
                          "/credit [hash] - for **Mainnet** $ETH\n",
    "credit_eth_base": "Send **Base** $ETH to your deposit address:\n"
                          "`{}`\n\n"
                          "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                          "Please provide a transaction hash of your deposit in this format:\n"
                          "/basecredit [hash] - for **Base** $ETH\n",
    "credit_sol": "Send **SOLANA** $SOL to your deposit address:\n"
                       "`{}`\n\n"
                       "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                       "Please provide a transaction hash of your deposit in this format:\n"
                       "/solcredit [hash] - for **SOLANA** $SOL\n",
    "credit_bnb": "Send **BEP-20** $BNB to your deposit address:\n"
                  "`{}`\n\n"
                  "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                  "Please provide a transaction hash of your deposit in this format:\n"
                  "/bnbcredit [hash] - for **BEP-20** $BNB\n",
    "credit_matic": "Send **POLYGON** $MATIC to your deposit address:\n"
                  "`{}`\n\n"
                  "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                  "Please provide a transaction hash of your deposit in this format:\n"
                  "/maticcredit [hash] - for **POLYGON** $MATIC\n",
    "credit_trx": "Send **TRC-20** $TRX to your deposit address:\n"
                    "`{}`\n\n"
                    "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                    "Please provide a transaction hash of your deposit in this format:\n"
                    "/trxcredit [hash] - for **TRC-20** $TRX\n",
    "credit_usdt_bsc": "Send **BEP-20** `Binance-Peg BSC-USD` to your deposit address:\n"
                  "`{}`\n\n"
                  "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                  "Please provide a transaction hash of your deposit in this format:\n"
                  "/usdtcredit_bsc [hash] - for **BEP-20** `Binance-Peg BSC-USD`\n",
    "credit_usdt_mainnet": "Send **ERC-20** $USDT to your deposit address:\n"
                       "`{}`\n\n"
                       "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                       "Please provide a transaction hash of your deposit in this format:\n"
                       "/usdtcredit_mainnet [hash] - for **ERC-20** $USDT\n",
    "credit_usdt_tron": "Send **TRC-20** $USDT to your deposit address:\n"
                           "`{}`\n\n"
                           "**Minimum deposit - 10$**\nPayment of $10+ must be in one transaction.\n\n"
                           "Please provide a transaction hash of your deposit in this format:\n"
                           "/usdtcredit_tron [hash] - for **TRC-20** $USDT\n",
    "card_creation": "**Zeno Card Creation**\n\n"
                     "Each card issuance costs **$1** flat fee and an additional **5%** fees.\n\n"
                     "To create a card, your balance must be at least **$12**\n\n"
                     "Your balance is **{}** USD.\n\n"
                     "How much would you like to charge to a card (${}-{} USD)?",
    "card_creation_request": "Card creation initiated. Please check /cards in a minute.",
    "top_up_card": "**Zeno Card Top Up**\n\n"
                   "Each card limit is {} and the top up is subjected to an additional 6% fees.\n\n"
                   "Your balance is {} USD.\n"
                   "Your current card balance is {} USD and you're able to top up {} USD more.\n\n"
                   "How much would you like to charge to a card?",
    "minimum_cost_creation": "You have entered an incorrect deposit amount.",
    "not_enough_balance": "You do not have enough balance to create a card with {} USD as it costs {}. Your current balance is {} USD.",
    "error_digit_amount": "Enter the correct amount for deposit.",
    "cards_limit_reached": "You have reached your card limit.",
    "support": "Contact support: Support@Zenocard.com",
    "wrong_deposit_amount": "This amount cannot be added to your card balance.",
    "card_balance_top_upped": "**You have successfully topped up your card balance with `{}` USD**\n"
                              "**Your current balance: `{}` USD**\n\n"
                              "**Wait a few minutes for the card balance to update.**",
    "creating_card_error": "An error occurred while creating the card, please contact support for advice.",
    "secure_code_notif": "New 3DS code {} for card ****{}",
    "increased_limit": "Your transaction has been accepted. The limit has been increased to {} USD.",
    "already_upgraded": "You have already increased your limit on the card.",
    # "deposit_limit_increase": "Burn **$200** worth of $ZENO tokens to elevate your card limit up to **${}!**\n\n"
    #                           "Send **$200** worth of $ZENO ≈ **{}** to this address:\n\n"
    #                           "`{}`",
    "deposit_limit_increase": "Burn **{}** $ZENO tokens to elevate your card limit up to **${}!**\n\n"
                              "Send **{}** $ZENO tokens to this address:\n\n"
                              "`{}`\n\n"
                              "Please provide a transaction hash of your deposit in this format:\n"
                              "/upgrade [hash]",
    "which_token_deposit": "Which token would you like to deposit?",
    "wait_text": "Please wait while the transaction is being processed.",
    }
