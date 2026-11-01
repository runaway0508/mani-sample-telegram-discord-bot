"""Platform-independent bot logic: FAQ auto-replies, simple orders stored in SQLite, admin listing.

Both telegram_bot.py and discord_bot.py call handle(); the logic is tested once in tests/.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass

MENU = {"latte": 4.5, "americano": 3.5, "bagel": 3.0}
FAQ = {
    ("hours", "open", "영업"): "Open daily 08:00-20:00.",
    ("wifi", "와이파이"): "Wi-Fi: ask the staff for today's password.",
    ("parking", "주차"): "Free parking for 1 hour with any order.",
}
HELP = ("Commands: /menu, /order <item> <qty>, /myorders, /help\n"
        "Admins: /orders (all open orders), /done <order_id>")


@dataclass
class Reply:
    text: str


class Store:
    def __init__(self, path: str = "bot.db"):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY, user_id TEXT, user_name TEXT, item TEXT, qty INTEGER,
            total REAL, status TEXT DEFAULT 'open', created TEXT DEFAULT CURRENT_TIMESTAMP)""")

    def add(self, user_id, user_name, item, qty) -> int:
        cur = self.db.execute("INSERT INTO orders(user_id,user_name,item,qty,total) VALUES(?,?,?,?,?)",
                              (user_id, user_name, item, qty, round(MENU[item] * qty, 2)))
        self.db.commit()
        return cur.lastrowid

    def by_user(self, user_id):
        return self.db.execute("SELECT id,item,qty,total,status FROM orders WHERE user_id=? ORDER BY id",
                               (user_id,)).fetchall()

    def open_orders(self):
        return self.db.execute("SELECT id,user_name,item,qty,total FROM orders WHERE status='open' ORDER BY id").fetchall()

    def close(self, order_id: int) -> bool:
        cur = self.db.execute("UPDATE orders SET status='done' WHERE id=? AND status='open'", (order_id,))
        self.db.commit()
        return cur.rowcount == 1


def handle(store: Store, text: str, user_id: str, user_name: str, is_admin: bool) -> Reply | None:
    """Return the reply for one incoming message, or None to stay silent."""
    text = (text or "").strip()
    if not text:
        return None
    if not text.startswith("/"):
        low = text.lower()
        for keys, answer in FAQ.items():
            if any(k in low for k in keys):
                return Reply(answer)
        return None
    cmd, *args = text.split()
    cmd = cmd.split("@")[0].lower()          # Telegram group form: /menu@MyBot
    if cmd in ("/start", "/help"):
        return Reply(HELP)
    if cmd == "/menu":
        return Reply("\n".join(f"{k} - ${v:.2f}" for k, v in MENU.items()))
    if cmd == "/order":
        if len(args) != 2 or args[0].lower() not in MENU or not args[1].isdigit() or not 0 < int(args[1]) <= 20:
            return Reply("Usage: /order <item> <qty 1-20>, e.g. /order latte 2")
        oid = store.add(user_id, user_name, args[0].lower(), int(args[1]))
        return Reply(f"Order #{oid} received: {args[1]} x {args[0].lower()}.")
    if cmd == "/myorders":
        rows = store.by_user(user_id)
        return Reply("\n".join(f"#{i} {q} x {it} ${t:.2f} [{s}]" for i, it, q, t, s in rows) or "No orders yet.")
    if cmd in ("/orders", "/done") and not is_admin:
        return Reply("Admins only.")
    if cmd == "/orders":
        rows = store.open_orders()
        return Reply("\n".join(f"#{i} {n}: {q} x {it} ${t:.2f}" for i, n, it, q, t in rows) or "No open orders.")
    if cmd == "/done":
        if not args or not args[0].isdigit():
            return Reply("Usage: /done <order_id>")
        return Reply(f"Order #{args[0]} closed." if store.close(int(args[0])) else f"Order #{args[0]} not found or already closed.")
    return Reply("Unknown command. " + HELP)
