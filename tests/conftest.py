"""
Test configuration and fixtures for AI Agent Memory System tests.
"""
import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Generator
import pytest


@pytest.fixture
def temp_memory_dir() -> Generator[str, None, None]:
    """Create a temporary memory directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        memory_dir = os.path.join(temp_dir, "test_memory")
        os.makedirs(os.path.join(memory_dir, "project_memory"))
        os.makedirs(os.path.join(memory_dir, "learning_memory"))
        os.makedirs(os.path.join(memory_dir, "session_logs"))
        os.makedirs(os.path.join(memory_dir, "orc_data"))
        yield memory_dir


@pytest.fixture
def sample_active_memory() -> Dict[str, Any]:
    """Sample active memory data for testing."""
    return {
        "last_updated": "2024-08-21T12:00:00Z",
        "current_session": {
            "project": "Test Project",
            "user": "test_user",
            "workspace": "/tmp/test",
            "session_focus": "Testing memory system",
            "key_accomplishments": ["Setup test environment"]
        },
        "user_preferences": {
            "collaboration_style": "Test-driven development",
            "technical_approach": "Comprehensive testing",
            "communication_style": "Clear and concise",
            "preferred_formats": {
                "documentation": "markdown",
                "code_style": "pep8"
            }
        }
    }


@pytest.fixture
def sample_project_memory() -> Dict[str, Any]:
    """Sample project memory data for testing."""
    return {
        "project_name": "Test Application",
        "project_type": "web application",
        "start_date": "2024-08-01",
        "status": "in development",
        "architecture": {
            "frontend": "React",
            "backend": "Python FastAPI",
            "database": "PostgreSQL",
            "deployment": "Docker containers"
        },
        "key_decisions": {
            "technology_choices": "React for component reusability",
            "architecture_patterns": "Microservices architecture",
            "important_tradeoffs": "Performance vs simplicity"
        },
        "current_progress": {
            "completed_features": ["User authentication", "Basic API"],
            "in_progress": ["Frontend components"],
            "next_priorities": ["Testing", "Deployment"]
        }
    }


@pytest.fixture
def memory_utils_module(temp_memory_dir, monkeypatch):
    """Mock memory_utils module with temporary directory."""
    # Patch the memory directory constant
    from pathlib import Path
    monkeypatch.setattr("utils.memory_utils.MEMORY_DIR", Path(temp_memory_dir))
    
    # Import after patching
    import utils.memory_utils as memory_utils
    return memory_utils


@pytest.fixture
def populated_memory_dir(temp_memory_dir, sample_active_memory, sample_project_memory):
    """Create a populated memory directory with sample data."""
    # Create active memory
    with open(os.path.join(temp_memory_dir, "active_memory.json"), "w") as f:
        json.dump(sample_active_memory, f, indent=2)
    
    # Create project memory
    project_file = os.path.join(temp_memory_dir, "project_memory", "test_project.json")
    with open(project_file, "w") as f:
        json.dump(sample_project_memory, f, indent=2)
    
    # Create learning memory
    learning_data = {
        "effective_patterns": {
            "test_pattern": {
                "pattern": "Test-driven development",
                "effectiveness": "High",
                "description": "Writing tests first improves code quality"
            }
        }
    }
    learning_file = os.path.join(temp_memory_dir, "learning_memory", "insights.json")
    with open(learning_file, "w") as f:
        json.dump(learning_data, f, indent=2)
    
    return temp_memory_dir


@pytest.fixture(scope="session")
def test_templates_dir():
    """Path to test templates directory."""
    return Path(__file__).parent / "templates"


class MockDatetime:
    """Mock datetime class for consistent testing."""
    
    @staticmethod
    def utcnow():
        """Return a fixed datetime for testing."""
        from datetime import datetime
        return datetime(2024, 8, 21, 12, 0, 0)
    
    @staticmethod
    def now():
        """Return a fixed datetime for testing."""
        from datetime import datetime
        return datetime(2024, 8, 21, 12, 0, 0)


@pytest.fixture
def mock_datetime(monkeypatch):
    """Mock datetime.utcnow() for consistent testing."""
    monkeypatch.setattr("utils.memory_utils.datetime", MockDatetime)
    return MockDatetime

