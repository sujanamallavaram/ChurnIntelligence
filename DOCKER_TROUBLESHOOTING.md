# Docker Desktop Troubleshooting

**Error**: "Docker Desktop is unable to start"

This guide will help you diagnose and fix the issue.

---

## 🔍 Step 1: Check System Requirements

### Verify Windows Version
```powershell
# Check Windows version
[System.Environment]::OSVersion.VersionString

# Should show: Windows 10 (Build 19041+) or Windows 11
```

### Check Virtualization is Enabled
```powershell
# Check if Hyper-V is available
Get-ComputerInfo | Select-Object HyperVRequirementProductionLive

# Should show: True
```

### If Hyper-V is Disabled:

**Option A: Enable Hyper-V (Recommended)**
```powershell
# Run as Administrator:
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Restart when prompted
```

**Option B: Use WSL 2 Backend (Alternative)**
```powershell
# Install WSL 2
wsl --install

# Restart computer
# Then enable WSL 2 as Docker backend in Docker settings
```

---

## 🛠️ Step 2: Repair Docker Desktop

### Option 1: Clean Restart

```powershell
# Run as Administrator:

# 1. Stop Docker completely
docker system prune -a --volumes -f

# 2. Uninstall Docker
# Settings → Apps → Apps & features
# Search "Docker" → Uninstall → Follow prompts
# Restart computer

# 3. Reinstall Docker
# Download from: https://www.docker.com/products/docker-desktop
# Run installer
# Restart again
```

### Option 2: Reset Docker to Factory Settings

```powershell
# 1. Right-click Docker icon in system tray
# 2. Click "Settings"
# 3. Click "Troubleshoot" (bottom of window)
# 4. Click "Reset to factory defaults"
# 5. Wait 2-3 minutes
# 6. Docker will restart automatically
```

### Option 3: Check Docker Service

```powershell
# Run as Administrator:

# Check if Docker service exists
Get-Service | Where-Object {$_.Name -like "*docker*"}

# Check Docker Desktop processes
Get-Process | Where-Object {$_.Name -like "*Docker*"}

# View Docker service status
Get-Service "Docker" -ErrorAction SilentlyContinue

# If service stopped, start it:
Start-Service Docker -ErrorAction SilentlyContinue
```

---

## 🔧 Step 3: Check System Resources

### Verify Free Disk Space
```powershell
# Check disk space
Get-Volume | Select-Object DriveLetter, SizeRemaining, Size

# Docker needs at least 2-5 GB free
# If less than 2 GB free:
#   1. Delete temporary files
#   2. Empty Recycle Bin
#   3. Uninstall unused programs
```

### Check Available Memory
```powershell
# Check RAM
Get-ComputerInfo | Select-Object CsTotalPhysicalMemory

# Should be at least 4 GB total
# Docker default allocation: 2 GB (can be increased in settings)
```

### Check CPU Support
```powershell
# Check for virtualization extensions
Get-WmiObject Win32_Processor | Select-Object Name, VirtualizationFirmwareEnabled

# Should show: VirtualizationFirmwareEnabled = True
```

---

## 📋 Step 4: Check Docker Configuration

### Verify Docker Settings

1. **Right-click Docker icon** → Settings
2. **General Tab:**
   - [ ] "Start Docker Desktop when you log in" - CHECK THIS
   - [ ] "Use the WSL 2 based engine" - RECOMMENDED
   - [ ] "Expose daemon on tcp://localhost:2375 without TLS" - UNCHECK

3. **Resources Tab:**
   - Memory: 2-4 GB (not more than half your total RAM)
   - CPUs: 2-4 cores (not more than half your total CPUs)
   - Disk Image size: 10-20 GB (must have space available)

4. **Advanced Tab:**
   - Check "Use new virtualization framework" if available

5. **Click Apply and Restart**

---

## 🔌 Step 5: Check Network Issues

### Verify Network Connectivity
```powershell
# Test connection to Docker registry
Test-NetConnection docker.io -Port 443

# Should show: TcpTestSucceeded = True
```

### Check Proxy Settings
```powershell
# If behind corporate proxy:
# Docker Settings → Resources → Proxies
# Configure HTTP/HTTPS proxy if needed
```

### Disable VPN (Temporary Test)
```
1. Disconnect from any VPN
2. Try starting Docker again
3. If works → VPN/Network issue
4. Reconnect to VPN after testing
```

---

## 🚨 Step 6: Check for Conflicts

### Port Conflicts
```powershell
# Check if ports are in use
netstat -ano | findstr :2375
netstat -ano | findstr :8501

# If ports are in use by other processes:
# Stop those processes or use different ports
```

### Antivirus/Firewall Issues
```
1. Temporarily disable antivirus
2. Try starting Docker
3. If works → Antivirus blocking Docker
4. Add Docker to antivirus whitelist:
   C:\Program Files\Docker\Docker\Docker.exe
   C:\Program Files\Docker\Docker\com.docker.service
```

### WSL 2 Issues
```powershell
# Check WSL status
wsl --list --verbose

# If issues:
# 1. Restart WSL:
wsl --shutdown

# 2. Check for WSL 2 kernel update needed
# Windows Update → Check for updates
# Look for "WSL 2 Linux kernel" update

# 3. Or manually update:
wsl --install
```

---

## 📊 Step 7: Check Logs

### View Docker Desktop Logs
```powershell
# Docker stores logs here:
"C:\Users\[YourUsername]\AppData\Local\Docker\log.log"

# View recent logs:
Get-Content "C:\Users\$env:USERNAME\AppData\Local\Docker\log.log" -Tail 50

# Look for error messages to diagnose issue
```

### Check System Event Viewer
```powershell
# Open Event Viewer:
eventvwr.msc

# Go to: Windows Logs → Application
# Look for Docker errors
# Check System logs for virtualization issues
```

---

## ✅ Step 8: Verify Fix

### Test Docker Again
```powershell
# Test basic commands
docker --version
docker ps
docker images
docker run hello-world

# If all work without errors → Docker is fixed!
```

---

## 🆘 If Nothing Works - Alternative Solutions

### Option A: Use Docker via WSL 2 Terminal

```powershell
# Install WSL 2 with Docker
wsl --install
wsl --install docker

# Run commands in WSL terminal:
wsl
docker ps
```

### Option B: Use Streamlit Without Docker

Since you already have Streamlit installed locally:

```powershell
cd C:\Sujana\project1
streamlit run app.py

# Access at: http://localhost:8501
```

**Advantages:**
- No Docker needed
- Same result (dashboard runs)
- Faster for development

**Disadvantages:**
- Not containerized
- Environment tied to your system
- More difficult to deploy

### Option C: Use Container Alternative

If Docker won't work, consider:
- **Podman** (Docker alternative, lighter weight)
- **Container solutions via cloud** (if you want containerization)
- **Direct Python execution** (simplest, already works)

---

## 📞 When to Seek Help

If you've tried all steps above, Docker might have a deeper issue. Consider:

1. **Check Docker forums:**
   - https://github.com/docker/for-win/issues

2. **Contact Docker support:**
   - https://www.docker.com/contact/

3. **Use alternative approach:**
   - Run Streamlit directly without Docker
   - Use cloud services for containerization

---

## ⚡ Quick Summary

**If Docker won't start:**

1. ✅ Check Windows version (10 or 11)
2. ✅ Enable Hyper-V or WSL 2
3. ✅ Free up disk space (2-5 GB)
4. ✅ Reset Docker to factory defaults
5. ✅ Check antivirus/firewall
6. ✅ Update WSL 2 kernel
7. ✅ View Docker logs for errors
8. ✅ If all else fails: Use Streamlit without Docker

---

## 🎯 Recommended Path Forward

**Given current issues, I recommend:**

```
1. Try Reset Docker to Factory Defaults (Option 2 above)
2. Wait 3-5 minutes for reset
3. Test: docker ps
4. If still fails → Use Streamlit directly
5. If needed later → Docker can be reinstalled
```

**For now, your dashboard works perfectly with:**
```powershell
cd C:\Sujana\project1
streamlit run app.py
```

This gives you the same result without Docker complexity!

---

**Status**: Troubleshooting guide provided  
**Alternative**: Streamlit without Docker ready to use  
**Next Step**: Try one of the solutions above or use Streamlit directly
