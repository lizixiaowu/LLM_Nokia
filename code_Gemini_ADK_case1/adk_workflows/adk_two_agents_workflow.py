from google.adk.runners import Runner
from adk_services.adk_session_service import get_adk_session_service

class ADKTwoAgentsWorkflow:
    """
    Defines a 2-agent collaborative ADK workflow: Planner ➜ Generator.
    """

    def __init__(self, planner, generator):
        # Runner now requires a session_service parameter in ADK 1.18.0
        self.runner = Runner(session_service=get_adk_session_service())
        self.planner = planner
        self.generator = generator

    def execute(self):
        print("=== [1] Running ADK Planner ===")
        plan_output = self.planner.run()
        print("\n--- Network Plan ---")
        print(plan_output)

        print("\n=== [2] Running ADK Generator ===")
        gen_output = self.generator.run(plan_output)
        print("\n--- Cisco Configuration ---")
        print(gen_output)

        print("\n✅ ADK Workflow Complete.")

