# Example Configurations

This directory contains example configurations organized into two categories:

## 📁 Directory Structure

```
examples/
├── directory-configs/          # Directory checker configuration files (YAML/JSON)
│   ├── generic-project-config.yaml
│   ├── web-development-config.yaml
│   ├── terraform-infrastructure-config.yaml
│   └── microservices-config.yaml
├── pre-commit-configs/         # Pre-commit hook configuration files
│   ├── simple.yaml
│   ├── basic-config.yaml
│   ├── advanced-config.yaml
│   ├── web-development.yaml
│   ├── terraform-infrastructure.yaml
│   └── minimal-output.yaml
└── README.md
```

## 🔧 Directory Checker Configurations (`directory-configs/`)

These files configure **how the directory structure validator works** - they define the validation rules, required files, and directory hierarchy.

### Available Directory Configurations

#### 1. Generic Project Configuration
**File:** `directory-configs/generic-project-config.yaml`  
**Use case:** General-purpose project structure for web applications

```yaml
root_dir: "src"
levels: ["module", "service", "component"]
valid_values:
  module: ["frontend", "backend", "shared", "common"]
  service: ["api", "web", "worker", "database", "cache"]
mandatory_files: ["package.json", "index.js"]
```

#### 2. Web Development Configuration  
**File:** `directory-configs/web-development-config.yaml`  
**Use case:** React/Node.js projects with frontend/backend separation

```yaml
root_dir: "src"
levels: ["tier", "module", "component"] 
valid_values:
  tier: ["frontend", "backend", "shared"]
  module: ["auth", "user", "dashboard", "api", "utils"]
mandatory_files: ["index.js", "package.json"]
```

#### 3. Terraform Infrastructure Configuration
**File:** `directory-configs/terraform-infrastructure-config.yaml`  
**Use case:** Infrastructure as Code repositories

```yaml
root_dir: "live"
levels: ["environment", "service", "region", "component"]
valid_values:
  environment: ["dev", "prd", "sandbox*"]
  service: ["networking", "compute", "storage", "security"]
mandatory_files: ["backend.tf", "versions.tf"]
```

#### 4. Microservices Configuration
**File:** `directory-configs/microservices-config.yaml`  
**Use case:** Domain-driven microservices architecture

```yaml
root_dir: "services"
levels: ["domain", "service", "environment"]
valid_values:
  domain: ["user-management", "payment", "order-processing"]
  service: ["api", "worker", "database"]
mandatory_files: ["Dockerfile", "docker-compose.yml"]
```

## 🪝 Pre-commit Hook Configurations (`pre-commit-configs/`)

These files configure **how to use the pre-commit hook** in your `.pre-commit-config.yaml` - they reference the directory configurations above.

### Available Pre-commit Configurations

#### 1. Simple Configuration
**File:** `pre-commit-configs/simple.yaml`  
**Description:** Uses default settings, expects `dir-checker-config.yaml` in repository root

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
```

#### 2. Basic Configuration
**File:** `pre-commit-configs/basic-config.yaml`  
**Description:** Uses custom config file with verbose output

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
        args:
          - --config=dir-checker-config.yaml
          - --verbose
```

#### 3. Web Development Configuration
**File:** `pre-commit-configs/web-development.yaml`  
**Description:** Configured for React/Node.js projects

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
        args:
          - --config=examples/directory-configs/web-development-config.yaml
          - --verbose
```

#### 4. Terraform Infrastructure Configuration
**File:** `pre-commit-configs/terraform-infrastructure.yaml`  
**Description:** Strict validation for infrastructure repositories

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
        args:
          - --config=examples/directory-configs/terraform-infrastructure-config.yaml
          - --strict
          - --log-level=warn
```

#### 5. Advanced Configuration
**File:** `pre-commit-configs/advanced-config.yaml`  
**Description:** Strict validation with detailed logging for microservices

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
        args:
          - --config=examples/directory-configs/microservices-config.yaml
          - --strict
          - --verbose
          - --log-level=info
```

#### 6. Minimal Output Configuration
**File:** `pre-commit-configs/minimal-output.yaml`  
**Description:** Shows only errors, suppresses warnings and info

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0
    hooks:
      - id: directory-checker
        args:
          - --config=examples/directory-configs/generic-project-config.yaml
          - --log-level=error
```

## Command Line Usage Examples

```bash
# Create a default configuration file
python -m dir_checker --create-config

# Use a specific example configuration
# Use a specific example configuration
python -m dir_checker --config examples/directory-configs/generic-project-config.yaml

# Use with terraform infrastructure config
python -m dir_checker --config examples/directory-configs/terraform-infrastructure-config.yaml --verbose

# Use with verbose output
python -m pre_commit_hooks.directory_checker --config examples/directory-configs/generic-project-config.yaml --verbose

# Use in strict mode (fail on warnings)
python -m pre_commit_hooks.directory_checker --config examples/directory-configs/microservices-config.yaml --strict

# Debug configuration parsing
python -m pre_commit_hooks.directory_checker --config examples/directory-configs/terraform-infrastructure-config.yaml --debug-config

# Combine multiple options
python -m pre_commit_hooks.directory_checker \
  --config examples/directory-configs/web-development-config.yaml \
  --verbose \
  --strict \
  --log-level info
```

## Example Directory Structures

### Web Development Structure (web-development-config.yaml)
```
src/
├── frontend/
│   ├── auth/
│   │   └── login-component/
│   │       ├── package.json
│   │       └── index.js
│   └── dashboard/
│       └── charts-component/
├── backend/
│   ├── api/
│   │   └── users-service/
│   └── utils/
│       └── helpers/
└── shared/
    └── components/
        └── ui-library/
```

### Microservices Structure (microservices-config.yaml)
```
services/
├── user-management/
│   ├── api/
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── worker/
│       ├── dev/
│       └── prod/
├── payment/
│   ├── api/
│   └── database/
└── order-processing/
    ├── api/
    └── worker/
```

### Infrastructure Structure (terraform-infrastructure-config.yaml)
```
live/
├── dev/
│   ├── networking/
│   │   ├── eu-central-1/
│   │   │   └── vpc/
│   │   │       ├── backend.tf
│   │   │       └── versions.tf
│   │   └── us-east-1/
│   └── compute/
│       └── eu-central-1/
│           └── ec2/
├── staging/
└── prod/
```

## Integration Examples

### With GitHub Actions
```yaml
# .github/workflows/structure-check.yml
name: Structure Check
on: [push, pull_request]

jobs:
  check-structure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install pre-commit
      - name: Run structure check
        run: |
          pre-commit run directory-checker --all-files
```

### With GitLab CI
```yaml
# .gitlab-ci.yml
structure-check:
  stage: test
  image: python:3.9
  script:
    - pip install pre-commit
    - pre-commit run directory-checker --all-files
```
