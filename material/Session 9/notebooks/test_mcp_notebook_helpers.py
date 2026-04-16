import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import sentinel


NOTEBOOK_DIR = Path(__file__).resolve().parent
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))


from mcp_notebook_helpers import NotebookSafeMCPServerStdio


class NotebookSafeMCPServerStdioTests(unittest.TestCase):
    def test_create_streams_uses_devnull_by_default(self):
        import mcp_notebook_helpers

        original = mcp_notebook_helpers.stdio_client
        calls = []

        def fake_stdio_client(params, errlog):
            calls.append((params, errlog))
            return sentinel.context_manager

        mcp_notebook_helpers.stdio_client = fake_stdio_client
        try:
            server = NotebookSafeMCPServerStdio(
                params={"command": "python", "args": ["demo.py"]},
            )
            result = server.create_streams()
        finally:
            mcp_notebook_helpers.stdio_client = original

        self.assertIs(result, sentinel.context_manager)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0].command, "python")
        self.assertEqual(calls[0][0].args, ["demo.py"])
        self.assertIs(calls[0][1], subprocess.DEVNULL)

    def test_create_streams_respects_explicit_errlog(self):
        import mcp_notebook_helpers

        original = mcp_notebook_helpers.stdio_client
        calls = []

        def fake_stdio_client(params, errlog):
            calls.append((params, errlog))
            return sentinel.context_manager

        mcp_notebook_helpers.stdio_client = fake_stdio_client
        try:
            server = NotebookSafeMCPServerStdio(
                params={"command": "python", "args": ["demo.py"]},
                errlog=sentinel.errlog,
            )
            server.create_streams()
        finally:
            mcp_notebook_helpers.stdio_client = original

        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0][1], sentinel.errlog)


if __name__ == "__main__":
    unittest.main()
