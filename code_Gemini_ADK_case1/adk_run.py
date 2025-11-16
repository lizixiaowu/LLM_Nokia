import os
import asyncio
from dotenv import load_dotenv
from uuid import uuid4

# === Gemini 模型封装 ===
from gemini_llm import GeminiLlm

# === 智能体定义 ===
from adk_agents.adk_planner_agent import build_adk_planner
from adk_agents.adk_generator_agent import build_adk_generator

# === Session 管理 ===
from adk_services.adk_session_service import get_adk_session_service

# === 插件系统 ===
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions.session import Session


# -----------------------------------------------------------------------------
# ✅ AgentPlugin：负责运行各个智能体
# -----------------------------------------------------------------------------
class AgentPlugin(BasePlugin):
    def __init__(self, name: str, agent, session_service):
        super().__init__(name)
        self.agent = agent
        self.session_service = session_service

    async def on_agent_start(self, planner_output=None):
        print(f"\n🧩 Plugin '{self.name}' started.")
        try:
            # 创建唯一 Session ID
            session_id = str(uuid4())
            raw_session = self.session_service.create_session(session_id=session_id)
            print(f"✅ Created session (raw): {raw_session}")

            # 如果返回的不是合法 Session 实例，则构造一个新的
            if not isinstance(raw_session, Session):
                session = Session(
                    id=session_id,
                    appName=self.name,
                    user_id="default-user"
                )
            else:
                session = raw_session

            # 选择模型
            llm = GeminiLlm(model_name="models/gemini-2.0-flash")

            # === 🚀 根据不同插件角色定义 prompt ===
            if "Planner" in self.name:
                system_prompt = (
                    "You are a network planner. Your job is to design a small enterprise LAN topology "
                    "for a company with 3 departments and 50 employees. "
                    "Include VLANs, IP subnets, and key devices such as routers and switches."
                    "=== TOKEN AWARE INSTRUCTIONS ===\n"
                    "Your answer must stay under 400 tokens.\n"
                    "Use concise bullet points.\n"
                    "Avoid explanations and focus only on essential network design details.\n"
                    "Do NOT repeat information.\n"
                    "Keep sections compact and technical."
                )
                response = llm.generate(system_prompt)
                print(f"🧠 [Planner Output]\n{response}")
                return response  # ✅ 返回 Planner 结果给外层

            elif "Generator" in self.name:
                if not planner_output:
                    print("⚠️ No planner output provided, skipping Generator step.")
                    return None

                generator_prompt = f"""
                You are a network configuration engineer.
                Based on the following network design plan, generate Cisco IOS configuration commands
                for the core switch and router.
                === TOKEN AWARE INSTRUCTIONS ===
                Your answer must stay under 1200 tokens.
                Generate only Cisco IOS configuration.
                Do NOT include explanations or comments.
                Do NOT repeat the network plan.
                Output compact and valid CLI commands only.
                Ensure the final output ends cleanly.
                === Network Plan ===
                {planner_output}
                """
                response = llm.generate(generator_prompt)
                print(f"🧠 [Generator Output]\n{response}")
                return response

            else:
                # 默认情况
                response = llm.generate("Hello from ADK Runtime!")
                print(f"🧠 {self.name} generic response:\n{response}")
                return response

        except Exception as e:
            print(f"❌ Plugin {self.name} failed: {e}")
            return None


# -----------------------------------------------------------------------------
# ✅ 主执行函数（保持原有结构）
# -----------------------------------------------------------------------------
async def main():
    print("🔧 Starting ADK runtime...")

    # 加载环境变量
    load_dotenv()

    # 初始化 ADK agents
    planner = build_adk_planner(model="models/gemini-2.0-flash")
    generator = build_adk_generator(model="models/gemini-2.0-flash")
    print("✅ Agents built successfully.")

    # 创建 Session service
    session_service = get_adk_session_service()

    # 启动插件
    planner_plugin = AgentPlugin("PlannerPlugin", planner, session_service)
    generator_plugin = AgentPlugin("GeneratorPlugin", generator, session_service)

    # 🚀 Step 1：运行 Planner
    planner_output = await planner_plugin.on_agent_start()
    await asyncio.sleep(30)

    # 🚀 Step 2：将 Planner 输出传递给 Generator
    if planner_output:
        await generator_plugin.on_agent_start(planner_output=planner_output)
    else:
        print("⚠️ Planner did not produce valid output, skipping Generator.")

    print("\n🏁 ADK Workflow finished successfully.")


if __name__ == "__main__":
    asyncio.run(main())
