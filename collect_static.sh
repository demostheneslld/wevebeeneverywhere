# Build JS
echo 'Building JS Toolchain'
cd ./_jstoolchain
npm run build
cd ../

# Collect Static
echo 'Collecting Static Files'
python3 manage.py collectstatic --noinput -i ckeditor