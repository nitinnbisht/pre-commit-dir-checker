#!/usr/bin/env python3
"""
Directory Structure Validator
A configurable pre-commit hook for validating directory structure and mandatory files.

Usage:
    python3 ds-validator.py [--config CONFIG_FILE] [--verbose] [--strict]

Configuration:
    Can be configured via YAML or JSON file. YAML is preferred for readability.
    Default config file: dir-checker-config.yaml (falls back to dir-checker-config.json)
    
    No e        # Report missing optional files as OPTIONAL_WARNING
        if missing_optional_files:
            self.add_error(
                "OPTIONAL_WARNING",
                f"Missing optional files: {', '.join(missing_optional_files)}",
                component_path
            )
        
        # Add INFO message for successful file validation
        if present_files:
            self.add_error("INFO", f"Found required files: {', '.join(sorted(present_files))}", component_path)
        
        if self.verbose and present_files:
            self.log(f"Found files: {', '.join(sorted(present_files))} in {component_path}")pendencies required - YAML parsing uses bash-style approach
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Set, Any, Optional, List
from dataclasses import dataclass, field
import fnmatch

# Import json (always available) 
import json
import subprocess

def colorize(text: str, color: str) -> str:
    """Add ANSI color codes to text."""
    colors = {
        'red': '\033[31m',
        'yellow': '\033[33m',
        'green': '\033[32m',
        'blue': '\033[34m',
        'cyan': '\033[36m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

@dataclass
class StructureConfig:
    """Configuration for repository structure validation."""
    
    # Root directory to validate (relative to repo root)
    root_dir: str = "src"
    
    # Directory structure levels (ordered list)
    levels: List[str] = field(default_factory=lambda: ["module", "service", "component"])
    
    # Maximum depth allowed (set to 0 to disable depth checking)
    max_depth: int = 3
    
    # Check depth limits
    check_depth: bool = False
    
    # Allow subdirectories in components
    allow_subdirs: bool = True
    
    # Respect .gitignore patterns
    respect_gitignore: bool = True
    
    # Valid values for each level
    valid_values: Dict[str, List[str]] = field(default_factory=lambda: {
        "module": ["frontend", "backend", "shared", "common"],
        "service": ["api", "web", "worker", "database", "cache"],
        "component": ["*"]  # Allow any component name
    })
    
    # Mandatory files in each component directory
    mandatory_files: List[str] = field(default_factory=lambda: [
        "index.js", "package.json"
    ])
    
    # Optional files (for reporting)
    optional_files: List[str] = field(default_factory=lambda: [
        "README.md", "test.js", "config.json"
    ])
    
    # Directories to skip during validation
    skip_dirs: Set[str] = field(default_factory=lambda: {
        "node_modules", ".git", "__pycache__", 
        ".mypy_cache", ".pytest_cache", "dist", "build", "coverage"
    })
    
    # File patterns to skip
    skip_files: Set[str] = field(default_factory=lambda: {
        ".DS_Store", "*.log", "*.tmp"
    })
    
    # Validation settings
    fail_on_missing_files: bool = True
    fail_on_invalid_structure: bool = True
    fail_on_invalid_values: bool = False  # Only warn by default
    
    # Logging settings
    log_level: str = "warn"  # Options: "error", "warn", "info"
    verbose: bool = True

def parse_yaml_with_bash(file_path: str) -> Dict[str, Any]:
    """
    Parse simple YAML files using bash commands (like pre-commit-terraform does).
    This avoids the need for PyYAML dependency.
    """
    config_data: Dict[str, Any] = {}
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        current_key = None
        current_subkey = None
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
                
            # Calculate indentation level
            indent = len(line) - len(line.lstrip())
            
            if ':' in stripped and not stripped.startswith('-'):
                parts = stripped.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().strip('"\'')
                    value = parts[1].strip().strip('"\'')
                    
                    if indent == 0:  # Top level
                        current_key = key
                        current_subkey = None
                        if not value:  # This indicates a structure follows
                            config_data[key] = {}
                        else:
                            # Direct value assignment
                            if value.lower() in ['true', 'false']:
                                config_data[key] = value.lower() == 'true'
                            elif value.isdigit():
                                config_data[key] = int(value)
                            else:
                                config_data[key] = value
                                
                    elif indent == 2 and current_key:  # Second level
                        current_subkey = key
                        if current_key not in config_data:
                            config_data[current_key] = {}
                        if not value:  # Structure follows
                            if isinstance(config_data[current_key], dict):
                                config_data[current_key][current_subkey] = {}
                        else:
                            if isinstance(config_data[current_key], dict):
                                if value.lower() in ['true', 'false']:
                                    config_data[current_key][current_subkey] = value.lower() == 'true'
                                elif value.isdigit():
                                    config_data[current_key][current_subkey] = int(value)
                                else:
                                    config_data[current_key][current_subkey] = value
                                
                    elif indent == 4 and current_key and current_subkey:  # Third level
                        subsubkey = key
                        if isinstance(config_data[current_key], dict) and isinstance(config_data[current_key].get(current_subkey), dict):
                            if not value:
                                config_data[current_key][current_subkey][subsubkey] = []
                            else:
                                config_data[current_key][current_subkey][subsubkey] = value
                        
            elif stripped.startswith('-') and current_key:
                item = stripped[1:].strip().strip('"\'')
                if item:
                    if indent == 2:  # List under top-level key
                        if current_key not in config_data:
                            config_data[current_key] = []
                        elif not isinstance(config_data[current_key], list):
                            config_data[current_key] = []
                        config_data[current_key].append(item)
                        
                    elif indent == 4 and current_subkey:  # List under second-level key
                        if (isinstance(config_data.get(current_key), dict) and 
                            current_subkey in config_data[current_key]):
                            if not isinstance(config_data[current_key][current_subkey], list):
                                config_data[current_key][current_subkey] = []
                            config_data[current_key][current_subkey].append(item)
                        elif isinstance(config_data.get(current_key), dict):
                            config_data[current_key][current_subkey] = [item]
                            
                    elif indent == 6 and current_key and current_subkey:  # List under third-level key
                        # This is for special_patterns section
                        if (isinstance(config_data.get(current_key), dict) and
                            isinstance(config_data[current_key].get(current_subkey), dict)):
                            # Find the last subsubkey that was defined
                            last_subsubkey = None
                            for k in config_data[current_key][current_subkey]:
                                if isinstance(config_data[current_key][current_subkey][k], list) or \
                                   config_data[current_key][current_subkey][k] == []:
                                    last_subsubkey = k
                            
                            if last_subsubkey:
                                if not isinstance(config_data[current_key][current_subkey][last_subsubkey], list):
                                    config_data[current_key][current_subkey][last_subsubkey] = []
                                config_data[current_key][current_subkey][last_subsubkey].append(item)
        
        return config_data
        
    except Exception as e:
        print(f"⚠️  Failed to parse YAML file {file_path}: {e}")
        return {}

class ValidationError:
    def __init__(self, level: str, message: str, path: Optional[Path] = None):
        self.level = level  # ERROR, WARNING, INFO
        self.message = message
        self.path = path
    
    def __str__(self):
        if self.level == "ERROR":
            prefix = colorize("Error", 'red')
        elif self.level == "WARNING":
            prefix = colorize("Warning", 'yellow')
        elif self.level == "OPTIONAL_WARNING":
            prefix = colorize("Warning", 'yellow')
        else:  # INFO
            prefix = colorize("Info", 'blue')
        
        if self.path:
            return f"{prefix}: {self.message}: {self.path}"
        return f"{prefix}: {self.message}"

class RepositoryValidator:
    def __init__(self, config: StructureConfig, verbose: bool = False, strict: bool = False):
        self.config = config
        self.verbose = verbose
        self.strict = strict
        self.errors: List[ValidationError] = []
        self.gitignore_patterns: List[str] = []
        self.stats = {
            "components_found": 0,
            "directories_scanned": 0,
            "files_checked": 0
        }
        
        # Define log level hierarchy
        self.log_levels = {"error": 0, "warn": 1, "info": 2}
        self.current_log_level = self.log_levels.get(config.log_level.lower(), 1)
        
        # Initialize after setup
        self.__post_init__()
    
    def should_show_message(self, level: str) -> bool:
        """Check if a message of given level should be shown based on current log level."""
        message_level = self.log_levels.get(level.lower(), 0)
        return message_level <= self.current_log_level
    
    def __post_init__(self):
        """Initialize validator after creation."""
        # Load gitignore patterns if requested
        if self.config.respect_gitignore:
            self.load_gitignore_patterns()
    
    def load_gitignore_patterns(self):
        """Load patterns from .gitignore file."""
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if line and not line.startswith('#'):
                            self.gitignore_patterns.append(line)
                self.log(f"Loaded {len(self.gitignore_patterns)} patterns from .gitignore")
            except Exception as e:
                self.log(f"Failed to load .gitignore: {e}", "WARNING")
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose or level != "INFO":
            print(f"[{level}] {message}")
    
    def add_error(self, level: str, message: str, path: Optional[Path] = None):
        """Add a validation error."""
        self.errors.append(ValidationError(level, message, path))
    
    def should_skip_path(self, path: Path) -> bool:
        """Check if a path should be skipped during validation."""
        # Check skip_dirs configuration
        path_parts = set(path.parts)
        if path_parts.intersection(self.config.skip_dirs):
            return True
            
        # Check gitignore patterns if enabled
        if self.config.respect_gitignore and self.gitignore_patterns:
            path_str = str(path)
            for pattern in self.gitignore_patterns:
                # Handle different gitignore pattern types
                if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
                    return True
                # Handle directory patterns ending with /
                if pattern.endswith('/') and path.is_dir():
                    dir_pattern = pattern[:-1]
                    if fnmatch.fnmatch(path_str, dir_pattern) or fnmatch.fnmatch(path.name, dir_pattern):
                        return True
                # Handle ** patterns (recursive)
                if '**' in pattern:
                    # Convert ** pattern to fnmatch pattern
                    fnmatch_pattern = pattern.replace('**/', '*/')
                    if fnmatch.fnmatch(path_str, fnmatch_pattern):
                        return True
        
        return False
    
    def validate_level_value(self, level_name: str, value: str) -> bool:
        """Validate a value against allowed values for a specific level."""
        if level_name not in self.config.valid_values:
            return True  # No restrictions defined
        
        valid_values = self.config.valid_values[level_name]
        
        for valid_value in valid_values:
            if valid_value == "*":  # Wildcard - allow anything
                return True
            elif "*" in valid_value:  # Pattern matching with wildcards
                # Use fnmatch for glob-style pattern matching
                if fnmatch.fnmatch(value, valid_value):
                    return True
            elif value == valid_value:  # Exact match
                return True
        
        return False
    
    def validate_directory_structure(self) -> None:
        """Validate the directory structure according to configuration."""
        root_path = Path(self.config.root_dir)
        
        if not root_path.exists():
            self.add_error("ERROR", f"Root directory '{self.config.root_dir}' not found")
            return
        
        self.log(f"Validating directory structure in: {root_path}")
        
        for path in root_path.rglob("*"):
            if not path.is_dir() or self.should_skip_path(path):
                continue
            
            self.stats["directories_scanned"] += 1
            relative_path = path.relative_to(root_path)
            parts = relative_path.parts
            depth = len(parts)
            
            # Check depth (if enabled)
            if self.config.check_depth and depth > self.config.max_depth:
                if not self.config.allow_subdirs or depth > self.config.max_depth + 1:
                    level = "ERROR" if self.config.fail_on_invalid_structure else "WARNING"
                    self.add_error(
                        level, 
                        f"Directory exceeds maximum depth ({self.config.max_depth})",
                        path
                    )
                elif depth == self.config.max_depth + 1:
                    self.add_error("INFO", "Subdirectory in component", path)
            
            # Validate component directories (exactly at max_depth)
            elif depth == self.config.max_depth:
                self.stats["components_found"] += 1
                self.validate_component_directory(path, parts)
    
    def validate_component_directory(self, path: Path, parts: tuple) -> None:
        """Validate a component directory structure and values."""
        # Add INFO message for component being validated
        self.add_error("INFO", f"Validating component directory", path)
        
        # Validate each level's value
        for i, (level_name, value) in enumerate(zip(self.config.levels, parts)):
            if not self.validate_level_value(level_name, value):
                level = "ERROR" if self.config.fail_on_invalid_values else "WARNING"
                valid_values = self.config.valid_values.get(level_name, ["*"])
                self.add_error(
                    level,
                    f"Invalid {level_name} '{value}'. Valid values: {valid_values}",
                    path
                )
            else:
                # Add INFO message for valid level values
                self.add_error("INFO", f"Valid {level_name}: '{value}'", path)
        
        # Validate mandatory and optional files
        self.validate_component_files(path)
    
    def validate_component_files(self, component_path: Path) -> None:
        """Validate that mandatory and optional files exist in a component directory."""
        missing_mandatory_files = []
        missing_optional_files = []
        present_files = []
        
        # Check mandatory files
        for required_file in self.config.mandatory_files:
            file_path = component_path / required_file
            self.stats["files_checked"] += 1
            
            if file_path.exists() and not any(pattern in file_path.name for pattern in self.config.skip_files):
                present_files.append(required_file)
            else:
                missing_mandatory_files.append(required_file)
        
        # Check optional files
        for optional_file in self.config.optional_files:
            file_path = component_path / optional_file
            
            if file_path.exists() and not any(pattern in file_path.name for pattern in self.config.skip_files):
                if optional_file not in present_files:  # Don't duplicate if already counted as mandatory
                    present_files.append(optional_file)
            else:
                missing_optional_files.append(optional_file)
        
        # Report missing mandatory files
        if missing_mandatory_files:
            level = "ERROR" if self.config.fail_on_missing_files else "WARNING"
            self.add_error(
                level,
                f"Missing mandatory files: {', '.join(missing_mandatory_files)}",
                component_path
            )
        
        # Report missing optional files as WARNING
        if missing_optional_files:
            self.add_error(
                "OPTIONAL_WARNING",
                f"Missing optional files: {', '.join(missing_optional_files)}",
                component_path
            )
        
        if self.verbose and present_files:
            self.log(f"Found files: {', '.join(sorted(present_files))} in {component_path}")
    
    def validate(self) -> int:
        """Run all validations and return exit code."""
        self.log("Starting repository structure validation...")
        
        try:
            self.validate_directory_structure()
            
            # Always print results for visibility
            self.print_results()
            
            # Determine exit code - only fail on errors, regardless of log level
            error_count = len([e for e in self.errors if e.level == "ERROR"])
            
            # Only fail on actual errors
            if error_count > 0:
                return 1
            
            # Handle strict mode (only applies if no errors)
            warning_count = len([e for e in self.errors if e.level == "WARNING"])
            optional_warning_count = len([e for e in self.errors if e.level == "OPTIONAL_WARNING"])
            if self.strict and (warning_count > 0 or optional_warning_count > 0):
                return 1
                
            return 0
                
        except Exception as e:
            self.log(f"Validation failed with exception: {e}", "ERROR")
            return 1
    
    def print_results(self) -> None:
        """Print validation results."""
        print(f"\n{colorize('Repository Structure Validation Results', 'cyan')}")
        print("=" * 50)
        
        # Print statistics
        print(f"{colorize('Statistics:', 'blue')}")
        print(f"   • Components found: {self.stats['components_found']}")
        print(f"   • Directories scanned: {self.stats['directories_scanned']}")
        print(f"   • Files checked: {self.stats['files_checked']}")
        
        # Group errors by level
        errors = [e for e in self.errors if e.level == "ERROR"]
        warnings = [e for e in self.errors if e.level == "WARNING"]
        optional_warnings = [e for e in self.errors if e.level == "OPTIONAL_WARNING"]
        infos = [e for e in self.errors if e.level == "INFO"]
        
        # Always show a summary, even if no issues
        if not errors and not warnings and not optional_warnings and not infos:
            print(f"\n{colorize('✅ All validations passed! Repository structure is compliant.', 'green')}")
        else:
            # Show summary counts even when passing
            total_issues = len(errors) + len(warnings) + len(optional_warnings) + len(infos)
            print(f"\n{colorize('Summary:', 'blue')}")
            if errors:
                print(f"   • {colorize(f'{len(errors)} error(s)', 'red')} - blocking issues")
            if warnings:
                print(f"   • {colorize(f'{len(warnings)} warning(s)', 'yellow')} - structure issues")
            if optional_warnings:
                print(f"   • {colorize(f'{len(optional_warnings)} optional file warning(s)', 'yellow')} - missing recommended files")
            if infos:
                print(f"   • {colorize(f'{len(infos)} info message(s)', 'blue')} - informational")
        
        # Print errors
        if errors:
            print(f"\n{colorize(f'Found {len(errors)} error(s):', 'red')}")
            for error in errors:
                print(f"   {error}")
        
        # Print warnings
        if warnings:
            print(f"\n{colorize(f'Found {len(warnings)} warning(s):', 'yellow')}")
            for warning in warnings:
                print(f"   {warning}")
        
        # Print optional file warnings (based on log level)
        if optional_warnings and (self.should_show_message("warn") or self.verbose):
            print(f"\n{colorize(f'Found {len(optional_warnings)} optional file warning(s):', 'yellow')}")
            for warning in optional_warnings:
                print(f"   {warning}")
        
        # Print info messages (based on log level)
        if infos and (self.should_show_message("info") or self.verbose):
            print(f"\n{colorize(f'Found {len(infos)} info message(s):', 'blue')}")
            for info in infos:
                print(f"   {info}")
        
        # Final status message
        if errors:
            print(f"\n{colorize('❌ Validation failed due to errors above.', 'red')}")
        elif warnings or optional_warnings or infos:
            print(f"\n{colorize('⚠️  Validation passed with warnings/info above.', 'yellow')}")
        else:
            print(f"\n{colorize('✅ Perfect! No issues found.', 'green')}")

def load_config(config_file: Optional[str] = None) -> StructureConfig:
    """Load configuration from file or use defaults."""
    config = StructureConfig()
    
    # Determine config file and format
    if config_file:
        config_path = Path(config_file)
    else:
        # Try YAML first (now supported without PyYAML), then JSON
        yaml_path = Path("dir-checker-config.yaml")
        json_path = Path("dir-checker-config.json")
        
        if yaml_path.exists():
            config_path = yaml_path
        elif json_path.exists():
            config_path = json_path
        else:
            config_path = yaml_path  # Default to YAML for better readability
    
    if config_path.exists():
        try:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                config_data = parse_yaml_with_bash(str(config_path))
            else:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
            
            # Update config with loaded values
            for key, value in config_data.items():
                if hasattr(config, key):
                    # Handle sets properly
                    if key in ['skip_dirs', 'skip_files'] and isinstance(value, list):
                        setattr(config, key, set(value))
                    else:
                        setattr(config, key, value)
            
            print(f"{colorize('✅ Loaded configuration from:', 'green')} {config_path}")
        except Exception as e:
            print(f"{colorize('Warning:', 'yellow')} Failed to load config from {config_path}: {e}")
    
    return config

def create_default_config_file(filename: Optional[str] = None) -> None:
    """Create a default configuration file."""
    config = StructureConfig()
    
    # Determine filename and format
    if filename:
        config_path = Path(filename)
    else:
        config_path = Path("dir-checker-config.yaml")  # Default to YAML for better readability
    
    if config_path.suffix.lower() in ['.yaml', '.yml']:
        # Create YAML file manually
        yaml_content = f"""# Repository Structure Validation Configuration
# This file configures the pre-commit hook for validating directory structure
# 
# This is a generic example configuration. Customize it for your project:
# - Change root_dir to your main source directory
# - Modify levels to match your project structure
# - Update valid_values to reflect your naming conventions
# - Set mandatory_files to files required in each component
# - Configure optional_files for recommended files

root_dir: "{config.root_dir}"

# Define the hierarchy levels in your project structure
# Example: module -> service -> component (adjust as needed)
levels:
{chr(10).join(f'  - "{level}"' for level in config.levels)}

max_depth: {config.max_depth}
check_depth: {str(config.check_depth).lower()}
allow_subdirs: {str(config.allow_subdirs).lower()}
respect_gitignore: {str(config.respect_gitignore).lower()}

# Valid values for each level (customize for your project)
# Use "*" to allow any name, or "prefix*" for prefix matching
valid_values:
{chr(10).join(f'  {level}:{chr(10)}{chr(10).join(f"    - \"{value}\"" for value in values)}' for level, values in config.valid_values.items())}

# Files that must exist in each component directory
mandatory_files:
{chr(10).join(f'  - "{file}"' for file in config.mandatory_files)}

# Files that are recommended but not required
optional_files:
{chr(10).join(f'  - "{file}"' for file in config.optional_files)}

# Directories to skip during validation
skip_dirs:
{chr(10).join(f'  - "{dir}"' for dir in sorted(config.skip_dirs))}

# File patterns to skip
skip_files:
{chr(10).join(f'  - "{file}"' for file in sorted(config.skip_files))}

# Validation settings
fail_on_missing_files: {str(config.fail_on_missing_files).lower()}
fail_on_invalid_structure: {str(config.fail_on_invalid_structure).lower()}
fail_on_invalid_values: {str(config.fail_on_invalid_values).lower()}

# Logging settings  
log_level: {config.log_level}
"""
        
        with open(config_path, 'w') as f:
            f.write(yaml_content)
    else:
        # Create JSON file
        config_dict = {
            "root_dir": config.root_dir,
            "levels": config.levels,
            "max_depth": config.max_depth,
            "check_depth": config.check_depth,
            "allow_subdirs": config.allow_subdirs,
            "respect_gitignore": config.respect_gitignore,
            "valid_values": config.valid_values,
            "mandatory_files": config.mandatory_files,
            "optional_files": config.optional_files,
            "skip_dirs": list(config.skip_dirs),
            "skip_files": list(config.skip_files),
            "fail_on_missing_files": config.fail_on_missing_files,
            "fail_on_invalid_structure": config.fail_on_invalid_structure,
            "fail_on_invalid_values": config.fail_on_invalid_values,
            "log_level": config.log_level
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2, sort_keys=False)
    
    print(f"✅ Created default configuration file: {config_path}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Directory Structure Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 dir-checker.py
  python3 dir-checker.py --config custom-config.json
  python3 dir-checker.py --verbose --strict
  python3 dir-checker.py --log-level info
  python3 dir-checker.py --log-level error
  python3 dir-checker.py --create-config
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file (default: dir-checker-config.yaml or dir-checker-config.json)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--strict", "-s",
        action="store_true",
        help="Fail on warnings as well as errors"
    )
    
    parser.add_argument(
        "--log-level", "-l",
        choices=["error", "warn", "info"],
        help="Set log level (error, warn, info). Default: warn"
    )
    
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create a default configuration file and exit"
    )
    
    parser.add_argument(
        "--debug-config",
        action="store_true",
        help="Debug configuration parsing and exit"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="dir-checker 1.0.0"
    )
    
    args = parser.parse_args()
    
    if args.create_config:
        create_default_config_file()
        return 0
    
    if args.debug_config:
        import json
        config = load_config(args.config)
        print("Loaded configuration:")
        print(f"  check_depth: {config.check_depth}")
        print(f"  mandatory_files: {config.mandatory_files}")
        print(f"  root_dir: {config.root_dir}")
        print(f"  levels: {config.levels}")
        return 0
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command-line flags
    if args.log_level:
        config.log_level = args.log_level
    
    # Create validator and run
    validator = RepositoryValidator(config, args.verbose, args.strict)
    return validator.validate()

if __name__ == "__main__":
    sys.exit(main())
