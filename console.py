"""Try the bot without any token: python console.py  (type messages; 'admin:' prefix = admin user)."""
from core import Store, handle

store = Store(":memory:")
while True:
    try:
        line = input("you> ")
    except EOFError:
        break
    admin = line.startswith("admin:")
    r = handle(store, line.removeprefix("admin:"), "admin" if admin else "u1", "Admin" if admin else "Guest", admin)
    print("bot>", r.text if r else "(no reply)")
