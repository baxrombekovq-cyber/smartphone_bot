
from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import Database
from buttons.phones import phones_buttons
from buttons.main import main_menu


router = Router()
db = Database()


# =========================================================
# 📱 TELEFONLAR
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "phones"
)
async def phones_handler(callback: CallbackQuery):

    await callback.message.edit_text(
        "📱 <b>TELEFONLAR</b>\n\n"
        "Telefon brendini tanlang:",
        reply_markup=phones_buttons()
    )

    await callback.answer()


# =========================================================
# 📱 BREND TANLASH
# =========================================================

@router.callback_query(
    lambda callback: callback.data in [
        "iphone",
        "samsung",
        "xiaomi",
        "redmi"
    ]
)
async def phone_brand_handler(callback: CallbackQuery):

    brands = {
        "iphone": "iPhone",
        "samsung": "Samsung",
        "xiaomi": "Xiaomi",
        "redmi": "Redmi"
    }

    brand = brands.get(callback.data)

    if not brand:

        await callback.answer(
            "❌ Brend topilmadi!",
            show_alert=True
        )
        return

    all_phones = db.get_phones()

    phones = [
        phone
        for phone in all_phones
        if len(phone) > 3 and phone[3] == brand
    ]

    if not phones:

        await callback.message.edit_text(
            f"❌ <b>{brand}</b> telefonlari topilmadi!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="⬅️ Orqaga",
                            callback_data="phones"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🏠 Bosh menyu",
                            callback_data="back_main"
                        )
                    ]
                ]
            )
        )

        await callback.answer()
        return

    text = (
        f"📱 <b>{brand}</b>\n\n"
        "Telefonlardan birini tanlang:\n\n"
    )

    buttons = []

    for phone in phones:

        phone_id = phone[0]
        name = phone[1]
        price = phone[2]

        text += (
            f"📱 <b>{name}</b>\n"
            f"💰 {price:,} so‘m\n\n"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📱 {name}",
                    callback_data=f"phone_{phone_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="phones"
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

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        )
    )

    await callback.answer()


# =========================================================
# 📦 TELEFON DETAIL
# =========================================================

@router.callback_query(
    lambda callback: callback.data.startswith("phone_")
)
async def phone_detail_handler(callback: CallbackQuery):

    try:

        phone_id = int(
            callback.data.replace(
                "phone_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )
        return

    phone = db.get_phone(phone_id)

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )
        return

    await show_phone(
        callback,
        phone_id
    )

    await callback.answer()


# =========================================================
# ❤️ TELEFONNI SEVIMLIGA
# =========================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("favorite_phone_")
)
async def add_favorite_handler(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "favorite_phone_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )
        return

    user_id = callback.from_user.id

    phone = db.get_phone(phone_id)

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )
        return

    # ✅ PARAMETRLAR TO‘G‘RI TARTIBDA
    already_favorite = db.is_favorite(
        user_id,
        "phone",
        phone_id
    )

    if already_favorite:

        await callback.answer(
            "❤️ Bu telefon allaqachon sevimlilarda!",
            show_alert=True
        )
        return

    # ✅ PARAMETRLAR TO‘G‘RI TARTIBDA
    db.add_favorite(
        user_id,
        "phone",
        phone_id
    )

    await show_phone(
        callback,
        phone_id
    )

    await callback.answer(
        "❤️ Telefon sevimlilarga qo‘shildi!",
        show_alert=True
    )


# =========================================================
# 💔 TELEFONNI SEVIMLIDAN O‘CHIRISH
# =========================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("unfavorite_phone_")
)
async def remove_favorite_handler(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "unfavorite_phone_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )
        return

    user_id = callback.from_user.id

    phone = db.get_phone(phone_id)

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )
        return

    # ✅ PARAMETRLAR TO‘G‘RI TARTIBDA
    db.remove_favorite(
        user_id,
        "phone",
        phone_id
    )

    await show_phone(
        callback,
        phone_id
    )

    await callback.answer(
        "💔 Telefon sevimlilardan o‘chirildi!",
        show_alert=True
    )


# =========================================================
# 📱 TELEFON DETAILINI KO‘RSATISH
# =========================================================

async def show_phone(
    callback: CallbackQuery,
    phone_id: int
):

    phone = db.get_phone(phone_id)

    if not phone:
        return

    (
        phone_id,
        name,
        price,
        brand,
        description,
        image
    ) = phone

    # =====================================================
    # ❤️ SEVIMLILIKNI TEKSHIRISH
    # =====================================================

    is_fav = db.is_favorite(
        callback.from_user.id,
        "phone",
        phone_id
    )

    if is_fav:

        favorite_text = "💔 Sevimlilardan o‘chirish"

        favorite_callback = (
            f"unfavorite_phone_{phone_id}"
        )

    else:

        favorite_text = "❤️ Sevimlilarga qo‘shish"

        favorite_callback = (
            f"favorite_phone_{phone_id}"
        )

    # =====================================================
    # 🎛 BUTTONLAR
    # =====================================================

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🛒 Savatchaga qo‘shish",
                    callback_data=f"addcart_{phone_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text=favorite_text,
                    callback_data=favorite_callback
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ Telefonlarga",
                    callback_data=brand.lower()
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 Bosh menyu",
                    callback_data="back_main"
                )
            ]

        ]
    )

    # =====================================================
    # 📝 MATN
    # =====================================================

    text = (
        f"📱 <b>{name}</b>\n\n"
        f"🏷 Brend: <b>{brand}</b>\n"
        f"💰 Narxi: <b>{price:,} so‘m</b>\n"
    )

    if description:

        text += (
            f"📝 Tavsif: {description}\n"
        )

    text += (
        "\n"
        "Kerakli amalni tanlang:"
    )

    # =====================================================
    # 🖼 RASM BOR BO‘LSA
    # =====================================================

    if image:

        try:

            await callback.message.delete()

            await callback.message.answer_photo(
                photo=image,
                caption=text,
                reply_markup=keyboard
            )

            return

        except Exception as error:

            print(
                f"❌ RASM CHIQARISHDA XATO: {error}"
            )

            await callback.message.answer(
                text,
                reply_markup=keyboard
            )

            return

    # =====================================================
    # 📝 RASM YO‘Q
    # =====================================================

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except Exception as error:

        print(
            f"❌ MATN O‘ZGARTIRISHDA XATO: {error}"
        )

        await callback.message.answer(
            text,
            reply_markup=keyboard
        )


# =========================================================
# 🛒 TELEFONNI SAVATCHAGA
# =========================================================

@router.callback_query(
    lambda callback:
        callback.data.startswith("addcart_")
)
async def add_to_cart_handler(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "addcart_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )
        return

    phone = db.get_phone(phone_id)

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )
        return

    (
        phone_id,
        name,
        price,
        brand,
        description,
        image
    ) = phone

    db.add_to_cart(
        callback.from_user.id,
        name,
        price
    )

    await callback.answer(
        f"✅ {name} savatchaga qo‘shildi!",
        show_alert=True
    )


# =========================================================
# ⬅️ BOSH MENYU
# =========================================================

@router.callback_query(
    lambda callback:
        callback.data == "back_main"
)
async def back_main_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "📱 <b>SMART PHONE SHOP</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{callback.from_user.first_name}</b> 👋\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu()
    )

    await callback.answer()

