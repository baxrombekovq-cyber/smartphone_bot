from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import CHANNEL_ID

from database import Database
from buttons.channel import channel_buttons
from buttons.main import main_menu


router = Router()

db = Database()

print("✅ START.PY ISHLADI")


# =========================================================
# 🔍 KANALGA OBUNANI TEKSHIRISH
# =========================================================

async def check_user_subscription(
    message: Message
):

    try:

        member = await message.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=message.from_user.id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as error:

        print(
            f"❌ KANAL TEKSHIRISHDA XATO: {error}"
        )

        return False


# =========================================================
# 🚀 START
# =========================================================

@router.message(
    CommandStart()
)
async def start_handler(
    message: Message
):

    print("📥 START BOSILDI")

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    full_name = message.from_user.full_name
    username = message.from_user.username or ""

    # =====================================================
    # 👤 USERNI DATABASEGA SAQLASH
    # =====================================================

    try:

        db.add_user(
            telegram_id=user_id,
            full_name=full_name,
            username=username
        )

        print(
            f"✅ USER SAQLANDI: "
            f"{user_id} | {full_name}"
        )

    except Exception as error:

        print(
            f"❌ USER SAQLASHDA XATO: {error}"
        )

    # =====================================================
    # 🔍 OBUNANI TEKSHIRISH
    # =====================================================

    subscribed = await check_user_subscription(
        message
    )

    print(
        f"📢 OBUNA HOLATI: {subscribed}"
    )

    # =====================================================
    # ✅ OBUNA BO‘LGAN
    # =====================================================

    if subscribed:

        await message.answer(
            "📱 <b>SMART PHONE SHOP</b>\n\n"
            f"Xush kelibsiz, <b>{first_name}</b> 👋\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(user_id)
        )

        return

    # =====================================================
    # ❌ OBUNA BO‘LMAGAN
    # =====================================================

    await message.answer(
        "📱 <b>SMART PHONE SHOP</b>\n\n"
        f"Assalomu alaykum, <b>{first_name}</b> 👋\n\n"
        "Botdan foydalanish uchun avval "
        "kanalimizga obuna bo‘ling 👇",
        reply_markup=channel_buttons()
    )