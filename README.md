# Telegram + Discord bot sample · 텔레그램·디스코드 봇 샘플

One shared logic file ([`core.py`](core.py)) used by both a Telegram bot and a Discord bot.

- `/menu`, `/order <item> <qty>`, `/myorders`; keyword FAQ auto-replies (hours, Wi-Fi, parking — Korean keywords too)
- Admins: `/orders`, `/done <id>` · orders stored in SQLite
- Tests: `pytest -q` checks the full order flow, FAQ, permissions, and that both adapters wire up
- Try it with no token: `python console.py`

```bash
pip install -r requirements.txt
TELEGRAM_TOKEN=... ADMIN_IDS=12345 python telegram_bot.py
DISCORD_TOKEN=...  ADMIN_IDS=12345 python discord_bot.py
```

한국어: 주문 받기·주문 내역·관리자 처리·자주 묻는 질문 자동 답변이 되는 봇입니다. 같은 로직을 텔레그램과 디스코드에 함께 씁니다. 토큰은 고객 봇 계정에서 발급받아 환경변수로만 넣습니다(코드에 저장하지 않음).

---
**About / 안내** — Sample by **MANI** (Korea). Built with AI-assisted development (Claude Code) and run/tested before publishing. Custom work available on Kmong and Fiverr.
MANI 샘플입니다. AI 보조 개발(Claude Code)로 만들고 공개 전에 직접 실행·테스트했습니다. 맞춤 작업은 크몽·Fiverr에서 주문할 수 있습니다.
