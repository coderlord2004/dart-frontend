import json
message = '{"status": "success", "message": "Login OK"}'
dict = dict(json.loads(message))
print(dict.get('status'))
