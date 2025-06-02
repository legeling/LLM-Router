import httpx
import json

def chat(prompt, model, base_url="http://localhost:8000", api_key="llm-gateway-key-001", **kwargs):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        **kwargs
    }
    
    with httpx.Client() as client:
        response = client.post(
            f"{base_url.rstrip('/')}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60.0
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API调用失败: {response.status_code}, {response.text}")


def list_models(base_url="http://localhost:8000", api_key="llm-gateway-key-001"):
    """
    获取可用模型列表
    Args:
        base_url: 网关地址
        api_key: API密钥
    Returns:
        模型列表
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    
    with httpx.Client() as client:
        response = client.get(
            f"{base_url.rstrip('/')}/v1/models",
            headers=headers,
            timeout=30.0
        )
        
        if response.status_code == 200:
            result = response.json()
            return [model["id"] for model in result["data"]]
        else:
            raise Exception(f"获取模型列表失败: {response.status_code}, {response.text}")


# 使用示例
if __name__ == "__main__":
    try:
        # 获取可用模型
        models = list_models()
        print("可用模型:", models)
        
        if models:
            # 发送聊天请求
            response = chat("你好", models[0])
            print(f"回复: {response}")
        
    except Exception as e:
        print(f"调用失败: {e}")