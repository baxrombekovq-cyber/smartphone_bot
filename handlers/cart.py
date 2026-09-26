from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database import Database
from buttons.cart import cart_buttons
from buttons.main import main_menu


router = Router()
db = Database()


# =========================================================
# 🛒 SAVATCHA
# =========================================================

@router.callback_query(F.data == "cart")
async def cart_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    # Savatchani bazadan olamiz
    cart = db.get_cart(user_id)

    # =====================================================
    # ❌ SAVATCHA BO‘SH
    # =====================================================

    if not cart:

        try:

            await callback.message.edit_text(
                "🛒 <b>SAVATCHA</b>\n\n"
                "Savatchangiz hozircha bo‘sh.",
                reply_markup=main_menu(user_id)
            )

        except TelegramBadRequest as error:

            # Telegram bir xil xabarni qayta edit qilishga ruxsat bermaydi
            if "message is not modified" in str(error):

                await callback.answer(
                    "🛒 Savatcha allaqachon ochilgan!"
                )

                return

            print(
                f"❌ SAVATCHA XATOSI: {error}"
            )

            await callback.answer(
                "❌ Xatolik yuz berdi!",
                show_alert=True
            )

            return

        await callback.answer()

        return

    # =====================================================
    # 📦 MAHSULOTLAR
    # =====================================================

    text = (
        "🛒 <b>SIZNING SAVATCHANGIZ</b>\n\n"
    )

    total = 0

    # get_cart() -> id, product_name, price
    for index, item in enumerate(cart, start=1):

        cart_id = item[0]
        name = item[1]
        price = item[2]

        text += (
            f"{index}. 📦 <b>{name}</b>\n"
            f"💰 {price:,} so‘m\n\n"
        )

        total += price

    # =====================================================
    # 💰 JAMI
    # =====================================================

    text += (
        "━━━━━━━━━━━━━━\n"
        f"💵 <b>Jami: {total:,} so‘m</b>"
    )

    # =====================================================
    # 🔘 TUGMALAR
    # =====================================================

    try:

        await callback.message.edit_text(
            text,
            reply_markup=cart_buttons()
        )

    except TelegramBadRequest as error:

        # Bir xil xabarni qayta yuborish
        if "message is not modified" in str(error):

            await callback.answer(
                "🛒 Savatcha allaqachon ochilgan!"
            )

            return

        print(
            f"❌ SAVATCHANI OCHISHDA XATO: {error}"
        )

        await callback.answer(
            "❌ Savatchani ochishda xatolik!",
            show_alert=True
        )

        return

    await callback.answer()


# =========================================================
# 🗑 SAVATCHANI TOZALASH
# =========================================================

@router.callback_query(F.data == "clear_cart")
async def clear_cart_handler(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    # =====================================================
    # 🗑 BAZADAN O‘CHIRISH
    # =====================================================

    db.clear_cart(user_id)

    # =====================================================
    # ✅ XABARNI YANGILASH
    # =====================================================

    try:

        await callback.message.edit_text(
            "🗑 <b>SAVATCHA TOZALANDI!</b>\n\n"
            "Barcha mahsulotlar savatchadan o‘chirildi.",
            reply_markup=main_menu(user_id)
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "🗑 Savatcha allaqachon tozalangan!"
            )

            return

        print(
            f"❌ SAVATCHANI TOZALASHDA XATO: {error}"
        )

        await callback.answer(
            "❌ Xatolik yuz berdi!",
            show_alert=True
        )

        return

    await callback.answer(
        "Savatcha tozalandi ✅"
    )


# =========================================================
# 🏠 BOSH MENYUGA QAYTISH
# =========================================================

@router.callback_query(F.data == "back_main")
async def cart_back_main(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    try:

        await callback.message.edit_text(
            "📱 <b>SMART PHONE SHOP</b>\n\n"
            f"Assalomu alaykum, "
            f"<b>{callback.from_user.first_name}</b> 👋\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(user_id)
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "🏠 Siz bosh menyudasiz!"
            )

            return

        print(
            f"❌ BOSH MENYU XATOSI: {error}"
        )

        await callback.answer(
            "❌ Xatolik yuz berdi!",
            show_alert=True
        )

        return

    await callback.answer()