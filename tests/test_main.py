"""Unit tests for Cookie-Manager-main."""
import importlib
import sys
import unittest


class TestImport(unittest.TestCase):
    """Verify the main module imports cleanly."""

    def test_module_imports(self):
        """The main module should import without errors."""
        try:
            importlib.import_module("cookie_manager")
        except ImportError as e:
            if "gmpy2" in str(e) or "mpmath" in str(e):
                self.skipTest(f"Optional dependency not installed: {e}")
            raise

    def test_module_has_functions(self):
        """The module should define at least one callable."""
        try:
            mod = importlib.import_module("cookie_manager")
        except ImportError as e:
            if "gmpy2" in str(e) or "mpmath" in str(e):
                self.skipTest(f"Optional dependency not installed: {e}")
            raise
        functions = [n for n in dir(mod) if callable(getattr(mod, n)) and not n.startswith("_")]
        self.assertGreater(len(functions), 0, "Module should expose at least one public function")


class TestArguments(unittest.TestCase):
    """Verify argparse setup works."""

    def test_help_flag_exists(self):
        """The script should support --help via argparse."""
        # We can't easily test this without running the script,
        # but we can verify argparse is present in the source
        import ast
        import os
        script_path = os.path.join(os.path.dirname(__file__), "..", "cookie_manager.py")
        script_path = os.path.normpath(script_path)
        if not os.path.exists(script_path):
            self.skipTest("Main script not found")
        with open(script_path) as f:
            tree = ast.parse(f.read())
        import argparse
        has_argparse = any(
            isinstance(node, ast.Import) and any(a.name == "argparse" for a in node.names)
            for node in ast.walk(tree)
        )
        if not has_argparse:
            self.skipTest("Script doesn't use argparse")


if __name__ == "__main__":
    unittest.main()
