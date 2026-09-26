from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from buttons.main import main_menu


router = Router()

print("✅ PAYMENT.PY ISHLADI")


# =========================================================
# 💳 KARTA MA'LUMOTLARI
# =========================================================

UZCARD_NUMBER = "UZCARD_RAQAMINI_SHU_YERGA_QOYING"
UZCARD_OWNER = "Maxliyo Raxmatillayeva"

HUMO_NUMBER = "HUMO_RAQAMINI_SHU_YERGA_QOYING"
HUMO_OWNER = "Maxliyo Raxmatillayeva"


# =========================================================
# 💳 TO‘LOV MENYUSI
# =========================================================

def payment_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="💳 Uzcard",
                    callback_data="pay_uzcard"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💳 Humo",
                    callback_data="pay_humo"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💵 Naqd pul",
                    callback_data="pay_cash"
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


# =========================================================
# 💳 TO‘LOV
# =========================================================

@router.callback_query(
    F.data == "payment"
)
async def payment_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "💳 <b>TO‘LOV USULI</b>\n\n"
        "To‘lov usulini tanlang:",
        reply_markup=payment_menu()
    )

    await callback.answer()


# =========================================================
# 💳 UZCARD
# =========================================================

@router.callback_query(
    F.data == "pay_uzcard"
)
async def uzcard_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "💳 <b>UZCARD ORQALI TO‘LOV</b>\n\n"
        f"💳 Karta raqami:\n"
        f"<code>{UZCARD_NUMBER}</code>\n\n"
        f"👤 Karta egasi:\n"
        f"<b>{UZCARD_OWNER}</b>\n\n"
        "Kerakli summani kartaga o‘tkazing.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="✅ To‘lov qildim",
                        callback_data="payment_done"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="⬅️ To‘lov usullari",
                        callback_data="payment"
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


# =========================================================
# 💳 HUMO
# =========================================================

@router.callback_query(
    F.data == "pay_humo"
)
async def humo_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "💳 <b>HUMO ORQALI TO‘LOV</b>\n\n"
        f"💳 Karta raqami:\n"
        f"<code>{HUMO_NUMBER}</code>\n\n"
        f"👤 Karta egasi:\n"
        f"<b>{HUMO_OWNER}</b>\n\n"
        "Kerakli summani kartaga o‘tkazing.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="✅ To‘lov qildim",
                        callback_data="payment_done"
                    )
                ],

                [
                    InlineKeyboardButton(
                        text="⬅️ To‘lov usullari",
                        callback_data="payment"
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


# =========================================================
# 💵 NAQD PUL
# =========================================================

@router.callback_query(
    F.data == "pay_cash"
)
async def cash_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "💵 <b>NAQD PUL</b>\n\n"
        "To‘lov mahsulot yetkazilganda "
        "amalga oshiriladi.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[

                [
                    InlineKeyboardButton(
                        text="⬅️ To‘lov usullari",
                        callback_data="payment"
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


# =========================================================
# ✅ TO‘LOV QILINDI
# =========================================================

@router.callback_query(
    F.data == "payment_done"
)
async def payment_done_handler(
    callback: CallbackQuery
):

    await callback.message.edit_text(
        "✅ <b>TO‘LOV MA'LUMOTI QABUL QILINDI</b>\n\n"
        "⏳ To‘lovingiz administrator tomonidan "
        "tekshiriladi.\n\n"
        "Buyurtma holati bot orqali yuboriladi.",
        reply_markup=main_menu(
            callback.from_user.id
        )
    )

    await callback.answer(
        "✅ To‘lov yuborildi!"
    )


# =========================================================
# 🏠 BOSH MENYU
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
        reply_markup=main_menu(
            callback.from_user.id
        )
    )

    await callback.answer()