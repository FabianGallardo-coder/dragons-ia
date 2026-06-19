# How to Install ngrok in the Dragons & Ia Docker Container

This guide explains how to install and configure ngrok inside the running `dragons-ia-app` Docker container to expose the backend API to the internet via a secure tunnel.

## Prerequisites

1. The `dragons-ia-app` container must be running (backend server on port 8000 inside the container).
2. You have Docker installed and can run `docker exec` commands.
3. You have an ngrok account (free tier is sufficient for basic use). Sign up at https://dashboard.ngrok.com/signup to get an authtoken.

## Step-by-Step Instructions

### 1. Access the Container Shell

First, open a shell inside the running container:

```bash
docker exec -it dragons-ia-app /bin/sh
```

If the container doesn't have `/bin/sh`, try `/bin/bash`:

```bash
docker exec -it dragons-ia-app /bin/bash
```

You should now see a shell prompt inside the container.

### 2. Install Dependencies (if needed)

The container is based on `python:3.11-slim` (Debian-based). Ngrok doesn't require many dependencies, but you might need `wget` or `curl` to download it.

Check if `wget` or `curl` is installed:

```sh
which wget || which curl
```

If neither is installed, install one:

```sh
apt-get update && apt-get install -y wget
```

### 3. Download and Install ngrok

Ngrok provides a pre-compiled binary for Linux. Download the latest stable version for Linux AMD64:

```sh
# Download ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Extract the binary
tar -xzf ngrok-v3-stable-linux-amd64.tgz

# Move the binary to a location in your PATH (e.g., /usr/local/bin)
mv ngrok /usr/local/bin/

# Make it executable (should already be executable)
chmod +x /usr/local/bin/ngrok

# Clean up the downloaded archive
rm ngrok-v3-stable-linux-amd64.tgz
```

### 4. Configure ngrok Authtoken

To use ngrok beyond the free trial limitations, you need to authenticate with your authtoken.

1. Get your authtoken from the ngrok dashboard: https://dashboard.ngrok.com/get-started/your-authtoken
2. In the container shell, run:

```sh
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

Replace `YOUR_AUTHTOKEN_HERE` with your actual authtoken.

### 5. Start the ngrok Tunnel

Now you can start a tunnel to expose the backend API. The backend inside the container listens on port 8000.

```sh
# Start ngrok on port 8000 (HTTP)
ngrok http 8000
```

You will see output similar to:

```
Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxxxxxx.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     in1     out1
                              0       0       0       0
```

### 6. Use the Public URL

The `Forwarding` line shows the public URL (e.g., `https://xxxxxxxx.ngrok.io`). You can use this URL to access the Dragons & IA backend from anywhere on the internet.

For example, to check the health endpoint:
```sh
curl https://xxxxxxxx.ngrok.io/health
```

### 7. Stopping ngrok

To stop the ngrok tunnel, press `Ctrl+C` in the terminal where it's running.

### 8. Making the Tunnel Persistent (Optional)

If you want the tunnel to restart automatically when the container restarts, consider:

- Creating a custom Docker image that includes ngrok pre-installed and configured.
- Using Docker Compose to add ngrok as a separate service that tunnels to the app container.

## Alternative: Using Docker Compose to Add ngrok as a Service

For a more integrated approach, you can modify `docker-compose.yml` to include ngrok as a separate service. Here's an example addition:

```yaml
services:
  # ... existing services ...
  ngrok:
    image: wernight/ngrok:latest
    ports:
      - "4040:4040"  # ngrok web interface
    command: http dragons-ia-app:8000
    environment:
      - NGROK_AUTHTOKEN=your_authtoken_here
    depends_on:
      - dragons-ia-app
```

Then run `docker-compose up -d` to start both services.

## Troubleshooting

- **"command not found: ngrok"**: Ensure the ngrok binary is in your PATH (`/usr/local/bin` is usually in PATH by default).
- **Connection refused**: Make sure the backend server is running inside the container on port 8000. You can check with `curl http://localhost:8000/health` inside the container.
- **Ngrok error: tunnel not found**: Verify that you're tunneling to the correct port and that the backend is accessible.

## Security Considerations

- Exposing your local development server to the internet poses security risks. Only use this for testing or sharing with trusted individuals.
- The free ngrok tier has limitations on bandwidth and session duration. For production use, consider a paid plan or alternative tunneling solutions.
- Never expose sensitive API keys or credentials through the tunnel. Ensure your `.env` file is secure and not committed to version control.

## Notes for the Dragons & Ia Project

- The backend API is accessible at `/` (health endpoint), `/auth`, `/characters`, `/game`, etc.
- When using ngrok, remember that the `BASE_URL` in your frontend might need to be updated if you're serving the frontend from a different origin. However, if you're serving the frontend from the same container (via the same backend), the relative URLs should still work.
- For CORS reasons, the backend is configured to allow requests from `http://localhost:3000`, `http://localhost:8000`, and `http://127.0.0.1:8000` in development, and `https://dragons-ia.onrender.com` in production. If you're using ngrok, you might need to adjust the CORS settings in `backend/main.py` to allow the ngrok domain, or use the backend's relative URLs from the frontend.

---
*Last updated: $(date)*