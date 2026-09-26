from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID


# =========================================================
# 📱 ASOSIY MENYU
# =========================================================

def main_menu(user_id=None):

    buttons = [

        [
            InlineKeyboardButton(
                text="📱 Telefonlar",
                callback_data="phones"
            )
        ],

        [
            InlineKeyboardButton(
                text="🎧 Aksessuarlar",
                callback_data="accessories"
            )
        ],

        [
            InlineKeyboardButton(
                text="🔎 Telefon qidirish",
                callback_data="search_phone"
            )
        ],

        [
            InlineKeyboardButton(
                text="🛒 Savatcha",
                callback_data="cart"
            ),
            InlineKeyboardButton(
                text="❤️ Sevimlilar",
                callback_data="favorites"
            )
        ],

        [
            InlineKeyboardButton(
                text="📦 Buyurtmalarim",
                callback_data="orders"
            )
        ],

        [
            InlineKeyboardButton(
                text="💳 To‘lov",
                callback_data="payment"
            )
        ],

        [
            InlineKeyboardButton(
                text="👤 Profil",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                text="📞 Aloqa",
                callback_data="contact"
            )
        ]
    ]

    # =====================================================
    # 👨‍💼 FAQAT ADMIN UCHUN
    # =====================================================

    if user_id == ADMIN_ID:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="⚙️ Admin Panel",
                    callback_data="admin_panel"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )