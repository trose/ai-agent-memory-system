"""
Unit tests for memory_utils.py module.
"""
import os
import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path


class TestMemoryUtils:
    """Test cases for memory utility functions."""
    
    def test_update_active_memory(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test updating active memory with new key-value pairs."""
        memory_utils = memory_utils_module
        
        # Test initial update
        memory_utils.update_active_memory("test_key", "test_value")
        
        # Verify file was created and contains correct data
        active_file = os.path.join(temp_memory_dir, "active_memory.json")
        assert os.path.exists(active_file)
        
        with open(active_file, "r") as f:
            data = json.load(f)
        
        assert data["test_key"] == "test_value"
        assert "last_updated" in data
        assert data["last_updated"] == "2024-08-21T12:00:00"
    
    def test_get_active_memory(self, memory_utils_module, populated_memory_dir):
        """Test retrieving active memory data."""
        memory_utils = memory_utils_module
        
        # Test getting all memory
        all_memory = memory_utils.get_active_memory()
        assert all_memory["current_session"]["project"] == "Test Project"
        
        # Test getting specific key
        session = memory_utils.get_active_memory("current_session")
        assert session["project"] == "Test Project"
        
        # Test getting non-existent key
        result = memory_utils.get_active_memory("non_existent")
        assert result is None
    
    def test_save_project_status(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test saving project status data."""
        memory_utils = memory_utils_module
        
        test_data = {
            "project_name": "New Project",
            "status": "active",
            "architecture": {"backend": "FastAPI"}
        }
        
        memory_utils.save_project_status(test_data)
        
        # Verify file was created
        project_file = os.path.join(temp_memory_dir, "project_memory", "ice_tea_current.json")
        assert os.path.exists(project_file)
        
        with open(project_file, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["project_name"] == "New Project"
        assert saved_data["status"] == "active"
        assert saved_data["last_updated"] == "2024-08-21T12:00:00"
    
    def test_get_project_status(self, memory_utils_module, populated_memory_dir):
        """Test retrieving project status."""
        memory_utils = memory_utils_module
        
        # First save a project status
        test_data = {"project_name": "Test Project", "status": "active"}
        memory_utils.save_project_status(test_data)
        
        # Then retrieve it
        status = memory_utils.get_project_status()
        assert status["project_name"] == "Test Project"
        assert status["status"] == "active"
    
    def test_save_session_insight(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test saving session insights."""
        memory_utils = memory_utils_module
        
        memory_utils.save_session_insight("Test insight", "test_category")
        
        # Verify file was created
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "technical_insights.json")
        assert os.path.exists(insights_file)
        
        with open(insights_file, "r") as f:
            data = json.load(f)
        
        assert "test_category" in data
        assert len(data["test_category"]) == 1
        assert data["test_category"][0]["insight"] == "Test insight"
        assert data["test_category"][0]["timestamp"] == "2024-08-21T12:00:00"
    
    def test_get_session_insights(self, memory_utils_module, temp_memory_dir):
        """Test retrieving session insights."""
        memory_utils = memory_utils_module
        
        # Save some insights first
        memory_utils.save_session_insight("Insight 1", "category1")
        memory_utils.save_session_insight("Insight 2", "category2")
        
        # Test getting all insights
        all_insights = memory_utils.get_session_insights()
        assert "category1" in all_insights
        assert "category2" in all_insights
        
        # Test getting specific category
        category1_insights = memory_utils.get_session_insights("category1")
        assert "category1" in category1_insights
        assert len(category1_insights["category1"]) == 1
        assert category1_insights["category1"][0]["insight"] == "Insight 1"
    
    def test_log_session_activity(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test logging session activities."""
        memory_utils = memory_utils_module
        
        memory_utils.log_session_activity("Test activity", "test_session.md")
        
        # Verify file was created
        log_file = os.path.join(temp_memory_dir, "session_logs", "test_session.md")
        assert os.path.exists(log_file)
        
        with open(log_file, "r") as f:
            content = f.read()
        
        assert "Test activity" in content
        assert "2024-08-21T12:00:00" in content
    
    def test_get_memory_system_overview(self, memory_utils_module, populated_memory_dir):
        """Test getting memory system overview."""
        memory_utils = memory_utils_module
        
        overview = memory_utils.get_memory_system_overview()
        
        assert "memory_directory" in overview
        assert "files" in overview
        assert "current_session" in overview
        assert "user_preferences" in overview
        
        # Check that it includes file listings
        assert "project_memory" in overview["files"]
        assert "learning_memory" in overview["files"]
        assert isinstance(overview["files"]["project_memory"], list)
    
    def test_load_json_nonexistent_file(self, memory_utils_module, temp_memory_dir):
        """Test loading JSON from non-existent file returns empty dict."""
        memory_utils = memory_utils_module
        
        result = memory_utils._load_json(os.path.join(temp_memory_dir, "nonexistent.json"))
        assert result == {}
    
    def test_save_json_creates_directory(self, memory_utils_module, temp_memory_dir):
        """Test that _save_json creates directories if they don't exist."""
        memory_utils = memory_utils_module
        
        new_dir = os.path.join(temp_memory_dir, "new_directory")
        new_file = os.path.join(new_dir, "test.json")
        
        test_data = {"key": "value"}
        memory_utils._save_json(new_file, test_data)
        
        assert os.path.exists(new_dir)
        assert os.path.exists(new_file)
        
        with open(new_file, "r") as f:
            saved_data = json.load(f)
        
        assert saved_data["key"] == "value"


class TestMemoryUtilsErrorHandling:
    """Test error handling in memory utilities."""
    
    def test_invalid_json_handling(self, memory_utils_module, temp_memory_dir):
        """Test handling of invalid JSON files."""
        memory_utils = memory_utils_module
        
        # Create a file with invalid JSON
        invalid_file = os.path.join(temp_memory_dir, "invalid.json")
        with open(invalid_file, "w") as f:
            f.write("invalid json content")
        
        # Should return empty dict for invalid JSON
        result = memory_utils._load_json(invalid_file)
        assert result == {}
    
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_permission_error_handling(self, mock_file, memory_utils_module):
        """Test handling of permission errors."""
        memory_utils = memory_utils_module
        
        with pytest.raises(PermissionError):
            memory_utils.update_active_memory("key", "value")
    
    def test_directory_creation_permissions(self, memory_utils_module, temp_memory_dir):
        """Test handling when directory cannot be created."""
        memory_utils = memory_utils_module
        
        # Create a file where we want to create a directory
        blocking_file = os.path.join(temp_memory_dir, "blocked")
        with open(blocking_file, "w") as f:
            f.write("blocking content")
        
        # Try to create a directory where the file exists
        with pytest.raises(OSError):
            memory_utils._save_json(os.path.join(blocking_file, "test.json"), {})


class TestMemoryUtilsIntegration:
    """Integration tests for memory utilities."""
    
    def test_full_workflow(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test a complete workflow of memory operations."""
        memory_utils = memory_utils_module
        
        # 1. Update active memory
        memory_utils.update_active_memory("current_session", {
            "project": "Integration Test",
            "focus": "Testing complete workflow"
        })
        
        # 2. Save project status
        memory_utils.save_project_status({
            "project_name": "Integration Test Project",
            "status": "testing",
            "key_features": ["memory system", "testing"]
        })
        
        # 3. Save insights
        memory_utils.save_session_insight("Integration testing is important", "testing")
        memory_utils.save_session_insight("Memory system works well", "memory")
        
        # 4. Log activity
        memory_utils.log_session_activity("Completed integration test")
        
        # 5. Verify everything is accessible
        overview = memory_utils.get_memory_system_overview()
        
        assert overview["current_session"]["project"] == "Integration Test"
        
        project_status = memory_utils.get_project_status()
        assert project_status["project_name"] == "Integration Test Project"
        
        insights = memory_utils.get_session_insights()
        assert "testing" in insights
        assert "memory" in insights
        
        # Verify files exist
        assert len(overview["files"]["project_memory"]) > 0
        assert len(overview["files"]["learning_memory"]) > 0
        assert len(overview["files"]["session_logs"]) > 0
    
    def test_concurrent_access_simulation(self, memory_utils_module, temp_memory_dir):
        """Test behavior under simulated concurrent access."""
        memory_utils = memory_utils_module
        
        # Simulate multiple rapid updates
        for i in range(10):
            memory_utils.update_active_memory(f"key_{i}", f"value_{i}")
            memory_utils.save_session_insight(f"Insight {i}", "concurrent")
        
        # Verify all updates were saved
        active_memory = memory_utils.get_active_memory()
        for i in range(10):
            assert active_memory[f"key_{i}"] == f"value_{i}"
        
        insights = memory_utils.get_session_insights("concurrent")
        assert len(insights["concurrent"]) == 10

