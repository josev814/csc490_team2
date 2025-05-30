# Stock Trading Strategies
This project started as a senior project from UNCFSU for csc490

# Local Requirements
- WSL2
- (Docker)[https://www.docker.com/get-started/]

# Optional Requirements
- (K3d)[https://k3d.io/stable/#requirements]
- (kubectl)[https://kubernetes.io/docs/tasks/tools/#kubectl]
- (Terraform)[https://developer.hashicorp.com/terraform/tutorials/docker-get-started/install-cli]
- (Helm)[https://helm.sh/docs/intro/install/]


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

_This will replace the Docker Compose setup_

## Windows
Run Powershell as an administrator
```pwsh
choco install terraform
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
kubectl create namespace csc490-stocks
```

# Django
## Check Program Status
Run the command below to check the status of program ran by supervisord

```bash
docker exec -it stocks_backend bash -c '${VENV_PATH}/bin/supervisorctl -c ${SUPERVISOR_CONFIG} status'
```

Additional command can be ran such as restarting a program and reloading it.

[Supervisorctl Actions](https://supervisord.org/running.html#supervisorctl-actions)

## Endpoints
Run the commands below to view the endpoints available for React to use

```bash
docker exec -it stocks_backend bash
source /var/local/bin/stocks_venv/bin/activate;
python manage.py show_urls | grep -vP "^/admin"
```

# Acknowledgements
Dr. Jin - UNCFSU Project Advisor
Jose' Vargas - Lead Dev
Stathis Jones - Backend Dev
Caileb Carter - Fronend Dev
