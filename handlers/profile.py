from aiogram import Router
from aiogram.types import CallbackQuery

from buttons.main import main_menu

router = Router()


@router.callback_query(lambda callback: callback.data == "profile")
async def profile_handler(callback: CallbackQuery):

    user = callback.from_user

    username = user.username or "username yo‘q"

    await callback.message.edit_text(
        "👤 <b>Sizning profilingiz</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Ism: {user.full_name}\n"
        f"🔗 Username: @{username}",
        reply_markup=main_menu()
    )

    await callback.answer()