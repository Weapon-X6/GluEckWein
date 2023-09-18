# GlückWein
A RESTful API for wines using Full-Text Search


### Features

* Supports pagination, filtering, ranking, and highlighting
* Provides a Postgres API along a more advanced Elastic Search API

### Up & Running
Just run
```
docker-compose up -d --build
```

Then you can use it through the React client at http://localhost:3000/

![React client|666x430](client/public/glueckwein.png)


You can also use the API directly either using:
- Elastic Search through http://localhost:8003/api/v1/catalog/wines/  or
- Postgres through http://localhost:8003/api/v1/catalog/pg-wines/
