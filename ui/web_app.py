# web_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import asyncio
import yaml
from agents.orchestrator_agent import create_orchestrator_agent

# 설정 로드 (config.yaml 파일 파싱)
with open("configs/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 애플리케이션 시작 시 에이전트 초기화 (비동기 함수 호출 처리)
agent = asyncio.get_event_loop().run_until_complete(create_orchestrator_agent(config))

# 사용자의 질문을 처리하는 함수 정의
def answer_question(user_input):
    # 에이전트에게 질문을 전달하고 응답 받기 (비동기 함수를 동기로 호출)
    response = asyncio.get_event_loop().run_until_complete(agent.run(task=user_input))
    return response

# Gradio UI 구성
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 오케스트레이터 에이전트 챗봇")
    chatbot = gr.Chatbot()    # 대화 기록 표시용 위젯
    msg = gr.Textbox(label="질문 입력")  # 질문 입력란
    clear = gr.Button("대화 초기화")

    # send 버튼 또는 엔터 입력 시 answer_question 호출 -> 챗봇 출력
    msg.submit(fn=answer_question, inputs=msg, outputs=chatbot)
    clear.click(fn=lambda: None, inputs=None, outputs=chatbot, queue=False)  # 대화 초기화 버튼

# 웹 앱 실행
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
