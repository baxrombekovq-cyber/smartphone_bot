from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# =========================
# 📱 TELEFON RAQAM
# =========================

def phone_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Telefon raqamni yuborish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# =========================
# 🇺🇿 VILOYATLAR
# =========================

def regions_button():

    regions = [
        ("🏙 Toshkent shahri", "Toshkent_shahri"),
        ("📍 Toshkent viloyati", "Toshkent_viloyati"),
        ("📍 Andijon viloyati", "Andijon"),
        ("📍 Buxoro viloyati", "Buxoro"),
        ("📍 Farg‘ona viloyati", "Fargona"),
        ("📍 Jizzax viloyati", "Jizzax"),
        ("📍 Namangan viloyati", "Namangan"),
        ("📍 Navoiy viloyati", "Navoiy"),
        ("📍 Qashqadaryo viloyati", "Qashqadaryo"),
        ("📍 Samarqand viloyati", "Samarqand"),
        ("📍 Sirdaryo viloyati", "Sirdaryo"),
        ("📍 Surxondaryo viloyati", "Surxondaryo"),
        ("📍 Xorazm viloyati", "Xorazm"),
        ("📍 Qoraqalpog‘iston", "Qoraqalpogiston"),
    ]

    keyboard = []

    for name, code in regions:
        keyboard.append([
            InlineKeyboardButton(
                text=name,
                callback_data=f"region_{code}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


# =========================
# 🏙 SHAHAR / TUMAN
# =========================

def cities_button(region):

    cities = {

        "Toshkent_shahri": [
            "Chilonzor",
            "Yunusobod",
            "Mirzo Ulug‘bek",
            "Sergeli",
            "Yakkasaroy",
            "Shayxontohur",
            "Olmazor",
            "Uchtepa",
            "Mirobod",
            "Bektemir",
            "Yashnobod",
            "Yangihayot"
        ],

        "Toshkent_viloyati": [
            "Chirchiq",
            "Olmaliq",
            "Angren",
            "Bekobod",
            "Ohangaron",
            "Yangiyo‘l",
            "Nurafshon",
            "Zangiota",
            "Qibray"
        ],

        "Andijon": [
            "Andijon shahri",
            "Asaka",
            "Xonobod",
            "Shahrixon",
            "Qo‘rg‘ontepa",
            "Marhamat"
        ],

        "Buxoro": [
            "Buxoro shahri",
            "Kogon",
            "G‘ijduvon",
            "Vobkent",
            "Romitan"
        ],

        "Fargona": [
            "Farg‘ona shahri",
            "Qo‘qon",
            "Marg‘ilon",
            "Quva",
            "Rishton",
            "Oltiariq"
        ],

        "Jizzax": [
            "Jizzax shahri",
            "G‘allaorol",
            "Zomin",
            "Paxtakor"
        ],

        "Namangan": [
            "Namangan shahri",
            "Chust",
            "Kosonsoy",
            "Pop",
            "Chortoq",
            "Uchqo‘rg‘on"
        ],

        "Navoiy": [
            "Navoiy shahri",
            "Zarafshon",
            "Karmana",
            "Konimex"
        ],

        "Qashqadaryo": [
            "Qarshi",
            "Shahrisabz",
            "Koson",
            "Kitob",
            "Chiroqchi"
        ],

        "Samarqand": [
            "Samarqand shahri",
            "Kattaqo‘rg‘on",
            "Urgut",
            "Jomboy",
            "Pastdarg‘om"
        ],

        "Sirdaryo": [
            "Guliston",
            "Shirin",
            "Yangiyer",
            "Boyovut"
        ],

        "Surxondaryo": [
            "Termiz",
            "Denov",
            "Sherobod",
            "Boysun",
            "Sho‘rchi"
        ],

        "Xorazm": [
            "Urganch",
            "Xiva",
            "Hazorasp",
            "Shovot",
            "Gurlan"
        ],

        "Qoraqalpogiston": [
            "Nukus",
            "Xo‘jayli",
            "Beruniy",
            "To‘rtko‘l",
            "Qo‘ng‘irot"
        ]
    }

    keyboard = []

    for city in cities.get(region, []):
        keyboard.append([
            InlineKeyboardButton(
                text=f"🏙 {city}",
                callback_data=f"city_{city}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


# =========================
# 💳 TO‘LOV USULLARI
# =========================

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
                    text="💵 Naqd pul",
                    callback_data="order_pay_cash"
                )
            ]
        ]
    )


# =========================
# ✅ TASDIQLASH
# =========================

def confirm_payment_button():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ To‘lovni tasdiqlash",
                    callback_data="confirm_order_payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Buyurtmani bekor qilish",
                    callback_data="cancel_order"
                )
            ]
        ]
    )