import pytest
import tempfile
import os
import json
from pathlib import Path
from dir_checker.main import (
    StructureConfig, 
    RepositoryValidator, 
    ValidationError,
    load_config,
    parse_yaml_with_bash,
    main
)


class TestStructureConfig:
    """Test the StructureConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = StructureConfig()
        assert config.root_dir == "src"
        assert config.levels == ["module", "service", "component"]
        assert config.max_depth == 3
        assert config.check_depth is False
        assert config.allow_subdirs is True
        assert "index.js" in config.mandatory_files
        assert "package.json" in config.mandatory_files


class TestYamlParser:
    """Test the bash-style YAML parser."""
    
    def test_simple_yaml_parsing(self, tmp_path):
        """Test parsing simple YAML structure."""
        yaml_content = """
root_dir: "test"
max_depth: 5
check_depth: true
levels:
  - "env"
  - "service"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)
        
        result = parse_yaml_with_bash(str(yaml_file))
        
        assert result["root_dir"] == "test"
        assert result["max_depth"] == 5
        assert result["check_depth"] is True
        assert result["levels"] == ["env", "service"]
    
    def test_nested_yaml_parsing(self, tmp_path):
        """Test parsing nested YAML structure."""
        yaml_content = """
valid_values:
  environment:
    - "dev"
    - "prod"
  service:
    - "api"
    - "web"
"""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text(yaml_content)
        
        result = parse_yaml_with_bash(str(yaml_file))
        
        assert "valid_values" in result
        assert result["valid_values"]["environment"] == ["dev", "prod"]
        assert result["valid_values"]["service"] == ["api", "web"]


class TestRepositoryValidator:
    """Test the RepositoryValidator class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.config = StructureConfig()
        self.config.root_dir = "test_root"
        self.config.levels = ["module", "service", "component"]
        self.config.max_depth = 3
        self.config.check_depth = True
        self.config.valid_values = {
            "module": ["frontend", "backend"],
            "service": ["api", "web"],
            "component": ["*"]
        }
        self.config.mandatory_files = ["index.js", "package.json"]
        self.config.optional_files = ["README.md"]
        
    def test_validator_initialization(self):
        """Test validator initialization."""
        validator = RepositoryValidator(self.config, verbose=True)
        assert validator.config == self.config
        assert validator.verbose is True
        assert validator.errors == []
    
    def test_add_error(self):
        """Test adding validation errors."""
        validator = RepositoryValidator(self.config)
        validator.add_error("ERROR", "Test error", Path("test/path"))
        
        assert len(validator.errors) == 1
        error = validator.errors[0]
        assert error.level == "ERROR"
        assert error.message == "Test error"
        assert error.path == Path("test/path")
    
    def test_should_skip_path(self):
        """Test path skipping logic."""
        validator = RepositoryValidator(self.config)
        
        # Test skip_dirs
        assert validator.should_skip_path(Path(".git/objects"))
        assert validator.should_skip_path(Path("node_modules/package"))
        assert not validator.should_skip_path(Path("src/main"))
    
    def test_validate_level_value(self):
        """Test level value validation."""
        validator = RepositoryValidator(self.config)
        
        # Test exact match
        assert validator.validate_level_value("module", "frontend") is True
        assert validator.validate_level_value("module", "backend") is True
        assert validator.validate_level_value("module", "staging") is False
        
        # Test wildcard
        assert validator.validate_level_value("component", "anything") is True
    
    def test_validate_level_value_with_patterns(self):
        """Test level value validation with patterns."""
        self.config.valid_values["module"] = ["sandbox*", "prod"]
        validator = RepositoryValidator(self.config)
        
        # Test pattern matching
        assert validator.validate_level_value("module", "sandbox1") is True
        assert validator.validate_level_value("module", "sandbox-test") is True
        assert validator.validate_level_value("module", "prod") is True
        assert validator.validate_level_value("module", "dev") is False
    
    def test_log_level_filtering(self):
        """Test log level filtering."""
        self.config.log_level = "error"
        validator = RepositoryValidator(self.config)
        
        assert validator.should_show_message("error") is True
        assert validator.should_show_message("warn") is False
        assert validator.should_show_message("info") is False
        
        self.config.log_level = "info"
        validator = RepositoryValidator(self.config)
        
        assert validator.should_show_message("error") is True
        assert validator.should_show_message("warn") is True
        assert validator.should_show_message("info") is True


class TestValidationError:
    """Test the ValidationError class."""
    
    def test_error_formatting(self):
        """Test error string formatting."""
        error = ValidationError("ERROR", "Test message", Path("test/path"))
        error_str = str(error)
        assert "Error" in error_str
        assert "Test message" in error_str
        assert "test/path" in error_str
        
        warning = ValidationError("WARNING", "Test warning")
        warning_str = str(warning)
        assert "Warning" in warning_str
        assert "Test warning" in warning_str


class TestConfigLoading:
    """Test configuration loading functionality."""
    
    def test_load_default_config(self):
        """Test loading default configuration when no config file exists."""
        # Test creating a StructureConfig directly (true default)
        config = StructureConfig()
        assert isinstance(config, StructureConfig)
        assert config.root_dir == "src"
    
    def test_load_yaml_config(self, tmp_path):
        """Test loading YAML configuration."""
        yaml_content = """
root_dir: "custom"
max_depth: 5
levels:
  - "env"
  - "service"
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml_content)
        
        config = load_config(str(config_file))
        assert config.root_dir == "custom"
        assert config.max_depth == 5
        assert config.levels == ["env", "service"]
    
    def test_load_json_config(self, tmp_path):
        """Test loading JSON configuration."""
        config_data = {
            "root_dir": "json_test",
            "max_depth": 6,
            "levels": ["a", "b", "c"]
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        config = load_config(str(config_file))
        assert config.root_dir == "json_test"
        assert config.max_depth == 6
        assert config.levels == ["a", "b", "c"]


class TestMainFunction:
    """Test the main entry point function."""
    
    def test_main_with_create_config(self, tmp_path, monkeypatch, capsys):
        """Test main function with --create-config flag."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr('sys.argv', ['dir-checker', '--create-config'])
        result = main()
        assert result == 0
        assert (tmp_path / "dir-checker-config.yaml").exists()
    
    def test_main_with_debug_config(self, tmp_path, monkeypatch, capsys):
        """Test main function with --debug-config flag."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr('sys.argv', ['dir-checker', '--debug-config'])
        result = main()
        assert result == 0
        
        captured = capsys.readouterr()
        assert "Loaded configuration:" in captured.out
        assert "check_depth:" in captured.out


class TestIntegration:
    """Integration tests with real directory structures."""
    
    def test_valid_structure_validation(self, tmp_path, monkeypatch):
        """Test validation of a valid directory structure."""
        monkeypatch.chdir(tmp_path)
        
        # Create a valid structure
        structure_path = tmp_path / "src" / "frontend" / "api" / "component1"
        structure_path.mkdir(parents=True)
        (structure_path / "index.js").write_text("// index file")
        (structure_path / "package.json").write_text('{"name": "component1"}')
        
        # Create config
        config = StructureConfig()
        config.root_dir = "src"
        config.levels = ["module", "service", "component"]
        config.valid_values = {
            "module": ["frontend", "backend"],
            "service": ["api", "web"],
            "component": ["*"]
        }
        
        validator = RepositoryValidator(config, verbose=False)
        result = validator.validate()
        
        # Should pass validation
        assert result == 0
        
        # Should find the component
        assert validator.stats["components_found"] >= 1
    
    def test_missing_files_validation(self, tmp_path, monkeypatch):
        """Test validation with missing mandatory files."""
        monkeypatch.chdir(tmp_path)
        
        # Create structure missing mandatory files
        structure_path = tmp_path / "src" / "frontend" / "api" / "component1"
        structure_path.mkdir(parents=True)
        # Don't create the mandatory files
        
        config = StructureConfig()
        config.root_dir = "src"
        config.levels = ["module", "service", "component"]
        config.valid_values = {
            "module": ["frontend", "backend"],
            "service": ["api", "web"], 
            "component": ["*"]
        }
        
        validator = RepositoryValidator(config, verbose=False)
        result = validator.validate()
        
        # Should fail validation due to missing files
        assert result == 1
        
        # Should have errors about missing files
        error_messages = [e.message for e in validator.errors if e.level == "ERROR"]
        assert any("Missing mandatory files" in msg for msg in error_messages)
    
    def test_invalid_structure_validation(self, tmp_path, monkeypatch):
        """Test validation with invalid directory names."""
        monkeypatch.chdir(tmp_path)
        
        # Create structure with invalid directory names
        structure_path = tmp_path / "src" / "invalid_module" / "api" / "component1"
        structure_path.mkdir(parents=True)
        (structure_path / "index.js").write_text("// index file")
        (structure_path / "package.json").write_text('{"name": "component1"}')
        
        config = StructureConfig()
        config.root_dir = "src"
        config.levels = ["module", "service", "component"]
        config.valid_values = {
            "module": ["frontend", "backend"],  # "invalid_module" not allowed
            "service": ["api", "web"],
            "component": ["*"]
        }
        config.fail_on_invalid_values = True
        
        validator = RepositoryValidator(config, verbose=False)
        result = validator.validate()
        
        # Should fail due to invalid directory name
        assert result == 1
        
        # Should have errors about invalid values
        error_messages = [e.message for e in validator.errors if e.level == "ERROR"]
        assert any("Invalid module" in msg for msg in error_messages)
