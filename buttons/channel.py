
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNEL_USERNAME


# =========================================================
# 📢 KANAL TUGMALARI
# =========================================================

def channel_buttons():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 Kanalga qo‘shilish",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )
            ]

        ]
    )

