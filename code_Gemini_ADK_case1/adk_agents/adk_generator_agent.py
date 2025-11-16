"""
ADK Generator Agent
根据网络规划（来自 Planner Agent）生成 Cisco IOS 配置命令。
"""

import time
from gemini_llm import GeminiLlm


# === 构建函数：供主流程调用 ===
def build_adk_generator(llm=None, model: str = "models/gemini-2.0-flash"):
    """
    构建 Generator Agent 实例。
    支持传入已有 LLM 对象或仅传模型名。
    """
    # === 如果用户没传 LLM 对象，则使用模型名创建 ===
    if llm is None:
        llm = GeminiLlm(model_name=model)

    # === 提取模型名（兼容 LLM 对象或字符串） ===
    if hasattr(llm, "model_name"):
        model_name = llm.model_name
    elif hasattr(llm, "model"):
        model_name = llm.model
    else:
        model_name = str(model)

    print(f"[build_adk_generator] ✅ Generator built with model: {model_name}")
    return GeneratorAgent(llm)


# === 核心 Agent 类 ===
class GeneratorAgent:
    """
    根据 Planner 输出的网络拓扑生成 Cisco 配置。
    """

    def __init__(self, llm: GeminiLlm):
        self.llm = llm
        print(f"[GeneratorAgent] ✅ Initialized with model: {getattr(llm, 'model_name', 'unknown')}")

    def run(self, plan_text: str) -> str:
        """
        根据网络规划文本生成配置命令。
        """
        system_prompt = (
            "You are 'Config Generator', a network engineer generating Cisco IOS configurations "
            "based on a provided network plan."
        )
        user_prompt = f"""
Using the following plan, generate Cisco configuration commands for the core switch.

Plan:
{plan_text}
"""
        print("[GeneratorAgent] 🚀 Generating configuration...")
        try:
            result = self.llm.generate(f"{system_prompt}\n\n{user_prompt}")
            print("[GeneratorAgent] ✅ Generation complete.")
            return result
        except Exception as e:
            print(f"[GeneratorAgent] ❌ Generation failed: {e}")
            return f"[GeneratorAgent Error] {e}"
