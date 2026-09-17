"""Put the repository root on `sys.path` so tests can import `scripts.*`
without an editable install.

D1 adds `core/` here as well, once pure logic moves out of the plugin.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
