import os
import json
from groq import AsyncGroq
from app.services.context_engine import context_engine, ctx_role
from app.services.mcp_client import GROQ_TOOLS, TOOL_FUNCTIONS

class AIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY is missing in .env")
        
        self.client = AsyncGroq(api_key=api_key)
        # self.model = "llama-3.3-70b-versatile"
        # self.model = "llama-3.1-8b-instant"
        self.model = "gemma2-9b-it"
        
        self.system_prompt = self._load_prompt("system_prompt.txt")
        self.guardrails = self._load_prompt("guardrails.txt")
        self.customer_template = self._load_prompt("customer_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        filepath = os.path.join("app", "prompts", filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _apply_output_guardrails(self, text: str, role: str) -> str:
        if not text:
            return ""
            
        text_upper = text.upper()
        if "CORE DIRECTIVES:" in text_upper or "SECURITY GUARDRAILS:" in text_upper or "CURRENT SYSTEM STATE" in text_upper:
            return "I am the Quantan AI Assistant. I can only help you with Quantan products and services."
            
        if role != 'ADMIN' and "admin_get_kiosk_revenue" in text:
            return "I am the Quantan AI Assistant. I can only help you with Quantan products and services."
            
        return text

    async def generate_response_async(self, query: str, context: str, history: list) -> str:
        user_role = ctx_role.get().upper()
        
        # Build dynamic context block
        full_system_instructions = context_engine.get_system_instruction(
            base_prompt=self.system_prompt, 
            guardrails=self.guardrails
        )
        
        # RBAC Filtering
        allowed_tools = GROQ_TOOLS
        if user_role != 'ADMIN':
            allowed_tools = [tool for tool in GROQ_TOOLS if tool.get('function', {}).get('name') != 'admin_get_kiosk_revenue']
            full_system_instructions = full_system_instructions.replace("admin_get_kiosk_revenue", "")
        
        # Inject RAG and query
        final_prompt = self.customer_template.format(
            context=context,
            query=query
        )
        
        # Initialize Groq messages array
        messages = [{"role": "system", "content": full_system_instructions}]
        messages.extend(history)
        messages.append({"role": "user", "content": final_prompt})
        
        try:
            # Tool calling loop
            while True:
                response = None
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = await self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            tools=allowed_tools,
                            tool_choice="auto",
                            max_tokens=1024
                        )
                        break
                    except Exception as e:
                        if "tool_use_failed" in str(e) and attempt < max_retries - 1:
                            print(f"Groq syntax error on attempt {attempt+1}, retrying...")
                            continue
                        raise e
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                
                # If no tool calls, we are done
                if not tool_calls:
                    final_text = response_message.content or ""
                    return self._apply_output_guardrails(final_text, user_role)

                # Append the assistant's tool call message
                messages.append(response_message)
                
                # Execute tools and append results
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = TOOL_FUNCTIONS.get(function_name)
                    
                    if function_to_call:
                        try:
                            args_str = tool_call.function.arguments
                            if not args_str or args_str.strip() == "null":
                                function_args = {}
                            else:
                                function_args = json.loads(args_str)
                                if function_args is None:
                                    function_args = {}
                                    
                            # Call our MCP wrapper
                            function_response = await function_to_call(**function_args)
                        except Exception as e:
                            function_response = json.dumps({"error": f"Failed to execute tool: {str(e)}"})
                            
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    else:
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps({"error": "Tool not found"}),
                        })
                        
        except Exception as e:
            return f"An error occurred while connecting to Groq AI: {str(e)}"

# Singleton instance
ai_service = AIService()
