variable "azure_region" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "task-manager"
}

variable "environment" {
  description = "Environment label (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "node_count" {
  description = "Number of AKS worker nodes"
  type        = number
  default     = 2
}

variable "node_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_B2s"
}

variable "container_port" {
  description = "Port exposed by the FastAPI backend container"
  type        = number
  default     = 8000
}
