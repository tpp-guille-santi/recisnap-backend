#!/bin/sh
uvicorn  "infrastructure.app:app" --host=0.0.0.0 --port=$PORT --reload
