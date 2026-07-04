#EXCEPTIONS
from mysql.connector import IntegrityError
from exceptions.user import UsernameExists, EmailExists
#MODELS
from domains.subscription import Subscription
from domains.user import User
from domains.invoice import Invoice


"""USER REPOSITORY FLOW"""
def save_user(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users(username, pwd, email) 
        VALUES (%s, %s, %s)""", (user.username, user.pwd, user.email))

        user.user_id=cursor.lastrowid

    except IntegrityError as e:
        msg = str(e)

        if "users.email" in msg:
            raise EmailExists()

        if "users.username" in msg:
            raise UsernameExists()
        raise

def get_user_by_username(conn, username):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT user_id, username, pwd, email
    FROM users WHERE username = %s""", (username,))

    row =  cursor.fetchone()
    return User(**row) if row else None

def get_user_by_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT user_id, username, pwd, email
    FROM users WHERE user_id = %s""", (user_id,))

    row = cursor.fetchone()
    return User(**row) if row else None

"""SUBSCRIPTION REPO FLOW"""
def save_subscription(conn, subscription):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO subscriptions(user_id, plan, started_at, expires_at, canceled_at) 
    VALUES (%s, %s, %s, %s, %s)""",
        (subscription.user_id,
         subscription.plan,
         subscription.started_at,
         subscription.expires_at,
         subscription.canceled_at
         )
                   )
    subscription.sub_id = cursor.lastrowid

def get_subs_list_by_user_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT sub_id, user_id,  plan, started_at, expires_at, canceled_at
    FROM subscriptions
    WHERE user_id = %s""",
                        (user_id,)
        )
    rows = cursor.fetchall()
    return [Subscription(**row) for row in rows]

def expire_subscription(conn, subscription):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    UPDATE subscriptions
    SET canceled_at = %s
    WHERE sub_id = %s""",

        (
            subscription.canceled_at,
            subscription.sub_id
         )
    )


"""INVOICE REPO FLOW"""
def expire_invoice(conn, invoice):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    UPDATE invoice
    SET status = %s
    WHERE sub_id = %s""",
        (invoice.status, invoice.sub_id)
    )

def get_invoices_list_by_user_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT i.*
    FROM invoice i
    JOIN subscriptions s
    ON i.sub_id = s.sub_id
    WHERE s.user_id = %s """, (user_id,)
                    )
    rows = cursor.fetchall()
    return [Invoice(**row) for row in rows] if rows else []

def get_invoice_by_sub_id(conn, sub_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT invoice_id, sub_id, status, amount, period_start, period_end
    FROM invoice 
    WHERE sub_id = %s """, (sub_id,)
                    )
    row = cursor.fetchone()
    return Invoice(**row) if row else None

def update_invoice_status(conn, invoice):
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE invoice
    SET status = %s 
    WHERE invoice_id = %s""", (invoice.status, invoice.invoice_id))


def save_invoice(conn, invoice):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO invoice(sub_id, status,
        amount, period_start, period_end)
        VALUES (%s, %s, %s, %s, %s)""",
                    (
                    invoice.sub_id,
                    invoice.status,
                    invoice.amount,
                    invoice.period_start,
                    invoice.period_end,
                    )
    )
    invoice.invoice_id=cursor.lastrowid


