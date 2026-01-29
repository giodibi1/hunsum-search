#!/bin/bash

exec fastapi run routers/router.py --host 0.0.0.0 --port 80
#fastapi run routers/router.py --port 80
#python main.py