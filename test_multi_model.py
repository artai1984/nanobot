#!/usr/bin/env python3
"""Test script for multi-model provider integration."""

import asyncio
import json
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from nanobot.config.loader import load_config
from nanobot.config.schema import Config
from nanobot.providers.multi_model_provider import MultiModelProvider
from loguru import logger


async def test_multi_model_provider():
    """Test the multi-model provider with fallback."""

    # Load config
    config = load_config()

    # Display config
    logger.info("=" * 60)
    logger.info("Multi-Model Provider Test")
    logger.info("=" * 60)
    logger.info(f"Enabled: {config.providers.multi_model.enabled}")
    logger.info(f"Models: {config.providers.multi_model.models}")
    logger.info(f"Default model: {config.providers.multi_model.default_model}")
    logger.info("=" * 60)

    # Create multi-model provider
    try:
        provider = MultiModelProvider(
            config=config,
            models=config.providers.multi_model.models,
            default_model=config.providers.multi_model.default_model,
        )

        logger.success("✓ MultiModelProvider created successfully")

        # Test basic chat
        messages = [
            {"role": "user", "content": "Say 'Hello from multi-model provider!' in one sentence."}
        ]

        logger.info("\nSending test message...")
        response = await provider.chat(
            messages=messages,
            max_tokens=100,
        )

        logger.success("\n" + "=" * 60)
        logger.success("✓ Chat completed successfully!")
        logger.success("=" * 60)
        logger.success(f"Content: {response.content}")
        logger.success(f"Finish reason: {response.finish_reason}")

        # Test with specific model
        logger.info("\n" + "-" * 60)
        logger.info("Testing with specific model (first model)...")
        logger.info("-" * 60)

        response2 = await provider.chat(
            messages=messages,
            model=config.providers.multi_model.default_model,
            max_tokens=100,
        )

        logger.success(f"Content: {response2.content}")
        logger.success(f"Finish reason: {response2.finish_reason}")

        logger.success("\n" + "=" * 60)
        logger.success("✓ All tests passed!")
        logger.success("=" * 60)

        return True

    except Exception as e:
        logger.error(f"\n✗ Test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


async def test_config_loading():
    """Test that config loads correctly with multi_model section."""

    logger.info("\n" + "=" * 60)
    logger.info("Config Loading Test")
    logger.info("=" * 60)

    try:
        config = load_config()

        if not hasattr(config.providers, 'multi_model'):
            logger.error("✗ multi_model config section not found")
            return False

        mm_config = config.providers.multi_model

        if not mm_config.enabled:
            logger.warning("⚠ Multi-model provider is disabled in config")
            logger.info("Enable it by setting 'enabled': true in config.json")
            return True

        if not mm_config.models:
            logger.error("✗ No models configured for multi-model provider")
            return False

        logger.success(f"✓ Config loaded successfully")
        logger.success(f"  Enabled: {mm_config.enabled}")
        logger.success(f"  Models count: {len(mm_config.models)}")
        logger.success(f"  Models: {mm_config.models}")
        logger.success(f"  Default: {mm_config.default_model}")

        return True

    except Exception as e:
        logger.error(f"✗ Config loading failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


async def main():
    """Run all tests."""

    # Test 1: Config loading
    config_ok = await test_config_loading()

    # Test 2: Provider functionality
    provider_ok = await test_multi_model_provider()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    logger.info(f"Config loading: {'✓ PASS' if config_ok else '✗ FAIL'}")
    logger.info(f"Provider test: {'✓ PASS' if provider_ok else '✗ FAIL'}")
    logger.info("=" * 60)

    if config_ok and provider_ok:
        logger.success("\n✓✓✓ All tests passed! Multi-model provider is working correctly. ✓✓✓")
        return 0
    else:
        logger.error("\n✗✗✗ Some tests failed. Please check the errors above. ✗✗✗")
        return 1


if __name__ == "__main__":
    import sys

    exit_code = asyncio.run(main())
    sys.exit(exit_code)
