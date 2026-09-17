"""Unit tests for lw-pulse.py's absolute()/relative() path guards."""
import importlib.util
import tempfile
import unittest
from pathlib import Path


PLUGIN_SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "LEAPWare-Pulse" / "scripts"


def _load_lw_pulse():
    spec = importlib.util.spec_from_file_location("lw_pulse_under_test", PLUGIN_SCRIPTS / "lw-pulse.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lw_pulse = _load_lw_pulse()


class AbsoluteTests(unittest.TestCase):
    def test_happy_path_resolves_an_absolute_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            resolved = lw_pulse.absolute(directory)
            self.assertEqual(resolved, Path(directory).resolve())
            self.assertTrue(resolved.is_absolute())

    def test_refuses_a_relative_path(self):
        with self.assertRaises(ValueError):
            lw_pulse.absolute("openspec/tasks.md")

    def test_refuses_traversal_segments(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                lw_pulse.absolute(str(Path(directory) / ".." / "evil"))


class RelativeTests(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name).resolve()
        (self.root / "openspec").mkdir()
        (self.root / "openspec" / "tasks.md").write_text("- [ ] a task\n", encoding="utf-8")

    def tearDown(self):
        self._temporary.cleanup()

    def test_happy_path_joins_under_root(self):
        joined = lw_pulse.relative(self.root, "openspec/tasks.md")
        self.assertEqual(joined, self.root / "openspec" / "tasks.md")

    def test_refuses_non_string_input(self):
        with self.assertRaises(ValueError):
            lw_pulse.relative(self.root, None)

    def test_refuses_empty_string_input(self):
        with self.assertRaises(ValueError):
            lw_pulse.relative(self.root, "")

    def test_refuses_traversal_segments(self):
        with self.assertRaises(ValueError):
            lw_pulse.relative(self.root, "../outside.md")

    def test_refuses_an_absolute_value(self):
        with self.assertRaises(ValueError):
            lw_pulse.relative(self.root, str(self.root / "openspec" / "tasks.md"))

    def test_refuses_a_path_resolving_outside_root_via_symlinked_segment(self):
        # A traversal that only escapes after resolution (no literal "..") must
        # still be refused: build a value whose resolved target sits outside root.
        outside = Path(self._temporary.name).parent
        with self.assertRaises(ValueError):
            lw_pulse.relative(self.root, f"openspec/../../{outside.name}")


if __name__ == "__main__":
    unittest.main()
