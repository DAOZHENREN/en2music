TIME=$(date +"T-%Y.%m.%d-%H.%M.%S-%3N") # 毫秒级时间
IMAGE_NAME=submit/en2music
IMAGE_TAG="${TIME}"
 
set -e
docker build -t "harbor-contest.4pd.io/dongjintao/${IMAGE_NAME}:${IMAGE_TAG}" .
docker login harbor-contest.4pd.io -u dongjintao -p msk4dFFi@
docker push "harbor-contest.4pd.io/dongjintao/${IMAGE_NAME}:${IMAGE_TAG}"
# docker rmi "harbor-contest.4pd.io/dongjintao/${IMAGE_NAME}:${IMAGE_TAG}"
echo "成功 ${IMAGE_NAME}:${IMAGE_TAG}"