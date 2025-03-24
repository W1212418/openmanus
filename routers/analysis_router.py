from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/api/analysis', tags=['账号分析'])

class AccountAnalysisRequest(BaseModel):
    account_name: str
    industry: str
    core_advantage: str
    target_audience: str
    competitor_account: str
    operation_goal: str

@router.post('/ip-plan')
async def generate_ip_plan(request: AccountAnalysisRequest):
    from ai_service import generate_ip_profile
    try:
        analysis_result = await generate_ip_profile(
            account_info=request.dict(),
            industry=request.industry,
            advantages=request.core_advantage
        )
        return {
            "ip_profile": analysis_result["profile"],
            "topic_suggestions": analysis_result["topics"][:20]
        }
    except Exception as e:
        return {"error": f"模型服务异常: {str(e)}"}

@router.post('/topics/fresh')
async def refresh_topics():
    # 待实现选题刷新逻辑
    return {"message": "换方向生成选题接口"}