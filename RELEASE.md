# Release Strategy for dir-checker

## How to Create Releases

This repository uses a manual release strategy optimized for pre-commit hook usage.

### Manual Release Process

1. **Prepare for Release**:
   - Ensure all changes are merged to `main`
   - Update version numbers if needed
   - Test thoroughly

2. **Create Release PR**:
   ```bash
   gh workflow run release.yaml
   ```
   This creates a release PR with:
   - Updated CHANGELOG.md
   - Version bumps in pyproject.toml and setup.py
   - Release notes

3. **Review and Merge**:
   - Review the auto-generated release PR
   - Merge the PR to create the actual release

4. **Tag is Created Automatically**:
   - Release-please automatically creates a Git tag
   - GitHub release is published

## Using in Pre-commit

Users can reference specific versions in their `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/nitinnbisht/pre-commit-dir-checker
    rev: v1.0.0  # Use specific version tag
    hooks:
      - id: dir-checker
```

## Version Strategy

- **Major** (1.0.0 → 2.0.0): Breaking changes to configuration or behavior
- **Minor** (1.0.0 → 1.1.0): New features, new configuration options
- **Patch** (1.0.0 → 1.0.1): Bug fixes, documentation updates

## Available Versions

Check available versions at: https://github.com/nitinnbisht/pre-commit-dir-checker/releases
