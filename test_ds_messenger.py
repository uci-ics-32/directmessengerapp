from ds_messenger import DirectMessenger

dm = DirectMessenger("168.235.86.101", "nokizzy", "journal")

dm.send("yo", "nokizzy")
new = dm.retrieve_new()
inbox = dm.retrieve_all()

new_msgs = []
all_msgs = []

for index, message in enumerate(new):
    new_msgs.append(new[index].message)

for index, message in enumerate(inbox):
    all_msgs.append(inbox[index].message)

print('All messages: ' + str(all_msgs))
print('New messages: ' + str(new_msgs))