from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.exceptions import TelegramBadRequest

from database import Database
from config import ADMIN_ID


router = Router()
db = Database()

print("✅ ADMIN.PY ISHLADI")


# =========================================================
# 🔐 ADMIN TEKSHIRISH
# =========================================================

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# =========================================================
# 🎛 ADMIN MENYU
# =========================================================

def admin_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="👥 Foydalanuvchilar",
                    callback_data="admin_users"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📱 Telefonlar",
                    callback_data="admin_phones"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎧 Aksessuarlar",
                    callback_data="admin_accessories"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📦 Buyurtmalar",
                    callback_data="admin_orders"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📊 Statistika",
                    callback_data="admin_statistics"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ Bosh menyu",
                    callback_data="admin_back_main"
                )
            ]

        ]
    )


# =========================================================
# 🚀 /ADMIN
# =========================================================

@router.message(Command("admin"))
async def admin_command(
    message: Message
):

    if not is_admin(
        message.from_user.id
    ):

        await message.answer(
            "⛔ Siz admin emassiz."
        )

        return

    await message.answer(
        "👨‍💼 <b>ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=admin_menu()
    )


# =========================================================
# ⚙️ ADMIN PANEL BUTTON
# =========================================================

@router.callback_query(
    F.data == "admin_panel"
)
async def admin_panel_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Siz admin emassiz!",
            show_alert=True
        )

        return

    try:

        await callback.message.edit_text(
            "👨‍💼 <b>ADMIN PANEL</b>\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=admin_menu()
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Siz allaqachon admin paneldasiz."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 👥 FOYDALANUVCHILAR
# =========================================================

@router.callback_query(
    F.data == "admin_users"
)
async def admin_users_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Ruxsat yo‘q!",
            show_alert=True
        )

        return

    users = db.get_all_users()

    if not users:

        try:

            await callback.message.edit_text(
                "👥 <b>FOYDALANUVCHILAR</b>\n\n"
                "Foydalanuvchilar mavjud emas.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="⬅️ Admin panel",
                                callback_data="admin_panel"
                            )
                        ]
                    ]
                )
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "✅ Ma'lumotlar o‘zgarmagan."
                )

                return

            raise

        await callback.answer()
        return

    text = (
        "👥 <b>FOYDALANUVCHILAR</b>\n\n"
    )

    for index, user in enumerate(
        users,
        start=1
    ):

        database_id = user[0]
        telegram_id = user[1]
        full_name = user[2] or "Ism yo‘q"
        username = user[3] or "username yo‘q"
        phone = user[4] or "Telefon yo‘q"

        text += (
            f"{index}. 🆔 ID: <code>{database_id}</code>\n"
            f"👤 Ism: <b>{full_name}</b>\n"
            f"🔹 Telegram ID: <code>{telegram_id}</code>\n"
            f"🔗 Username: <b>{username}</b>\n"
            f"📞 Telefon: <b>{phone}</b>\n"
            "━━━━━━━━━━━━━━\n"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Ma'lumotlar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 📱 TELEFONLAR
# =========================================================

@router.callback_query(
    F.data == "admin_phones"
)
async def admin_phones_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Ruxsat yo‘q!",
            show_alert=True
        )

        return

    phones = db.get_phones()

    if not phones:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Admin panel",
                        callback_data="admin_panel"
                    )
                ]
            ]
        )

        try:

            await callback.message.edit_text(
                "📱 <b>TELEFONLAR</b>\n\n"
                "Telefonlar mavjud emas.",
                reply_markup=keyboard
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "✅ Ma'lumotlar allaqachon yangilangan."
                )

                return

            raise

        await callback.answer()
        return

    text = "📱 <b>TELEFONLAR</b>\n\n"

    for phone in phones:

        phone_id = phone[0]
        name = phone[1]
        price = phone[2]
        brand = phone[3]

        text += (
            f"🆔 <b>#{phone_id}</b>\n"
            f"📱 <b>{name}</b>\n"
            f"🏷 Brend: <b>{brand}</b>\n"
            f"💰 Narx: <b>{price:,} so‘m</b>\n"
            "━━━━━━━━━━━━━━\n"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Ma'lumotlar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 🎧 AKSESSUARLAR
# =========================================================

@router.callback_query(
    F.data == "admin_accessories"
)
async def admin_accessories_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Ruxsat yo‘q!",
            show_alert=True
        )

        return

    accessories = db.get_accessories()

    if not accessories:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Admin panel",
                        callback_data="admin_panel"
                    )
                ]
            ]
        )

        try:

            await callback.message.edit_text(
                "🎧 <b>AKSESSUARLAR</b>\n\n"
                "Aksessuarlar mavjud emas.",
                reply_markup=keyboard
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "✅ Ma'lumotlar allaqachon yangilangan."
                )

                return

            raise

        await callback.answer()
        return

    text = "🎧 <b>AKSESSUARLAR</b>\n\n"

    for accessory in accessories:

        accessory_id = accessory[0]
        name = accessory[1]
        price = accessory[2]
        category = accessory[3]

        text += (
            f"🆔 <b>#{accessory_id}</b>\n"
            f"🎧 <b>{name}</b>\n"
            f"📂 Kategoriya: <b>{category}</b>\n"
            f"💰 Narx: <b>{price:,} so‘m</b>\n"
            "━━━━━━━━━━━━━━\n"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Ma'lumotlar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 📦 BUYURTMALAR
# =========================================================

@router.callback_query(
    F.data == "admin_orders"
)
async def admin_orders_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Ruxsat yo‘q!",
            show_alert=True
        )

        return

    try:

        db.cursor.execute(
            """
            SELECT
                id,
                telegram_id,
                product_name,
                price,
                full_name,
                phone,
                region,
                city,
                address,
                payment,
                status,
                payment_status,
                created_at
            FROM orders
            ORDER BY id DESC
            """
        )

        orders = db.cursor.fetchall()

    except Exception as error:

        db.connection.rollback()

        print(
            f"❌ BUYURTMALARDA XATO: {error}"
        )

        await callback.answer(
            "❌ Buyurtmalarni olishda xato!",
            show_alert=True
        )

        return

    if not orders:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Admin panel",
                        callback_data="admin_panel"
                    )
                ]
            ]
        )

        try:

            await callback.message.edit_text(
                "📦 <b>BUYURTMALAR</b>\n\n"
                "Buyurtmalar mavjud emas.",
                reply_markup=keyboard
            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "✅ Ma'lumotlar allaqachon yangilangan."
                )

                return

            raise

        await callback.answer()
        return

    text = "📦 <b>BUYURTMALAR</b>\n\n"

    buttons = []

    for order in orders:

        order_id = order[0]
        product_name = order[2]
        price = order[3]
        status = order[10] or "pending"

        if status == "Tasdiqlandi":

            status_text = "✅ Tasdiqlandi"

        elif status == "Rad etildi":

            status_text = "❌ Rad etildi"

        else:

            status_text = "⏳ Yangi"

        text += (
            f"🆔 <b>#{order_id}</b>\n"
            f"📦 {product_name}\n"
            f"💰 {price:,} so‘m\n"
            f"📌 {status_text}\n"
            "━━━━━━━━━━━━━━\n"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📦 #{order_id}",
                    callback_data=f"admin_order_{order_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Admin panel",
                callback_data="admin_panel"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Buyurtmalar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 📦 BUYURTMA DETAIL
# =========================================================

@router.callback_query(
    F.data.regexp(r"^admin_order_\d+$")
)
async def admin_order_detail_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Ruxsat yo‘q!",
            show_alert=True
        )

        return

    try:

        order_id = int(
            callback.data.split("_")[2]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Buyurtma ID noto‘g‘ri!",
            show_alert=True
        )

        return

    order = db.get_order(
        order_id
    )

    if not order:

        await callback.answer(
            "❌ Buyurtma topilmadi!",
            show_alert=True
        )

        return

    (
        order_id,
        telegram_id,
        product_name,
        price,
        full_name,
        phone,
        region,
        city,
        address,
        payment,
        status,
        payment_status,
        created_at
    ) = order

    if status == "Tasdiqlandi":

        status_text = "✅ Tasdiqlandi"

    elif status == "Rad etildi":

        status_text = "❌ Rad etildi"

    else:

        status_text = "⏳ Yangi"

    text = (
        f"📦 <b>BUYURTMA #{order_id}</b>\n\n"
        f"👤 Ism: <b>{full_name or 'Kiritilmagan'}</b>\n"
        f"📞 Telefon: <b>{phone or 'Kiritilmagan'}</b>\n"
        f"📦 Mahsulot: <b>{product_name}</b>\n"
        f"💰 Narx: <b>{price:,} so‘m</b>\n"
        f"🌍 Viloyat: <b>{region or 'Kiritilmagan'}</b>\n"
        f"🏙 Shahar: <b>{city or 'Kiritilmagan'}</b>\n"
        f"📍 Manzil: <b>{address or 'Kiritilmagan'}</b>\n"
        f"💳 To‘lov: <b>{payment or 'Kiritilmagan'}</b>\n"
        f"📌 Holat: <b>{status_text}</b>\n"
        f"💳 To‘lov holati: <b>"
        f"{payment_status or 'Noma’lum'}"
        f"</b>\n"
        f"🕒 Sana: <b>{created_at}</b>"
    )

    buttons = []

    if status != "Tasdiqlandi":

        buttons.append(
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"admin_confirm_{order_id}"
                )
            ]
        )

    if status != "Rad etildi":

        buttons.append(
            [
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"admin_reject_{order_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Buyurtmalar",
                callback_data="admin_orders"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Admin panel",
                callback_data="admin_panel"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Ma'lumotlar allaqachon yangilangan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# ✅ BUYURTMANI TASDIQLASH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^admin_confirm_\d+$")
)
async def admin_confirm_order(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Siz admin emassiz!",
            show_alert=True
        )

        return

    try:

        order_id = int(
            callback.data.split("_")[2]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Buyurtma ID noto‘g‘ri!",
            show_alert=True
        )

        return

    order = db.get_order(
        order_id
    )

    if not order:

        await callback.answer(
            "❌ Buyurtma topilmadi!",
            show_alert=True
        )

        return

    telegram_id = order[1]
    product_name = order[2]

    db.update_order_status(
        order_id,
        "Tasdiqlandi"
    )

    db.update_payment_status(
        order_id,
        "Tasdiqlangan"
    )

    try:

        await callback.bot.send_message(
            telegram_id,
            "✅ <b>BUYURTMANGIZ TASDIQLANDI!</b>\n\n"
            f"📦 Mahsulot: <b>{product_name}</b>\n"
            f"🆔 Buyurtma: <b>#{order_id}</b>\n\n"
            "Buyurtmangiz tayyorlanmoqda."
        )

    except Exception as error:

        print(
            f"❌ USERGA XABAR YUBORISHDA XATO: {error}"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    try:

        await callback.message.edit_text(
            "✅ <b>BUYURTMA TASDIQLANDI</b>\n\n"
            f"🆔 Buyurtma: <b>#{order_id}</b>\n"
            f"📦 Mahsulot: <b>{product_name}</b>",
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Buyurtma allaqachon tasdiqlangan."
            )

            return

        raise

    await callback.answer(
        "✅ Buyurtma tasdiqlandi!"
    )


# =========================================================
# ❌ BUYURTMANI RAD ETISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^admin_reject_\d+$")
)
async def admin_reject_order(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Siz admin emassiz!",
            show_alert=True
        )

        return

    try:

        order_id = int(
            callback.data.split("_")[2]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Buyurtma ID noto‘g‘ri!",
            show_alert=True
        )

        return

    order = db.get_order(
        order_id
    )

    if not order:

        await callback.answer(
            "❌ Buyurtma topilmadi!",
            show_alert=True
        )

        return

    telegram_id = order[1]
    product_name = order[2]

    db.update_order_status(
        order_id,
        "Rad etildi"
    )

    db.update_payment_status(
        order_id,
        "Bekor qilindi"
    )

    try:

        await callback.bot.send_message(
            telegram_id,
            "❌ <b>BUYURTMANGIZ RAD ETILDI</b>\n\n"
            f"📦 Mahsulot: <b>{product_name}</b>\n"
            f"🆔 Buyurtma: <b>#{order_id}</b>\n\n"
            "Batafsil ma’lumot uchun administrator "
            "bilan bog‘lanishingiz mumkin."
        )

    except Exception as error:

        print(
            f"❌ USERGA XABAR YUBORISHDA XATO: {error}"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    try:

        await callback.message.edit_text(
            "❌ <b>BUYURTMA RAD ETILDI</b>\n\n"
            f"🆔 Buyurtma: <b>#{order_id}</b>\n"
            f"📦 Mahsulot: <b>{product_name}</b>",
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "❌ Buyurtma allaqachon rad etilgan."
            )

            return

        raise

    await callback.answer(
        "❌ Buyurtma rad etildi!"
    )


# =========================================================
# 📊 STATISTIKA
# =========================================================

@router.callback_query(
    F.data == "admin_statistics"
)
async def admin_statistics_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Siz admin emassiz!",
            show_alert=True
        )

        return

    # -----------------------------------------
    # 📊 MA'LUMOTLARNI OLISH
    # -----------------------------------------

    users_count = db.get_users_count()
    phones_count = db.get_phones_count()
    accessories_count = db.get_accessories_count()
    orders_count = db.get_orders_count()

    # -----------------------------------------
    # 📝 STATISTIKA MATNI
    # -----------------------------------------

    text = (
        "📊 <b>STATISTIKA</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{users_count}</b>\n"
        f"📱 Telefonlar: <b>{phones_count}</b>\n"
        f"🎧 Aksessuarlar: <b>{accessories_count}</b>\n"
        f"📦 Buyurtmalar: <b>{orders_count}</b>\n\n"
        "━━━━━━━━━━━━━━"
    )

    # -----------------------------------------
    # 🔘 TUGMALAR
    # -----------------------------------------

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="admin_statistics"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Admin panel",
                    callback_data="admin_panel"
                )
            ]
        ]
    )

    # -----------------------------------------
    # ✏️ XABARNI YANGILASH
    # -----------------------------------------

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        # Telegram xabarda hech narsa o‘zgarmaganida
        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Statistika allaqachon yangilangan!"
            )

            return

        # Boshqa xatoni yashirmaymiz
        raise

    await callback.answer(
        "✅ Statistika yangilandi!"
    )


# =========================================================
# 🏠 ADMIN PANELDAN BOSH MENYUGA
# =========================================================

@router.callback_query(
    F.data == "admin_back_main"
)
async def admin_back_main_handler(
    callback: CallbackQuery
):

    if not is_admin(
        callback.from_user.id
    ):

        await callback.answer(
            "⛔ Siz admin emassiz!",
            show_alert=True
        )

        return

    from buttons.main import main_menu

    keyboard = main_menu(
        callback.from_user.id
    )

    try:

        await callback.message.edit_text(
            "📱 <b>SMART PHONE SHOP</b>\n\n"
            f"Assalomu alaykum, "
            f"<b>{callback.from_user.first_name}</b> 👋\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "✅ Siz allaqachon bosh menyudasiz."
            )

            return

        raise

    await callback.answer()