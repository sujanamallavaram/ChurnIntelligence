# WSL 2 Installation Guide

**Problem**: WSL 2 (Windows Subsystem for Linux) is required for Docker Desktop to run

**Solution**: Install WSL 2 in 3 steps (10 minutes total)

---

## ⚡ Quick Fix (Copy & Paste)

### Step 1: Open PowerShell as Administrator

```
1. Press Windows Key
2. Type "PowerShell"
3. Right-click "Windows PowerShell"
4. Click "Run as Administrator"
5. If prompted, click "Yes"
```

### Step 2: Install WSL 2

```powershell
# Paste this command:
wsl --install

# This will:
# - Enable WSL
# - Install WSL 2 kernel
# - Install Ubuntu (default Linux distro)
```

**Expected output:**
```
Installing Windows Subsystem for Linux...
[====================100.0%====================]
Unpacking files...
The operation completed successfully.
Please restart your computer to complete the installation.
```

### Step 3: Restart Computer

```
1. Save your work
2. Close all programs
3. Click "Restart" when prompted
   OR
4. Run: shutdown /r /t 30
```

---

## ✅ Verify WSL 2 Installation

After restart, open PowerShell and run:

```powershell
wsl --version

# Should show:
# WSL version: 1.3.x
# Kernel version: 5.x.x
# WSLg version: 1.0.x
```

---

## 🐳 Now Start Docker

After WSL 2 is installed:

```powershell
# 1. Start Docker Desktop
# (Click in Windows Start Menu or run exe)

# 2. Wait 20-30 seconds for Docker to initialize

# 3. Test Docker
docker ps

# Should work without errors!
```

---

## 🆘 If Installation Fails

### Issue: "Windows Subsystem for Linux is not installed"

**Fix:**
```powershell
# Run as Administrator:
wsl.exe --install

# Or use full command:
wsl.exe --install --distribution Ubuntu
```

### Issue: "This operation failed"

**Fix:**
```powershell
# Update Windows first:
# Windows Key + I → System → About → Check for updates
# Install all updates and restart

# Then retry:
wsl --install
```

### Issue: "Virtualization disabled"

**Fix:**
```powershell
# Enable Virtual Machine Platform:
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Then restart and retry wsl --install
```

---

## 📋 Complete Instructions (If Copy-Paste Doesn't Work)

### Manual Step-by-Step

**1. Enable Virtual Machine Platform**
```powershell
# Run as Administrator:
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Wait for completion
```

**2. Enable WSL Feature**
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All

# When prompted, type: Y and press Enter
```

**3. Restart Computer**
```
Restart now!
```

**4. Install WSL 2 Kernel**
```powershell
# After restart, run as Administrator:
wsl --install
```

**5. Set WSL 2 as Default**
```powershell
wsl --set-default-version 2
```

**6. Verify Installation**
```powershell
wsl --version
wsl --list --verbose
```

---

## 🎯 Next Steps After WSL 2 Installation

Once WSL 2 is installed and working:

### 1. Start Docker Desktop
```powershell
# Click Docker icon in Start Menu
# Or run:
& "C:\Program Files\Docker\Docker\Docker.exe"
```

### 2. Wait for Initialization
```
Watch system tray (bottom-right)
Docker icon should appear
Wait 20-30 seconds for full startup
```

### 3. Test Docker
```powershell
docker ps
docker --version
docker run hello-world

# All should work without errors
```

### 4. Build Your Project
```powershell
cd C:\Sujana\project1
docker build -t churn-portal:latest .
docker-compose up
```

### 5. Access Dashboard
```
http://localhost:8501
```

---

## 📊 WSL 2 vs Hyper-V

**What you need to know:**

| Feature | WSL 2 | Hyper-V |
|---------|-------|---------|
| Docker support | ✅ Yes | ✅ Yes |
| Windows 10/11 | ✅ Both | ✅ Both (Pro/Enterprise) |
| Performance | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good |
| Linux access | ✅ Full | ❌ No direct access |
| Lightweight | ✅ Yes | ❌ Heavier |
| **Recommended** | ✅ **YES** | ❌ Legacy option |

**WSL 2 is the recommended approach** for Docker on Windows.

---

## 🔄 Installation Timeline

```
Total Time: ~15-20 minutes

- PowerShell setup: 1 minute
- wsl --install command: 2-3 minutes
- Computer restart: 3-5 minutes
- Docker initialization: 1-2 minutes
- Testing: 1-2 minutes
- Total: 10-15 minutes
```

---

## ✨ Once Docker is Working

```powershell
cd C:\Sujana\project1

# Build image
docker build -t churn-portal:latest .

# Run container
docker-compose up

# Access: http://localhost:8501
```

---

## 📞 Troubleshooting Commands

```powershell
# Check WSL status
wsl --list --verbose

# Check Docker connection
docker ps
docker version
docker info

# View Docker logs
Get-Content "C:\Users\$env:USERNAME\AppData\Local\Docker\log.log" -Tail 50

# Check disk space
Get-Volume
```

---

## 🎓 What WSL 2 Does

WSL 2 (Windows Subsystem for Linux 2) is:
- Lightweight Linux kernel running in Windows
- Provides `/` (root) filesystem access
- Enables Docker to run containers
- ~100-150 MB footprint
- Runs in background (minimal resource usage when idle)

---

**Status**: WSL 2 missing - need to install  
**Time Required**: 10-15 minutes  
**Difficulty**: Easy (3 commands + 1 restart)  
**Result**: Docker will work perfectly after!

---

## 🚀 GO DO THIS NOW

1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart computer
4. Then Docker will work!

That's it! 🎉
