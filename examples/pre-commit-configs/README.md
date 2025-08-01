# Pre-commit Hook Configurations

These files show **how to configure the pre-commit hook** in your `.pre-commit-config.yaml`. They demonstrate different ways to use the directory checker with various options.

## How to Use

1. **Copy** the contents of one of these files into your `.pre-commit-config.yaml`
2. **Adjust** the `--config` path to point to your directory checker configuration
3. **Customize** the arguments as needed

## Available Configurations

- **`simple.yaml`** - Minimal configuration, uses default settings
- **`basic-config.yaml`** - Custom config file with verbose output  
- **`web-development.yaml`** - Configured for React/Node.js projects
- **`terraform-infrastructure.yaml`** - Strict validation for infrastructure
- **`advanced-config.yaml`** - Full options for microservices
- **`minimal-output.yaml`** - Shows only errors, quiet output

## Command Line Arguments

Common arguments you can use:

- `--config=path/to/config.yaml` - Specify directory checker configuration
- `--verbose` - Show detailed output
- `--strict` - Fail on warnings as well as errors
- `--log-level=error|warn|info` - Control output verbosity

## Example Usage

Copy one of these configurations and paste into your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/nitinnbisht/dir-checker
    rev: v1.0.0
    hooks:
      - id: dir-checker
        args:
          - --config=examples/directory-configs/web-development-config.yaml
          - --verbose
```
