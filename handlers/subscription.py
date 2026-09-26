from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import CHANNEL_ID
from buttons.main import main_menu

router = Router()


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery):

    member = await callback.bot.get_chat_member(
        chat_id=CHANNEL_ID,
        user_id=callback.from_user.id
    )

    if member.status in ["member", "administrator", "creator"]:

        await callback.message.edit_text(
            "✅ <b>Obuna tasdiqlandi!</b>\n\n"
            "📱 <b>SMART PHONE SHOP</b>\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu()
        )

        await callback.answer()

    else:
        await callback.answer(
            "❌ Avval kanalga obuna bo‘ling!",
            show_alert=True
        )