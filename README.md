# image-predictor-service

Nanoservice that receives an image and returns the detected material.

#### Build & Run application

To build the application:

`docker compose build`

To run the application:

`docker compose up`

To stop the application:

`docker compose down`

To add env variables to heroku

#### Heroku Deploy

```
heroku config:set PORT=8000 -a peaceful-refuge-34158
heroku config:set MONGODB_URL=mongodb+srv://<user>:<password>@cluster0.b3b5klh.mongodb.net/test -a peaceful-refuge-34158
heroku container:push web -a peaceful-refuge-34158
heroku container:release web -a peaceful-refuge-34158
```

#### Pre-commit

After cloning the repo, you should run the following command in order to add the pre-commit hook to
git:

```
pre-commit install
```

If you don't have pre-commit installed you can do it by running:

```
pip install pre-commit
```

Now, whenever you try making a commit, the pre-commit hook will run automatically before that. If
every step passes, the commit will proceed as usual. If any of the pre-commit steps fails, the
commit won't be executed.

In the case where the failure was just because there was a formatting problem that got fixed
automatically during the pre-commit, you can try committing again and the commit should proceed as
usual.

But if there was a step that required manual changes, you must fix them before being able to
continue with the commit.

If you want to just execute the pre-commit steps, you can run the command:

```
pre-commit run --all-files
```
