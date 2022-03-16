from ds_messenger import DirectMessenger

dm = DirectMessenger("168.235.86.101", "vanillamilkshake", "yum")

dm.send("yo", "nokizzy")
new = dm.retrieve_new()
inbox = dm.retrieve_all()

new_msgs = []
all_msgs = []

for index, message in enumerate(new):
    new_msgs.append(new[index].message)

for index, message in enumerate(inbox):
    all_msgs.append(inbox[index].message)

# {"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript" "timestamp":"1603167689.3928561"}]}}

print('All messages: ' + str(all_msgs))
print('New messages: ' + str(new_msgs))