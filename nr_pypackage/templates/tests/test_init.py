# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test modules."""


def test_init(hello_world):
    """Run a test."""
    import {{ package_name_safe }}

    # Test __init__
    assert hasattr({{ package_name_safe }}, '__version__')

    # Test pytest fixtures
    assert(hello_world == "Hello World!")
