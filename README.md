# Blog App – Agile & DevOps Project (24MIS0386)

Topic: **Blog**
- **v1** – Add Post
- **v2** – Add Post + Edit Post
- **v3** – Add Post + Edit Post + Delete Post

Tech: Python Flask · Git/GitHub · Jenkins · Docker · DockerHub · Kubernetes

```
blog-devops/
├── v1/   app.py, requirements.txt, Dockerfile
├── v2/   app.py, requirements.txt, Dockerfile
├── v3/   app.py, requirements.txt, Dockerfile
├── k8s/  blog-v1.yaml, blog-v2.yaml, blog-v3.yaml  (Deployment + Service each)
├── Jenkinsfile
└── README.md
```

| Version | Feature | URL |
|---|---|---|
| v1 | Add Post | http://localhost:8081 |
| v2 | Add + Edit | http://localhost:8082 |
| v3 | Add + Edit + Delete | http://localhost:8083 |

---

## What you need installed (Windows)
1. **VS Code**
2. **Git**
3. **Python 3** (only to test locally)
4. **Docker Desktop**, and in its Settings → Kubernetes → tick **Enable Kubernetes**
5. **Jenkins** (with Docker Desktop running on the same machine)
6. A **GitHub** account and a **DockerHub** account

> Replace `YOUR_DOCKERHUB_USERNAME` in **Jenkinsfile** and in the 3 files inside **k8s/** with your real DockerHub username.

---

## Step 1 – Open in VS Code and test locally
```bash
cd blog-devops
pip install flask
python v1/app.py      # open http://localhost:5000, Ctrl+C to stop
python v2/app.py
python v3/app.py
```

## Step 2 – Push to GitHub (separate commits for v1, v2, v3)
Create an empty repo on GitHub called `blog-devops`, then in the VS Code terminal:
```bash
git init
git branch -M main

git add .gitignore .dockerignore v1 README.md
git commit -m "v1: Add Post feature"
git tag v1

git add v2
git commit -m "v2: Edit Post feature"
git tag v2

git add v3 k8s Jenkinsfile
git commit -m "v3: Delete Post feature + Jenkins + Kubernetes"
git tag v3

git remote add origin https://github.com/<your-github-username>/blog-devops.git
git push -u origin main --tags
```
If sir wants **branches** too, add them from the tags:
```bash
git branch version-1 v1
git branch version-2 v2
git branch version-3 v3
git push origin version-1 version-2 version-3
```

## Step 3 – Docker (manual check, before Jenkins)
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/blog-app:v1 v1
docker build -t YOUR_DOCKERHUB_USERNAME/blog-app:v2 v2
docker build -t YOUR_DOCKERHUB_USERNAME/blog-app:v3 v3
docker images
```

## Step 4 – Push to DockerHub
```bash
docker login
docker push YOUR_DOCKERHUB_USERNAME/blog-app:v1
docker push YOUR_DOCKERHUB_USERNAME/blog-app:v2
docker push YOUR_DOCKERHUB_USERNAME/blog-app:v3
```

## Step 5 – Jenkins pipeline
1. Open Jenkins (http://localhost:8080).
2. **Manage Jenkins → Credentials → (global) → Add Credentials**
   Kind: *Username with password* · Username: DockerHub username · Password: DockerHub password/access token · **ID: `dockerhub-creds`**
3. **New Item** → name `blog-pipeline` → **Pipeline** → OK.
4. Pipeline section → Definition: **Pipeline script from SCM** → SCM: **Git** → Repository URL: your GitHub repo → Branch: `*/main` → Script Path: `Jenkinsfile` → Save.
5. Click **Build Now**. Stages: Checkout → Build Docker Images → Push to DockerHub → Deploy to Kubernetes.

> If the Deploy stage says kubectl cannot connect, Jenkins is running as a different Windows user. Copy `C:\Users\<you>\.kube\config` to the Jenkins user's `.kube` folder, or just run Step 6 manually.

## Step 6 – Kubernetes (3 deployments + 3 services)
```bash
kubectl apply -f k8s/
kubectl get deployments
kubectl get pods
kubectl get services
```
On Docker Desktop, `LoadBalancer` services open on localhost directly:
- v1 → http://localhost:8081
- v2 → http://localhost:8082
- v3 → http://localhost:8083

If a page does not open (e.g. on Minikube), use port-forward in 3 terminals:
```bash
kubectl port-forward service/blog-v1-service 8081:8081
kubectl port-forward service/blog-v2-service 8082:8082
kubectl port-forward service/blog-v3-service 8083:8083
```

## Step 7 – Screenshots to take for submission
1. VS Code with the project open
2. GitHub repo showing the 3 commits / tags
3. Jenkins pipeline Stage View (all green)
4. `docker images` output
5. DockerHub repo showing tags v1, v2, v3
6. `kubectl get deployments` and `kubectl get services`
7. Browser: localhost:8081, 8082, 8083 side by side (v1 only Add, v2 has Edit, v3 has Edit + Delete)

## Clean up
```bash
kubectl delete -f k8s/
```
