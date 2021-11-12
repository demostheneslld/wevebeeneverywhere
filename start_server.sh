# Build JS
echo 'Building JS Toolchain'
cd ./_jstoolchain
npm run build
cd ../

# Run Python
echo 'Activating Virtual Environment'
source ./_env/bin/activate
echo 'Collecting Static Files'
python3 manage.py collectstatic --noinput
echo 'Running Application'
python3 manage.py runserver 127.0.0.1:8000