# orchestrator_agent.py
from autogen_agentchat.agents import AssistantAgent
from llm.llm_client import get_llm_client
from tools.mcp_tool import load_mcp_tools

async def create_orchestrator_agent(config):
    """오케스트레이터 에이전트를 생성하여 반환 (비동기)."""
    # 1. LLM 클라이언트 초기화 (예: OpenAI API 클라이언트)
    model_client = get_llm_client(config["llm"])
    
    # 2. MCP 툴 목록 가져오기 (config에 정의된 MCP 서버에 연결)
    mcp_tools = await load_mcp_tools(config["mcp"])
    
    # 3. AutoGen AssistantAgent 생성 (이 에이전트가 툴 사용)
    agent = AssistantAgent(
        name="orchestrator",
        model_client=model_client,
        tools=mcp_tools,                        # MCP 툴 어댑터 리스트 주입
        system_message=config.get("system_message", "주어진 도구를 사용하여 사용자 요청을 처리하세요.")
    )
    return agent
