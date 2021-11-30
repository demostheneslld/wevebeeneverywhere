# Build Docker Image
echo 'Starting Docker Build'
docker build --pull --rm -f "Dockerfile" -t ghcr.io/demostheneslld/wevebeeneverywhere:latest "."