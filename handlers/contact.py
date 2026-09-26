from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.callback_query(
    lambda callback: callback.data == "contact"
)
async def contact_handler(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👨‍💼 Admin bilan bog‘lanish",
                    url="https://t.me/dilshodovich_770"
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

    await callback.message.edit_text(
        "📞 <b>BIZ BILAN BOG‘LANISH</b>\n\n"
        "📱 <b>Telefon:</b> +998 98 777 73 35\n"
        "👨‍💼 <b>Admin:</b> @dilshodovich_770\n"
        "⏰ <b>Ish vaqti:</b> 09:00 — 22:00\n"
        "📍 <b>Manzil:</b> Qarshi shahri\n\n"
        "Savollaringiz bo‘lsa, biz bilan bog‘laning.",
        reply_markup=keyboard
    )

    await callback.answer()