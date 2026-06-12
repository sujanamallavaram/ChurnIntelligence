# Complete Docker Configuration Guide

Step-by-step guide to configure Docker for your Churn Insight & Intervention Portal.

## ✅ System Status

```
✓ Docker Desktop: 29.5.3 installed
✓ Docker Compose: v5.1.4 installed
✓ Project: C:\Sujana\project1
✓ Dockerfile: Present and configured
✓ docker-compose.yml: Present and configured
⚠ Docker Daemon: Not responding (needs startup)
```

---

## 🚨 Docker Desktop Not Starting - Solutions

### Solution 1: Start Docker Desktop via GUI (Easiest)

**Step 1: Open Windows Start Menu**
```
Click Windows icon in bottom-left corner
OR
Press Windows Key
```

**Step 2: Search for Docker**
```
Type: "Docker"
You should see "Docker Desktop" appear
```

**Step 3: Click to Launch**
```
Click on "Docker Desktop" 
Wait 20-30 seconds for it to fully start
Look for Docker whale icon in system tray (bottom-right)
```

**Step 4: Verify Docker is Running**
```
Look at bottom-right corner (system tray)
You should see Docker icon (whale 🐳)
Icon should be stable (not blinking/spinning)
```

---

### Solution 2: Start Docker Desktop via PowerShell

**Open PowerShell as Administrator:**
```powershell
# Right-click on PowerShell
# Select "Run as Administrator"
```

**Then run one of these commands:**

```powershell
# Option A: Direct path
& "C:\Program Files\Docker\Docker\Docker.exe"

# Option B: Using cmd
cmd /c start "Docker" "C:\Program Files\Docker\Docker\Docker.exe"

# Option C: Using WSL
wsl -d docker-desktop
```

**Wait for startup:**
```
Docker Desktop will launch (new window opens)
Wait 20-30 seconds for full initialization
You'll see a Docker icon in system tray
```

---

### Solution 3: Check for Startup Issues

**Test Docker Connection:**
```powershell
# After Docker Desktop has started, test:
docker --version
docker ps
docker info
```

**Expected Output:**
```
Docker version 29.5.3, build d1c06ef
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty list is fine)
```

**If Still Not Working:**
```powershell
# Check if Docker daemon is listening
Test-NetConnection localhost -Port 2375 -CommonTCPPort docker

# Check Docker logs
docker system df

# Restart Docker completely
# 1. Right-click Docker icon in tray
# 2. Select "Quit Docker Desktop"
# 3. Wait 10 seconds
# 4. Click Docker icon again to restart
```

---

### Solution 4: Docker Desktop Configuration

**Check Docker Settings:**

1. **Right-click Docker icon** → Select "Settings"
2. **General Tab:**
   - ✓ Ensure "Start Docker Desktop when you log in" is checked
   - ✓ "Use the WSL 2 based engine" is recommended

3. **Resources Tab:**
   - Memory: At least 2-4 GB
   - CPUs: At least 2-4
   - Disk Image size: At least 10 GB

4. **Advanced Tab:**
   - Ensure network settings are default
   - Check "Use new virtualization framework" (if available)

5. **Apply and Restart**

---

## 🔧 Configure Docker for Your Project

Once Docker Desktop is running and responding to `docker ps`:

### Step 1: Navigate to Project Directory

```powershell
cd C:\Sujana\project1
ls -la

# You should see:
# - Dockerfile
# - docker-compose.yml
# - requirements.txt
# - app.py
# - config.py
# - data_utils.py
# - viz_utils.py
```

### Step 2: Build the Docker Image

```powershell
# Build with specific tag
docker build -t churn-portal:latest .
```

**What's happening:**
```
[1] Reading Dockerfile
[2] Downloading Python 3.11-slim base image (from Docker Hub)
[3] Setting up /app directory
[4] Copying requirements.txt
[5] Installing Python packages (streamlit, pandas, plotly, numpy)
[6] Copying your application files
[7] Setting port 8501
[8] Creating the image
```

**Expected output:**
```
[+] Building 45.3s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/8] FROM python:3.11-slim
 => [2/8] WORKDIR /app
 => [3/8] COPY requirements.txt .
 => [4/8] RUN pip install --no-cache-dir -r requirements.txt
    Collecting streamlit==1.40.1
    Collecting pandas==2.2.0
    Collecting plotly==5.24.0
    Collecting numpy==1.26.4
    Installing collected packages...
 => [5/8] COPY . .
 => [6/8] EXPOSE 8501
 => [7/8] CMD ["streamlit", "run", "app.py", ...]
 => exporting to image
 => naming to docker.io/library/churn-portal:latest

Successfully tagged churn-portal:latest
```

**Build time:** 30-60 seconds (first time, slower due to base image download)

### Step 3: Verify Image Was Created

```powershell
# List Docker images
docker images

# Look for churn-portal
```

**Expected output:**
```
REPOSITORY      TAG       IMAGE ID       CREATED        SIZE
churn-portal    latest    abc123def456   2 minutes ago   685MB
```

### Step 4: Run the Container

**Option A: Using Docker Compose (Recommended)**

```powershell
cd C:\Sujana\project1

docker-compose up
```

**Expected output:**
```
[+] Running 1/1
 ✓ Container sujana-project1-churn-portal-1  Created
Attaching to sujana-project1-churn-portal-1
sujana-project1-churn-portal-1  | 
sujana-project1-churn-portal-1  | 2024-06-12 12:34:56.789 
sujana-project1-churn-portal-1  |   You can now view your Streamlit app in your browser.
sujana-project1-churn-portal-1  |
sujana-project1-churn-portal-1  |   Local URL: http://localhost:8501
sujana-project1-churn-portal-1  |   Network URL: http://172.17.0.2:8501
```

**Option B: Using Docker Run (Direct)**

```powershell
docker run \
  --name churn-portal \
  -p 8501:8501 \
  -v ${PWD}:/app \
  churn-portal:latest
```

### Step 5: Access Your Application

**Open Browser:**
```
http://localhost:8501
```

**You should see:**
- 📊 Churn Insight & Intervention Portal
- 4 KPI cards (Total Customers, At Risk, Total MRR, MRR at Risk)
- 6 interactive charts
- Scenario simulation controls
- At-risk customer recommendations table

---

## 🛑 Stop the Container

### Stop Docker Compose

```powershell
# While docker-compose is running, press:
Ctrl + C

# Or in another terminal:
docker-compose down
```

### Stop Direct Container

```powershell
docker stop churn-portal
docker rm churn-portal
```

---

## 📋 Common Docker Commands

### View Running Containers
```powershell
docker ps
```

### View All Containers (including stopped)
```powershell
docker ps -a
```

### View Container Logs (Real-time)
```powershell
docker-compose logs -f

# Or for direct container:
docker logs churn-portal -f
```

### Enter Container Shell
```powershell
docker exec -it churn-portal powershell

# Then:
cd /app
ls
python --version
```

### Rebuild Image After Code Changes
```powershell
docker build -t churn-portal:latest .
docker-compose up --build
```

### Remove Containers and Images
```powershell
# Stop container first
docker-compose down

# Remove image
docker rmi churn-portal:latest

# Remove all unused
docker system prune -a
```

---

## 🔧 Docker Configuration Files Explained

### Dockerfile (Your Container Blueprint)

```dockerfile
FROM python:3.11-slim
# Use lightweight Python 3.11 image (base layer)

WORKDIR /app
# Set working directory to /app inside container

COPY requirements.txt .
# Copy requirements.txt from host to container

RUN pip install --no-cache-dir -r requirements.txt
# Install Python packages
# --no-cache-dir saves space (don't cache pip packages)

COPY . .
# Copy entire project directory to /app

EXPOSE 8501
# Expose port 8501 (Streamlit's default)

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Run Streamlit on container startup
# --server.address=0.0.0.0 makes it accessible from outside container
```

### docker-compose.yml (Container Orchestration)

```yaml
version: '3.8'
# Docker Compose format version

services:
  churn-portal:
    # Service name (how you reference it)
    
    build: .
    # Build image from Dockerfile in current directory
    
    ports:
      - "8501:8501"
    # Map port 8501 on host to port 8501 in container
    # Format: "HOST_PORT:CONTAINER_PORT"
    
    volumes:
      - .:/app
    # Mount current directory to /app in container
    # Allows live code updates without rebuild
    
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      # Run in headless mode (no browser auto-open)
      
      - STREAMLIT_SERVER_PORT=8501
      # Streamlit server port
      
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      # Listen on all network interfaces
    
    command: streamlit run app.py
    # Override CMD from Dockerfile
```

---

## ❓ Troubleshooting

### Error: "Docker Desktop is unable to start"

**Cause:** Docker daemon not running or failed to initialize

**Solutions:**
1. **Restart Docker Desktop**
   - Right-click Docker icon → Quit Docker Desktop
   - Wait 10 seconds
   - Click Docker icon to restart

2. **Check System Resources**
   - Docker needs 2-4 GB RAM available
   - Check Task Manager → Performance tab
   - Close other apps if needed

3. **Check Docker Installation**
   ```powershell
   # Verify Docker executable exists
   Test-Path "C:\Program Files\Docker\Docker\Docker.exe"
   
   # Should return: True
   ```

4. **Reset Docker**
   - Settings → General → "Reset Docker to Factory Defaults"
   - This will take 2-3 minutes

### Error: "Port 8501 already in use"

```powershell
# Find what's using port 8501
netstat -ano | findstr :8501

# Kill the process (replace 12345 with PID)
taskkill /PID 12345 /F

# Or use different port in docker-compose.yml:
# Change "8501:8501" to "8502:8501"
# Then access at http://localhost:8502
```

### Error: "Cannot connect to Docker daemon"

```powershell
# Check if Docker Desktop is running
Get-Process docker -ErrorAction SilentlyContinue

# Check Docker socket
Test-NetConnection localhost -Port 2375

# Start Docker Desktop manually
& "C:\Program Files\Docker\Docker\Docker.exe"
```

### Slow Build/Run Speed

```powershell
# Allocate more resources to Docker
# Settings → Resources → Increase Memory/CPU

# Check current usage
docker stats

# Prune unused images/containers
docker system prune -a
```

### Container Exits Immediately

```powershell
# Check logs
docker-compose logs

# If Streamlit fails, verify requirements.txt is present
# and all dependencies listed
```

---

## 📊 Docker Resource Usage

**Typical Resource Usage:**
```
Image Size:        ~685 MB (Python 3.11-slim + dependencies)
Container Memory:  300-500 MB typical
Container CPU:     Low (idle), peaks during data processing
Disk Space:        ~2 GB for Docker (images + containers)
```

**Optimize if Tight on Resources:**
```powershell
# Remove old images
docker image prune

# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune

# Check disk usage
docker system df
```

---

## ✅ Verification Checklist

- [ ] Docker Desktop installed (29.5.3 ✓)
- [ ] Docker Compose installed (v5.1.4 ✓)
- [ ] Docker Desktop is running (check system tray)
- [ ] `docker ps` returns container list (no error)
- [ ] Project files present (Dockerfile, docker-compose.yml, requirements.txt, app.py)
- [ ] Image built successfully (`docker images` shows churn-portal)
- [ ] Container running (`docker ps` shows running container)
- [ ] Application accessible at http://localhost:8501
- [ ] Dashboard loads and shows KPI cards
- [ ] Charts and tables are interactive

---

## 🚀 Complete Workflow

```powershell
# 1. Ensure Docker Desktop is running
docker ps

# 2. Navigate to project
cd C:\Sujana\project1

# 3. Build image (do this once, or after code changes)
docker build -t churn-portal:latest .

# 4. Run container
docker-compose up

# 5. Open browser
# http://localhost:8501

# 6. Stop when done
# Press Ctrl+C in terminal
# Or: docker-compose down
```

---

## 📚 Additional Resources

- **Docker Docs:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **Streamlit + Docker:** https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker
- **Windows Docker Setup:** https://docs.docker.com/desktop/install/windows-install/

---

**Status:** ✅ Ready to configure  
**Estimated Setup Time:** 5-10 minutes (first time build)  
**Subsequent Runs:** 5-10 seconds  
**Last Updated:** June 2024
