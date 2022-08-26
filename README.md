# image-predictor-service

Nanoservice that receives an image and returns the detected material.

#### Build & Run application

To build the application:

`docker compose -f docker-compose.dev.yml build`

To run the application:

`docker compose -f docker-compose.dev.yml up`

To stop the application:

`docker compose -f docker-compose.dev.yml down`

To add env variables to heroku

#### Heroku Deploy

```
heroku config:set PORT=8000 -a peaceful-refuge-34158
heroku config:set MONGODB_URL=mongodb+srv://databasemanager:PiOnnLtfdyZrL7h5@cluster0.b3b5klh.mongodb.net/test -a peaceful-refuge-34158
heroku container:push web -a peaceful-refuge-34158
heroku container:release web -a peaceful-refuge-34158
```
