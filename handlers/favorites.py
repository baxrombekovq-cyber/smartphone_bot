from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

from database import Database
from buttons.main import main_menu


router = Router()
db = Database()

print("✅ FAVORITES.PY ISHLADI")


# =========================================================
# ❤️ SEVIMLILAR MA'LUMOTINI OLISH
# =========================================================

def get_user_favorites(user_id: int):

    try:
        db.cursor.execute(
            """
            SELECT
                f.item_type,
                f.item_id,
                p.name,
                p.price,
                p.brand
            FROM favorites f
            INNER JOIN phones p
                ON f.item_type = 'phone'
                AND f.item_id = p.id
            WHERE f.telegram_id = %s

            UNION ALL

            SELECT
                f.item_type,
                f.item_id,
                a.name,
                a.price,
                a.category
            FROM favorites f
            INNER JOIN accessories a
                ON f.item_type = 'accessory'
                AND f.item_id = a.id
            WHERE f.telegram_id = %s

            ORDER BY name
            """,
            (user_id, user_id)
        )

        return db.cursor.fetchall()

    except Exception as error:

        db.connection.rollback()

        print(
            f"❌ SEVIMLILARNI OLISHDA XATO: {error}"
        )

        return []


# =========================================================
# ❤️ SEVIMLILAR
# =========================================================

@router.callback_query(
    F.data == "favorites"
)
async def favorites_handler(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    favorites = get_user_favorites(
        user_id
    )

    # =====================================================
    # ❤️ SEVIMLILAR BO‘SH
    # =====================================================

    if not favorites:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏠 Bosh menyu",
                        callback_data="back_main"
                    )
                ]
            ]
        )

        try:

            await callback.message.edit_text(
                "❤️ <b>SEVIMLILAR</b>\n\n"
                "Sizda hozircha sevimli mahsulotlar yo‘q.",
                reply_markup=keyboard
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "❤️ Sevimlilar allaqachon ko‘rsatilgan."
                )

                return

            raise

        await callback.answer()
        return

    # =====================================================
    # 📝 MATN
    # =====================================================

    text = (
        "❤️ <b>SEVIMLI MAHSULOTLAR</b>\n\n"
    )

    buttons = []

    for index, favorite in enumerate(
        favorites,
        start=1
    ):

        item_type = favorite[0]
        item_id = favorite[1]
        name = favorite[2]
        price = favorite[3]
        category = favorite[4] or ""

        # Telefon
        if item_type == "phone":

            emoji = "📱"

            text += (
                f"{index}. {emoji} <b>{name}</b>\n"
                f"🏷 Brend: <b>{category}</b>\n"
                f"💰 Narx: <b>{price:,} so‘m</b>\n"
                "━━━━━━━━━━━━━━\n"
            )

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {name}",
                        callback_data=f"remove_favorite_phone_{item_id}"
                    )
                ]
            )

        # Aksessuar
        elif item_type == "accessory":

            emoji = "🎧"

            text += (
                f"{index}. {emoji} <b>{name}</b>\n"
                f"📂 Kategoriya: <b>{category}</b>\n"
                f"💰 Narx: <b>{price:,} so‘m</b>\n"
                "━━━━━━━━━━━━━━\n"
            )

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {name}",
                        callback_data=f"remove_favorite_accessory_{item_id}"
                    )
                ]
            )

    # =====================================================
    # 🏠 BOSH MENYU
    # =====================================================

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Bosh menyu",
                callback_data="back_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "❤️ Ma'lumotlar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# ❌ TELEFONNI SEVIMLILARDAN O‘CHIRISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^remove_favorite_phone_\d+$")
)
async def remove_favorite_phone(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    try:

        phone_id = int(
            callback.data.split("_")[-1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )

        return

    try:

        db.remove_favorite(
            user_id,
            "phone",
            phone_id
        )

    except Exception as error:

        db.connection.rollback()

        print(
            f"❌ TELEFONNI SEVIMLIDAN O‘CHIRISHDA XATO: {error}"
        )

        await callback.answer(
            "❌ O‘chirishda xatolik!",
            show_alert=True
        )

        return

    await callback.answer(
        "💔 Sevimlilardan o‘chirildi."
    )

    # Ro‘yxatni qayta chiqarish
    await show_favorites_again(
        callback
    )


# =========================================================
# ❌ AKSESSUARNI SEVIMLILARDAN O‘CHIRISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^remove_favorite_accessory_\d+$")
)
async def remove_favorite_accessory(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    try:

        accessory_id = int(
            callback.data.split("_")[-1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Aksessuar ID noto‘g‘ri!",
            show_alert=True
        )

        return

    try:

        db.remove_favorite(
            user_id,
            "accessory",
            accessory_id
        )

    except Exception as error:

        db.connection.rollback()

        print(
            f"❌ AKSESSUARNI SEVIMLIDAN O‘CHIRISHDA XATO: {error}"
        )

        await callback.answer(
            "❌ O‘chirishda xatolik!",
            show_alert=True
        )

        return

    await callback.answer(
        "💔 Sevimlilardan o‘chirildi."
    )

    # Ro‘yxatni qayta chiqarish
    await show_favorites_again(
        callback
    )


# =========================================================
# 🔄 SEVIMLILARNI QAYTA KO‘RSATISH
# =========================================================

async def show_favorites_again(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    favorites = get_user_favorites(
        user_id
    )

    # =====================================================
    # ❤️ BO‘SH QOLDI
    # =====================================================

    if not favorites:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏠 Bosh menyu",
                        callback_data="back_main"
                    )
                ]
            ]
        )

        try:

            await callback.message.edit_text(
                "❤️ <b>SEVIMLILAR</b>\n\n"
                "Sizda hozircha sevimli mahsulotlar yo‘q.",
                reply_markup=keyboard
            )

        except TelegramBadRequest as error:

            if "message is not modified" not in str(error):
                raise

        return

    # =====================================================
    # 📝 MATN
    # =====================================================

    text = (
        "❤️ <b>SEVIMLI MAHSULOTLAR</b>\n\n"
    )

    buttons = []

    for index, favorite in enumerate(
        favorites,
        start=1
    ):

        item_type = favorite[0]
        item_id = favorite[1]
        name = favorite[2]
        price = favorite[3]
        category = favorite[4] or ""

        if item_type == "phone":

            text += (
                f"{index}. 📱 <b>{name}</b>\n"
                f"🏷 Brend: <b>{category}</b>\n"
                f"💰 Narx: <b>{price:,} so‘m</b>\n"
                "━━━━━━━━━━━━━━\n"
            )

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {name}",
                        callback_data=f"remove_favorite_phone_{item_id}"
                    )
                ]
            )

        elif item_type == "accessory":

            text += (
                f"{index}. 🎧 <b>{name}</b>\n"
                f"📂 Kategoriya: <b>{category}</b>\n"
                f"💰 Narx: <b>{price:,} so‘m</b>\n"
                "━━━━━━━━━━━━━━\n"
            )

            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"❌ {name}",
                        callback_data=f"remove_favorite_accessory_{item_id}"
                    )
                ]
            )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Bosh menyu",
                callback_data="back_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):
            return

        raise


# =========================================================
# 🏠 BOSH MENYU
# =========================================================

@router.callback_query(
    F.data == "back_main"
)
async def favorites_back_main(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    await callback.message.edit_text(
        "📱 <b>SMART PHONE SHOP</b>\n\n"
        f"Xush kelibsiz, "
        f"<b>{callback.from_user.first_name}</b> 👋\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu(user_id)
    )

    await callback.answer()