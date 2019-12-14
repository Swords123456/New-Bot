from discord.ext import commands


def amountToString(amount):
    if amount >= 1000000000:
        if amount / 10000000000 == 0:
            amount = int(amount)
        return f"{round(amount / 1000000000, 1)}b"
    
    if amount >= 1000000:
        if amount / 10000000 == 0:
            amount = int(amount)
        return f"{round(amount / 1000000, 1)}m";
    
    if amount >= 1000:
        if amount / 10000 == 0:
            amount = int(amount)
        return f"{round(amount / 1000, 1)}k";
    else:
        return f"{round(amount, 1)}"


def amountValid(bot, userID, amount, type):
    if bot.get_amount(userID, type) < amount:
        raise Exception(f"Not enough {type.formatString()}")

    if amount < 0:
        raise Exception(f"Can't gamble negative numbers")

    if amount < type.minAmount():
        raise Exception(f"Amount: {amountToString(amount)} is below minimum for {type.formatString()}")

    if bot.get_amount(bot.user.id, type) / 2 < amount:
        raise Exception(f"Bot does not have enough money.")