# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0](https://github.com/nitinnbisht/pre-commit-dir-checker/compare/v0.1.0...v0.2.0) (2025-08-01)


### Features

* Initial release of dir-checker ([#1](https://github.com/nitinnbisht/pre-commit-dir-checker/issues/1)) ([78ad02d](https://github.com/nitinnbisht/pre-commit-dir-checker/commit/78ad02d79cb62c5c39051c34f0bbe7262893a6ad))


### Bug Fixes

* update release type to simple and enable skip labeling ([be5c9b5](https://github.com/nitinnbisht/pre-commit-dir-checker/commit/be5c9b531f795904e14d20cdb6ac77aa32e512b4))

## 1.0.0 (2025-08-01)


### Features

* Initial release of dir-checker ([#1](https://github.com/nitinnbisht/pre-commit-dir-checker/issues/1)) ([78ad02d](https://github.com/nitinnbisht/pre-commit-dir-checker/commit/78ad02d79cb62c5c39051c34f0bbe7262893a6ad))


### Bug Fixes

* update release type to simple and enable skip labeling ([be5c9b5](https://github.com/nitinnbisht/pre-commit-dir-checker/commit/be5c9b531f795904e14d20cdb6ac77aa32e512b4))

## [Unreleased]

## [1.0.0] - 2025-08-01

### Added
- **Comprehensive Directory Structure Validator**: Complete rewrite with advanced validation capabilities
- **Configurable Multi-Level Hierarchies**: Define and validate complex directory structures (environment/service/region/component)
- **Pattern Matching Support**: Wildcard (`*`) and prefix matching (`prefix*`) for directory names
- **Mandatory File Validation**: Ensure required files exist in component directories
- **Optional File Tracking**: Report missing recommended files as warnings
- **Flexible Configuration System**: Support for YAML and JSON configuration files
- **Custom YAML Parser**: Built-in YAML parsing without external dependencies
- **Gitignore Integration**: Respect `.gitignore` patterns during validation
- **Rich Output System**: Colored terminal output with multiple message levels
- **Configurable Log Levels**: Control output verbosity (error/warn/info)
- **Strict Mode**: Option to fail on warnings as well as errors
- **Depth Control**: Configure maximum directory depth validation
- **Skip Patterns**: Define directories and files to skip during validation
- **Statistics Reporting**: Detailed validation statistics and summaries

### Configuration Features
- **Root Directory Configuration**: Specify which directory to validate
- **Level Definitions**: Define ordered directory hierarchy levels
- **Valid Values per Level**: Specify allowed values for each directory level
- **File Requirements**: Configure mandatory and optional files
- **Validation Behavior**: Control when to fail vs. warn
- **Output Control**: Configure logging and display preferences

### Command Line Interface
- `--config` - Specify custom configuration file
- `--verbose` - Enable detailed output
- `--strict` - Fail on warnings as well as errors
- `--log-level` - Set output verbosity (error/warn/info)
- `--create-config` - Generate default configuration file
- `--debug-config` - Debug configuration parsing

### Integration Features
- **Pre-commit Hook Integration**: Seamless integration with pre-commit framework
- **GitHub Actions Support**: CI/CD workflow examples
- **No External Dependencies**: Uses only Python standard library
- **Cross-platform Support**: Works on Linux, macOS, and Windows
- **Python 3.6+ Compatibility**: Supports wide range of Python versions

### Use Cases
- Infrastructure as Code repositories (Terraform, AWS, etc.)
- Multi-environment codebases (dev/staging/prod)
- Component-based architectures
- Enterprise repositories with compliance requirements
- Microservices directory organization
- Project structure standardization

### Example Supported Structures
```
live/
├── dev/networking/eu-central-1/vpc/
├── prod/compute/us-east-1/ec2/
└── staging/storage/global/s3/
```

### Breaking Changes
- Complete rewrite from original simple directory checker
- New configuration file format required
- Different command-line arguments
- Enhanced validation logic

[Unreleased]: https://github.com/nitinnbisht/dir-checker/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nitinnbisht/dir-checker/releases/tag/v1.0.0
