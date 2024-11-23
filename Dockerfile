# 使用官方的Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /

# 克隆Git仓库（注意：这通常不是推荐的做法，因为它依赖于外部网络）
RUN git clone https://github.com/hylnb/MenuBApi.git .

# 安装Python依赖（假设requirements.txt在克隆的仓库中）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（如果Flask应用运行在默认端口5000上）
EXPOSE 5000

# 设置容器启动时执行的命令（假设Flask应用有一个名为app.py的文件）
CMD ["python", "app.py"]
