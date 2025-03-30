variable "vpc_id" {
  type = string
}

variable "public_subnet_tag" {
  type    = string
  default = "Name"
}

variable "private_subnet_tag" {
  type    = string
  default = "Name"
}

variable "public_subnet_regex" {
  type    = string
  default = "Public"
}

variable "private_subnet_regex" {
  type    = string
  default = "Private"
}

variable "tags" {
  type        = map(any)
  default     = {}
  description = "A map of tags to assign"
}

variable "subnets_desired_count" {
  type    = number
  default = 2
}
