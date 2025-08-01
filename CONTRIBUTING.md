# Contributing to dir-checker

Thank you for your interest in contributing to the pre-commit directory checker! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Git
- pre-commit (for development)

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/your-username/dir-checker.git
cd dir-checker
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

5. Install pre-commit hooks:
```bash
pre-commit install
```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bug fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the coding standards below

3. Write or update tests for your changes

4. Run the test suite:
```bash
python -m pytest tests/ -v
```

5. Test the hook manually:
```bash
python -m dir_checker --forbidden-dirs=temp test_file.txt
```

6. Run pre-commit to check your changes:
```bash
pre-commit run --all-files
```

### Coding Standards

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate
- Keep functions focused and relatively small
- Write descriptive commit messages

### Testing

- Write unit tests for new functionality
- Ensure all existing tests pass
- Aim for good test coverage
- Test edge cases and error conditions
- Include integration tests where appropriate

### Documentation

- Update the README.md if you add new features
- Add examples for new functionality
- Update the CHANGELOG.md
- Include docstrings in your code

## Submitting Changes

### Pull Request Process

1. Ensure your code follows the coding standards
2. Make sure all tests pass
3. Update documentation as needed
4. Create a pull request with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots or examples if applicable

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or logs

### Feature Requests

For feature requests, please include:
- Description of the feature
- Use case or motivation
- Proposed implementation (if any)
- Examples of usage

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainers

Thank you for contributing!
