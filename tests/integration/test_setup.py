"""
Integration tests for setup.sh script and complete system initialization.
"""
import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
import pytest


class TestSetupScript:
    """Test the setup.sh script functionality."""
    
    def test_setup_script_execution(self, temp_memory_dir, monkeypatch):
        """Test that setup script runs successfully."""
        # Change to temporary directory for testing
        original_home = os.environ.get("HOME", "")
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        # Get the setup script path
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        
        # Run setup script
        result = subprocess.run(
            ["bash", str(setup_script)],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        
        # Check that script executed successfully
        assert result.returncode == 0, f"Setup failed: {result.stderr}"
        assert "Setup complete!" in result.stdout
        
        # Verify directory structure was created
        memory_dir = os.path.join(temp_memory_dir, "claude_memory")
        assert os.path.exists(memory_dir)
        assert os.path.exists(os.path.join(memory_dir, "project_memory"))
        assert os.path.exists(os.path.join(memory_dir, "learning_memory"))
        assert os.path.exists(os.path.join(memory_dir, "session_logs"))
        assert os.path.exists(os.path.join(memory_dir, "orc_data"))
        
        # Verify files were created
        assert os.path.exists(os.path.join(memory_dir, "active_memory.json"))
        assert os.path.exists(os.path.join(memory_dir, "memory_utils.py"))
    
    def test_setup_creates_valid_active_memory(self, temp_memory_dir, monkeypatch):
        """Test that setup creates a valid active memory file."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        
        subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        # Check active memory file
        active_memory_file = os.path.join(temp_memory_dir, "claude_memory", "active_memory.json")
        with open(active_memory_file, "r") as f:
            data = json.load(f)
        
        # Verify structure
        assert "last_updated" in data
        assert "current_session" in data
        assert "user_preferences" in data
        
        # Verify template values are preserved
        assert data["current_session"]["project"] == "Replace with your project name"
        assert data["user_preferences"]["collaboration_style"] == "How you like to work (detailed/concise/step-by-step)"
    
    def test_setup_creates_learning_memory(self, temp_memory_dir, monkeypatch):
        """Test that setup creates initial learning memory."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        
        subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        # Check learning memory file
        learning_file = os.path.join(
            temp_memory_dir, "claude_memory", "learning_memory", "collaboration_patterns.json"
        )
        with open(learning_file, "r") as f:
            data = json.load(f)
        
        assert "effective_patterns" in data
        assert "session_continuity" in data["effective_patterns"]
    
    def test_setup_installs_utilities(self, temp_memory_dir, monkeypatch):
        """Test that setup installs memory utilities."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        
        subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        # Check memory utilities
        utils_file = os.path.join(temp_memory_dir, "claude_memory", "memory_utils.py")
        assert os.path.exists(utils_file)
        assert os.access(utils_file, os.X_OK)  # Should be executable
    
    def test_setup_idempotent(self, temp_memory_dir, monkeypatch):
        """Test that running setup multiple times is safe."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        
        # Run setup twice
        result1 = subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        result2 = subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        assert result1.returncode == 0
        assert result2.returncode == 0
        
        # Files should still exist and be valid
        active_memory_file = os.path.join(temp_memory_dir, "claude_memory", "active_memory.json")
        with open(active_memory_file, "r") as f:
            data = json.load(f)
        
        assert "current_session" in data


class TestFullSystemIntegration:
    """Test complete system functionality after setup."""
    
    def test_memory_system_after_setup(self, temp_memory_dir, monkeypatch):
        """Test that memory system works correctly after setup."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        # Run setup
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        # Import and test memory utilities
        memory_dir = os.path.join(temp_memory_dir, "claude_memory")
        import sys
        sys.path.insert(0, memory_dir)
        
        # Patch the memory utilities to use our test directory
        monkeypatch.setattr("memory_utils.MEMORY_DIR", memory_dir)
        
        import memory_utils
        
        # Test basic operations
        memory_utils.update_active_memory("test_key", "test_value")
        result = memory_utils.get_active_memory("test_key")
        assert result == "test_value"
        
        # Test project status
        test_project = {"name": "Test Project", "status": "active"}
        memory_utils.save_project_status(test_project)
        saved_project = memory_utils.get_project_status()
        assert saved_project["name"] == "Test Project"
    
    def test_template_functionality(self, temp_memory_dir):
        """Test that templates are functional and valid."""
        repo_root = Path(__file__).parent.parent.parent
        
        # Test active memory template
        active_template = repo_root / "templates" / "active_memory_template.json"
        with open(active_template, "r") as f:
            template_data = json.load(f)
        
        # Verify required fields
        assert "current_session" in template_data
        assert "user_preferences" in template_data
        assert "project" in template_data["current_session"]
        
        # Test project memory template
        project_template = repo_root / "templates" / "project_memory_template.json"
        with open(project_template, "r") as f:
            project_data = json.load(f)
        
        assert "project_name" in project_data
        assert "architecture" in project_data
        assert "current_progress" in project_data
    
    def test_examples_validity(self, temp_memory_dir):
        """Test that example files are valid and complete."""
        repo_root = Path(__file__).parent.parent.parent
        examples_dir = repo_root / "examples"
        
        for example_file in examples_dir.glob("*.json"):
            with open(example_file, "r") as f:
                example_data = json.load(f)
            
            # Basic structure validation
            assert "project_name" in example_data
            assert "project_type" in example_data
            
            # Verify realistic content
            assert len(example_data["project_name"]) > 0
            assert example_data["project_name"] != "placeholder"


class TestDocumentationIntegration:
    """Test that documentation examples actually work."""
    
    def test_readme_quick_start(self, temp_memory_dir, monkeypatch):
        """Test that README quick start instructions work."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        # Simulate the quick start process
        memory_dir = os.path.join(temp_memory_dir, "claude_memory")
        os.makedirs(os.path.join(memory_dir, "project_memory"))
        os.makedirs(os.path.join(memory_dir, "learning_memory"))
        os.makedirs(os.path.join(memory_dir, "session_logs"))
        os.makedirs(os.path.join(memory_dir, "orc_data"))
        
        # Copy template as described in README
        repo_root = Path(__file__).parent.parent.parent
        template_file = repo_root / "templates" / "active_memory_template.json"
        active_file = os.path.join(memory_dir, "active_memory.json")
        shutil.copy(template_file, active_file)
        
        # Verify the setup works
        assert os.path.exists(active_file)
        with open(active_file, "r") as f:
            data = json.load(f)
        
        assert "current_session" in data
    
    def test_use_case_examples_completeness(self):
        """Test that use case examples in documentation are complete."""
        repo_root = Path(__file__).parent.parent.parent
        use_cases_file = repo_root / "docs" / "USE_CASES.md"
        
        with open(use_cases_file, "r") as f:
            content = f.read()
        
        # Verify key sections exist
        assert "Software Development Projects" in content
        assert "Research Projects" in content
        assert "Ice Tea Identity Verification Platform" in content
        assert "270+ tests" in content  # Reference to our proven results
        
        # Verify examples are realistic
        assert "React" in content or "FastAPI" in content  # Real technology references


class TestErrorRecovery:
    """Test system behavior under error conditions."""
    
    def test_partial_setup_recovery(self, temp_memory_dir, monkeypatch):
        """Test recovery from partially completed setup."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        # Create partial directory structure
        memory_dir = os.path.join(temp_memory_dir, "claude_memory")
        os.makedirs(os.path.join(memory_dir, "project_memory"))
        # Missing other directories
        
        # Run setup - should complete successfully
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        result = subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        assert result.returncode == 0
        
        # Verify all directories now exist
        assert os.path.exists(os.path.join(memory_dir, "learning_memory"))
        assert os.path.exists(os.path.join(memory_dir, "session_logs"))
        assert os.path.exists(os.path.join(memory_dir, "orc_data"))
    
    def test_corrupted_file_handling(self, temp_memory_dir, monkeypatch):
        """Test handling of corrupted memory files."""
        monkeypatch.setenv("HOME", temp_memory_dir)
        
        # Run setup first
        repo_root = Path(__file__).parent.parent.parent
        setup_script = repo_root / "setup.sh"
        subprocess.run(["bash", str(setup_script)], cwd=str(repo_root))
        
        # Corrupt the active memory file
        memory_dir = os.path.join(temp_memory_dir, "claude_memory")
        active_file = os.path.join(memory_dir, "active_memory.json")
        with open(active_file, "w") as f:
            f.write("corrupted json content")
        
        # Add memory_dir to Python path and import utilities
        import sys
        sys.path.insert(0, memory_dir)
        
        # Patch the memory directory
        monkeypatch.setattr("memory_utils.MEMORY_DIR", memory_dir)
        
        import memory_utils
        
        # Should handle corrupted file gracefully
        result = memory_utils.get_active_memory()
        assert result == {}  # Should return empty dict for corrupted file
        
        # Should be able to update and recover
        memory_utils.update_active_memory("recovery_test", "success")
        recovered = memory_utils.get_active_memory("recovery_test")
        assert recovered == "success"
