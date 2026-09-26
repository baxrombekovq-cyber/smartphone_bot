import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat
)

from config import BOT_TOKEN, ADMIN_ID

from handlers import start
from handlers import channel
from handlers import commands
from handlers import phones
from handlers import cart
from handlers import accessories
from handlers import search
from handlers import order
from handlers import profile
from handlers import payment
from handlers import favorites
from handlers import contact
from handlers import admin


# =========================================================
# 📝 LOG
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)


# =========================================================
# 🤖 BOT
# =========================================================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


# =========================================================
# 📡 DISPATCHER
# =========================================================

dp = Dispatcher()


# =========================================================
# 🔌 ROUTERLARNI ULASH
# =========================================================

dp.include_router(start.router)
dp.include_router(channel.router)
dp.include_router(commands.router)
dp.include_router(phones.router)
dp.include_router(cart.router)
dp.include_router(accessories.router)
dp.include_router(search.router)
dp.include_router(order.router)
dp.include_router(profile.router)
dp.include_router(payment.router)
dp.include_router(favorites.router)
dp.include_router(contact.router)
dp.include_router(admin.router)


# =========================================================
# 📋 BOT COMMANDS
# =========================================================

async def set_bot_commands():

    # =====================================================
    # 👤 ODDIY FOYDALANUVCHI
    # =====================================================

    user_commands = [

        BotCommand(
            command="start",
            description="🤖 Botni boshlash"
        ),

        BotCommand(
            command="search",
            description="🔎 Telefon qidirish"
        ),

        BotCommand(
            command="orders",
            description="📦 Buyurtmalarim"
        ),

        BotCommand(
            command="profile",
            description="👤 Profil"
        ),

        BotCommand(
            command="payment",
            description="💳 To‘lov"
        )
    ]


    # =====================================================
    # 🌍 BARCHA PRIVATE CHATLAR UCHUN
    # =====================================================

    await bot.set_my_commands(
        user_commands,
        scope=BotCommandScopeAllPrivateChats()
    )


    # =====================================================
    # ⚙️ ADMIN UCHUN
    # =====================================================

    admin_commands = [

        BotCommand(
            command="start",
            description="🤖 Botni boshlash"
        ),

        BotCommand(
            command="search",
            description="🔎 Telefon qidirish"
        ),

        BotCommand(
            command="orders",
            description="📦 Buyurtmalarim"
        ),

        BotCommand(
            command="profile",
            description="👤 Profil"
        ),

        BotCommand(
            command="payment",
            description="💳 To‘lov"
        ),

        BotCommand(
            command="admin",
            description="⚙️ Admin panel"
        )
    ]


    await bot.set_my_commands(
        admin_commands,
        scope=BotCommandScopeChat(
            chat_id=ADMIN_ID
        )
    )


    print("✅ BOT COMMANDLAR O‘RNATILDI")


# =========================================================
# 🚀 MAIN
# =========================================================

async def main():

    print("🤖 BOT ISHGA TUSHDI")

    # Komandalarni o‘rnatish
    await set_bot_commands()

    # Eski webhook/update larni tozalash
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    # Botni ishga tushirish
    await dp.start_polling(
        bot
    )


# =========================================================
# ▶️ START
# =========================================================

if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "🛑 BOT TO‘XTADI"
        )

    except Exception as error:

        print(
            f"❌ XATOLIK: {error}"
        )