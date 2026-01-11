variable "app_name" {
  description = "The name of the application."
  type        = string
  default     = "iris-api"
}

variable "replica_count" {
  description = "The number of replicas for the application."
  type        = number
  default     = 5
}

variable "image" {
  description = "Which image to use for the application."
  type        = string
  default     = "iris-api:latest"
}

variable "namespace" {
  description = "The Kubernetes namespace to deploy the application."
  type        = string
  default     = "default"
}
