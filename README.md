# csc490_team2

# Local Requirements
- WSL2
- Docker
- Terraform
- Python 3


# Containers
- Nginx
  - This serves the requests between the client and our React application
- ReactJS
  - This is the front-end of the application.
    - To make react reflect changes run `docker compose -f "BuildTools/docker-compose.yml" restart frontend`
- Django
  - This is our backend framework
- Mysql
  - The database where all of our data is stored


# The Docker application
We use docker compose to build app image and to link the app to mariadb.

## Configuration
Under the Build directory copy the envvars.example and name it .envvars
Edit the .envvars to have the database creds you want for the db

## Standing up the application
**IN WSL**
```bash
bash setup_containers.sh teardown cleanup standup
```

or

```bash
docker compose -f BuildTools/docker-compose.yml up -d --build --remove-orphans
```

or

```bash
docker-compose -f BuildTools/docker-compose.yml build --no-cache && docker compose -f BuildTools/docker-compose.yml up -d
```
### The used flags
- -f
  - Defines where the compose file is
- --build
  - Builds images before starting containers
- --remove-orphans
  - Removes containers for services not listed in the compose file for the project

### additional build options for docker
- --force-create
  - this allows us to force recreating of the images
- --no-cache
  - do not use any cache when building the images
- --always-recreate-deps
  - this allows to recreate the dependent containers


## Teardown the application
```bash
docker compose -f "BuildTools/docker-compose.yml" down --volumes --remove-orphans
```
- (--volumes|-v)
  - Removes named and anonymous volumes pertaining to the service
- --rmi (local|all)
  - Removes the images used for the application



# Install Terraform
## Windows
```pwsh
https://releases.hashicorp.com/terraform/1.7.2/terraform_1.7.2_windows_amd64.zip
```

# Install kubectl and az-cli
Enable Kubernetes within Docker Desktop's settings first

Run Powershell as an administrator

Run this powershell command and when prompted enter A to accept all prompts
```pwsh
choco install azure-cli kubernetes-cli
```

Verify the installation
```pwsh
kubectl version
kubctl cluster-info
```

The cluster information should have a Kubernetes control plane and Core DNS with a url containing `kubernetes.docker.internal`

# Setup Kubernetes Pods
```pwsh
kubectl create naespace csc490-stocks
```
