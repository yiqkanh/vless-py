# VLESS Proxy (Python实现)

基于Python的高性能VLESS代理服务器实现，使用aiohttp和asyncio。

## 功能特性

- 支持VLESS协议的WebSocket传输
- 异步高性能实现
- 支持多UUID配置
- 自动文件下载功能
- 可配置监听端口

## 安装

1. 克隆仓库
```bash
git clone https://github.com/your-repo/vless-py.git
cd vless-py
```

2. 创建虚拟环境并安装依赖
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 配置

### 推荐使用`.env`文件配置

1. 复制示例文件:
```bash
cp .env.example .env
```

2. 编辑`.env`文件，填写你的配置:
```ini
VLESS_UUIDS=your-uuid-here
PORT=8080
# 服务器名称(用于VLESS配置标识)
NAME=my-server
# 其他可选配置...
```

NAME配置说明:
- 用于VLESS配置的标识名称
- 默认使用主机名
- 如果包含"server"或"hostypanel"会自动生成多IP配置

3. 程序会自动加载`.env`文件中的配置

### 环境变量加载顺序:
1. 优先使用`.env`文件中的配置
2. 其次使用系统环境变量
3. 最后会提示交互式输入

### 或者直接通过环境变量配置:

```bash
# 必需配置
export VLESS_UUIDS="your-uuid1,your-uuid2"

# 可选配置
export PORT=8080
export VLESS_BINARY_URL="https://example.com/vless-binary"
export VLESS_BINARY_PATH="./bin/vless"
```

或运行时会提示交互式输入配置。

安全提示:
- 不要将`.env`文件提交到版本控制
- 使用强密码UUID
- 生产环境应配置TLS

## 运行

推荐使用启动脚本(首次运行需添加执行权限):

```bash
# 添加执行权限(只需一次)
chmod +x run.sh

# 启动服务
./run.sh
```

或直接运行:

```bash
python main.py
```

## 使用示例

1. 获取VLESS配置链接：
```
http://your-server:8080/your-uuid
```

2. 客户端配置：
- 地址: your-server
- 端口: 8080
- UUID: your-uuid
- 传输协议: WebSocket
- 路径: /ws/your-uuid

## 注意事项

1. 确保服务器防火墙开放相应端口
2. 生产环境建议配置TLS证书
3. 定期更新UUID保证安全