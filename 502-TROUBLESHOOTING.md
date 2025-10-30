# 🚨 502 Bad Gateway Troubleshooting Guide
## Dr. Kishan Bhalani Medical Documentation Services

### 🔍 **What is a 502 Bad Gateway Error?**

A 502 error means nginx (the ingress controller) cannot reach your backend service. The nginx proxy is working, but your application is not responding.

### 🎯 **Common Causes & Solutions**

#### **1. Server Not Binding to 0.0.0.0**
**Problem:** Server only binds to localhost/127.0.0.1
**Solution:** Ensure server binds to `0.0.0.0`

```python
# ❌ Wrong - only accessible from localhost
uvicorn.run(app, host="127.0.0.1", port=8000)

# ✅ Correct - accessible from all interfaces
uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### **2. Wrong Port Configuration**
**Problem:** Service expects different port than container exposes
**Solution:** Check port consistency

```yaml
# Container port
ports:
- containerPort: 8000

# Service port mapping
ports:
- port: 80
  targetPort: 8000  # Must match container port

# Environment variable
env:
- name: PORT
  value: "8000"  # Must match containerPort
```

#### **3. Health Check Failures**
**Problem:** Kubernetes kills pods due to failed health checks
**Solution:** Ensure health endpoints work

```bash
# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/healthz
curl http://localhost:8000/ready
```

#### **4. Application Startup Issues**
**Problem:** App crashes during startup
**Solution:** Check logs and fix import/dependency issues

```bash
# Check pod logs
kubectl logs -f deployment/dr-kishan-medical-services

# Check pod status
kubectl get pods -l app=dr-kishan-medical-services
```

### 🛠️ **Diagnostic Steps**

#### **Step 1: Check Pod Status**
```bash
kubectl get pods -l app=dr-kishan-medical-services
kubectl describe pod <pod-name>
```

**Look for:**
- Pod status: Should be `Running`
- Ready status: Should be `1/1`
- Restart count: Should be low

#### **Step 2: Check Pod Logs**
```bash
kubectl logs -f <pod-name>
```

**Look for:**
- Server startup messages
- Port binding confirmation
- Error messages
- Health check responses

#### **Step 3: Test Pod Directly**
```bash
# Port forward to test pod directly
kubectl port-forward <pod-name> 8000:8000

# Test in another terminal
curl http://localhost:8000/health
```

#### **Step 4: Check Service**
```bash
kubectl get svc dr-kishan-medical-services
kubectl describe svc dr-kishan-medical-services
```

**Verify:**
- Service has endpoints
- Port mapping is correct
- Selector matches pod labels

#### **Step 5: Check Ingress**
```bash
kubectl get ingress dr-kishan-medical-services
kubectl describe ingress dr-kishan-medical-services
```

**Verify:**
- Ingress has backend service
- Host configuration is correct
- SSL/TLS settings

### 🔧 **Quick Fixes**

#### **Fix 1: Use K8s-Optimized Server**
Replace your current startup command with:
```bash
python k8s_server.py
```

#### **Fix 2: Update Railway Configuration**
Update `railway.json`:
```json
{
  "deploy": {
    "startCommand": "python k8s_server.py"
  }
}
```

#### **Fix 3: Run Diagnostics**
```bash
# Run diagnostic tool
python k8s-diagnostic.py diagnose

# Or start with diagnostics
python k8s-diagnostic.py
```

### 📋 **Kubernetes Health Check Requirements**

Your application MUST:
1. ✅ Bind to `0.0.0.0` (not localhost)
2. ✅ Respond to health checks within timeout
3. ✅ Start within startup probe timeout
4. ✅ Not crash after startup
5. ✅ Handle graceful shutdown signals

### 🚀 **Recommended Configuration**

#### **Use This Server Configuration:**
```python
uvicorn.run(
    app,
    host="0.0.0.0",  # Critical for K8s
    port=int(os.environ.get("PORT", 8000)),
    timeout_keep_alive=30,
    timeout_graceful_shutdown=30
)
```

#### **Health Check Endpoints:**
```python
@app.get("/health")    # General health
@app.get("/healthz")   # K8s liveness
@app.get("/ready")     # K8s readiness  
@app.get("/alive")     # Simple liveness
```

#### **Kubernetes Probe Configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /alive
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5

startupProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  failureThreshold: 30
```

### 🔍 **Debug Commands**

```bash
# Check if pods are running
kubectl get pods

# Check pod logs
kubectl logs -f <pod-name>

# Check service endpoints
kubectl get endpoints

# Test service directly
kubectl run test-pod --image=curlimages/curl -it --rm -- /bin/sh
# Inside pod: curl http://dr-kishan-medical-services/health

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

### ✅ **Success Indicators**

When working correctly, you should see:
- ✅ Pods in `Running` state with `1/1` ready
- ✅ Service has endpoints listed
- ✅ Health checks return 200 OK
- ✅ No error logs in pod or ingress controller
- ✅ Application responds to direct curl tests

### 🆘 **Still Getting 502?**

1. **Use the K8s diagnostic server:** `python k8s_server.py`
2. **Check all health endpoints work**
3. **Verify port binding to 0.0.0.0**
4. **Test pod directly with port-forward**
5. **Check ingress controller logs**
6. **Verify service selector matches pod labels**

The 502 error will resolve once your application properly responds to health checks and binds to the correct interface! 🎯