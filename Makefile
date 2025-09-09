# Define the VM name and paths
VM_NAME = default
VM_WORKDIR = /home/vagrant/app
SERVICE_NAME = kali_terminal
HOST = 0.0.0.0
PORT = 8000

# Start the Vagrant VM and provision it
mcpserver_start:
	@echo "Starting the Vagrant VM..."
	vagrant up

	@echo "Copying file to the VM..."
	vagrant scp -r ./tools $(VM_NAME):$(VM_WORKDIR)/tools
	vagrant scp ./pyproject.toml $(VM_NAME):$(VM_WORKDIR)/
	vagrant scp ./mcpserver.py $(VM_NAME):$(VM_WORKDIR)/

	@echo "Starting the service on the VM..."
	vagrant ssh -c "cd $(VM_WORKDIR) && uv run mcpserver.py $(SERVICE_NAME) $(HOST):$(PORT)"

	@echo "Service $(SERVICE_NAME) started successfully."


# Stop the VM
mcpserver_stop:
	@echo "Stopping the Vagrant VM..."
	vagrant halt

	@echo "Vagrant VM stopped."

