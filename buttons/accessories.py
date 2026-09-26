from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =====================================================
# 🎧 AKSESSUARLAR MENYUSI
# =====================================================

def accessories_buttons():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            # 🔌 Zaryadlovchi
            [
                InlineKeyboardButton(
                    text="🔌 Zaryadlovchi",
                    callback_data="acc_Zaryadlovchi"
                )
            ],

            # 🔋 Powerbank
            [
                InlineKeyboardButton(
                    text="🔋 Powerbank",
                    callback_data="acc_Powerbank"
                )
            ],

            # 🎧 Quloqchin
            [
                InlineKeyboardButton(
                    text="🎧 Quloqchin",
                    callback_data="acc_Quloqchin"
                )
            ],

            # 🔌 USB kabel
            [
                InlineKeyboardButton(
                    text="🔌 USB kabel",
                    callback_data="acc_USB kabel"
                )
            ],

            # 📱 Chexol
            [
                InlineKeyboardButton(
                    text="📱 Chexol",
                    callback_data="acc_Chexol"
                )
            ],

            # 🛡 Himoya oynasi
            [
                InlineKeyboardButton(
                    text="🛡 Himoya oynasi",
                    callback_data="acc_Himoya oynasi"
                )
            ],

            # 📡 Simsiz zaryadlovchi
            [
                InlineKeyboardButton(
                    text="📡 Simsiz zaryadlovchi",
                    callback_data="acc_Simsiz zaryadlovchi"
                )
            ],

            # 🚗 Avto aksessuar
            [
                InlineKeyboardButton(
                    text="🚗 Avto aksessuar",
                    callback_data="acc_Avto aksessuar"
                )
            ],

            # 📱 Telefon stendi
            [
                InlineKeyboardButton(
                    text="📱 Telefon stendi",
                    callback_data="acc_Telefon stendi"
                )
            ],

            # 🔄 OTG adapter
            [
                InlineKeyboardButton(
                    text="🔄 OTG adapter",
                    callback_data="acc_OTG adapter"
                )
            ],

            # 🔊 Kolonka
            [
                InlineKeyboardButton(
                    text="🔊 Kolonka",
                    callback_data="acc_Kolonka"
                )
            ],

            # ⬅️ Orqaga
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="back_main"
                )
            ]
        ]
    )