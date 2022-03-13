import ds_protocol
import socket
import json

# Test
msg = {"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}
msg2 = {"response": {"type": "ok", "message": "Direct message sent"}}

print(ds_protocol.convert_to_list(msg))
print(ds_protocol.convert_to_list(msg2))
