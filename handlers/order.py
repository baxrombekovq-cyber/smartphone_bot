from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from database import Database
from config import ADMIN_ID
from buttons.main import main_menu


router = Router()
db = Database()

print("✅ ORDER.PY ISHLADI")


# =========================================================
# 💳 KARTA MA'LUMOTLARI
# =========================================================

UZCARD_NUMBER = "5440.8103.1125.2984"
UZCARD_OWNER = "Maxliyo Raxmatillayeva"

HUMO_NUMBER = "9860.0803.1141.1351"
HUMO_OWNER = "Maxliyo Raxmatillayeva"

VISA_NUMBER = "4466.1369.5126.6783"
VISA_OWNER = "Jasmina Bakhrombekova"


# =========================================================
# 🚚 YETKAZIB BERISH MUDDATLARI
# =========================================================

DELIVERY_DAYS = {

    "Toshkent shahri": "1–2 kun",

    "Toshkent viloyati": "1–2 kun",

    "Andijon viloyati": "2–3 kun",

    "Namangan viloyati": "2–3 kun",

    "Farg‘ona viloyati": "2–3 kun",

    "Sirdaryo viloyati": "2–3 kun",

    "Jizzax viloyati": "2–3 kun",

    "Samarqand viloyati": "2–3 kun",

    "Qashqadaryo viloyati": "1–2 kun",

    "Surxondaryo viloyati": "3–4 kun",

    "Buxoro viloyati": "3–4 kun",

    "Navoiy viloyati": "3–4 kun",

    "Xorazm viloyati": "4–5 kun",

    "Qoraqalpog‘iston Respublikasi": "4–5 kun"
}


# =========================================================
# 📦 ORDER STATES
# =========================================================

class OrderState(StatesGroup):

    waiting_full_name = State()
    waiting_phone = State()
    waiting_region = State()
    waiting_city = State()
    waiting_address = State()
    waiting_payment = State()


# =========================================================
# 📍 VILOYATLAR
# =========================================================

REGIONS = [

    "Toshkent shahri",
    "Toshkent viloyati",
    "Andijon viloyati",
    "Namangan viloyati",
    "Farg‘ona viloyati",
    "Sirdaryo viloyati",
    "Jizzax viloyati",
    "Samarqand viloyati",
    "Qashqadaryo viloyati",
    "Surxondaryo viloyati",
    "Buxoro viloyati",
    "Navoiy viloyati",
    "Xorazm viloyati",
    "Qoraqalpog‘iston Respublikasi"
]


# =========================================================
# 🏙 SHAHARLAR
# =========================================================

CITIES = {

    "Toshkent shahri": [
        "Toshkent"
    ],

    "Toshkent viloyati": [
        "Chirchiq",
        "Olmaliq",
        "Angren",
        "Bekobod",
        "Yangiyo‘l"
    ],

    "Andijon viloyati": [
        "Andijon",
        "Asaka",
        "Shahrixon",
        "Xonobod"
    ],

    "Namangan viloyati": [
        "Namangan",
        "Chortoq",
        "Chust",
        "Pop",
        "Kosonsoy"
    ],

    "Farg‘ona viloyati": [
        "Farg‘ona",
        "Qo‘qon",
        "Marg‘ilon",
        "Quva"
    ],

    "Sirdaryo viloyati": [
        "Guliston",
        "Yangiyer",
        "Shirin"
    ],

    "Jizzax viloyati": [
        "Jizzax",
        "G‘allaorol",
        "Zomin"
    ],

    "Samarqand viloyati": [
        "Samarqand",
        "Kattaqo‘rg‘on",
        "Urgut",
        "Jomboy"
    ],

    "Qashqadaryo viloyati": [
        "Qarshi",
        "Shahrisabz",
        "Kitob",
        "Koson"
    ],

    "Surxondaryo viloyati": [
        "Termiz",
        "Denov",
        "Sherobod",
        "Boysun"
    ],

    "Buxoro viloyati": [
        "Buxoro",
        "G‘ijduvon",
        "Kogon",
        "Vobkent"
    ],

    "Navoiy viloyati": [
        "Navoiy",
        "Zarafshon",
        "Karmana"
    ],

    "Xorazm viloyati": [
        "Urganch",
        "Xiva",
        "Shovot",
        "Hazorasp"
    ],

    "Qoraqalpog‘iston Respublikasi": [
        "Nukus",
        "Qo‘ng‘irot",
        "Mo‘ynoq"
    ]
}


# =========================================================
# 💳 TO‘LOV TUGMALARI
# =========================================================

def payment_buttons():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="💳 Uzcard",
                    callback_data="order_pay_uzcard"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💳 Humo",
                    callback_data="order_pay_humo"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💳 Visa",
                    callback_data="order_pay_visa"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💵 Naqd pul",
                    callback_data="order_pay_cash"
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
# 📍 VILOYAT TUGMALARI
# =========================================================

def region_buttons():

    buttons = []

    for index in range(
        0,
        len(REGIONS),
        2
    ):

        row = [
            InlineKeyboardButton(
                text=REGIONS[index],
                callback_data=f"region_{index}"
            )
        ]

        if index + 1 < len(REGIONS):

            row.append(
                InlineKeyboardButton(
                    text=REGIONS[index + 1],
                    callback_data=f"region_{index + 1}"
                )
            )

        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text="🏠 Bosh menyu",
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# 🏙 SHAHAR TUGMALARI
# =========================================================

def city_buttons(region):

    cities = CITIES.get(
        region,
        []
    )

    buttons = []

    for index in range(
        0,
        len(cities),
        2
    ):

        row = [
            InlineKeyboardButton(
                text=f"🏙 {cities[index]}",
                callback_data=f"city_{index}"
            )
        ]

        if index + 1 < len(cities):

            row.append(
                InlineKeyboardButton(
                    text=f"🏙 {cities[index + 1]}",
                    callback_data=f"city_{index + 1}"
                )
            )

        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text="🏠 Bosh menyu",
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# 📦 BUYURTMA BOSHLASH
# =========================================================

@router.callback_query(
    F.data == "create_order"
)
async def create_order_handler(
    callback: CallbackQuery,
    state: FSMContext
):

    user_id = callback.from_user.id

    cart = db.get_cart(
        user_id
    )

    if not cart:

        await callback.answer(
            "❌ Savatchangiz bo‘sh!",
            show_alert=True
        )

        return

    await state.set_state(
        OrderState.waiting_full_name
    )

    try:

        await callback.message.edit_text(
            "📦 <b>BUYURTMA BERISH</b>\n\n"
            "1️⃣ Ism va familiyangizni yozing:"
        )

    except TelegramBadRequest as error:

        if "message is not modified" not in str(error):
            raise

    await callback.answer()


# =========================================================
# 👤 ISM VA FAMILIYA
# =========================================================

@router.message(
    OrderState.waiting_full_name
)
async def order_full_name(
    message: Message,
    state: FSMContext
):

    full_name = (
        message.text or ""
    ).strip()

    if len(full_name) < 2:

        await message.answer(
            "❌ Ism va familiyani to‘g‘ri kiriting."
        )

        return

    await state.update_data(
        full_name=full_name
    )

    await state.set_state(
        OrderState.waiting_phone
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📞 Telefon raqamimni yuborish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "📞 <b>2️⃣ Telefon raqamingizni yuboring:</b>\n\n"
        "Pastdagi tugmani bosing 👇",
        reply_markup=keyboard
    )


# =========================================================
# 📞 TELEFON RAQAMINI QABUL QILISH
# =========================================================

@router.message(
    OrderState.waiting_phone,
    F.contact
)
async def order_phone(
    message: Message,
    state: FSMContext
):

    contact = message.contact

    if (
        contact.user_id
        and
        contact.user_id != message.from_user.id
    ):

        await message.answer(
            "❌ Iltimos, o‘zingizning telefon "
            "raqamingizni yuboring."
        )

        return

    phone = contact.phone_number

    await state.update_data(
        phone=phone
    )

    db.update_user_phone(
        message.from_user.id,
        phone
    )

    await message.answer(
        "✅ <b>Telefon raqamingiz qabul qilindi.</b>",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(
        OrderState.waiting_region
    )

    await message.answer(
        "📍 <b>3️⃣ Viloyatingizni tanlang:</b>",
        reply_markup=region_buttons()
    )


# =========================================================
# 📍 VILOYAT
# =========================================================

@router.callback_query(
    F.data.regexp(r"^region_\d+$")
)
async def order_region(
    callback: CallbackQuery,
    state: FSMContext
):

    try:

        index = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Viloyat noto‘g‘ri!",
            show_alert=True
        )

        return

    if index >= len(REGIONS):

        await callback.answer(
            "❌ Viloyat topilmadi!",
            show_alert=True
        )

        return

    region = REGIONS[index]

    await state.update_data(
        region=region
    )

    await state.set_state(
        OrderState.waiting_city
    )

    cities = CITIES.get(
        region,
        []
    )

    if not cities:

        await state.set_state(
            OrderState.waiting_address
        )

        await callback.message.edit_text(
            f"📍 Viloyat: <b>{region}</b>\n\n"
            "🏠 <b>4️⃣ To‘liq manzilingizni yozing:</b>"
        )

        await callback.answer()

        return

    await callback.message.edit_text(
        f"📍 Viloyat: <b>{region}</b>\n\n"
        "🏙 <b>4️⃣ Shaharingizni tanlang:</b>",
        reply_markup=city_buttons(region)
    )

    await callback.answer()


# =========================================================
# 🏙 SHAHAR
# =========================================================

@router.callback_query(
    F.data.regexp(r"^city_\d+$")
)
async def order_city(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    region = data.get(
        "region"
    )

    if not region:

        await callback.answer(
            "❌ Avval viloyatni tanlang!",
            show_alert=True
        )

        return

    try:

        index = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Shahar noto‘g‘ri!",
            show_alert=True
        )

        return

    cities = CITIES.get(
        region,
        []
    )

    if index >= len(cities):

        await callback.answer(
            "❌ Shahar topilmadi!",
            show_alert=True
        )

        return

    city = cities[index]

    await state.update_data(
        city=city
    )

    await state.set_state(
        OrderState.waiting_address
    )

    await callback.message.edit_text(
        f"📍 Viloyat: <b>{region}</b>\n"
        f"🏙 Shahar: <b>{city}</b>\n\n"
        "🏠 <b>5️⃣ To‘liq manzilingizni yozing:</b>\n\n"
        "Masalan:\n"
        "Chilonzor 5-mavze, 12-uy, 25-xonadon"
    )

    await callback.answer()


# =========================================================
# 🏠 MANZIL
# =========================================================

@router.message(
    OrderState.waiting_address
)
async def order_address(
    message: Message,
    state: FSMContext
):

    address = (
        message.text or ""
    ).strip()

    if len(address) < 3:

        await message.answer(
            "❌ To‘liq manzilni kiriting."
        )

        return

    await state.update_data(
        address=address
    )

    await state.set_state(
        OrderState.waiting_payment
    )

    await message.answer(
        "💳 <b>6️⃣ TO‘LOV USULINI TANLANG:</b>",
        reply_markup=payment_buttons()
    )


# =========================================================
# 💳 UZCARD
# =========================================================

@router.callback_query(
    F.data == "order_pay_uzcard"
)
async def order_pay_uzcard(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        selected_payment="Uzcard"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ To‘lov qildim",
                    callback_data="payment_confirm_uzcard"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ To‘lov turini o‘zgartirish",
                    callback_data="back_order_payment"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "💳 <b>UZCARD ORQALI TO‘LOV</b>\n\n"
        "💳 <b>Karta raqami:</b>\n"
        f"<code>{UZCARD_NUMBER}</code>\n\n"
        "👤 <b>Karta egasi:</b>\n"
        f"<b>{UZCARD_OWNER}</b>\n\n"
        "💡 To‘lovni amalga oshirgandan keyin "
        "«✅ To‘lov qildim» tugmasini bosing.",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================================================
# 💳 HUMO
# =========================================================

@router.callback_query(
    F.data == "order_pay_humo"
)
async def order_pay_humo(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        selected_payment="Humo"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ To‘lov qildim",
                    callback_data="payment_confirm_humo"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ To‘lov turini o‘zgartirish",
                    callback_data="back_order_payment"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "💳 <b>HUMO ORQALI TO‘LOV</b>\n\n"
        "💳 <b>Karta raqami:</b>\n"
        f"<code>{HUMO_NUMBER}</code>\n\n"
        "👤 <b>Karta egasi:</b>\n"
        f"<b>{HUMO_OWNER}</b>\n\n"
        "💡 To‘lovni amalga oshirgandan keyin "
        "«✅ To‘lov qildim» tugmasini bosing.",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================================================
# 💳 VISA
# =========================================================

@router.callback_query(
    F.data == "order_pay_visa"
)
async def order_pay_visa(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        selected_payment="Visa"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ To‘lov qildim",
                    callback_data="payment_confirm_visa"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ To‘lov turini o‘zgartirish",
                    callback_data="back_order_payment"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "💳 <b>VISA ORQALI TO‘LOV</b>\n\n"
        "💳 <b>Karta raqami:</b>\n"
        f"<code>{VISA_NUMBER}</code>\n\n"
        "👤 <b>Karta egasi:</b>\n"
        f"<b>{VISA_OWNER}</b>\n\n"
        "💡 To‘lovni amalga oshirgandan keyin "
        "«✅ To‘lov qildim» tugmasini bosing.",
        reply_markup=keyboard
    )

    await callback.answer()


# =========================================================
# ✅ UZCARD TO‘LOV QILINDI
# =========================================================

@router.callback_query(
    F.data == "payment_confirm_uzcard"
)
async def payment_confirm_uzcard(
    callback: CallbackQuery,
    state: FSMContext
):

    await finish_order(
        callback=callback,
        state=state,
        payment_method="Uzcard"
    )


# =========================================================
# ✅ HUMO TO‘LOV QILINDI
# =========================================================

@router.callback_query(
    F.data == "payment_confirm_humo"
)
async def payment_confirm_humo(
    callback: CallbackQuery,
    state: FSMContext
):

    await finish_order(
        callback=callback,
        state=state,
        payment_method="Humo"
    )


# =========================================================
# ✅ VISA TO‘LOV QILINDI
# =========================================================

@router.callback_query(
    F.data == "payment_confirm_visa"
)
async def payment_confirm_visa(
    callback: CallbackQuery,
    state: FSMContext
):

    await finish_order(
        callback=callback,
        state=state,
        payment_method="Visa"
    )


# =========================================================
# 💵 NAQD PUL
# =========================================================

@router.callback_query(
    F.data == "order_pay_cash"
)
async def order_pay_cash(
    callback: CallbackQuery,
    state: FSMContext
):

    await finish_order(
        callback=callback,
        state=state,
        payment_method="Naqd pul"
    )


# =========================================================
# ⬅️ TO‘LOV TURINI O‘ZGARTIRISH
# =========================================================

@router.callback_query(
    F.data == "back_order_payment"
)
async def back_order_payment(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        OrderState.waiting_payment
    )

    await callback.message.edit_text(
        "💳 <b>TO‘LOV USULINI TANLANG:</b>",
        reply_markup=payment_buttons()
    )

    await callback.answer()


# =========================================================
# 📦 BUYURTMANI YAKUNLASH
# =========================================================

async def finish_order(
    callback: CallbackQuery,
    state: FSMContext,
    payment_method: str
):

    user_id = callback.from_user.id

    # -----------------------------------------------------
    # STATE MA'LUMOTLARI
    # -----------------------------------------------------

    data = await state.get_data()

    full_name = data.get(
        "full_name",
        ""
    )

    phone = data.get(
        "phone",
        ""
    )

    region = data.get(
        "region",
        ""
    )

    city = data.get(
        "city",
        ""
    )

    address = data.get(
        "address",
        ""
    )

    # -----------------------------------------------------
    # 🚚 YETKAZIB BERISH
    # -----------------------------------------------------

    delivery_days = DELIVERY_DAYS.get(
        region,
        "3–5 kun"
    )

    # -----------------------------------------------------
    # 🛒 SAVATCHA
    # -----------------------------------------------------

    cart = db.get_cart(
        user_id
    )

    if not cart:

        await state.clear()

        await callback.answer(
            "❌ Savatchangiz bo‘sh!",
            show_alert=True
        )

        return

    # =====================================================
    # 🛍 MAHSULOTLARNI BITTA BUYURTMAGA YIG‘ISH
    # =====================================================

    products_text = ""

    total_price = 0

    for index, item in enumerate(
        cart,
        start=1
    ):

        product_name = item[1]
        price = item[2]

        products_text += (
            f"{index}. 📦 <b>{product_name}</b>\n"
            f"   💰 {price:,} so‘m\n"
        )

        total_price += price

    # =====================================================
    # 📦 BITTA ORDER YARATISH
    # =====================================================

    order_id = db.create_order(

        telegram_id=user_id,

        product_name=products_text,

        price=total_price,

        full_name=full_name,

        phone=phone,

        region=region,

        city=city,

        address=address,

        payment_method=payment_method,

        payment_status="Admin tasdig‘ini kutmoqda"
    )

    if not order_id:

        await callback.answer(
            "❌ Buyurtma yaratishda xatolik!",
            show_alert=True
        )

        return

    # =====================================================
    # 🗑 SAVATCHANI TOZALASH
    # =====================================================

    db.clear_cart(
        user_id
    )

    # =====================================================
    # 👨‍💼 ADMIN XABARI
    # =====================================================

    admin_text = (

        "📦 <b>YANGI BUYURTMA</b>\n\n"

        f"🆔 Buyurtma № <b>{order_id}</b>\n\n"

        "👤 <b>MIJOZ MA'LUMOTLARI</b>\n"

        f"👤 Ism: <b>{full_name}</b>\n"

        f"📞 Telefon: <b>{phone}</b>\n"

        f"📍 Viloyat: <b>{region}</b>\n"

        f"🏙 Shahar: <b>{city}</b>\n"

        f"🏠 Manzil: <b>{address}</b>\n\n"

        "🛍 <b>MAHSULOTLAR</b>\n"

        f"{products_text}\n"

        "━━━━━━━━━━━━━━━━━━\n"

        f"💰 <b>JAMI: {total_price:,} so‘m</b>\n"

        f"💳 To‘lov: <b>{payment_method}</b>\n"

        f"🚚 Yetkazib berish: <b>{delivery_days}</b>\n\n"

        "⏳ <b>Holat:</b> "
        "Admin tasdig‘ini kutmoqda"

    )

    # =====================================================
    # 🔘 ADMIN TUGMALARI
    # =====================================================

    admin_keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"admin_confirm_{order_id}"
                ),

                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"admin_reject_{order_id}"
                )

            ]

        ]

    )

    # =====================================================
    # 📤 ADMINGA YUBORISH
    # =====================================================

    try:

        await callback.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            reply_markup=admin_keyboard
        )

    except Exception as error:

        print(
            f"❌ ADMINGA XABAR YUBORISH XATOSI: {error}"
        )

    # =====================================================
    # 👤 USERGA XABAR
    # =====================================================

    user_text = (

        "✅ <b>BUYURTMANGIZ QABUL QILINDI!</b>\n\n"

        f"🆔 Buyurtma № <b>{order_id}</b>\n\n"

        "🛍 <b>MAHSULOTLAR</b>\n"

        f"{products_text}\n"

        "━━━━━━━━━━━━━━━━━━\n"

        f"💰 <b>JAMI: {total_price:,} so‘m</b>\n"

        f"💳 To‘lov: <b>{payment_method}</b>\n"

        f"🚚 Yetkazib berish: <b>{delivery_days}</b>\n\n"

        "⏳ Buyurtmangiz admin tomonidan "
        "tasdiqlanishini kutmoqda."

    )

    try:

        await callback.message.edit_text(
            user_text
        )

    except TelegramBadRequest as error:

        if "message is not modified" not in str(error):

            await callback.message.answer(
                user_text
            )

    except Exception:

        await callback.message.answer(
            user_text
        )

    await state.clear()

    await callback.answer(
        "✅ Buyurtma qabul qilindi!"
    )


# =========================================================
# 📦 MENING BUYURTMALARIM
# =========================================================

@router.callback_query(
    F.data == "orders"
)
async def my_orders(
    callback: CallbackQuery
):

    user_id = callback.from_user.id

    orders = db.get_orders(
        user_id
    )

    # -----------------------------------------------------
    # BUYURTMALAR YO‘Q
    # -----------------------------------------------------

    if not orders:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[

                [

                    InlineKeyboardButton(
                        text="🏠 Bosh menyu",
                        callback_data="back_main"
                    )

                ]

            ]
        )

        try:

            await callback.message.edit_text(

                "📦 <b>BUYURTMALARIM</b>\n\n"

                "Sizda hali buyurtmalar mavjud emas.",

                reply_markup=keyboard

            )

        except TelegramBadRequest as error:

            if "message is not modified" in str(error):

                await callback.answer(
                    "📦 Buyurtmalar oynasi ochilgan."
                )

                return

        await callback.answer()

        return

    # -----------------------------------------------------
    # BUYURTMALAR RO‘YXATI
    # -----------------------------------------------------

    text = (
        "📦 <b>BUYURTMALARIM</b>\n\n"
    )

    buttons = []

    for order in orders:

        order_id = order[0]
        price = order[2]
        status = order[3]
        payment_status = order[4]
        created_at = order[5]

        text += (

            f"🆔 <b>Buyurtma №{order_id}</b>\n"

            f"💰 {price:,} so‘m\n"

            f"📌 Holat: <b>{status}</b>\n"

            f"💳 To‘lov: <b>{payment_status}</b>\n"

        )

        if created_at:

            text += (
                f"🕒 {created_at}\n"
            )

        text += (
            "━━━━━━━━━━━━━━\n"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"📦 Buyurtma №{order_id}",
                    callback_data=f"user_order_{order_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Bosh menyu",
                callback_data="back_main"
            )
        ]
    )

    try:

        await callback.message.edit_text(

            text,

            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=buttons
            )

        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "📦 Buyurtmalar oynasi allaqachon ochilgan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 📦 BITTA BUYURTMA
# =========================================================

@router.callback_query(
    F.data.regexp(r"^user_order_\d+$")
)
async def user_order_detail(
    callback: CallbackQuery
):

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
        db_order_id,
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

    if telegram_id != callback.from_user.id:

        await callback.answer(
            "❌ Bu buyurtma sizniki emas!",
            show_alert=True
        )

        return

    delivery_days = DELIVERY_DAYS.get(
        region,
        "3–5 kun"
    )

    text = (

        f"📦 <b>BUYURTMA №{db_order_id}</b>\n\n"

        "👤 <b>MIJOZ</b>\n"

        f"👤 Ism: <b>{full_name}</b>\n"

        f"📞 Telefon: <b>{phone}</b>\n"

        f"📍 Viloyat: <b>{region}</b>\n"

        f"🏙 Shahar: <b>{city}</b>\n"

        f"🏠 Manzil: <b>{address}</b>\n\n"

        "🛍 <b>MAHSULOTLAR</b>\n"

        f"{product_name}\n"

        "━━━━━━━━━━━━━━━━━━\n"

        f"💰 <b>JAMI: {price:,} so‘m</b>\n"

        f"💳 To‘lov: <b>{payment}</b>\n"

        f"🚚 Yetkazib berish: <b>{delivery_days}</b>\n"

        f"📌 Holat: <b>{status}</b>\n"

        f"💳 To‘lov holati: <b>{payment_status}</b>\n"

    )

    if created_at:

        text += (
            f"\n🕒 <b>Yaratilgan:</b> {created_at}"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📦 Buyurtmalarim",
                    callback_data="orders"
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

    try:

        await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "📦 Bu buyurtma allaqachon ochilgan."
            )

            return

        raise

    await callback.answer()


# =========================================================
# 🏠 BOSH MENYU
# =========================================================

@router.callback_query(
    F.data == "back_main"
)
async def order_back_main(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    try:

        await callback.message.edit_text(

            "📱 <b>SMART PHONE SHOP</b>\n\n"

            f"Assalomu alaykum, "
            f"<b>{callback.from_user.first_name}</b> 👋\n\n"

            "Kerakli bo‘limni tanlang:",

            reply_markup=main_menu(
                callback.from_user.id
            )

        )

    except TelegramBadRequest as error:

        if "message is not modified" in str(error):

            await callback.answer(
                "🏠 Siz bosh menyudasiz."
            )

            return

        raise

    await callback.answer()