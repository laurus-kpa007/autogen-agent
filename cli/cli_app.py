# cli_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse, asyncio, yaml
from agents.orchestrator_agent import create_orchestrator_agent

async def main():
    # 설정 로드
    #config = yaml.safe_load(open("configs/config.yaml", "r"))
    with open("configs/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    agent = await create_orchestrator_agent(config)
    
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description="오케스트레이터 에이전트 CLI")
    parser.add_argument("-q", "--question", help="에이전트에게 보낼 질문")
    args = parser.parse_args()
    
    if args.question:
        # 1. 질문 인자가 주어진 경우: 한 번 질문하고 종료
        answer = await agent.run(task=args.question)
        print(answer)
    else:
        # 2. 인자가 없으면 대화형 모드 진입
        print("대화형 모드 - 질문을 입력하고 Enter 키를 누르세요. (종료: exit)")
        while True:
            user_input = input("질문> ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            answer = await agent.run(task=user_input)
            print(f"에이전트: {answer}\n")

# 비동기 main 실행
if __name__ == "__main__":
    asyncio.run(main())
