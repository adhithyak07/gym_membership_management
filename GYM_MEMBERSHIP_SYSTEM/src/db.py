import os
import logging
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, date

# -------------------- Setup --------------------
logging.basicConfig(level=logging.INFO)
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# -------------------- Utility --------------------
def to_iso(value):
    """Convert date/datetime to ISO string."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value

# -------------------- Gymrats Table --------------------
def add_member(name, phone, plan, start_date=None, end_date=None):
    if start_date is None:
        start_date = date.today()
    payload = {
        "name": name,
        "phone": phone,
        "plan": plan,
        "start_date": to_iso(start_date),
        "end_date": to_iso(end_date) if end_date else None
    }
    try:
        resp = supabase.table("gymrats").insert(payload).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_members(order_by="start_date"):
    try:
        resp = supabase.table("gymrats").select("*").order(order_by, desc=True).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_member(member_id, new_plan, new_end_date=None):
    payload = {
        "plan": new_plan,
        "end_date": to_iso(new_end_date) if new_end_date else None
    }
    try:
        resp = supabase.table("gymrats").update(payload).eq("id", str(member_id)).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_member(member_id):
    try:
        resp = supabase.table("gymrats").delete().eq("id", str(member_id)).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

# -------------------- Payments Table --------------------
def add_payment(member_id, amount, payment_date=None, method=None):
    if payment_date is None:
        payment_date = datetime.now()
    payload = {
        "gymrat_id": str(member_id),
        "amount": amount,
        "payment_date": to_iso(payment_date),
    }
    if method:
        payload["method"] = method
    try:
        resp = supabase.table("payments").insert(payload).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_payments(order_by="payment_date"):
    try:
        resp = supabase.table("payments").select("*").order(order_by, desc=True).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_payments_by_member(member_id):
    try:
        resp = supabase.table("payments").select("*").eq("gymrat_id", str(member_id)).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_payment(payment_id):
    try:
        resp = supabase.table("payments").delete().eq("id", str(payment_id)).execute()
        return {"success": True, "data": resp.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
