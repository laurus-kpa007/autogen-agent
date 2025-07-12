# web_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import streamlit as st
# import asyncio
# import yaml
# from agents.orchestrator_agent import create_orchestrator_agent

# # YAML 설정 로드
# with open("configs/config.yaml", "r", encoding="utf-8") as f:
#     config = yaml.safe_load(f)

# # 에이전트 생성 (Streamlit-safe with caching)
# @st.cache_resource
# def get_agent():
#     return asyncio.run(create_orchestrator_agent(config))

# agent = get_agent()

# # 사용자 질문 처리 함수
# def chat_with_agent(user_input):
#     response = asyncio.run(agent.run(task=user_input))

#     # 메시지 오브젝트에서 답변 텍스트만 추출
#     if isinstance(response, dict) and "messages" in response:
#         messages = response["messages"]
#         for msg in reversed(messages):
#             if msg.get('source') == 'orchestrator':
#                 return msg.get('content'), response
#         return "답변을 찾을 수 없습니다.", response
#     elif isinstance(response, str):
#         return response, response
#     else:
#         return str(response), response

# # Streamlit UI
# st.title("🤖 오케스트레이터 챗봇")

# user_input = st.text_input("질문을 입력하세요:")

# show_raw = st.checkbox("🔍 메시지 객체 전체 보기")

# if st.button("답변 받기") and user_input:
#     response_text, full_response = chat_with_agent(user_input)
#     st.write(response_text)

#     if show_raw:
#         st.subheader("📦 Raw 메시지 객체")
#         st.json(full_response)

# st.markdown("---")
# st.caption("Made with Autogen & Streamlit")

import streamlit as st
import asyncio
import yaml
from agents.orchestrator_agent import create_orchestrator_agent

# Streamlit 페이지 설정 (브라우저 탭 타이틀 변경)
st.set_page_config(page_title="🤖 오케스트레이터 챗봇")

# YAML 설정 로드
with open("configs/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 에이전트 생성 (Streamlit-safe with caching)
@st.cache_resource
def get_agent():
    return asyncio.run(create_orchestrator_agent(config))

agent = get_agent()

# 사용자 질문 처리 함수
async def chat_with_agent_async(user_input):
    log_steps = []
    response = await agent.run(task=user_input)

    log_steps.append("✅ 에이전트 실행 완료")

    if isinstance(response, dict) and "messages" in response:
        messages = response["messages"]
        log_steps.append(f"🔍 메시지 {len(messages)}건 수신")

        for msg in reversed(messages):
            content = getattr(msg, 'content', None)
            if content:
                if isinstance(content, list):
                    log_steps.append("📄 content: 리스트 반환")
                    return str(content), log_steps
                elif isinstance(content, str):
                    log_steps.append("📄 content: 텍스트 반환")
                    return content, log_steps
        log_steps.append("❗ 답변 content 없음")
        return "답변을 찾을 수 없습니다.", log_steps

    elif isinstance(response, str):
        log_steps.append("📄 문자열 응답 반환")
        return response, log_steps

    else:
        log_steps.append("❗ 예외 응답 유형")
        return str(response), log_steps

# Streamlit UI
st.title("🤖 오케스트레이터 챗봇")

if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input("질문을 입력하세요:", value=st.session_state.user_input, key="input_text")

with col2:
    if st.button("❌"):
        st.session_state.user_input = ""
        st.session_state.input_text = ""
        st.rerun()

if user_input and user_input.strip():
    response_text, log_steps = asyncio.run(chat_with_agent_async(user_input))
    st.session_state.history.append({
        "question": user_input,
        "answer": response_text,
        "log": log_steps
    })
    st.session_state.user_input = ""
    st.session_state.input_text = ""
    st.rerun()

for i, entry in enumerate(st.session_state.history):
    st.markdown(f"**🙋 질문 {i+1}:** {entry['question']}")
    st.markdown(f"**🤖 답변:** {entry['answer']}")

    with st.expander(f"📝 단계별 처리 로그 (질문 {i+1})"):
        for step in entry['log']:
            st.markdown(f"- {step}")

st.markdown("---")
st.caption("Made with Autogen & Streamlit")
