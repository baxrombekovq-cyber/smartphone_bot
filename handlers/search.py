from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import Database
from buttons.main import main_menu


router = Router()
db = Database()

print("✅ SEARCH.PY ISHLADI")


# =========================================================
# 🔎 SEARCH STATE
# =========================================================

class SearchState(StatesGroup):
    waiting_for_text = State()


# =========================================================
# 🔎 TELEFON QIDIRISHNI BOSHLASH
# =========================================================

@router.callback_query(F.data == "search_phone")
async def search_phone_handler(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        SearchState.waiting_for_text
    )

    await callback.message.edit_text(
        "🔎 <b>TELEFON QIDIRISH</b>\n\n"
        "Telefon nomi yoki brendini yozing.\n\n"
        "Masalan:\n"
        "📱 iPhone\n"
        "📱 iPhone 15\n"
        "📱 Samsung\n"
        "📱 Galaxy S24\n"
        "📱 Xiaomi\n"
        "📱 Redmi"
    )

    await callback.answer()


# =========================================================
# 🔎 TELEFONNI QIDIRISH
# =========================================================

@router.message(SearchState.waiting_for_text)
async def search_phone_result(
    message: Message,
    state: FSMContext
):

    search_text = (message.text or "").strip()

    # -----------------------------------------------------
    # BO'SH QIDIRUV
    # -----------------------------------------------------

    if not search_text:

        await message.answer(
            "❌ <b>Qidiruv matni bo‘sh bo‘lishi mumkin emas.</b>\n\n"
            "Telefon nomi yoki brendini yozing."
        )

        return

    # -----------------------------------------------------
    # BARCHA TELEFONLARNI OLAMIZ
    # -----------------------------------------------------

    phones = db.get_phones()

    if not phones:

        await state.clear()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔎 Qayta qidirish",
                        callback_data="search_phone"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📱 Telefonlar",
                        callback_data="phones"
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

        await message.answer(
            "❌ <b>Hozircha telefonlar mavjud emas.</b>",
            reply_markup=keyboard
        )

        return

    # -----------------------------------------------------
    # QIDIRUVNI TAYYORLASH
    # -----------------------------------------------------

    search_lower = search_text.casefold()

    # Bo'shliqsiz variant
    search_normalized = (
        search_lower
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )

    results = []

    # -----------------------------------------------------
    # QIDIRISH
    # -----------------------------------------------------

    for phone in phones:

        # id, name, price, brand, description, image

        phone_id = phone[0]
        name = phone[1] or ""
        price = phone[2] or 0
        brand = phone[3] or ""
        description = phone[4] or ""
        image = phone[5] or ""

        # -------------------------
        # Oddiy text
        # -------------------------

        name_lower = name.casefold()
        brand_lower = brand.casefold()
        description_lower = description.casefold()

        # -------------------------
        # Bo'shliqsiz text
        # -------------------------

        name_normalized = (
            name_lower
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        brand_normalized = (
            brand_lower
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        description_normalized = (
            description_lower
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        # -------------------------
        # QIDIRUV SHARTI
        # -------------------------

        found = (
            search_lower in name_lower
            or search_lower in brand_lower
            or search_lower in description_lower
            or search_normalized in name_normalized
            or search_normalized in brand_normalized
            or search_normalized in description_normalized
        )

        if found:
            results.append(
                phone
            )

    # =====================================================
    # ❌ NATIJA TOPILMADI
    # =====================================================

    if not results:

        await state.clear()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔎 Qayta qidirish",
                        callback_data="search_phone"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📱 Telefonlar",
                        callback_data="phones"
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

        await message.answer(
            f"🔎 <b>Qidiruv:</b> {search_text}\n\n"
            "❌ <b>Bunday telefon hozirda mavjud emas.</b>",
            reply_markup=keyboard
        )

        return

    # =====================================================
    # ✅ NATIJALAR
    # =====================================================

    text = (
        "🔎 <b>QIDIRUV NATIJASI</b>\n\n"
        f"🔍 Qidiruv: <b>{search_text}</b>\n"
        f"📦 Topildi: <b>{len(results)}</b> ta telefon\n\n"
    )

    buttons = []

    for phone in results:

        (
            phone_id,
            name,
            price,
            brand,
            description,
            image
        ) = phone

        text += (
            f"📱 <b>{name}</b>\n"
            f"🏷 Brend: <b>{brand}</b>\n"
            f"💰 Narxi: <b>{price:,} so‘m</b>\n"
        )

        if description:
            text += (
                f"📝 {description}\n"
            )

        text += (
            "━━━━━━━━━━━━━━━━\n"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📱 {name}",
                    callback_data=f"search_phone_{phone_id}"
                )
            ]
        )

    # Yangi qidiruv
    buttons.append(
        [
            InlineKeyboardButton(
                text="🔎 Yangi qidiruv",
                callback_data="search_phone"
            )
        ]
    )

    # Telefonlar
    buttons.append(
        [
            InlineKeyboardButton(
                text="📱 Telefonlar",
                callback_data="phones"
            )
        ]
    )

    # Bosh menyu
    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Bosh menyu",
                callback_data="back_main"
            )
        ]
    )

    await state.clear()

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        )
    )


# =========================================================
# 📱 TELEFON DETAIL
# =========================================================

@router.callback_query(
    F.data.regexp(r"^search_phone_\d+$")
)
async def search_phone_detail(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "search_phone_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )

        return

    # -----------------------------------------------------
    # TELEFONNI OLAMIZ
    # -----------------------------------------------------

    phone = db.get_phone(
        phone_id
    )

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )

        return

    (
        phone_id,
        name,
        price,
        brand,
        description,
        image
    ) = phone

    # -----------------------------------------------------
    # DETAIL MATNI
    # -----------------------------------------------------

    text = (
        f"📱 <b>{name}</b>\n\n"
        f"🏷 Brend: <b>{brand}</b>\n"
        f"💰 Narxi: <b>{price:,} so‘m</b>\n"
    )

    if description:

        text += (
            f"📝 Tavsif: {description}\n"
        )

    # -----------------------------------------------------
    # FAVORITE TEKSHIRISH
    # -----------------------------------------------------

    user_id = callback.from_user.id

    try:

        is_fav = db.is_favorite(
            user_id,
            "phone",
            phone_id
        )

    except Exception as error:

        print(
            f"❌ FAVORITE TEKSHIRISH XATOSI: {error}"
        )

        is_fav = False

    # -----------------------------------------------------
    # TUGMALAR
    # -----------------------------------------------------

    favorite_text = (
        "💔 Sevimlilardan olib tashlash"
        if is_fav
        else
        "❤️ Sevimlilarga qo‘shish"
    )

    favorite_callback = (
        f"search_unfav_{phone_id}"
        if is_fav
        else
        f"search_fav_{phone_id}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Savatchaga qo‘shish",
                    callback_data=f"search_add_cart_{phone_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=favorite_text,
                    callback_data=favorite_callback
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔎 Qidirishga qaytish",
                    callback_data="search_phone"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Telefonlar",
                    callback_data="phones"
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

    # =====================================================
    # 🖼 RASM BOR
    # =====================================================

    if image:

        try:

            await callback.message.delete()

            await callback.message.answer_photo(
                photo=image,
                caption=text,
                reply_markup=keyboard
            )

        except Exception as error:

            print(
                f"❌ RASM XATOSI: {error}"
            )

            await callback.message.answer(
                text,
                reply_markup=keyboard
            )

    # =====================================================
    # 📝 RASM YO‘Q
    # =====================================================

    else:

        try:

            await callback.message.edit_text(
                text,
                reply_markup=keyboard
            )

        except Exception as error:

            print(
                f"❌ TELEFON DETAIL XATOSI: {error}"
            )

            await callback.message.answer(
                text,
                reply_markup=keyboard
            )

    await callback.answer()


# =========================================================
# 🛒 SAVATCHAGA QO‘SHISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^search_add_cart_\d+$")
)
async def search_add_cart(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "search_add_cart_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )

        return

    phone = db.get_phone(
        phone_id
    )

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )

        return

    (
        phone_id,
        name,
        price,
        brand,
        description,
        image
    ) = phone

    # -----------------------------------------------------
    # SAVATCHAGA QO‘SHAMIZ
    # -----------------------------------------------------

    db.add_to_cart(
        callback.from_user.id,
        name,
        price
    )

    await callback.answer(
        "✅ Savatchaga qo‘shildi!",
        show_alert=True
    )

    await callback.message.answer(
        f"✅ <b>{name}</b>\n\n"
        "🛒 Savatchaga muvaffaqiyatli qo‘shildi.\n"
        f"💰 Narxi: <b>{price:,} so‘m</b>"
    )


# =========================================================
# ❤️ SEVIMLIGA QO‘SHISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^search_fav_\d+$")
)
async def search_add_favorite(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "search_fav_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )

        return

    phone = db.get_phone(
        phone_id
    )

    if not phone:

        await callback.answer(
            "❌ Telefon topilmadi!",
            show_alert=True
        )

        return

    user_id = callback.from_user.id

    # -----------------------------------------------------
    # ALLAQACHON BOR
    # -----------------------------------------------------

    if db.is_favorite(
        user_id,
        "phone",
        phone_id
    ):

        await callback.answer(
            "❤️ Bu telefon allaqachon sevimlilarda!",
            show_alert=True
        )

        return

    # -----------------------------------------------------
    # SEVIMLIGA QO‘SHISH
    # -----------------------------------------------------

    db.add_favorite(
        user_id,
        "phone",
        phone_id
    )

    await callback.answer(
        "❤️ Sevimlilarga qo‘shildi!",
        show_alert=True
    )

    # Detail oynasini yangilaymiz
    phone = db.get_phone(phone_id)

    if phone:

        (
            phone_id,
            name,
            price,
            brand,
            description,
            image
        ) = phone

        text = (
            f"📱 <b>{name}</b>\n\n"
            f"🏷 Brend: <b>{brand}</b>\n"
            f"💰 Narxi: <b>{price:,} so‘m</b>\n"
        )

        if description:
            text += f"📝 Tavsif: {description}\n"

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Savatchaga qo‘shish",
                        callback_data=f"search_add_cart_{phone_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="💔 Sevimlilardan olib tashlash",
                        callback_data=f"search_unfav_{phone_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔎 Qidirishga qaytish",
                        callback_data="search_phone"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📱 Telefonlar",
                        callback_data="phones"
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

        if image:

            try:

                await callback.message.delete()

                await callback.message.answer_photo(
                    photo=image,
                    caption=text,
                    reply_markup=keyboard
                )

            except Exception as error:

                print(
                    f"❌ FAVORITE RASM XATOSI: {error}"
                )

        else:

            try:

                await callback.message.edit_text(
                    text,
                    reply_markup=keyboard
                )

            except Exception as error:

                print(
                    f"❌ FAVORITE TEXT XATOSI: {error}"
                )


# =========================================================
# 💔 SEVIMLIDAN O‘CHIRISH
# =========================================================

@router.callback_query(
    F.data.regexp(r"^search_unfav_\d+$")
)
async def search_remove_favorite(
    callback: CallbackQuery
):

    try:

        phone_id = int(
            callback.data.replace(
                "search_unfav_",
                "",
                1
            )
        )

    except ValueError:

        await callback.answer(
            "❌ Telefon ID noto‘g‘ri!",
            show_alert=True
        )

        return

    user_id = callback.from_user.id

    db.remove_favorite(
        user_id,
        "phone",
        phone_id
    )

    await callback.answer(
        "💔 Sevimlilardan olib tashlandi!",
        show_alert=True
    )

    phone = db.get_phone(
        phone_id
    )

    if not phone:
        return

    (
        phone_id,
        name,
        price,
        brand,
        description,
        image
    ) = phone

    text = (
        f"📱 <b>{name}</b>\n\n"
        f"🏷 Brend: <b>{brand}</b>\n"
        f"💰 Narxi: <b>{price:,} so‘m</b>\n"
    )

    if description:
        text += f"📝 Tavsif: {description}\n"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Savatchaga qo‘shish",
                    callback_data=f"search_add_cart_{phone_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❤️ Sevimlilarga qo‘shish",
                    callback_data=f"search_fav_{phone_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔎 Qidirishga qaytish",
                    callback_data="search_phone"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Telefonlar",
                    callback_data="phones"
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

    if image:

        try:

            await callback.message.delete()

            await callback.message.answer_photo(
                photo=image,
                caption=text,
                reply_markup=keyboard
            )

        except Exception as error:

            print(
                f"❌ UNFAV RASM XATOSI: {error}"
            )

    else:

        try:

            await callback.message.edit_text(
                text,
                reply_markup=keyboard
            )

        except Exception as error:

            print(
                f"❌ UNFAV TEXT XATOSI: {error}"
            )


# =========================================================
# 🏠 BOSH MENYU
# =========================================================

@router.callback_query(
    F.data == "back_main"
)
async def search_back_main(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.clear()

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