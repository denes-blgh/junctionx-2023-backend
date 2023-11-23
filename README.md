# JunctionX Budapest 2023 - Backend

## Local development

Build container:
```
docker build -t junctionx .
```

Run container with auto-reload:
```
docker run -p 127.0.0.1:7000:7000 -it -v .:/app junctionx
```

Create migrations
```
aerich migrate
```

Run migrations
```
aerich upgrade
```

Access the Swagger UI docs: http://localhost:7000/docs/

Jenkins deployment: https://dene.sh/junctionx/api/
