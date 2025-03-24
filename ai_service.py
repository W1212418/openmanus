import os
from typing import Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

async def generate_ip_profile(account_info: Dict[str, Any], industry: str, advantages: str):
    """
    调用深度求索R1大模型生成IP人设方案
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    prompt = f"""根据以下账号信息生成IP人设方案和爆款选题：
    行业分类：{industry}
    核心优势：{advantages}
    账号基础信息：{account_info}
    
    要求：
    1. 人设方案包含性格特征、内容风格、视觉呈现等维度
    2. 爆款选题需结合行业热点和账号优势
    3. 输出结构化为JSON格式"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-r1",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        
        if response.status_code != 200:
            error_detail = {
                "error_type": "API_REQUEST_FAILED",
                "status_code": response.status_code,
                "response_text": response.text[:200]  # 截取前200字符避免敏感信息泄露
            }
            st.error(f"深度求索API请求异常：状态码{response.status_code}")
            raise ValueError(error_detail)

        try:
            result = response.json()
            if 'choices' not in result or len(result['choices']) == 0:
                raise json.JSONDecodeError("Missing choices field", doc='', pos=0)

            content = result['choices'][0]['message']['content']
            parsed_content = json.loads(content)
            
            # 验证必要字段
            required_fields = ['profile', 'topics']
            for field in required_fields:
                if field not in parsed_content:
                    raise KeyError(f"缺少必要字段: {field}")
            
            return parsed_content
            
        except json.JSONDecodeError as e:
            error_detail = {
                "error_type": "RESPONSE_PARSE_ERROR",
                "raw_content": content[:200],
                "exception": str(e)
            }
            st.error("响应内容解析失败，请检查API返回格式")
            raise ValueError(error_detail)
            
        except KeyError as e:
            error_detail = {
                "error_type": "MISSING_REQUIRED_FIELD",
                "missing_field": str(e),
                "available_fields": list(parsed_content.keys())
            }
            st.error(f"API响应缺少必要字段: {e}")
            raise ValueError(error_detail)
        
        except Exception as e:
            error_detail = {
                "error_type": "UNEXPECTED_ERROR",
                "exception": str(e)
            }
            st.error("发生未预期错误")
            raise ValueError(error_detail)