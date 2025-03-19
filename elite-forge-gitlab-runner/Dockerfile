# 通用GitLab Runner
# 包含 Python3.9.21 和 openJDK11环境
FROM python:3.9.21-alpine3.21

# 配置镜像源（可选）
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 设置 Maven 版本和路径
ENV MAVEN_VERSION=3.9.9
ENV MAVEN_HOME=/opt/maven
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="${JAVA_HOME}/bin:${MAVEN_HOME}/bin:${PATH}"

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
# 复制本地 Maven 安装包到容器（确保 `apache-maven-3.9.9-bin.tar.gz` 在当前目录）
COPY apache-maven-${MAVEN_VERSION}-bin.tar.gz /tmp/

# 安装 Maven
RUN mkdir -p /opt && \
    tar -xzf /tmp/apache-maven-${MAVEN_VERSION}-bin.tar.gz -C /opt && \
    mv /opt/apache-maven-${MAVEN_VERSION} ${MAVEN_HOME} && \
    rm -f /tmp/apache-maven-${MAVEN_VERSION}-bin.tar.gz

# 验证安装
RUN java -version && \
    git --version && \
    curl --version && \
    python --version && \
    mvn -v && \
    cat /scripts/git-check.py

# 设置工作目录
WORKDIR /app

# 保持容器运行
CMD ["tail", "-f", "/dev/null"]