"""Tests for ORM Schema Modernization, Relationship Cycles, and Warning Elimination (F6, F7, F8).

Covers:
- Verification of 0 SAWarning during configure_mappers()
- Bidirectional back_populates contract between User, ChatParticipant, ChatMessage, and BarangayInfo
- Verification of 0 SAWarning on Base.metadata.create_all() and Base.metadata.drop_all() (foreign key cycle resolution via use_alter=True)
- Static and introspection checks verifying zero occurrences of deprecated datetime.utcnow() in backend/app/models/
"""
from __future__ import annotations

import re
import subprocess
import sys
import warnings
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import configure_mappers

from backend.app.models.barangay import BarangayInfo
from backend.app.models.base import Base
from backend.app.models.chat import ChatMessage, ChatParticipant
from backend.app.models.user import User

# ───────────────────────────────────────────────────────────────
# F6: Mapper Relationships & SAWarning Elimination
# ───────────────────────────────────────────────────────────────

def test_zero_sa_warnings_on_configure_mappers_in_clean_process():
    """Verify configure_mappers() produces 0 SAWarning in a clean process."""
    cmd = [
        sys.executable,
        "-c",
        (
            "import warnings\n"
            "from sqlalchemy.exc import SAWarning\n"
            "from sqlalchemy.orm import configure_mappers\n"
            "# Import all models to register mappers\n"
            "import backend.app.models.base\n"
            "import backend.app.models.user\n"
            "import backend.app.models.chat\n"
            "import backend.app.models.barangay\n"
            "import backend.app.models.booking\n"
            "import backend.app.models.attractions\n"
            "import backend.app.models.business\n"
            "import backend.app.models.announcements\n"
            "import backend.app.models.analytics\n"
            "import backend.app.models.document\n"
            "import backend.app.models.events\n"
            "import backend.app.models.gallery\n"
            "import backend.app.models.gamification\n"
            "import backend.app.models.heritage\n"
            "import backend.app.models.notifications\n"
            "\n"
            "with warnings.catch_warnings(record=True) as recorded:\n"
            "    warnings.simplefilter('always')\n"
            "    configure_mappers()\n"
            "    sa_warnings = [str(w.message) for w in recorded if issubclass(w.category, SAWarning)]\n"
            "    if sa_warnings:\n"
            "        for w in sa_warnings:\n"
            "            print('SA_WARNING:', w)\n"
            "        exit(1)\n"
            "exit(0)\n"
        ),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, (
        f"configure_mappers() emitted SAWarning in clean process:\n{proc.stdout}\n{proc.stderr}"
    )


def test_mapper_relationships_bidirectional_back_populates():
    """Verify bidirectional back_populates contracts between models to avoid column overlapping."""
    # User <-> ChatParticipant
    assert User.chat_memberships.property.back_populates == "user", (
        f"User.chat_memberships must define back_populates='user', got {User.chat_memberships.property.back_populates!r}"
    )
    assert ChatParticipant.user.property.back_populates == "chat_memberships", (
        f"ChatParticipant.user must define back_populates='chat_memberships', got {ChatParticipant.user.property.back_populates!r}"
    )

    # User <-> ChatMessage
    assert User.sent_messages.property.back_populates == "sender", (
        f"User.sent_messages must define back_populates='sender', got {User.sent_messages.property.back_populates!r}"
    )
    assert ChatMessage.sender.property.back_populates == "sent_messages", (
        f"ChatMessage.sender must define back_populates='sent_messages', got {ChatMessage.sender.property.back_populates!r}"
    )

    # User <-> BarangayInfo (manager relationship)
    assert User.managed_barangay_info.property.back_populates == "manager", (
        f"User.managed_barangay_info must define back_populates='manager', got {User.managed_barangay_info.property.back_populates!r}"
    )
    assert BarangayInfo.manager.property.back_populates == "managed_barangay_info", (
        f"BarangayInfo.manager must define back_populates='managed_barangay_info', got {BarangayInfo.manager.property.back_populates!r}"
    )


def test_zero_sa_warnings_on_metadata_create_and_drop_all():
    """Verify Base.metadata.drop_all() produces 0 SAWarning (resolves cyclic foreign keys)."""
    engine = create_engine("sqlite:///:memory:")

    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        Base.metadata.create_all(engine)
        Base.metadata.drop_all(engine)
        engine.dispose()

        sa_warnings = [
            w for w in recorded
            if issubclass(w.category, SAWarning)
        ]

    assert len(sa_warnings) == 0, (
        f"Expected 0 SAWarning on create_all/drop_all, but got {len(sa_warnings)}:\n"
        + "\n".join(f"- {w.message}" for w in sa_warnings)
    )


def test_foreign_key_cycle_resolution_use_alter():
    """Verify BarangayInfo.user_id foreign key declares use_alter=True and has explicit name."""
    user_id_col = BarangayInfo.__table__.c.user_id
    fks = list(user_id_col.foreign_keys)

    assert len(fks) == 1, "BarangayInfo.user_id must have exactly 1 ForeignKey"
    fk = fks[0]

    assert fk.use_alter is True, (
        "BarangayInfo.user_id ForeignKey must set use_alter=True to break cyclic table dependency with USER"
    )
    assert fk.name is not None and len(fk.name) > 0, (
        f"BarangayInfo.user_id ForeignKey must define a constraint name when use_alter=True, got {fk.name!r}"
    )


# ───────────────────────────────────────────────────────────────
# F7: Python 3.12+ Datetime Modernization
# ───────────────────────────────────────────────────────────────

def test_zero_occurrences_of_datetime_utcnow_in_models():
    """Verify zero occurrences of deprecated datetime.utcnow across all models files."""
    models_dir = Path(__file__).resolve().parent.parent / "backend" / "app" / "models"
    assert models_dir.exists() and models_dir.is_dir(), f"Models directory not found at {models_dir}"

    pattern = re.compile(r"\bdatetime\.utcnow\b")
    violations: list[str] = []

    for file_path in models_dir.glob("*.py"):
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_num, line in enumerate(lines, start=1):
            if pattern.search(line):
                violations.append(f"{file_path.name}:{line_num}: {line.strip()}")

    assert not violations, (
        f"Found {len(violations)} occurrences of deprecated 'datetime.utcnow' in models:\n"
        + "\n".join(f"  {v}" for v in violations)
    )
