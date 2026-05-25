#EXCEPTIONS
from mysql.connector import IntegrityError
from exceptions.user import UsernameExists, EmailExists
#MODELS
from models.subscription import Subscription
from models.user import User
from models.invoice import Invoice

class Repository:
    def __init__(self, conn):
        self.conn = conn

#USER REPOSITORY FLOW
    def save_user(self, user):
        try: # conn
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT INTO users(username, pwd, email) 
            VALUES (%s, %s, %s)""", (user.username, user.pwd, user.email))

        except IntegrityError as e:
            msg = str(e)

            if "users.email" in msg:
                raise EmailExists()

            if "users.username" in msg:
                raise UsernameExists()

    def get_user_by_username(self, username):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT user_id, username, pwd, email
        FROM users WHERE username = %s""", (username,))

        row =  cursor.fetchone()
        return User(**row) if row else None

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT user_id, username, pwd, email
        FROM users WHERE user_id = %s""", (user_id,))

        row = cursor.fetchone()
        return User(**row) if row else None

#SUBSCRIPTION REPO FLOW
    def save_subscription(self, sub):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO subscriptions(user_id, status, plan, started_at, expires_at) 
        VALUES (%s, %s, %s, %s, %s)""",
            (sub.user_id, sub.status, sub.plan, sub.started_at, sub.expires_at))
        sub.sub_id = cursor.lastrowid

    def get_subs_by_user_id(self, user_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT sub_id, status, plan, started_at, expires_at, user_id
        FROM subscriptions
        WHERE user_id = %s""",
                        (user_id,)
        )
        rows = cursor.fetchall()
        return [Subscription(**row) for row in rows]

    def expire_subscription(self, sub):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        UPDATE subscriptions
        SET status = %s, canceled_at = %s
        WHERE sub_id = %s""",
            (sub.status, sub.canceled_at, sub.sub_id)
        )

    def update_subscription(self, sub):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        UPDATE subscriptions
        SET plan = %s, expires_at = %s
            WHERE sub_id = %s """, (sub.plan, sub.expires_at, sub.sub_id)
        )

#INVOICE REPO FLOW
    def expire_invoice(self, invoice):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        UPDATE invoice
        SET status = %s, canceled_at = %s
        WHERE sub_id = %s""",
            (invoice.status, invoice.canceled_at, invoice.invoice_id)
        )

    def get_invoices_by_user_id(self, user_id):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        SELECT user_id, sub_id, status, sub_plan, issued_at, amount, currency, expires_at, canceled_at, invoice_id
        FROM invoice 
        WHERE user_id = %s """, (user_id,)
                       )
        rows = cursor.fetchall()
        return [Invoice(**row) for row in rows]

    def update_invoice(self, invoice):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
        UPDATE invoice
        SET sub_plan = %s
            WHERE invoice_id = %s """,
                       (invoice.sub_plan, invoice.invoice_id)
        )

    def save_invoice(self, invoice):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO invoice(user_id, sub_id, status, sub_plan,
            issued_at, amount, currency, expires_at, canceled_at)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (
                        invoice.user_id,
                        invoice.sub_id,
                        invoice.status,
                        invoice.sub_plan,
                        invoice.issued_at,
                        invoice.amount,
                        invoice.currency,
                        invoice.expires_at,
                        invoice.canceled_at
                       )
        )


