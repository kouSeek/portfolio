#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified test runner for Kalyani App."""

from pathlib import Path
import sys
import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
