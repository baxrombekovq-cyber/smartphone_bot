from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import Database
from handlers.search import SearchState
from buttons.main import main_menu
from handlers.payment import payment_menu


router = Router()
db = Database()

print("✅ COMMANDS.PY ISHLADI")


# =========================================================
# 🔎 /SEARCH
# =========================================================

@router.message(Command("search"))
async def search_command(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        SearchState.waiting_for_text
    )

    await message.answer(
        "🔎 <b>TELEFON QIDIRISH</b>\n\n"
        "Telefon nomini yozing:\n\n"
        "Masalan:\n"
        "📱 iPhone 15\n"
        "📱 Samsung A55\n"
        "📱 Redmi Note 13"
    )


# =========================================================
# 📦 /ORDERS
# =========================================================

@router.message(Command("orders"))
async def orders_command(
    message: Message
):

    user_id = message.from_user.id

    orders = db.get_orders(
        user_id
    )

    if not orders:

        await message.answer(
            "📦 <b>BUYURTMALARIM</b>\n\n"
            "Sizda hali buyurtmalar mavjud emas.",
            reply_markup=main_menu(user_id)
        )

        return

    text = "📦 <b>BUYURTMALARIM</b>\n\n"

    for order in orders:

        order_id = order[0]
        product_name = order[1]
        price = order[2]
        status = order[3] or "pending"
        payment_status = order[4] or "waiting"
        created_at = order[5]

        # Buyurtma holati
        if status == "Tasdiqlandi":

            status_text = "✅ Tasdiqlandi"

        elif status == "Rad etildi":

            status_text = "❌ Rad etildi"

        else:

            status_text = "⏳ Kutilmoqda"

        # To‘lov holati
        if payment_status == "Tasdiqlangan":

            payment_text = "✅ To‘langan"

        elif payment_status == "Bekor qilindi":

            payment_text = "❌ Bekor qilingan"

        else:

            payment_text = "⏳ Kutilmoqda"

        text += (
            f"🆔 <b>#{order_id}</b>\n"
            f"📦 <b>{product_name}</b>\n"
            f"💰 <b>{price:,} so‘m</b>\n"
            f"📌 Holat: <b>{status_text}</b>\n"
            f"💳 To‘lov: <b>{payment_text}</b>\n"
            f"🕒 Sana: <b>{created_at}</b>\n"
            "━━━━━━━━━━━━━━\n"
        )

    await message.answer(
        text,
        reply_markup=main_menu(user_id)
    )


# =========================================================
# 👤 /PROFILE
# =========================================================

@router.message(Command("profile"))
async def profile_command(
    message: Message
):

    user_id = message.from_user.id

    user = db.get_user(
        user_id
    )

    if not user:

        await message.answer(
            "❌ <b>Profil topilmadi.</b>\n\n"
            "Avval /start buyrug‘ini yuboring."
        )

        return

    database_id = user[0]
    telegram_id = user[1]
    full_name = user[2] or "Ism yo‘q"
    username = user[3] or "Username yo‘q"
    phone = user[4] or "Telefon yo‘q"

    if username != "Username yo‘q":

        if not username.startswith("@"):

            username = f"@{username}"

    text = (
        "👤 <b>MENING PROFILIM</b>\n\n"
        f"🆔 ID: <code>{database_id}</code>\n"
        f"👤 Ism: <b>{full_name}</b>\n"
        f"🔹 Telegram ID: <code>{telegram_id}</code>\n"
        f"🔗 Username: <b>{username}</b>\n"
        f"📞 Telefon: <b>{phone}</b>"
    )

    await message.answer(
        text,
        reply_markup=main_menu(user_id)
    )


# =========================================================
# 💳 /PAYMENT
# =========================================================

@router.message(Command("payment"))
async def payment_command(
    message: Message
):

    await message.answer(
        "💳 <b>TO‘LOV BO‘LIMI</b>\n\n"
        "To‘lov turini tanlang:",
        reply_markup=payment_menu()
    )