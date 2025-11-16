import ollama

def chat_with_agent(agent_name, role_description, message):
    print(f"[{agent_name}] thinking...")
    response = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': f'You are {agent_name}. Your role: {role_description}'},
            {'role': 'user', 'content': message}
        ],
        options={"num_predict": 180}  # Keep replies short and fast
    )
    content = response['message']['content'].strip()
    print(f"[{agent_name}] reply:\n{content}\n")
    return content


def main():
    print("=== Network Automation Multi-Agent Demo ===")

    # Step 1: Network Planner - design the network
    planner_output = chat_with_agent(
        "Network Planner",
        "A senior network architect who designs LAN topologies for small companies.",
        "Design a simple LAN topology for a company with 3 departments and 50 employees. "
        "Describe the key devices, IP subnets, and connectivity in a concise format."
    )

    # Step 2: Config Generator - build device configuration
    config_output = chat_with_agent(
        "Config Generator",
        "A network engineer that writes Cisco IOS configuration commands based on the planned topology.",
        f"Using the following network plan, generate basic Cisco configuration commands for the core and access switches:\n{planner_output}"
    )

    # Step 3: Validator - check the configuration
    validator_output = chat_with_agent(
        "Validator",
        "A network operations expert who validates Cisco configurations for best practices and security.",
        f"Review the following configuration and list 3 potential issues or improvements:\n{config_output}"
    )

    # Step 4: Reporter - summarize the results
    reporter_output = chat_with_agent(
        "Reporter",
        "A technical writer summarizing the collaboration results for documentation.",
        f"Summarize the final network plan and configurations in a short technical report:\n"
        f"Plan:\n{planner_output}\nConfiguration:\n{config_output}\nValidation:\n{validator_output}"
    )

    print("=== Final Report ===")
    print(reporter_output)


if __name__ == "__main__":
    main()
import ollama

def chat_with_agent(agent_name, role_description, message):
    print(f"[{agent_name}] thinking...")
    response = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': f'You are {agent_name}. Your role: {role_description}'},
            {'role': 'user', 'content': message}
        ],
        options={"num_predict": 180}  # Keep replies short and fast
    )
    content = response['message']['content'].strip()
    print(f"[{agent_name}] reply:\n{content}\n")
    return content


def main():
    print("=== Network Automation Multi-Agent Demo ===")

    # Step 1: Network Planner - design the network
    planner_output = chat_with_agent(
        "Network Planner",
        "A senior network architect who designs LAN topologies for small companies.",
        "Design a simple LAN topology for a company with 3 departments and 50 employees. "
        "Describe the key devices, IP subnets, and connectivity in a concise format."
    )

    # Step 2: Config Generator - build device configuration
    config_output = chat_with_agent(
        "Config Generator",
        "A network engineer that writes Cisco IOS configuration commands based on the planned topology.",
        f"Using the following network plan, generate basic Cisco configuration commands for the core and access switches:\n{planner_output}"
    )

    # Step 3: Validator - check the configuration
    validator_output = chat_with_agent(
        "Validator",
        "A network operations expert who validates Cisco configurations for best practices and security.",
        f"Review the following configuration and list 3 potential issues or improvements:\n{config_output}"
    )

    # Step 4: Reporter - summarize the results
    reporter_output = chat_with_agent(
        "Reporter",
        "A technical writer summarizing the collaboration results for documentation.",
        f"Summarize the final network plan and configurations in a short technical report:\n"
        f"Plan:\n{planner_output}\nConfiguration:\n{config_output}\nValidation:\n{validator_output}"
    )

    print("=== Final Report ===")
    print(reporter_output)


if __name__ == "__main__":
    main()

