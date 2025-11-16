from agents.planner_agent import plan_network
from agents.generator_agent import generate_config

def main():
    print("\n🚀 Running 2-Agent Demo (Planner → Generator)...\n")

    context = {}

    print("🧭 Running Planner...")
    context = plan_network(context)
    print("\n--- Network Plan ---\n", context.get("network_plan", "No plan."))

    print("\n⚙️ Running Generator...")
    context = generate_config(context)
    print("\n--- Cisco Config ---\n", context.get("config", "No config."))

    print("\n✅ Done! Two agents collaborated successfully.\n")

if __name__ == "__main__":
    main()

