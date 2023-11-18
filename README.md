# Keep your free RTX4090

请勿声张, 有些事不需要公之于众.

Please keep quiet about it, as it doesn't need to be publicized.

## How to use

### Environment

- Python 3.6+ (3.8, 3.10, 3.11 测试通过, 但 3.6+ 应该也没问题)
- pip (一般跟随 Python 一起自动安装)


- Python 3.6+ (tested on 3.8, 3.10, 3.11, but should work on 3.6+)
- pip (should be installed with Python)

### 安装

1. 克隆或下载此仓库
2. 在仓库目录下运行 `pip install -r requirements.txt`
3. 将 `example.config.ini` 复制为 `config.ini` 并编辑其中的内容
4. 运行 `python app.py`
5. (建议) 将此项目部署到服务器上, 并添加一个 cron job 每小时运行一次

### Installation

1. Clone or download this repository
2. Run `pip install -r requirements.txt` in the repository directory.
3. Copy `example.config.ini` to `config.ini` and edit it.
4. Run `python app.py` to start this script.
5. (Optional but recommended) Use this project on a server, and add a cron job to run it about every 1 hour.
