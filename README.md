# TF Module Instance Generator

A tool for creating an instance of a Terraform module from the variables.tf file.

## Usage

```bash
docker run -v $(pwd):/data tf-module-instance:main /data/variables.tf MODULE_INSTANCE_NAME PATH_TO_MODULE_SOURCE
```

- `MODULE_INSTANCE_NAME`  : The name of the module instance to be used in the output
- `PATH_TO_MODULE_SOURCE` : The path to the module source to be used in the output

## Example

```bash
docker run -v $(pwd):/data tf-module-instance:main /data/variables.tf vpc "./modules/vpc" > main.tf
```