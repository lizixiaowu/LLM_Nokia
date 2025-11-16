from google.adk.agents.llm_agent import LlmAgent

def build_adk_planner(llm=None, model: str = "models/gemini-2.0-flash"):
    """
    Build the Planner agent for ADK workflow.
    Minimal fix: support either an existing LLM object or a model name.
    """

    # === 如果用户没传 LLM 对象，则使用模型名创建 ===
    if llm is None:
        from gemini_llm import GeminiLlm
        llm = GeminiLlm(model_name=model)

    # === 提取模型名（兼容 LLM 对象或字符串） ===
    model_name = getattr(llm, "model", None)
    if hasattr(model_name, "model_name"):
        model_name = model_name.model_name
    elif not isinstance(model_name, str):
        model_name = str(model_name)

    # === 构建 ADK Agent ===
    planner_agent = LlmAgent(
        name="Planner_ADK",
        description="Plans the enterprise LAN topology using Gemini model.",
        model=model_name,
    )

    print(f"[build_adk_planner] ✅ Planner built with model: {model_name}")
    return planner_agent

