variable "gcp_project_id" {
  type        = string
  description = "The GCP project ID to apply this config to"
}

variable "region" {
  type        = string
  description = "Region of the VM"
  default     = "[NON_CRITICAL_APP_REGION]"
}

variable "zone" {
  type        = string
  description = "Zone of the VM"
  default     = "[NON_CRITICAL_APP_ZONE]"
}
