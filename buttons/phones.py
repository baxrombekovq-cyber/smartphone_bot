from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def phones_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📱 iPhone",
                    callback_data="iphone"
                ),
                InlineKeyboardButton(
                    text="📱 Samsung",
                    callback_data="samsung"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Xiaomi",
                    callback_data="xiaomi"
                ),
                InlineKeyboardButton(
                    text="📱 Redmi",
                    callback_data="redmi"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="back_main"
                )
            ]
        ]
    )