# llm/llm_client.py

import os
import yaml
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

def load_llm_config(config_file_path: str) -> dict:
    """
    llm_config.yaml 파일을 로드하여 딕셔너리로 반환합니다.
    """
    with open(config_file_path, 'r', encoding='utf-8') as f:
        llm_config = yaml.safe_load(f)
    return llm_config


def get_llm_client(llm_config: dict):
    """
    llm_config 딕셔너리를 기반으로 LLM 클라이언트를 생성하여 반환합니다.
    LM Studio 등 API 키 없이 사용하는 환경도 'lm-studio'라는 더미 키를 넣어 강제 통과시킵니다.
    """
    provider = llm_config.get("provider", "openai")
    model_name = llm_config.get("model", "gpt-3.5-turbo")

    if provider == "openai":
        # 설정 또는 환경 변수에 키가 없으면 'lm-studio' 더미 키를 사용
        api_key = llm_config.get("api_key") or os.environ.get("OPENAI_API_KEY") or "lm-studio"
        base_url = llm_config.get("base_url")  # LM Studio 사용 시 필수

        return OpenAIChatCompletionClient(
            model=model_name,
            openai_api_key=api_key,
            base_url=base_url
        )

    elif provider == "azure":
        # Azure 환경에서는 실제 키가 반드시 필요하다고 가정
        azure_endpoint = llm_config["azure_endpoint"]
        azure_deployment = llm_config["azure_deployment"]
        azure_api_key = llm_config.get("azure_api_key") or os.environ.get("AZURE_API_KEY")
        if not azure_api_key:
            raise ValueError("Azure OpenAI 환경변수 AZURE_API_KEY가 설정되어 있지 않습니다.")
        return AzureOpenAIChatCompletionClient(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=llm_config.get("azure_api_version", "2023-05-15"),
            api_key=azure_api_key,
            model=model_name
        )

    else:
        raise ValueError(f"지원하지 않는 LLM provider: {provider}")
