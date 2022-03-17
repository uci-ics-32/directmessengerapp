from ds_messenger import DirectMessenger

# Creates an object for the DirectMessenger class
dm = DirectMessenger("168.235.86.101", "vanillamilkshake", "yum")

# Sends a message over the server
dm.send("yo", "vanillamilkshake")
# Retrieves all new messages from the server for this profile
new = dm.retrieve_new()
# Retrieves ALL messages from the server for this profile
inbox = dm.retrieve_all()

new_msgs = []
all_msgs = []

for index, message in enumerate(new):
    new_msgs.append(new[index].message)

for index, message in enumerate(inbox):
    all_msgs.append(inbox[index].message)


print('All messages: ' + str(all_msgs))
print('New messages: ' + str(new_msgs))