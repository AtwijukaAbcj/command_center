from tinydb import TinyDB, Query
db = TinyDB("static/auth.json")
# items = []
# db.insert_multiple(items)
# db.truncate()
token = 'c558a80a-f319-4c10-95d4-4282ef745b4b' 
t = Query()

def demo_token():
    return str(token)

# change settings here 
def live_token():
    return str(token)



