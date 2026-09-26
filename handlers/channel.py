from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from config import CHANNEL_ID

from buttons.channel import channel_buttons
from buttons.main import main_menu


router = Router()


# =========================================================
# ✅ OBUNANI TEKSHIRISH
# =========================================================

@router.callback_query(
    F.data == "check_subscription"
)
async def check_subscription(
    callback: CallbackQuery
):

    try:

        member = await callback.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=callback.from_user.id
        )

        subscribed = member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as error:

        print(
            f"❌ KANAL TEKSHIRISHDA XATO: {error}"
        )

        await callback.answer(
            "❌ Kanalni tekshirishda xatolik!",
            show_alert=True
        )

        return


    # =====================================================
    # ✅ OBUNA BOR
    # =====================================================

    if subscribed:

        try:

            await callback.message.edit_text(
                "✅ <b>Obuna tasdiqlandi!</b>\n\n"
                "📱 <b>SMART PHONE SHOP</b>\n\n"
                "Kerakli bo‘limni tanlang:",
                reply_markup=main_menu(
                    callback.from_user.id
                )
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "✅ Siz allaqachon obuna bo‘lgansiz."
                )

            else:

                print(
                    f"❌ XABAR XATOSI: {error}"
                )

                await callback.answer(
                    "❌ Xatolik yuz berdi!",
                    show_alert=True
                )

        else:

            await callback.answer(
                "✅ Obuna tasdiqlandi!"
            )

        return


    # =====================================================
    # ❌ OBUNA YO‘Q
    # =====================================================

    try:

        await callback.message.edit_text(
            "❌ <b>Siz hali kanalga obuna bo‘lmagansiz!</b>\n\n"
            "Avval kanalimizga obuna bo‘ling 👇",
            reply_markup=channel_buttons()
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "❌ Avval kanalga obuna bo‘ling!",
                show_alert=True
            )

        else:

            print(
                f"❌ XABAR XATOSI: {error}"
            )

            await callback.answer(
                "❌ Xatolik yuz berdi!",
                show_alert=True
            )

        return

    await callback.answer(
        "❌ Avval kanalga obuna bo‘ling!",
        show_alert=True
    )