#!/bin/bash

# Pornește consumer-ul în background, rulându-l ca modul
python -m app.consumer &

# Pornește serverul web în prim-plan
exec uvicorn app.main:app --host 0.0.0.0 --port 8000