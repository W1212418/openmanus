import streamlit as st
from dotenv import load_dotenv
from ai_service import generate_ip_profile
import os

load_dotenv()

st.set_page_config(
    page_title="抖音账号分析系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.form("account_analysis_form"):
    st.header("账号信息录入")
    account_name = st.text_input("Account Name")
    industry = st.text_input("Industry")
    core_advantage = st.text_area("Core Advantages")
    target_audience = st.text_input("Target Audience")
    competitor_account = st.text_input("Competitor Account")
    operation_goal = st.selectbox(
        "运营目标",
        options=["品牌曝光", "产品转化", "粉丝增长", "用户互动"]
    )
    submitted = st.form_submit_button("开始分析")

if submitted:
    with st.spinner('正在生成账号分析报告...'):
        try:
            analysis_result = generate_ip_profile({
                "account_name": account_name,
                "industry": industry,
                "core_advantage": core_advantage,
                "target_audience": target_audience,
                "competitor_account": competitor_account,
                "operation_goal": operation_goal
            })
            
            st.success("分析完成！")
            st.subheader("IP人设定位")
            st.markdown(f"""{analysis_result['profile']}""")

            st.subheader("推荐选题方向")
            for i, topic in enumerate(analysis_result['topics'][:20], 1):
                st.markdown(f"{i}. {topic}")
        
        if st.button("换方向生成新选题"):
            with st.spinner('正在生成新选题...'):
                try:
                    new_topics = generate_ip_profile({
                        "account_name": account_name,
                        "industry": industry,
                        "core_advantage": core_advantage,
                        "target_audience": target_audience,
                        "competitor_account": competitor_account,
                        "operation_goal": operation_goal
                    })['topics'][:20]
                    for i, topic in enumerate(new_topics, 1):
                        st.markdown(f"{i}. {topic}")
                except Exception as e:
                    st.error(f"选题刷新失败：{str(e)}")

        except Exception as e:
            st.error(f"分析失败：{str(e)}")