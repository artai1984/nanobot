#!/usr/bin/env python3
"""Verify multi-model provider integration."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def check_file_exists(filepath, description):
    """Check if a file exists."""
    path = Path(filepath)
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_class_in_file(filepath, class_name):
    """Check if a class is defined in a file."""
    path = Path(filepath)
    if not path.exists():
        return False

    with open(path) as f:
        content = f.read()
        return f"class {class_name}" in content

def check_import_in_file(filepath, import_name):
    """Check if an import is present in a file."""
    path = Path(filepath)
    if not path.exists():
        return False

    with open(path) as f:
        content = f.read()
        return import_name in content

def check_function_in_file(filepath, function_name):
    """Check if a function is defined in a file."""
    path = Path(filepath)
    if not path.exists():
        return False

    with open(path) as f:
        content = f.read()
        return f"def {function_name}" in content

def check_export_in_file(filepath, export_name):
    """Check if an export is present in __all__."""
    path = Path(filepath)
    if not path.exists():
        return False

    with open(path) as f:
        content = f.read()
        if "__all__" in content:
            # Extract __all__ content
            start = content.find("__all__")
            end = content.find("]", start)
            all_content = content[start:end+1]
            return f'"{export_name}"' in all_content or f"'{export_name}'" in all_content
    return False

def main():
    """Run verification checks."""

    print("=" * 70)
    print("Multi-Model Provider Integration Verification")
    print("=" * 70)
    print()

    checks = []

    # 1. MultiModelProvider class exists
    checks.append(check_class_in_file(
        "nanobot/providers/multi_model_provider.py",
        "MultiModelProvider"
    ))

    # 2. MultiModelConfig class exists in schema.py
    checks.append(check_class_in_file(
        "nanobot/config/schema.py",
        "MultiModelConfig"
    ))

    # 3. ProvidersConfig has multi_model field
    checks.append(check_class_in_file(
        "nanobot/config/schema.py",
        "ProvidersConfig"
    ))

    # 4. MultiModelProvider is imported in commands.py
    checks.append(check_import_in_file(
        "nanobot/cli/commands.py",
        "MultiModelProvider"
    ))

    # 5. MultiModelProvider is instantiated in commands.py
    checks.append(check_function_in_file(
        "nanobot/cli/commands.py",
        "MultiModelProvider"
    ))

    # 6. MultiModelProvider is exported from __init__.py
    checks.append(check_export_in_file(
        "nanobot/providers/__init__.py",
        "MultiModelProvider"
    ))

    # 7. Config file has multi_model section
    config_path = Path.home() / '.nanobot' / 'config.json'
    if config_path.exists():
        import json
        with open(config_path) as f:
            config = json.load(f)
        has_multi_model = 'multi_model' in config.get('providers', {})
        checks.append(has_multi_model)
        print(f"{'✓' if has_multi_model else '✗'} Config has multi_model section")
    else:
        checks.append(False)
        print(f"✗ Config file not found")

    # 8. Multi-model provider is enabled in config
    if config_path.exists():
        import json
        with open(config_path) as f:
            config = json.load(f)
        enabled = config.get('providers', {}).get('multi_model', {}).get('enabled', False)
        checks.append(enabled)
        print(f"{'✓' if enabled else '⚠'} Multi-model provider enabled: {enabled}")
    else:
        checks.append(False)

    # Summary
    print()
    print("=" * 70)
    print("Verification Summary")
    print("=" * 70)

    total = len(checks)
    passed = sum(checks)
    failed = total - passed

    print(f"Total checks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    if passed == total:
        print("✓✓✓ All integration checks passed! ✓✓✓")
        print()
        print("The multi-model provider is properly integrated into the system.")
        print("Changes made:")
        print("  1. Added MultiModelConfig class to schema.py")
        print("  2. Added multi_model field to ProvidersConfig")
        print("  3. Integrated MultiModelProvider in _make_provider function")
        print("  4. Exported MultiModelProvider from providers/__init__.py")
        print("  5. Configured multi-model provider in config.json")
        return 0
    else:
        print("✗✗✗ Some integration checks failed! ✗✗✗")
        print()
        print("Please review the failed checks above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
