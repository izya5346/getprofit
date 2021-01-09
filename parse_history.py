from steam_community_market import Market, AppID
market = Market("RUB")
item = "Sticker | Battle Scarred"
current = market.get_lowest_price(item, AppID.CSGO)
current = float(current[: current.find(" ") + 1].replace(',','.'))
print(current)

# from steam_community_market import Market, AppID
# market = Market('RUB')

# market.get_lowest_price()