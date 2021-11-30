# Run Docker Image Locally
echo 'Starting Docker Run Local'
docker run -it --env-file ./.env --network=host ghcr.io/demostheneslld/wevebeeneverywhere:latest 