# 部署 gitlab runner

拉取镜像：  
```
docker pull --platform linux/amd64 gitlab/gitlab-runner:alpine3.21-bleeding && \
docker pull --platform linux/amd64 gitlab/gitlab-runner-helper:alpine3.21-x86_64-bleeding
```

标记镜像：
```
docker tag gitlab/gitlab-runner:alpine3.21-bleeding hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding && \
docker tag gitlab/gitlab-runner-helper:alpine3.21-x86_64-bleeding hub-poseidon.cisdigital.cn/mirror/gitlab/gitlab-runner-helper:alpine3.21-x86_64-bleeding
```

登陆harbor：  
```
docker login hub-poseidon.cisdigital.cn
```

推送镜像到harbor：  
```
docker push hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding && \
docker push hub-poseidon.cisdigital.cn/mirror/gitlab/gitlab-runner-helper:alpine3.21-x86_64-bleeding
```

登陆到目标服务器，启动runner容器：  
```
mkdir -p /data/gitlab-runner-data/config/ && \
docker run -d --name gitlab-runner \
--restart always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /data/gitlab-runner-data/config:/etc/gitlab-runner \
hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding
```

# 注册 gitlab runner
> gitlab cicd -> runner页面上会展示注册需要的url和registration token  

容器启动成功后，执行(注意修改token)：  
```
export PROJECT_REGISTRATION_TOKEN="bmVJDUQxsxmvfkgn4iVk" && \
ip=$(hostname -I | awk '{print $1}') && \
docker run --rm \
  -v /data/gitlab-runner-data/config:/etc/gitlab-runner \
  hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding register \
  --non-interactive \
  --url "https://git.cisdigital.cn/" \
  --registration-token "$PROJECT_REGISTRATION_TOKEN" \
  --executor "docker" \
  --docker-image "hub-poseidon.cisdigital.cn/mirror/gitlab-ci-cd:1.0.0" \
  --description "gitlab-runner-${ip}" \
  --maintenance-note "" \
  --tag-list "datakits" \
  --run-untagged="true" \
  --locked="false" \
  --access-level="not_protected"
```

# All In One

```
mkdir -p /data/gitlab-runner-data/config/ && \
docker run -d --name gitlab-runner \
--restart always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /data/gitlab-runner-data/config:/etc/gitlab-runner \
hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding && \
export PROJECT_REGISTRATION_TOKEN="bmVJDUQxsxmvfkgn4iVk" && \
ip=$(hostname -I | awk '{print $1}') && \
docker run --rm \
  -v /data/gitlab-runner-data/config:/etc/gitlab-runner \
  hub-poseidon.cisdigital.cn/mirror/gitlab-runner:alpine3.21-bleeding register \
  --non-interactive \
  --url "https://git.cisdigital.cn/" \
  --registration-token "$PROJECT_REGISTRATION_TOKEN" \
  --executor "docker" \
  --docker-helper-image "hub-poseidon.cisdigital.cn/mirror/gitlab/gitlab-runner-helper:alpine3.21-x86_64-bleeding" \
  --docker-image "hub-poseidon.cisdigital.cn/mirror/gitlab-ci-cd:1.0.0" \
  --description "gitlab-runner-${ip}" \
  --maintenance-note "" \
  --tag-list "datakits" \
  --run-untagged="true" \
  --locked="false" \
  --access-level="not_protected"
```
