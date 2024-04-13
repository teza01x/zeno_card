


dictionary = {
    "start_msg": "**Welcome back to Zeno Card!**\n\n"
                 "Zenocard is an innovative web3 platform enabling users to effortlessly convert their digital crypto assets into versatile virtual credit cards.\n\n"
                 "With Zenocard, users can seamlessly utilize their crypto holdings for real-world transactions, including bill payments, purchasing gift cards, and shopping on e-commerce platforms.\n\n"
                 "To get started, deposit cryptocurrency to your wallet addresses.\n\n"
                 "**for $ETH:**\n"
                 "`{}`\n\n"
                 "**for $SOL:**\n"
                 "`{}`\n\n"
                 "We accept **Mainnet, Base** $ETH | **Solana** $SOL. Run the /deposit command for more info.",
    "deposit_msg": "**Zeno Deposit Process**\n\n"
                    "Send **Mainnet / Base** $ETH to your deposit address:\n"
                    "`{}`\n\n"
                    "Send **Solana** $SOL to your deposit address:\n"
                    "`{}`\n\n"
                    "Once your transaction has been made, use the commands below to process your transaction:\n\n"
                    "/credit [transaction hash] for **Mainnet** $ETH\n"
                    "/basecredit [transaction hash] for **Base** $ETH\n"
                    "/solcredit [transaction hash] for **Solana** $SOL",
    "error_hash": "You entered an incorrect transaction hash. Try again.",
    "not_eligible_hash": "This transaction cannot be accepted.",
    "successful_deposit": "Transaction successfully processed!\nYou have been credited with {} $ETH.",
    "successful_deposit_sol": "Transaction successfully processed!\nYou have been credited with {} $SOL.",
    "balance": "**Zeno Balance**\n\nYour current balance is: **{}** USD.\n\nYour current deposit limit: **{}** USD",
    "credit": "Please provide a transaction hash of your deposit in this format:\n"
              "/credit [hash] - for **Mainnet** $ETH\n"
              "/basecredit [hash] - for **Base** $ETH\n"
              "/solcredit [hash] - for **Solana** $SOL",
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
    }