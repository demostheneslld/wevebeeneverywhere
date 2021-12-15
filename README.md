# wevebeeneverywhere
Travel Blog with Integrated Maps

# docker
Build: `docker build . -t ghcr.io/demostheneslld/wevebeeneverywhere:latest`
Test: `docker run -it -p 80:8000 --env-file .env ghcr.io/demostheneslld/wevebeeneverywhere:latest`
Push: `docker push ghcr.io/demostheneslld/wevebeeneverywhere:latest`

# exec into azure docker container
https://docs.microsoft.com/en-us/azure/container-instances/container-instances-exec
`az container exec --resource-group wevebeeneverywhere --name wbe2 --exec-command "/bin/bash"`

# backup/restore db
`python manage.py dumpdata -e sessions.Session --indent 2 > dump.json`
Comment out @receiver hooks on creating profiles
`python manage.py loaddata dump.json`