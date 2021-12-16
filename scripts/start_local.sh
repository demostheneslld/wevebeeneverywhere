./scripts/build_node.sh
./scripts/collect_static.sh

# Run Python
echo 'Running Application'
python3 manage.py runserver 127.0.0.1:8000