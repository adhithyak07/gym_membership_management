from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from datetime import date, datetime
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fix the import path - try multiple approaches
try:
    # Method 1: Direct import if src is in the same directory
    from src.logic import GymratManager, PaymentManager
except ImportError:
    try:
        # Method 2: Add current directory to path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from src.logic import GymratManager, PaymentManager
    except ImportError:
        try:
            # Method 3: Import from current directory
            from src.logic import GymratManager, PaymentManager
        except ImportError:
            # Method 4: Manual path addition
            current_dir = os.path.dirname(os.path.abspath(__file__))
            src_dir = os.path.join(current_dir, 'src')
            sys.path.insert(0, src_dir)
            from src.logic import GymratManager, PaymentManager

app = FastAPI(title="Gym Membership API", version="1.0")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

gymrat_mgr = GymratManager()
payment_mgr = PaymentManager()

# -------------------- Schemas --------------------
class MemberCreate(BaseModel):
    name: str
    phone: str
    plan: str
    start_date: date | None = None
    end_date: date | None = None

class MemberUpdate(BaseModel):
    new_plan: str
    new_end_date: date | None = None

class PaymentCreate(BaseModel):
    member_id: str  # MUST BE STRING
    amount: float
    payment_date: datetime | None = None
    method: str | None = None

# -------------------- Debug Routes --------------------
@app.get("/debug/model-info")
def debug_model_info():
    """Get information about PaymentCreate model fields"""
    fields_info = {}
    for field_name, field_info in PaymentCreate.model_fields.items():
        fields_info[field_name] = {
            "annotation": str(field_info.annotation),
            "required": field_info.is_required(),
            "default": str(field_info.default) if field_info.default else None
        }
    return {
        "model": "PaymentCreate",
        "fields": fields_info
    }

@app.get("/debug/payment-schema")
def debug_payment_schema():
    """Debug endpoint to check PaymentCreate schema"""
    # Test data that should work
    test_data = {
        "member_id": "f66aae8d-c61b-4baa-885e-d12fdf2fa152",
        "amount": 1000.00,
        "method": "Cash"
    }
    
    try:
        payment = PaymentCreate(**test_data)
        return {
            "success": True, 
            "message": "PaymentCreate model working correctly",
            "parsed_data": payment.model_dump()
        }
    except ValidationError as e:
        return {
            "success": False,
            "error": str(e),
            "error_details": e.errors()
        }

@app.post("/debug/test-payment")
def debug_test_payment(data: dict):
    """Debug endpoint to test raw payment data"""
    try:
        # Try to create PaymentCreate object from raw data
        payment = PaymentCreate(**data)
        return {
            "success": True,
            "message": "Data parsed successfully",
            "parsed": payment.model_dump(),
            "received": data
        }
    except ValidationError as e:
        return {
            "success": False,
            "error": "Validation failed",
            "error_details": e.errors(),
            "received": data
        }

# -------------------- Main Routes --------------------
@app.get("/")
def root():
    return {"status": "API running 🚀", "timestamp": datetime.now().isoformat()}

# --- Members ---
@app.post("/members/")
def add_member(member: MemberCreate):
    result = gymrat_mgr.add_member(member.name, member.phone, member.plan, member.start_date, member.end_date)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.get("/members/")
def get_all_members():
    result = gymrat_mgr.get_all_members()
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.put("/members/{member_id}")
def update_member(member_id: str, update: MemberUpdate):
    result = gymrat_mgr.update_member(member_id, update.new_plan, update.new_end_date)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.delete("/members/{member_id}")
def delete_member(member_id: str):
    result = gymrat_mgr.delete_member(member_id)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

# --- Payments ---
@app.post("/payments/")
def add_payment(payment: PaymentCreate):
    print(f"DEBUG: Received payment data: {payment}")  # Debug print
    print(f"DEBUG: member_id type: {type(payment.member_id)}")  # Debug print
    
    result = payment_mgr.add_payment(payment.member_id, payment.amount, payment.payment_date, payment.method)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.get("/payments/")
def get_all_payments():
    result = payment_mgr.get_all_payments()
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.get("/payments/member/{member_id}")
def get_payments_by_member(member_id: str):
    result = payment_mgr.get_payments_by_member(member_id)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: str):
    result = payment_mgr.delete_payment(payment_id)
    if result["success"]:
        return result
    raise HTTPException(status_code=400, detail=result.get("error", result["message"]))

# -------------------- Run --------------------
def start():
   import uvicorn
   uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)  # Added reload=True for development

if __name__ == "__main__":
    start()