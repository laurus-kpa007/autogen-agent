# mcp_tool.py
import asyncio
from autogen_ext.tools.mcp import StdioServerParams, SseServerParams, mcp_server_tools

async def load_mcp_tools(mcp_config):
    """MCP 서버에 연결하여 사용 가능한 툴 리스트 반환"""
    protocol = mcp_config.get("protocol", "stdio")
    # 1. MCP 서버 파라미터 설정 (STDIO 또는 SSE 방식 선택)
    if protocol == "stdio":
        params = StdioServerParams(
            command=mcp_config["command"],        # 예: 실행할 서버 명령 (ex: "docker")
            args=mcp_config.get("args", []),      # 서버 실행 인자 리스트
            env=mcp_config.get("env", {})         # 환경변수 (토큰 등)
        )
    elif protocol == "sse":
        params = SseServerParams(
            url=mcp_config["url"],               # 원격 MCP 서버의 SSE URL
            headers=mcp_config.get("headers", {}),# 인증 헤더 등
            timeout=mcp_config.get("timeout", 5),
            sse_read_timeout=mcp_config.get("sse_read_timeout", 300)
        )
    else:
        raise ValueError(f"Unsupported MCP protocol: {protocol}")
    
    # 2. MCP 서버로부터 툴 가져오기 (동적으로 툴 목록 조회)
    tools = await mcp_server_tools(params)
    return tools
