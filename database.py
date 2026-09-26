
import psycopg2

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


# =========================================================
# 🗄 DATABASE
# =========================================================

class Database:

    def __init__(self):

        try:

            self.connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

            self.cursor = self.connection.cursor()

            print("✅ DATABASE ULANDI")

            self.create_tables()

        except Exception as error:

            print(
                f"❌ DATABASE ULANISHDA XATO: {error}"
            )

            raise


    # =====================================================
    # 🏗 TABLELARNI YARATISH
    # =====================================================

    def create_tables(self):

        try:

            # =================================================
            # 👤 USERS
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    full_name TEXT,
                    username TEXT,
                    phone TEXT
                )
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS phone TEXT
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE users
                DROP COLUMN IF EXISTS language
                """
            )

            # =================================================
            # 📱 PHONES
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price BIGINT NOT NULL,
                    brand TEXT NOT NULL,
                    description TEXT,
                    image TEXT
                )
                """
            )

            # =================================================
            # 🎧 ACCESSORIES
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS accessories (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price BIGINT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    image TEXT
                )
                """
            )

            # =================================================
            # 🛒 CART
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cart (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL,
                    product_name TEXT NOT NULL,
                    price BIGINT NOT NULL
                )
                """
            )

            # =================================================
            # ❤️ FAVORITES
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS favorites (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL,
                    item_type TEXT NOT NULL,
                    item_id INTEGER NOT NULL
                )
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE favorites
                ADD COLUMN IF NOT EXISTS telegram_id BIGINT
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE favorites
                ADD COLUMN IF NOT EXISTS item_type TEXT
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE favorites
                ADD COLUMN IF NOT EXISTS item_id INTEGER
                """
            )

            # =================================================
            # 📦 ORDERS
            # =================================================

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT NOT NULL,
                    product_name TEXT NOT NULL,
                    price BIGINT NOT NULL,
                    full_name TEXT,
                    phone TEXT,
                    region TEXT,
                    city TEXT,
                    address TEXT,
                    payment TEXT,
                    status TEXT DEFAULT 'pending',
                    payment_status TEXT DEFAULT 'waiting',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            self.cursor.execute(
                """
                ALTER TABLE orders
                ADD COLUMN IF NOT EXISTS payment_status TEXT
                DEFAULT 'waiting'
                """

            )

            self.connection.commit()

            print("✅ TABLELAR TAYYOR")

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TABLE YARATISHDA XATO: {error}"
            )

            raise


    # =====================================================
    # 👤 USER QO‘SHISH
    # =====================================================

    def add_user(
        self,
        telegram_id,
        full_name,
        username=""
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO users (
                    telegram_id,
                    full_name,
                    username
                )
                VALUES (%s, %s, %s)

                ON CONFLICT (telegram_id)
                DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    username = EXCLUDED.username
                """,
                (
                    telegram_id,
                    full_name,
                    username
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ USER SAQLASHDA XATO: {error}"
            )


    # =====================================================
    # 👤 USERNI YANGILASH
    # =====================================================

    def update_user(
        self,
        telegram_id,
        full_name=None,
        username=None,
        phone=None
    ):

        try:

            self.cursor.execute(
                """
                UPDATE users
                SET
                    full_name = COALESCE(%s, full_name),
                    username = COALESCE(%s, username),
                    phone = COALESCE(%s, phone)
                WHERE telegram_id = %s
                """,
                (
                    full_name,
                    username,
                    phone,
                    telegram_id
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ USER YANGILASHDA XATO: {error}"
            )


    # =====================================================
    # 📞 TELEFON SAQLASH
    # =====================================================

    def update_user_phone(
        self,
        telegram_id,
        phone
    ):

        try:

            self.cursor.execute(
                """
                UPDATE users
                SET phone = %s
                WHERE telegram_id = %s
                """,
                (
                    phone,
                    telegram_id
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TELEFON SAQLASHDA XATO: {error}"
            )


    # =====================================================
    # 👤 BITTA USER
    # =====================================================

    def get_user(
        self,
        telegram_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    telegram_id,
                    full_name,
                    username,
                    phone
                FROM users
                WHERE telegram_id = %s
                """,
                (
                    telegram_id,
                )
            )

            return self.cursor.fetchone()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ USER OLISHDA XATO: {error}"
            )

            return None


    # =====================================================
    # 👥 BARCHA USERLAR
    # =====================================================

    def get_all_users(self):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    telegram_id,
                    full_name,
                    username,
                    phone
                FROM users
                ORDER BY id DESC
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ USERLARNI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 📱 TELEFON QO‘SHISH
    # =====================================================

    def add_phone(
        self,
        name,
        price,
        brand,
        description="",
        image=""
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO phones (
                    name,
                    price,
                    brand,
                    description,
                    image
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    name,
                    price,
                    brand,
                    description,
                    image
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TELEFON QO‘SHISHDA XATO: {error}"
            )


    # =====================================================
    # 📱 BARCHA TELEFONLAR
    # =====================================================

    def get_phones(self):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    name,
                    price,
                    brand,
                    description,
                    image
                FROM phones
                ORDER BY id DESC
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TELEFONLARNI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 📱 BITTA TELEFON
    # =====================================================

    def get_phone(
        self,
        phone_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    name,
                    price,
                    brand,
                    description,
                    image
                FROM phones
                WHERE id = %s
                """,
                (
                    phone_id,
                )
            )

            return self.cursor.fetchone()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TELEFON OLISHDA XATO: {error}"
            )

            return None


    # =====================================================
    # 🎧 AKSESSUAR QO‘SHISH
    # =====================================================

    def add_accessory(
        self,
        name,
        price,
        category,
        description="",
        image=""
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO accessories (
                    name,
                    price,
                    category,
                    description,
                    image
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    name,
                    price,
                    category,
                    description,
                    image
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ AKSESSUAR QO‘SHISHDA XATO: {error}"
            )


    # =====================================================
    # 🎧 BARCHA AKSESSUARLAR
    # =====================================================

    def get_accessories(self):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    name,
                    price,
                    category,
                    description,
                    image
                FROM accessories
                ORDER BY id DESC
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ AKSESSUARLARNI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 🎧 BITTA AKSESSUAR
    # =====================================================

    def get_accessory(
        self,
        accessory_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    name,
                    price,
                    category,
                    description,
                    image
                FROM accessories
                WHERE id = %s
                """,
                (
                    accessory_id,
                )
            )

            return self.cursor.fetchone()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ AKSESSUAR OLISHDA XATO: {error}"
            )

            return None


    # =====================================================
    # 🛒 SAVATCHAGA QO‘SHISH
    # =====================================================

    def add_to_cart(
        self,
        telegram_id,
        product_name,
        price
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO cart (
                    telegram_id,
                    product_name,
                    price
                )
                VALUES (%s, %s, %s)
                """,
                (
                    telegram_id,
                    product_name,
                    price
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SAVATCHAGA QO‘SHISHDA XATO: {error}"
            )


    # =====================================================
    # 🛒 SAVATCHANI OLISH
    # =====================================================

    def get_cart(
        self,
        telegram_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    product_name,
                    price
                FROM cart
                WHERE telegram_id = %s
                ORDER BY id
                """,
                (
                    telegram_id,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SAVATCHANI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 🗑 SAVATCHANI TOZALASH
    # =====================================================

    def clear_cart(
        self,
        telegram_id
    ):

        try:

            self.cursor.execute(
                """
                DELETE FROM cart
                WHERE telegram_id = %s
                """,
                (
                    telegram_id,
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SAVATCHANI TOZALASHDA XATO: {error}"
            )


    # =====================================================
    # ❤️ SEVIMLIGA QO‘SHISH
    # =====================================================

    def add_favorite(
        self,
        telegram_id,
        item_type,
        item_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM favorites
                WHERE telegram_id = %s
                AND item_type = %s
                AND item_id = %s
                """,
                (
                    telegram_id,
                    item_type,
                    item_id
                )
            )

            exists = self.cursor.fetchone()

            if not exists:

                self.cursor.execute(
                    """
                    INSERT INTO favorites (
                        telegram_id,
                        item_type,
                        item_id
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        telegram_id,
                        item_type,
                        item_id
                    )
                )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SEVIMLIGA QO‘SHISHDA XATO: {error}"
            )


    # =====================================================
    # 💔 SEVIMLIDAN O‘CHIRISH
    # =====================================================

    def remove_favorite(
        self,
        telegram_id,
        item_type,
        item_id
    ):

        try:

            self.cursor.execute(
                """
                DELETE FROM favorites
                WHERE telegram_id = %s
                AND item_type = %s
                AND item_id = %s
                """,
                (
                    telegram_id,
                    item_type,
                    item_id
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SEVIMLIDAN O‘CHIRISHDA XATO: {error}"
            )


    # =====================================================
    # ❤️ SEVIMLIDA BORMI?
    # =====================================================

    def is_favorite(
        self,
        telegram_id,
        item_type,
        item_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM favorites
                WHERE telegram_id = %s
                AND item_type = %s
                AND item_id = %s
                """,
                (
                    telegram_id,
                    item_type,
                    item_id
                )
            )

            return self.cursor.fetchone() is not None

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SEVIMLINI TEKSHIRISHDA XATO: {error}"
            )

            return False


    # =====================================================
    # ❤️ SEVIMLILAR
    # =====================================================

    def get_favorites(
        self,
        telegram_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    item_type,
                    item_id
                FROM favorites
                WHERE telegram_id = %s
                ORDER BY id DESC
                """,
                (
                    telegram_id,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ SEVIMLILARNI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 📦 BUYURTMA YARATISH
    # =====================================================

    def create_order(
        self,
        telegram_id,
        product_name,
        price,
        full_name,
        phone,
        region,
        city,
        address,
        payment=None,
        payment_method=None,
        payment_status="waiting"
    ):

        try:

            # payment_method kelsa shuni ishlatamiz
            selected_payment = (
                payment_method
                if payment_method is not None
                else payment
            )

            self.cursor.execute(
                """
                INSERT INTO orders (
                    telegram_id,
                    product_name,
                    price,
                    full_name,
                    phone,
                    region,
                    city,
                    address,
                    payment,
                    payment_status
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                RETURNING id
                """,
                (
                    telegram_id,
                    product_name,
                    price,
                    full_name,
                    phone,
                    region,
                    city,
                    address,
                    selected_payment,
                    payment_status
                )
            )

            order_id = self.cursor.fetchone()[0]

            self.connection.commit()

            print(
                f"✅ BUYURTMA YARATILDI: {order_id}"
            )

            return order_id

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ BUYURTMA YARATISHDA XATO: {error}"
            )

            return None


    # =====================================================
    # 📦 BITTA BUYURTMA
    # =====================================================

    def get_order(
        self,
        order_id
    ):

        try:

            self.cursor.execute(
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
                WHERE id = %s
                """,
                (
                    order_id,
                )
            )

            return self.cursor.fetchone()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ BUYURTMANI OLISHDA XATO: {error}"
            )

            return None


    # =====================================================
    # 📦 USER BUYURTMALARI
    # =====================================================

    def get_orders(
        self,
        telegram_id
    ):

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    product_name,
                    price,
                    status,
                    payment_status,
                    created_at
                FROM orders
                WHERE telegram_id = %s
                ORDER BY id DESC
                """,
                (
                    telegram_id,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ BUYURTMALARNI OLISHDA XATO: {error}"
            )

            return []


    # =====================================================
    # 🔄 BUYURTMA STATUSI
    # =====================================================

    def update_order_status(
        self,
        order_id,
        status
    ):

        try:

            self.cursor.execute(
                """
                UPDATE orders
                SET status = %s
                WHERE id = %s
                """,
                (
                    status,
                    order_id
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ BUYURTMA STATUSINI YANGILASHDA XATO: {error}"
            )


    # =====================================================
    # 💳 TO‘LOV STATUSI
    # =====================================================

    def update_payment_status(
        self,
        order_id,
        payment_status
    ):

        try:

            self.cursor.execute(
                """
                UPDATE orders
                SET payment_status = %s
                WHERE id = %s
                """,
                (
                    payment_status,
                    order_id
                )
            )

            self.connection.commit()

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TO‘LOV STATUSINI YANGILASHDA XATO: {error}"
            )


    # =====================================================
    # 👥 USERLAR SONI
    # =====================================================

    def get_users_count(self):

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM users
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ USERLAR SONINI OLISHDA XATO: {error}"
            )

            return 0


    # =====================================================
    # 📱 TELEFONLAR SONI
    # =====================================================

    def get_phones_count(self):

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM phones
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ TELEFONLAR SONINI OLISHDA XATO: {error}"
            )

            return 0


    # =====================================================
    # 🎧 AKSESSUARLAR SONI
    # =====================================================

    def get_accessories_count(self):

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM accessories
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ AKSESSUARLAR SONINI OLISHDA XATO: {error}"
            )

            return 0


    # =====================================================
    # 📦 BUYURTMALAR SONI
    # =====================================================

    def get_orders_count(self):

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM orders
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            self.connection.rollback()

            print(
                f"❌ BUYURTMALAR SONINI OLISHDA XATO: {error}"
            )

            return 0


    # =====================================================
    # 📱 DEFAULT TELEFONLAR
    # =====================================================

    def add_default_phones(self):

        phones = [

            (
                "iPhone 15",
                12000000,
                "iPhone",
                "Apple iPhone 15",
                ""
            ),

            (
                "iPhone 15 Pro",
                15000000,
                "iPhone",
                "Apple iPhone 15 Pro",
                ""
            ),

            (
                "Samsung Galaxy S24",
                11000000,
                "Samsung",
                "Samsung Galaxy S24",
                ""
            ),

            (
                "Samsung Galaxy A55",
                6000000,
                "Samsung",
                "Samsung Galaxy A55",
                ""
            ),

            (
                "Xiaomi 14",
                8500000,
                "Xiaomi",
                "Xiaomi 14",
                ""
            ),

            (
                "Redmi Note 13",
                3500000,
                "Redmi",
                "Redmi Note 13",
                ""
            )

        ]

        for phone in phones:

            self.add_phone(
                phone[0],
                phone[1],
                phone[2],
                phone[3],
                phone[4]
            )


    # =====================================================
    # 🎧 DEFAULT AKSESSUARLAR
    # =====================================================

    def add_default_accessories(self):

        accessories = [

            (
                "Zaryadlovchi",
                150000,
                "Zaryadlovchi",
                "Tez zaryadlovchi",
                ""
            ),

            (
                "Powerbank",
                250000,
                "Powerbank",
                "Kuchli powerbank",
                ""
            ),

            (
                "Quloqchin",
                180000,
                "Quloqchin",
                "Simsiz quloqchin",
                ""
            ),

            (
                "USB kabel",
                70000,
                "USB kabel",
                "Sifatli USB kabel",
                ""
            ),

            (
                "Chexol",
                100000,
                "Chexol",
                "Telefon uchun himoya chexol",
                ""
            ),

            (
                "Himoya oynasi",
                50000,
                "Himoya oynasi",
                "Mustahkam himoya oynasi",
                ""
            ),

            (
                "Simsiz zaryadlovchi",
                220000,
                "Simsiz zaryadlovchi",
                "Wireless charger",
                ""
            ),

            (
                "Avto aksessuar",
                180000,
                "Avto aksessuar",
                "Avtomobil uchun telefon aksessuari",
                ""
            ),

            (
                "Telefon stendi",
                120000,
                "Telefon stendi",
                "Telefon uchun stend",
                ""
            ),

            (
                "OTG adapter",
                80000,
                "OTG adapter",
                "USB OTG adapter",
                ""
            ),

            (
                "Kolonka",
                300000,
                "Kolonka",
                "Bluetooth kolonka",
                ""
            )

        ]

        for accessory in accessories:

            self.add_accessory(
                accessory[0],
                accessory[1],
                accessory[2],
                accessory[3],
                accessory[4]
            )


    # =====================================================
    # 🔴 DATABASE YOPISH
    # =====================================================

    def close(self):

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

            print("✅ DATABASE YOPILDI")

        except Exception as error:

            print(
                f"❌ DATABASE YOPISHDA XATO: {error}"
            )

