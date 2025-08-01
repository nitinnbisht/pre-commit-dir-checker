# dir-checker

A powerful and configurable pre-commit hook for validating directory structure, enforcing naming conventions, and ensuring mandatory files exist in your repositories.

## Features

- **Configurable Directory Structure Validation**: Define multi-level directory hierarchies with validation rules
- **Mandatory File Checking**: Ensure required files exist in component directories
- **Optional File Reporting**: Track optional/recommended files
- **Pattern Matching**: Support for wildcards and glob patterns in directory names
- **Depth Control**: Configure maximum directory depth limits
- **Gitignore Integration**: Respect `.gitignore` patterns during validation
- **Flexible Configuration**: YAML or JSON configuration files
- **Rich Output**: Colored output with different log levels (error, warn, info)
- **Strict Mode**: Option to fail on warnings as well as errors
- **No External Dependencies**: Uses only Python standard library

## Use Cases

This tool is particularly useful for:
- **Web Development Projects** with frontend/backend separation
- **Microservices Architectures** requiring consistent organization
- **Infrastructure as Code repositories** with standardized directory structures
- **Multi-tier Applications** (frontend/backend/shared)
- **Component-based architectures** requiring consistent file organization
- **Enterprise repositories** with strict compliance requirements

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/nitinnbisht/dir-checker
    rev: v1.0.0  # Use the ref you want to point at
    hooks:
      - id: dir-checker
        args: 
          - --config=dir-checker-config.yaml
          - --verbose
```

## Configuration

The hook uses a configuration file to define validation rules. Create a `dir-checker-config.yaml` (or `.json`) file in your repository root:

```yaml
# Repository Structure Validation Configuration
# This is a generic example configuration. Customize it for your project:

root_dir: "src"

# Define the hierarchy levels in your project structure
levels:
  - "module"     # Top-level modules (frontend, backend, shared)
  - "service"    # Service types (api, web, worker, etc.)
  - "component"  # Individual components

max_depth: 3
check_depth: true
allow_subdirs: true
respect_gitignore: true

# Valid values for each level (customize for your project)
valid_values:
  module:
    - "frontend"
    - "backend"
    - "shared"
    - "common"
  service:
    - "api"
    - "web"
    - "worker"
    - "database"
    - "cache"
  component:
    - "*"  # Allow any component name

# Files that must exist in each component directory
mandatory_files:
  - "package.json"
  - "index.js"

# Files that are recommended but not required
optional_files:
  - "README.md"
  - "test.js"
  - "config.json"

# Directories to skip during validation
skip_dirs:
  - "node_modules"
  - "dist"
  - "build"
  - ".git"
  - "__pycache__"

# Validation settings
fail_on_missing_files: true
fail_on_invalid_structure: true
fail_on_invalid_values: false  # Only warn by default

# Logging settings
log_level: "warn"  # Options: "error", "warn", "info"
```

## Command Line Usage

```bash
# Create a default configuration file
python -m dir_checker --create-config

# Run with default config
python -m dir_checker

# Run with custom config
python -m dir_checker --config custom-config.yaml

# Verbose output
python -m dir_checker --verbose

# Strict mode (fail on warnings)
python -m dir_checker --strict

# Set log level
python -m dir_checker --log-level info

# Debug configuration
python -m dir_checker --debug-config
```

## Configuration Options

### Directory Structure

- **`root_dir`**: Root directory to validate (relative to repo root)
- **`levels`**: Ordered list of directory levels to validate
- **`max_depth`**: Maximum allowed directory depth
- **`check_depth`**: Enable/disable depth checking
- **`allow_subdirs`**: Allow subdirectories in component directories

### Validation Rules

- **`valid_values`**: Define allowed values for each directory level
  - Use `*` for wildcards (allow anything)
  - Use `prefix*` for prefix matching
  - Use exact strings for strict matching

### File Requirements

- **`mandatory_files`**: Files that must exist in component directories
- **`optional_files`**: Files to report if missing (warnings only)

### Behavior Control

- **`fail_on_missing_files`**: Fail build if mandatory files are missing
- **`fail_on_invalid_structure`**: Fail build on structure violations
- **`fail_on_invalid_values`**: Fail build on invalid directory names
- **`respect_gitignore`**: Honor .gitignore patterns
- **`skip_dirs`**: Directories to skip during validation
- **`log_level`**: Control output verbosity (error/warn/info)

## Example Configurations

This repository includes organized example configurations to get you started:

### Directory Structure
```
examples/
├── directory-configs/          # Directory validation configurations
│   ├── README.md              # Explains these config files
│   ├── generic-project-config.yaml
│   └── terraform-infrastructure-config.yaml
└── pre-commit-configs/        # Pre-commit hook configurations  
    ├── README.md              # Explains these config files
    ├── basic-config.yaml
    └── terraform-infrastructure.yaml
```

### Configuration Types

**Directory Configs (`examples/directory-configs/`)**: These are the actual validation rules that define your directory structure requirements. Use these with the `--config` argument:

```bash
python -m dir_checker --config examples/directory-configs/generic-project-config.yaml
```

**Pre-commit Configs (`examples/pre-commit-configs/`)**: These are `.pre-commit-config.yaml` files that show how to integrate the directory checker into your pre-commit setup:

```bash
# Copy one of these as your .pre-commit-config.yaml
cp examples/pre-commit-configs/basic-setup.yaml .pre-commit-config.yaml
```

## Examples

### Basic Web Application
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
```

### With Custom Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/nitinnbisht/dir-checker
    rev: v1.0.0
    hooks:
      - id: dir-checker
        args:
          - --config=examples/directory-configs/generic-project-config.yaml
          - --strict
          - --log-level=info
```

### Web Application Structure
```
src/
├── frontend/
│   ├── api/
│   │   └── auth-component/
│   │       ├── package.json     # ✅ Required
│   │       ├── index.js         # ✅ Required
│   │       ├── README.md        # ✅ Optional
│   │       └── test.js          # ✅ Optional
│   └── web/
│       └── dashboard-component/
├── backend/
│   └── api/
│       └── user-service/
└── shared/
    └── utils/
        └── common-helpers/
```

### Infrastructure/Terraform Structure
```
live/
├── dev/
│   ├── networking/
│   │   ├── eu-central-1/
│   │   │   └── vpc/
│   │   │       ├── backend.tf      # ✅ Required
│   │   │       ├── versions.tf     # ✅ Required
│   │   │       ├── main.tf         # ✅ Optional
│   │   │       └── variables.tf    # ✅ Optional
│   │   └── us-east-1/
│   │       └── vpc/
│   └── compute/
└── prod/
    └── networking/
```

## Output Examples

### Successful Validation
```
✅ Loaded configuration from: dir-checker-config.yaml

Repository Structure Validation Results
==================================================
Statistics:
   • Components found: 2
   • Directories scanned: 6
   • Files checked: 4

✅ All validations passed! Repository structure is compliant.
```

### Validation with Issues
```
❌ Loaded configuration from: dir-checker-config.yaml

Repository Structure Validation Results
==================================================
Statistics:
   • Components found: 1
   • Directories scanned: 4
   • Files checked: 2

Summary:
   • 1 error(s) - blocking issues
   • 1 optional file warning(s) - missing recommended files

Found 1 error(s):
   Error: Missing mandatory files: package.json: src/frontend/api/auth-component

Found 1 optional file warning(s):
   Warning: Missing optional files: README.md, test.js: src/frontend/api/auth-component

❌ Validation failed due to errors above.
```

## Development

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/nitinnbisht/dir-checker.git
cd dir-checker
```

2. Install in development mode:
```bash
pip install -e .
```

3. Create a test configuration:
```bash
python -m dir_checker --create-config
```

4. Run tests:
```bash
python -m pytest tests/
```

### Testing Your Configuration

```bash
# Test with your config
python -m dir_checker --config your-config.yaml --verbose

# Debug configuration parsing
python -m dir_checker --debug-config

# Run in strict mode
python -m dir_checker --strict
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release with comprehensive directory structure validation
- Configurable multi-level directory hierarchies
- Mandatory and optional file checking
- Pattern matching with wildcards
- Gitignore integration
- Rich colored output with multiple log levels
- YAML and JSON configuration support
- No external dependencies