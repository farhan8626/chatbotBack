import json
import os
import random

# Target directory
KNOWLEDGE_DIR = "app/knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def save_json(filename, data):
    with open(os.path.join(KNOWLEDGE_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Generated {filename} with {len(data) if isinstance(data, list) else 1} items.")

def generate_company():
    data = {
        "company_name": "Quantan Technologies Pvt Ltd",
        "headquarters": "Pune, Maharashatra, India",
        "mission": "Empowering businesses with intelligent self-service kiosks and AI solutions.",
        "founded": 2024,
        "support_email": "support@quantan.io",
        "support_phone": "+91-800-123-4567"
    }
    save_json("company.json", data)

def generate_products():
    categories = ["Printing Kiosk", "Payment Kiosk", "Information Kiosk"]
    products = []
    for i in range(1, 21):
        cat = random.choice(categories)
        products.append({
            "product_id": f"PRD-{(1000+i)}",
            "name": f"Quantan {cat.split()[0]} Pro V{random.randint(1,4)}",
            "category": cat,
            "description": f"High performance {cat.lower()} designed for high-traffic areas. Features industrial grade components.",
            "price": random.randint(1500, 5000),
            "features": ["Touchscreen", "Thermal Printer", "Card Reader"]
        })
    save_json("products.json", products)

def generate_faqs():
    faqs = []
    topics = ["Kiosk Setup", "Software Updates", "Payment Gateway", "Hardware Maintenance", "General"]
    for i in range(1, 101):
        topic = random.choice(topics)
        faqs.append({
            "faq_id": f"FAQ-{i:03d}",
            "topic": topic,
            "question": f"How do I handle a {topic.lower()} issue (Scenario {i})?",
            "answer": f"For {topic.lower()} scenarios like this, please reboot the system. If the problem persists, check the manual or contact support."
        })
    # Add some specific realistic ones
    faqs[0]["question"] = "How do I load paper into the printing kiosk?"
    faqs[0]["answer"] = "Open the front panel using the master key, release the printer latch, and insert the 80mm thermal roll ensuring it feeds from underneath."
    save_json("faq.json", faqs)

def generate_troubleshooting():
    issues = []
    symptoms = ["Screen freezing", "Printer jam", "Card reader not responding", "Network disconnected", "Power failure"]
    for i in range(1, 31):
        sym = random.choice(symptoms)
        issues.append({
            "issue_id": f"TS-{i:03d}",
            "symptom": f"{sym} on unit type {random.choice(['A','B','C'])}",
            "resolution": f"Step 1: Restart. Step 2: Check cables. Step 3: Run diagnostic tool 4. If unresolved, escalate ticket."
        })
    save_json("troubleshooting.json", issues)

def generate_policies():
    policies = []
    for i in range(1, 16):
        policies.append({
            "policy_id": f"POL-{i:03d}",
            "name": f"Corporate Policy {i}",
            "details": "Quantan Technologies adheres to strict guidelines regarding data privacy and SLA uptimes."
        })
    save_json("policies.json", policies)

def generate_shipping():
    rules = []
    for i in range(1, 11):
        rules.append({
            "rule_id": f"SHP-{i:03d}",
            "region": f"Region {chr(64+i)}",
            "cost": 150 + (i * 10),
            "estimated_days": random.randint(3, 14)
        })
    save_json("shipping.json", rules)

def generate_installation():
    steps = []
    for i in range(1, 21):
        steps.append({
            "step_number": i,
            "task": f"Phase {i} of Hardware Assembly",
            "instruction": f"Ensure all structural bolts are tightened to {random.randint(15, 30)} Nm torque before powering on the mainboard."
        })
    save_json("installation.json", steps)

def main():
    generate_company()
    generate_products()
    generate_faqs()
    generate_troubleshooting()
    generate_policies()
    generate_shipping()
    generate_installation()
    # Add minimal files for others requested
    save_json("warranty.json", [{"id": 1, "terms": "1 Year Standard Hardware Warranty."}])
    save_json("software.json", [{"version": "2.4.1", "notes": "Bug fixes for payment gateway."}])

if __name__ == "__main__":
    print("Generating Quantan Knowledge Base...")
    main()
    print("Knowledge Base Generation Complete!")
