#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
pip install -r requirements.txt

# 启动服务
python main.py