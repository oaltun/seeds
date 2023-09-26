podman build . --tag=evolver:latest
podman run  -e OPENAI_API_KEY=$OPENAI_API_KEY -it -v $(pwd)/image:/app/image -w /app/image evolver:latest  /app/venv/bin/python3 main.py
