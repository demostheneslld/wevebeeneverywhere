# Build JS
cd ./jstoolchain
npm run build

cd ../

# Run Python
source ./env/bin/activate
python3 manage.py collectstatic --noinput
python3 manage.py runserver 127.0.0.1:8000