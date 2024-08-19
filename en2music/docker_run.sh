# 更新本地镜像版本
docker login harbor-contest.4pd.io -u dongjintao -p msk4dFFi@
docker pull harbor-contest.4pd.io/dongjintao/env:2.0
# 清理同名容器

docker kill dongjintao-en2music
docker rm dongjintao-en2music
# 拉起容器
docker run --name dongjintao-en2music -p 80:80  -v ~/en2music:/workspace/  -it --privileged  --gpus all harbor-contest.4pd.io/dongjintao/env:2.0 /bin/bash