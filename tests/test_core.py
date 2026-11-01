from core import Store, handle


def run(store, text, admin=False, uid="u1"):
    r = handle(store, text, uid, "Guest", admin)
    return r.text if r else None


def test_flow():
    s = Store(":memory:")
    assert "latte" in run(s, "/menu")
    assert run(s, "/order latte 2") == "Order #1 received: 2 x latte."
    assert run(s, "/order pizza 1").startswith("Usage")
    assert run(s, "/order latte 99").startswith("Usage")
    assert run(s, "/myorders") == "#1 2 x latte $9.00 [open]"
    assert run(s, "/orders") == "Admins only."
    assert run(s, "/orders", admin=True) == "#1 Guest: 2 x latte $9.00"
    assert run(s, "/done 1", admin=True) == "Order #1 closed."
    assert run(s, "/done 1", admin=True).endswith("already closed.")
    assert run(s, "/menu@MyShopBot").startswith("latte")


def test_faq_and_silence():
    s = Store(":memory:")
    assert run(s, "what are your hours?").startswith("Open daily")
    assert run(s, "주차 되나요") .startswith("Free parking")
    assert run(s, "thanks!") is None


def test_adapters_wire_up():
    import discord_bot
    import telegram_bot
    app = telegram_bot.build("123456:TEST-TOKEN-not-real")
    assert len(app.handlers[0]) == 1
    assert discord_bot.build().intents.message_content
