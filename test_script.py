import unittest
import os
import tempfile
from script import (
    parse_terraform_variable,
    parse_variables_file,
    generate_module_instance,
)


class TestTerraformModuleGenerator(unittest.TestCase):

    def test_parse_terraform_variable_with_string_type(self):
        var_block = """variable "vpc_id" {
  type = string
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "vpc_id")
        self.assertEqual(default, None)

    def test_parse_terraform_variable_with_string_default(self):
        var_block = """variable "region" {
  type    = string
  default = "us-west-2"
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "region")
        self.assertEqual(default, '"us-west-2"')

    def test_parse_terraform_variable_with_number_type(self):
        var_block = """variable "count" {
  type    = number
  default = 2
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "count")
        self.assertEqual(default, "2")

    def test_parse_terraform_variable_with_map_type(self):
        var_block = """variable "tags" {
  type    = map(any)
  default = {}
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "tags")
        self.assertEqual(default, "{}")

    def test_parse_terraform_variable_with_description(self):
        var_block = """variable "vpc_id" {
  type        = string
  description = "The VPC ID to use"
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "vpc_id")
        self.assertEqual(default, None)

    def test_parse_variables_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp.write(
                """
variable "vpc_id" {
  type = string
}
variable "public_subnet_tag" {
  type    = string
  default = "Name"
}
variable "subnets_desired_count" {
  type    = number
  default = 2
}
variable "tags" {
  type        = map(any)
  default     = {}
  description = "A map of tags to assign"
}
"""
            )
            temp_filename = temp.name

        try:
            variables = parse_variables_file(temp_filename)
            self.assertEqual(len(variables), 4)
            self.assertEqual(variables["vpc_id"], None)
            self.assertEqual(variables["public_subnet_tag"], '"Name"')
            self.assertEqual(variables["subnets_desired_count"], "2")
            self.assertEqual(variables["tags"], "{}")
        finally:
            os.unlink(temp_filename)

    def test_generate_module_instance(self):
        variables = {
            "vpc_id": None,
            "public_subnet_tag": '"Name"',
            "subnets_desired_count": "2",
            "tags": "{}",
        }

        expected_output = """module "test_module" {
  source = "test/path"
  vpc_id = "" # Needs to be defined
  public_subnet_tag = "Name"
  subnets_desired_count = 2
  tags = {}
}"""

        module_instance = generate_module_instance(
            variables, "test_module", "test/path"
        )
        self.assertEqual(module_instance, expected_output)

    def test_parse_terraform_variable_with_boolean_type(self):
        var_block = """variable "enable_nat_gateway" {
  type    = bool
  default = true
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "enable_nat_gateway")
        self.assertEqual(default, "true")

    def test_parse_terraform_variable_with_list_type(self):
        var_block = """variable "availability_zones" {
  type    = list(string)
  default = ["us-west-2a", "us-west-2b"]
}"""
        name, default = parse_terraform_variable(var_block)
        self.assertEqual(name, "availability_zones")
        self.assertEqual(default, '["us-west-2a", "us-west-2b"]')


if __name__ == "__main__":
    unittest.main()
