from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import Database
from buttons.accessories import accessories_buttons
from buttons.main import main_menu


router = Router()
db = Database()

print("✅ ACCESSORIES.PY ISHLADI")


# =========================================================
# 🎨 AKSESSUAR EMOJILARI
# =========================================================

ACCESSORY_EMOJIS = {
    "Zaryadlovchi": "🔌",
    "Powerbank": "🔋",
    "Quloqchin": "🎧",
    "USB kabel": "🔌",
    "Chexol": "📱",
    "Himoya oynasi": "🛡",
    "Simsiz zaryadlovchi": "📡",
    "Avto aksessuar": "🚗",
    "Telefon stendi": "📱",
    "OTG adapter": "🔄",
    "Kolonka": "🔊"
}


def get_accessory_emoji(category):
    return ACCESSORY_EMOJIS.get(
        category,
        "📦"
    )


# =========================================================
# 🎧 AKSESSUARLAR
# =========================================================

@router.callback_query(
    F.data == "accessories"
)
async def accessories_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "🎧 <b>AKSESSUARLAR</b>\n\n"
        "Aksessuar turini tanlang:",
        reply_markup=accessories_buttons()
    )

    await callback.answer()


# =========================================================
# 📦 AKSESSUAR KATEGORIYASI
# =========================================================

@router.callback_query(
    F.data.startswith("acc_")
)
async def accessory_category_handler(
    callback: CallbackQuery
):

    category = callback.data.replace(
        "acc_",
        "",
        1
    )

    all_accessories = db.get_accessories()

    accessories = [
        accessory
        for accessory in all_accessories
        if len(accessory) > 3
        and accessory[3] == category
    ]

    icon = get_accessory_emoji(
        category
    )

    if not accessories:

        await callback.message.edit_text(
            f"{icon} <b>{category}</b>\n\n"
            "❌ Hozircha mahsulotlar mavjud emas.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[

                    [
                        InlineKeyboardButton(
                            text="⬅️ Orqaga",
                            callback_data="accessories"
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
        f"{icon} <b>{category}</b>\n\n"
        "Mahsulotlardan birini tanlang:"
    )

    buttons = []

    for accessory in accessories:

        accessory_id = accessory[0]
        name = accessory[1]
        price = accessory[2]

        product_icon = get_accessory_emoji(
            category
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{product_icon} "
                        f"{name} — "
                        f"{price:,} so‘m"
                    ),
                    callback_data=(
                        f"accessory_{accessory_id}"
                    )
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="accessories"
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
# 📦 AKSESSUAR DETAIL
# =========================================================

@router.callback_query(
    F.data.regexp(r"^accessory_\d+$")
)
async def accessory_detail_handler(
    callback: CallbackQuery
):

    try:

        accessory_id = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Mahsulot ID noto‘g‘ri!",
            show_alert=True
        )

        return

    accessory = db.get_accessory(
        accessory_id
    )

    if not accessory:

        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )

        return

    await show_accessory(
        callback,
        accessory_id
    )

    await callback.answer()


# =========================================================
# ❤️ SEVIMLIGA QO‘SHISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^favorite_accessory_\d+$")
)
async def add_favorite_accessory_handler(
    callback: CallbackQuery
):

    try:

        accessory_id = int(
            callback.data.split("_")[2]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Mahsulot ID noto‘g‘ri!",
            show_alert=True
        )

        return

    user_id = callback.from_user.id

    accessory = db.get_accessory(
        accessory_id
    )

    if not accessory:

        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )

        return

    already_favorite = db.is_favorite(
        user_id,
        "accessory",
        accessory_id
    )

    if already_favorite:

        await callback.answer(
            "❤️ Bu mahsulot allaqachon sevimlilarda!",
            show_alert=True
        )

        return

    db.add_favorite(
        user_id,
        "accessory",
        accessory_id
    )

    await show_accessory(
        callback,
        accessory_id
    )

    await callback.answer(
        "❤️ Aksessuar sevimlilarga qo‘shildi!",
        show_alert=True
    )


# =========================================================
# 💔 SEVIMLIDAN O‘CHIRISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^unfavorite_accessory_\d+$")
)
async def remove_favorite_accessory_handler(
    callback: CallbackQuery
):

    try:

        accessory_id = int(
            callback.data.split("_")[2]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Mahsulot ID noto‘g‘ri!",
            show_alert=True
        )

        return

    user_id = callback.from_user.id

    accessory = db.get_accessory(
        accessory_id
    )

    if not accessory:

        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )

        return

    db.remove_favorite(
        user_id,
        "accessory",
        accessory_id
    )

    await show_accessory(
        callback,
        accessory_id
    )

    await callback.answer(
        "💔 Aksessuar sevimlilardan o‘chirildi!",
        show_alert=True
    )


# =========================================================
# 🎧 AKSESSUAR DETAILINI KO‘RSATISH
# =========================================================

async def show_accessory(
    callback: CallbackQuery,
    accessory_id: int
):

    accessory = db.get_accessory(
        accessory_id
    )

    if not accessory:

        return

    (
        accessory_id,
        name,
        price,
        category,
        description,
        image
    ) = accessory

    icon = get_accessory_emoji(
        category
    )

    # =====================================================
    # ❤️ SEVIMLILIKNI TEKSHIRISH
    # =====================================================

    is_fav = db.is_favorite(
        callback.from_user.id,
        "accessory",
        accessory_id
    )

    if is_fav:

        favorite_text = (
            "💔 Sevimlilardan o‘chirish"
        )

        favorite_callback = (
            f"unfavorite_accessory_{accessory_id}"
        )

    else:

        favorite_text = (
            "❤️ Sevimlilarga qo‘shish"
        )

        favorite_callback = (
            f"favorite_accessory_{accessory_id}"
        )

    # =====================================================
    # 🎛 BUTTONLAR
    # =====================================================

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🛒 Savatchaga qo‘shish",
                    callback_data=(
                        f"addacc_{accessory_id}"
                    )
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
                    text="⬅️ Aksessuarlarga",
                    callback_data=f"acc_{category}"
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
        f"{icon} <b>{name}</b>\n\n"
        f"📂 Kategoriya: <b>{category}</b>\n"
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
                f"❌ AKSESSUAR RASM XATOSI: {error}"
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
            f"❌ AKSESSUAR EDIT XATOSI: {error}"
        )

        await callback.message.answer(
            text,
            reply_markup=keyboard
        )


# =========================================================
# 🛒 AKSESSUARNI SAVATCHAGA QO‘SHISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^addacc_\d+$")
)
async def add_accessory_to_cart_handler(
    callback: CallbackQuery
):

    try:

        accessory_id = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Mahsulot ID noto‘g‘ri!",
            show_alert=True
        )

        return

    accessory = db.get_accessory(
        accessory_id
    )

    if not accessory:

        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )

        return

    (
        accessory_id,
        name,
        price,
        category,
        description,
        image
    ) = accessory

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
    F.data == "back_main"
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