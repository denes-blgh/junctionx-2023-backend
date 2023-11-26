# JunctionX Budapest 2023 - Backend

The backend repository of our project, see the bottom of the page for the frontend. You can try our dashboard without installing through this link:

https://junctionx-2023-frontend.vercel.app/

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
docker exec -it <container-id> aerich migrate
```

Run migrations
```
docker exec -it <container-id> aerich upgrade
```

Every branch is available on a Jenkins deployment with the format `https://dene.sh/junctionx/{branch}/api/`.

Check out the Swagger UI Docs on https://dene.sh/junctionx/master/api/docs.

## Frontend repository

https://github.com/ZsombiTech/junctionx-2023-frontend

