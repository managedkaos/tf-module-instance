import re
import sys
import os.path


def parse_terraform_variable(var_block):
    """Parse a single Terraform variable block and extract its properties."""
    var_name = re.search(r'variable\s+"([^"]+)"', var_block).group(1)

    # Extract type
    type_match = re.search(r"type\s+=\s+([^\n]+)", var_block)
    var_type = type_match.group(1).strip() if type_match else None

    # Extract default value
    default_match = re.search(r"default\s+=\s+([^\n]+)", var_block)
    default_value = default_match.group(1).strip() if default_match else None

    # For map type with empty default, format properly
    if default_value == "{}":
        return var_name, default_value

    # Format default value based on type
    if default_value is not None:
        if var_type == "string":
            # Keep quotes for string values
            if not (default_value.startswith('"') and default_value.endswith('"')):
                default_value = f'"{default_value}"'
        elif var_type == "number":
            # Ensure numbers are formatted without quotes
            default_value = default_value.strip('"')

    return var_name, default_value


def parse_variables_file(file_path):
    """Parse a Terraform variables.tf file and extract all variables."""
    with open(file_path, "r") as f:
        content = f.read()

    # Extract all variable blocks
    var_blocks = re.findall(r'variable\s+"[^"]+"\s+\{[^}]+\}', content, re.DOTALL)

    variables = {}
    for block in var_blocks:
        name, default = parse_terraform_variable(block)
        variables[name] = default

    return variables


def generate_module_instance(variables, module_name="example", source_path=""):
    """Generate a Terraform module instance with the parsed variables."""
    module_lines = [f'module "{module_name}" {{']
    module_lines.append(f'  source = "{source_path}"')

    for name, default in variables.items():
        if default is None:
            module_lines.append(f'  {name} = "" # Needs to be defined')
        else:
            module_lines.append(f"  {name} = {default}")

    module_lines.append("}")

    return "\n".join(module_lines)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python script.py <path_to_variables.tf> [module_name] [source_path]"
        )
        sys.exit(1)

    variables_file = sys.argv[1]
    module_name = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.basename(os.path.dirname(variables_file))
    )
    source_path = sys.argv[3] if len(sys.argv) > 3 else ""

    if not os.path.exists(variables_file):
        print(f"Error: File {variables_file} not found")
        sys.exit(1)

    try:
        variables = parse_variables_file(variables_file)
        module_instance = generate_module_instance(variables, module_name, source_path)
        print(module_instance)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
