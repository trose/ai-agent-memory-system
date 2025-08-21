"""
Integration tests for AI agent memory system initialization using templates.
"""
import os
import json
import tempfile
import shutil
from pathlib import Path
import pytest


class TestMemorySystemTemplates:
    """Test that templates and utilities are accessible for AI agent setup."""
    
    def test_templates_exist_and_valid(self):
        """Test that all required templates exist and are valid JSON."""
        repo_root = Path(__file__).parent.parent.parent
        templates_dir = repo_root / "templates"
        
        # Verify templates directory exists
        assert templates_dir.exists(), "Templates directory not found"
        
        # Test active memory template
        active_template = templates_dir / "active_memory_template.json"
        assert active_template.exists(), "Active memory template not found"
        
        with open(active_template, 'r') as f:
            template_data = json.load(f)
            assert "current_session" in template_data
            assert "user_preferences" in template_data
            assert "current_context" in template_data
            assert "important_insights" in template_data
        
        # Test project memory template
        project_template = templates_dir / "project_memory_template.json"
        assert project_template.exists(), "Project memory template not found"
        
        with open(project_template, 'r') as f:
            project_data = json.load(f)
            assert isinstance(project_data, dict), "Project template should be valid JSON object"
    
    def test_memory_utils_exists_and_importable(self):
        """Test that memory utilities exist and can be imported."""
        repo_root = Path(__file__).parent.parent.parent
        utils_file = repo_root / "utils" / "memory_utils.py"
        
        assert utils_file.exists(), "Memory utils file not found"
        
        # Test that it's valid Python by attempting to compile
        with open(utils_file, 'r') as f:
            content = f.read()
            compile(content, str(utils_file), 'exec')
    
    def test_ai_agent_memory_creation(self, temp_memory_dir):
        """Test simulated AI agent memory system creation from templates."""
        # Simulate what an AI agent would do
        repo_root = Path(__file__).parent.parent.parent
        memory_dir = Path(temp_memory_dir) / "ai_memory"
        
        # Create directory structure
        memory_dir.mkdir(exist_ok=True)
        (memory_dir / "project_memory").mkdir(exist_ok=True)
        (memory_dir / "learning_memory").mkdir(exist_ok=True)
        (memory_dir / "session_logs").mkdir(exist_ok=True)
        
        # Copy template to active memory
        template_file = repo_root / "templates" / "active_memory_template.json"
        active_memory_file = memory_dir / "active_memory.json"
        shutil.copy2(template_file, active_memory_file)
        
        # Copy utilities
        utils_source = repo_root / "utils" / "memory_utils.py"
        utils_dest = memory_dir / "memory_utils.py"
        shutil.copy2(utils_source, utils_dest)
        
        # Verify setup worked
        assert active_memory_file.exists()
        assert utils_dest.exists()
        assert (memory_dir / "project_memory").exists()
        assert (memory_dir / "learning_memory").exists()
        assert (memory_dir / "session_logs").exists()
        
        # Verify active memory is valid
        with open(active_memory_file, 'r') as f:
            data = json.load(f)
            assert "current_session" in data
            assert "user_preferences" in data
    
    def test_template_structure_completeness(self):
        """Test that templates contain all necessary fields for AI agent operation."""
        repo_root = Path(__file__).parent.parent.parent
        
        # Test active memory template completeness
        with open(repo_root / "templates" / "active_memory_template.json", 'r') as f:
            active_template = json.load(f)
        
        # Verify essential fields exist
        assert "last_updated" in active_template
        assert "current_session" in active_template
        assert "user_preferences" in active_template
        assert "current_context" in active_template
        assert "important_insights" in active_template
        
        # Verify current_session has required fields
        session = active_template["current_session"]
        assert "project" in session
        assert "user" in session
        assert "workspace" in session
        
        # Verify user_preferences has collaboration fields
        prefs = active_template["user_preferences"]
        assert "collaboration_style" in prefs
        assert "technical_approach" in prefs
        assert "communication_style" in prefs


class TestMemorySystemIntegration:
    """Test complete memory system functionality after template-based setup."""
    
    def test_memory_system_full_workflow(self, temp_memory_dir):
        """Test complete memory workflow using templates."""
        repo_root = Path(__file__).parent.parent.parent
        memory_dir = Path(temp_memory_dir) / "ai_memory"
        
        # Simulate AI agent setup
        memory_dir.mkdir(exist_ok=True)
        (memory_dir / "project_memory").mkdir(exist_ok=True)
        (memory_dir / "learning_memory").mkdir(exist_ok=True)
        (memory_dir / "session_logs").mkdir(exist_ok=True)
        
        # Copy templates and utilities
        shutil.copy2(
            repo_root / "templates" / "active_memory_template.json",
            memory_dir / "active_memory.json"
        )
        shutil.copy2(
            repo_root / "utils" / "memory_utils.py",
            memory_dir / "memory_utils.py"
        )
        
        # Test that we can read the templates and they're valid
        with open(memory_dir / "active_memory.json", 'r') as f:
            active_data = json.load(f)
            assert "current_session" in active_data
            assert "user_preferences" in active_data
        
        # Test that utilities file exists and is valid Python
        with open(memory_dir / "memory_utils.py", 'r') as f:
            utils_content = f.read()
            compile(utils_content, str(memory_dir / "memory_utils.py"), 'exec')
        
        # Verify directory structure is complete
        assert (memory_dir / "project_memory").exists()
        assert (memory_dir / "learning_memory").exists()
        assert (memory_dir / "session_logs").exists()
    
    def test_template_based_project_memory(self, temp_memory_dir):
        """Test project memory functionality using templates."""
        repo_root = Path(__file__).parent.parent.parent
        memory_dir = Path(temp_memory_dir) / "ai_memory"
        
        # Setup memory system
        memory_dir.mkdir(exist_ok=True)
        (memory_dir / "project_memory").mkdir(exist_ok=True)
        
        # Copy project template
        shutil.copy2(
            repo_root / "templates" / "project_memory_template.json",
            memory_dir / "project_memory" / "test_project.json"
        )
        
        # Verify template was copied and is valid
        project_file = memory_dir / "project_memory" / "test_project.json"
        assert project_file.exists()
        
        with open(project_file, 'r') as f:
            project_data = json.load(f)
            assert isinstance(project_data, dict)