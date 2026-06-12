# Docker Configuration Guide

Complete guide to configure and run the Churn Insight & Intervention Portal in Docker.

## ✅ Prerequisites Verified

```
✓ Docker Desktop: 29.5.3 installed
✓ Docker Compose: v5.1.4 installed
✓ Dockerfile: Configured correctly
✓ docker-compose.yml: Configured correctly
```

## 🚀 Step 1: Start Docker Desktop

### Option A: Via Windows Start Menu (Recommended)
```
1. Press Windows Key + S to open Search
2. Type "Docker" and press Enter
3. Click "Docker Desktop" to launch
4. Wait 15-30 seconds for Docker to fully start
5. Look for Docker icon in system tray (bottom right)
```

### Option B: Via Command Line
```powershell
# Option 1: Using the exe directly
"C:\Program Files\Docker\Docker\Docker.exe"

# Option 2: Using WSL (if installed)
wsl -d docker-desktop

# Option 3: Check if already running
docker ps
```

### Option C: Verify Docker is Running
```powershell
docker --version
docker ps
```

Expected output:
```
Docker version 29.5.3, build d1c06ef
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty list means no containers running yet)
```

---

## 🐳 Step 2: Build the Docker Image

Once Docker Desktop is running:

### Build the Image
```powershell
cd C:\Sujana\project1

# Build the Docker image
docker build -t churn-portal:latest .
```

**What this does:**
- Reads the `Dockerfile`
- Downloads Python 3.11-slim base image (~150 MB)
- Installs dependencies from `requirements.txt`
- Packages your application

**Expected output:**
```
[+] Building 45.3s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/8] FROM python:3.11-slim
 => [2/8] WORKDIR /app
 => [3/8] COPY requirements.txt .
 => [4/8] RUN pip install --no-cache-dir -r requirements.txt
 => [5/8] COPY . .
 => [6/8] EXPOSE 8501
 => [7/8] CMD ["streamlit", "run", "app.py", ...]
 => exporting to image
 => naming to docker.io/library/churn-portal:latest

Successfully built 123abc456def
```

### Verify the Image Built
```powershell
docker images | grep churn-portal
```

Expected output:
```
churn-portal      latest    123abc456def   2 minutes ago   685MB
```

---

## ▶️ Step 3: Run the Container

### Option A: Using Docker Compose (Recommended)

```powershell
cd C:\Sujana\project1

# Start the service
docker-compose up
```

**Expected output:**
```
[+] Running 1/1
 ⠿ Container project1-churn-portal-1  Created
Attaching to project1-churn-portal-1
project1-churn-portal-1  |
project1-churn-portal-1  |   You can now view your Streamlit app in your browser.
project1-churn-portal-1  |
project1-churn-portal-1  |   Local URL: http://localhost:8501
project1-churn-portal-1  |   Network URL: http://172.17.0.2:8501
```

Then access the app at: **http://localhost:8501**

### Option B: Using Docker Run (Direct)

```powershell
cd C:\Sujana\project1

docker run \
  --name churn-portal \
  -p 8501:8501 \
  -v ${PWD}:/app \
  churn-portal:latest
```

Then access the app at: **http://localhost:8501**

---

## 🛑 Step 4: Stop the Container

### Stop Docker Compose
```powershell
# Press Ctrl+C in the terminal where docker-compose is running

# Or, in another terminal:
docker-compose down
```

### Stop a Direct Container
```powershell
docker stop churn-portal
docker rm churn-portal
```

---

## 📋 Useful Docker Commands

### View Running Containers
```powershell
docker ps
```

### View All Containers (including stopped)
```powershell
docker ps -a
```

### View Container Logs
```powershell
# Real-time logs
docker-compose logs -f

# Or for direct container:
docker logs churn-portal -f
```

### Enter Container Shell
```powershell
docker exec -it churn-portal bash

# Then explore:
ls -la
python --version
pip list
```

### Remove Unused Images and Containers
```powershell
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything (careful!)
docker system prune
```

### Rebuild Image (after code changes)
```powershell
docker build -t churn-portal:latest .
docker-compose up --build
```

---

## 🔧 Docker Configuration Explanation

### Dockerfile Breakdown

```dockerfile
FROM python:3.11-slim
# Use lightweight Python 3.11 as base image

WORKDIR /app
# Set working directory to /app

COPY requirements.txt .
# Copy your dependencies file

RUN pip install --no-cache-dir -r requirements.txt
# Install Python packages (--no-cache saves space)

COPY . .
# Copy entire project

EXPOSE 8501
# Expose port 8501 (where Streamlit runs)

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Run Streamlit on startup
```

### docker-compose.yml Breakdown

```yaml
version: '3.8'
# Docker Compose format version

services:
  churn-portal:
    build: .
    # Build image from ./Dockerfile

    ports:
      - "8501:8501"
    # Map port 8501 (host) to 8501 (container)

    volumes:
      - .:/app
    # Mount current directory to /app (live code updates)

    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    # Configure Streamlit behavior

    command: streamlit run app.py
    # Run this command on startup
```

---

## ❓ Troubleshooting

### Docker Daemon Not Responding
```
Error: Cannot connect to Docker daemon
```

**Solution:**
1. Verify Docker Desktop is running (check system tray)
2. Restart Docker Desktop:
   - Right-click Docker icon → Restart
3. Or restart from command line:
   ```powershell
   docker system prune -a
   docker ps
   ```

### Port Already in Use
```
Error: bind: address already in use
```

**Solution 1: Use different port**
```powershell
docker run -p 8502:8501 churn-portal:latest
# Access at http://localhost:8502
```

**Solution 2: Kill process on port**
```powershell
# Find what's using port 8501
netstat -ano | findstr :8501

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Docker Out of Disk Space
```
Error: no space left on device
```

**Solution:**
```powershell
# Clean up unused containers, images, volumes
docker system prune -a --volumes

# Check Docker disk usage
docker system df
```

### Permission Denied
```
Error: permission denied while trying to connect
```

**Solution:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → Run as Administrator
# Then retry Docker commands
```

---

## 📊 Quick Reference

| Task | Command |
|------|---------|
| Start container | `docker-compose up` |
| Stop container | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Rebuild image | `docker build -t churn-portal:latest .` |
| Enter container | `docker exec -it churn-portal bash` |
| List containers | `docker ps -a` |
| Remove container | `docker rm churn-portal` |
| Remove image | `docker rmi churn-portal:latest` |

---

## 🚀 Next Steps

1. **Start Docker Desktop** (if not already running)
2. **Build the image**: `docker build -t churn-portal:latest .`
3. **Run the container**: `docker-compose up`
4. **Access the app**: Open http://localhost:8501
5. **View logs**: `docker-compose logs -f`
6. **Make changes**: Edit code, Docker will auto-reload
7. **Stop**: Press Ctrl+C or `docker-compose down`

---

## 📚 Additional Resources

- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Streamlit in Docker: https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
- Python Docker Best Practices: https://docs.docker.com/language/python/

---

**Status**: ✅ Ready to configure  
**Image Size**: ~685 MB (lightweight)  
**Container Memory**: ~300-500 MB typical  
**Startup Time**: 5-10 seconds after container starts
