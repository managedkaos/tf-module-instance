# TF Module Instance Generator

A tool for creating an instance of a Terraform module from the variables.tf file.

## Usage

```bash
docker run -v $(pwd):/data tf-module-instance:main /data/variables.tf MODULE_INSTANCE_NAME PATH_TO_MODULE_SOURCE
```

- `MODULE_INSTANCE_NAME`  : The name of the module instance to be used in the output
- `PATH_TO_MODULE_SOURCE` : The path to the module source to be used in the output

## Example

**Input**: `variables.tf`

```hcl
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
```


**Command**:

```bash
docker run -v $(pwd):/data tf-module-instance:main /data/variables.tf vpc "./modules/vpc" | tee main.tf
```

**Output**: `main.tf`

```hcl
module "vpc" {
  source = "./modules/vpc"
  vpc_id = "" # Needs to be defined
  public_subnet_tag = "Name"
  private_subnet_tag = "Name"
  public_subnet_regex = "Public"
  private_subnet_regex = "Private"
  tags = {}
  subnets_desired_count = 2
}
```