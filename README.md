![example branch parameter](https://github.com/Weapon-X6/GluEckWein/actions/workflows/django.yml/badge.svg)
[![codecov](https://codecov.io/gh/Weapon-X6/GluEckWein/graph/badge.svg?token=3UHVPNOGUL)](https://codecov.io/gh/Weapon-X6/GluEckWein)

# GlückWein
A RESTful API for wines using Full-Text Search

### Features

* Supports pagination, filtering, ranking, and highlighting
* Also offer suggestions for misspelled words
* Provides a Postgres API along with a more advanced Elasticsearch API
* React client use E2E testing (Cypress)

### Up & Running
First  run
```
docker-compose up -d --build
```

Then load fixtures --you should see something like: Installed 150930 object(s) from 1 fixture(s)
```
docker-compose exec server python manage.py loaddata wines.json --format=json
```


And finally, update mapping
```
docker-compose exec server python manage.py elasticsearch
```

Then you can use it through the React client at http://localhost:3000/

![React client|666x430](client/public/glueckwein_DE.png)


You can also use the API directly either using:
- Elasticsearch through http://localhost:8003/api/v1/catalog/wines/  or
- Postgres through http://localhost:8003/api/v1/catalog/pg-wines/
