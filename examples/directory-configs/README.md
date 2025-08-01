# Directory Checker Configurations

These files define **validation rules** for your directory structure. They configure:

- Which directory hierarchy to validate
- What files must/should exist in components  
- Valid names for each directory level
- Validation behavior and output settings

## How to Use

1. **Copy** one of these files to your repository root as `dir-checker-config.yaml`
2. **Customize** the values to match your project structure
3. **Reference** it in your `.pre-commit-config.yaml` (see `../pre-commit-configs/`)

## Available Configurations

- **`generic-project-config.yaml`** - General web development projects
- **`terraform-infrastructure-config.yaml`** - Infrastructure as Code for Terraform mono-repos

## Creating Your Own

Use the `--create-config` command to generate a generic template:

```bash
python -m dir_checker --create-config
```

This creates a `dir-checker-config.yaml` with helpful comments and generic examples.
