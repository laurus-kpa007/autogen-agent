autogen_agent/
├── agents/               # 에이전트 구성 모듈 (오케스트레이터 에이전트 등)
│   ├── __init__.py
│   └── orchestrator_agent.py    # 오케스트레이터 에이전트 정의 및 생성
├── tools/                # 외부 툴 연동 모듈 (MCP 툴 등)
│   ├── __init__.py
│   └── mcp_tool.py           # MCP 툴 등록 및 관리
├── llm/                  # LLM 연결 모듈 (OpenAI, Azure 등)
│   ├── __init__.py
│   └── llm_client.py         # LLM 클라이언트 초기화 및 설정
├── ui/                   # 웹 UI 인터페이스 모듈
│   ├── __init__.py
│   └── web_app.py            # Gradio/Streamlit 기반 웹 인터페이스
├── cli/                  # CLI 인터페이스 모듈
│   ├── __init__.py
│   └── cli_app.py            # 터미널에서 실행되는 CLI 프로그램
├── configs/              # 설정 파일 디렉토리
│   ├── config.yaml           # 주요 설정 (LLM, MCP 서버 정보 등)
│   └── llm_config.yaml       # (옵션) LLM별 세부 설정 분리 가능
└── requirements.txt      # 의존성 패키지 목록
# autogen-agent
