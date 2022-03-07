from ds_messenger import DirectMessenger

dm = DirectMessenger("168.235.86.101", "nokizzy", "journal")



# TODO: move
dm.send("hello hottie", "nokizzy")
new = dm.retrieve_new()
print(new)
print("new", new)
print(new[0].recipient)
print("all", dm.retrieve_all())