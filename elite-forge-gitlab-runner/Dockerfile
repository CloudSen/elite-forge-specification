# 使用 Python官方Alpine镜像作为基础
FROM python:3.9.21-alpine3.21

# 配置镜像源（可选）
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 安装系统依赖
RUN apk update && \
    apk add --no-cache \
    git \
    curl \
    openjdk11 && \
    # 设置时区
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' > /etc/timezone && \
    # 清理缓存
    rm -rf /var/cache/apk/*

# 复制git-check.py到容器中
COPY git-check.py /scripts/git-check.py

# 配置Java环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# 验证安装
RUN java -version && \
    git --version && \
    curl --version && \
    python --version && \
    cat /scripts/git-check.py

# 设置工作目录
WORKDIR /app

# 保持容器运行
CMD ["tail", "-f", "/dev/null"]