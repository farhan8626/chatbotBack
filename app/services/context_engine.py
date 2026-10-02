import contextvars
from datetime import datetime

# Context variables for implicit state injection
ctx_role = contextvars.ContextVar('role', default='consumer')
ctx_kiosk_id = contextvars.ContextVar('kiosk_id', default=None)
ctx_mobile_number = contextvars.ContextVar('mobile_number', default=None)

class ContextEngine:
    @staticmethod
    def get_system_instruction(base_prompt: str, guardrails: str) -> str:
        role = ctx_role.get()
        kiosk_id = ctx_kiosk_id.get()
        mobile_number = ctx_mobile_number.get()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build dynamic context block
        dynamic_context = f"\n\n--- CURRENT SYSTEM STATE ---\nTime: {now}\nUser Role: {role.upper()}\n"
        
        if kiosk_id:
            dynamic_context += f"Kiosk ID: {kiosk_id} (Hardware Status: Online, Paper: OK)\n"
        if mobile_number:
            dynamic_context += f"User Mobile Number: {mobile_number}\n"
            
        dynamic_context += "----------------------------\n"
        
        return f"{base_prompt}\n{guardrails}{dynamic_context}"

context_engine = ContextEngine()
