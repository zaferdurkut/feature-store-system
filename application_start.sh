#!/bin/bash
/wait-for-it.sh redis:6379 -t 60 --strict
/wait-for-it.sh batch-redis:6379 -t 60 --strict
uvicorn main:app --host 0.0.0.0 --port 80
