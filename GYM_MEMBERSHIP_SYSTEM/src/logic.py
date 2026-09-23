from src.db import (
    add_member, get_all_members, update_member, delete_member,
    add_payment, get_all_payments, get_payments_by_member, delete_payment
)

# ===================== Gymrat Manager =====================
class GymratManager:
    """Handles all operations related to gym members."""

    def add_member(self, name, phone, plan, start_date=None, end_date=None):
        result = add_member(name, phone, plan, start_date, end_date)
        if result["success"]:
            return {"success": True, "message": f"Member '{name}' added successfully.", "data": result["data"]}
        return {"success": False, "message": f"Failed to add member '{name}'.", "error": result.get("error")}

    def get_all_members(self):
        result = get_all_members()
        if result["success"]:
            return {"success": True, "data": result["data"], "message": "Fetched all members successfully."}
        return {"success": False, "message": "Failed to fetch members.", "error": result.get("error")}

    def update_member(self, member_id, new_plan, new_end_date=None):
        result = update_member(member_id, new_plan, new_end_date)
        if result["success"]:
            return {"success": True, "message": f"Member '{member_id}' updated successfully.", "data": result["data"]}
        return {"success": False, "message": f"Failed to update member '{member_id}'.", "error": result.get("error")}

    def delete_member(self, member_id):
        result = delete_member(member_id)
        if result["success"]:
            return {"success": True, "message": f"Member '{member_id}' deleted successfully.", "data": result["data"]}
        return {"success": False, "message": f"Failed to delete member '{member_id}'.", "error": result.get("error")}

# ===================== Payment Manager =====================
class PaymentManager:
    """Handles all operations related to payments."""

    def add_payment(self, member_id, amount, payment_date=None, method=None):
        result = add_payment(member_id, amount, payment_date, method)
        if result["success"]:
            return {"success": True, "message": f"Payment of {amount} added for member '{member_id}'.", "data": result["data"]}
        return {"success": False, "message": f"Failed to add payment for member '{member_id}'.", "error": result.get("error")}

    def get_all_payments(self):
        result = get_all_payments()
        if result["success"]:
            return {"success": True, "data": result["data"], "message": "Fetched all payments successfully."}
        return {"success": False, "message": "Failed to fetch payments.", "error": result.get("error")}

    def get_payments_by_member(self, member_id):
        result = get_payments_by_member(member_id)
        if result["success"]:
            return {"success": True, "data": result["data"], "message": f"Fetched payments for member '{member_id}' successfully."}
        return {"success": False, "message": f"Failed to fetch payments for member '{member_id}'.", "error": result.get("error")}

    def delete_payment(self, payment_id):
        result = delete_payment(payment_id)
        if result["success"]:
            return {"success": True, "message": f"Payment '{payment_id}' deleted successfully.", "data": result["data"]}
        return {"success": False, "message": f"Failed to delete payment '{payment_id}'.", "error": result.get("error")}
