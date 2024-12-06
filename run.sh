#!/bin/bash
gunicorn -w $(nproc) -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app