# vless-py

一个基于Python的轻量级VLESS代理服务器实现（v0.5.20 beta3），使用WebSocket作为传输协议。
参照源代码： https://github.com/yonggekkk/sb-nodejs
## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/vless-py.git
cd vless-py/vless-py

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

## 配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，设置以下参数：
```
# 必需配置
UUID=你的UUID    # 用于客户端验证的唯一标识符
DOMAIN=你的域名   # 服务器域名

# 可选配置
PORT=8080       # 服务器监听端口，默认8080
WEB_PATH=/      # WebSocket路径，默认/
```

## 使用

### 方式一：使用脚本启动

```bash
chmod +x run.sh  # 添加执行权限（仅首次需要）
./run.sh
```

### 方式二：手动启动

```bash
# 确保已激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 启动服务器
python main.py
```

### 配置链接

启动服务器后，访问以下地址获取配置链接：
```
http://你的域名:端口/UUID
```

配置链接格式：
```
vless://{UUID}@{域名}:443?encryption=none&security=tls&sni={域名}&fp=chrome&type=ws&host={域名}&path=/
```

## 特性

- 支持WebSocket传输
- 支持IPv4和IPv6
- 支持TLS加密
- 支持多IP负载均衡（特定服务器名称）
- 轻量级实现
- 自动生成配置链接

## 高级功能

### 多IP支持
当服务器名称包含"server"或"hostypanel"时，系统会自动生成多个配置链接，包括：
- 多个IPv4地址（104.16.0.0 - 104.27.0.0系列）
- IPv6地址（2606:4700:: 和 2400:cb00:2049::）

### 协议细节
- 加密方式：none
- 安全性：TLS
- 指纹：chrome
- 传输类型：WebSocket

## 注意事项

- 请确保正确配置UUID和域名
- 建议在生产环境中使用TLS加密
- 默认监听端口为8080，可通过环境变量修改
- 项目依赖：
  - aiohttp==3.9.3
  - websockets==12.0
- 本项目仍处于测试阶段（beta3版本）

## 技术细节

- 使用Python asyncio实现异步I/O
- 支持WebSocket升级和双向通道
- 实现了完整的VLESS协议
- 支持域名和IP（v4/v6）目标地址
## 使用说明，参照
https://github.com/yonggekkk/sb-nodejs
