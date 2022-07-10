#!/bin/sh
uvicorn --factory "infrastructure.app:create_app" --host=0.0.0.0 --port=$PORT --reload
