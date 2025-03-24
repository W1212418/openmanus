# 抖音人设分析系统

## 项目结构
```
douyin-analyzer-backend/
├── douyinrenshe_script.py    # 主程序
├── ai_service.py            # AI服务模块
├── requirements.txt          # 依赖清单
└── .env                     # 环境配置
```

## 快速开始
1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```env
DEEPSEEK_API_KEY=your_api_key
```

3. 启动应用
```bash
streamlit run douyinrenshe_script.py
```

## 开发规范
- 接口命名使用小写+下划线格式
- 配置文件统一存放在config目录
- 日志记录采用python-logging模块