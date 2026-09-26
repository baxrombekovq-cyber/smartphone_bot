from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cart_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Buyurtma berish",
                    callback_data="create_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Savatchani tozalash",
                    callback_data="clear_cart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Bosh menyu",
                    callback_data="back_main"
                )
            ]
        ]
    )