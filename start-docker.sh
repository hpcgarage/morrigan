ROOT_DIR="$(pwd)"

docker build -t morrigan-docker .
docker run --rm -it --name="morrigan" -v "${ROOT_DIR}/":/morrigan -w="/morrigan" morrigan-docker