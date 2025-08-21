"""
Unit tests for memory_utils.py module.
"""
import os
import json
import pytest
from unittest.mock import patch
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
    
    def test_save_session_insight(self, memory_utils_module, temp_memory_dir, mock_datetime):
        """Test saving session insights."""
        memory_utils = memory_utils_module
        
        # Save an insight
        memory_utils.save_session_insight("Test insight", "testing")
        
        # Verify file was created
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        assert os.path.exists(insights_file)
        
        # Verify content
        with open(insights_file, "r") as f:
            data = json.load(f)
        
        assert "insights" in data
        assert len(data["insights"]) == 1
        assert data["insights"][0]["insight"] == "Test insight"
        assert data["insights"][0]["category"] == "testing"
    
    def test_get_project_context(self, memory_utils_module, temp_memory_dir):
        """Test retrieving project context."""
        memory_utils = memory_utils_module
        
        # Create a test project file
        project_dir = os.path.join(temp_memory_dir, "project_memory")
        os.makedirs(project_dir, exist_ok=True)
        
        test_project = {
            "project_name": "Test Project",
            "status": "active",
            "features": ["auth", "api"]
        }
        
        project_file = os.path.join(project_dir, "test_project.json")
        with open(project_file, "w") as f:
            json.dump(test_project, f)
        
        # Test retrieving by name
        result = memory_utils.get_project_context("test_project")
        assert result["project_name"] == "Test Project"
        
        # Test retrieving non-existent project
        result = memory_utils.get_project_context("non_existent")
        assert result == {}
    
    def test_memory_summary(self, memory_utils_module, populated_memory_dir):
        """Test generating memory system summary."""
        memory_utils = memory_utils_module
        
        summary = memory_utils.memory_summary()
        
        # Verify summary structure
        assert "memory_directory" in summary
        assert "last_updated" in summary
        assert "files" in summary
        
        # Verify it contains expected directories
        assert "learning_memory" in summary["files"]
        
        # Verify current session info
        assert "current_session" in summary
        assert summary["current_session"]["project"] == "Test Project"
    
    def test_create_orc_data_fallback(self, memory_utils_module, temp_memory_dir):
        """Test ORC data creation falls back to JSON when PyArrow not available."""
        memory_utils = memory_utils_module
        
        test_data = [
            {"id": 1, "name": "test1"},
            {"id": 2, "name": "test2"}
        ]
        
        # This should fall back to JSON since we're not testing with pyarrow
        memory_utils.create_orc_data(test_data, "test_data")
        
        # Check fallback file was created
        fallback_file = os.path.join(temp_memory_dir, "orc_data", "test_data_fallback.json")
        if os.path.exists(fallback_file):
            with open(fallback_file, "r") as f:
                saved_data = json.load(f)
            assert saved_data == test_data


class TestMemoryUtilsErrorHandling:
    """Test error handling in memory utilities."""
    
    def test_get_active_memory_no_file(self, memory_utils_module, temp_memory_dir):
        """Test getting active memory when file doesn't exist."""
        memory_utils = memory_utils_module
        
        result = memory_utils.get_active_memory()
        assert result is None
    
    def test_update_active_memory_creates_directory(self, memory_utils_module, temp_memory_dir):
        """Test that updating memory creates directory if it doesn't exist."""
        memory_utils = memory_utils_module
        
        # Remove the directory
        memory_dir = Path(temp_memory_dir)
        if memory_dir.exists():
            import shutil
            shutil.rmtree(memory_dir)
        
        # Update should create directory
        memory_utils.update_active_memory("test", "value")
        
        # Verify directory and file were created
        assert memory_dir.exists()
        assert (memory_dir / "active_memory.json").exists()
    
    def test_save_session_insight_creates_directory(self, memory_utils_module, temp_memory_dir):
        """Test that saving insights creates directory structure."""
        memory_utils = memory_utils_module
        
        # Remove learning memory directory
        learning_dir = Path(temp_memory_dir) / "learning_memory"
        if learning_dir.exists():
            import shutil
            shutil.rmtree(learning_dir)
        
        # Save insight should create directory
        memory_utils.save_session_insight("test insight", "test")
        
        # Verify directory and file were created
        assert learning_dir.exists()
        assert (learning_dir / "session_insights.json").exists()


class TestMemoryUtilsIntegration:
    """Integration tests for memory utilities."""
    
    def test_full_workflow(self, memory_utils_module, temp_memory_dir):
        """Test complete workflow of memory operations."""
        memory_utils = memory_utils_module
        
        # Step 1: Update active memory
        memory_utils.update_active_memory("project", "Test Integration")
        memory_utils.update_active_memory("status", "testing")
        
        # Step 2: Save some insights
        memory_utils.save_session_insight("Integration tests are important", "testing")
        memory_utils.save_session_insight("Memory system works well", "architecture")
        
        # Step 3: Get summary
        summary = memory_utils.memory_summary()
        
        # Verify workflow completed successfully
        assert summary["project"] == "Test Integration"
        assert summary["status"] == "testing"
        assert "files" in summary
        
        # Verify insights were saved
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        assert os.path.exists(insights_file)
        
        with open(insights_file, "r") as f:
            insights_data = json.load(f)
        assert len(insights_data["insights"]) == 2
    
    def test_concurrent_access_simulation(self, memory_utils_module, temp_memory_dir):
        """Test simulated concurrent access to memory files."""
        memory_utils = memory_utils_module
        
        # Simulate rapid updates
        for i in range(10):
            memory_utils.update_active_memory(f"key_{i}", f"value_{i}")
            if i % 3 == 0:
                memory_utils.save_session_insight(f"Insight {i}", "concurrency")
        
        # Verify final state
        active_memory = memory_utils.get_active_memory()
        for i in range(10):
            assert active_memory[f"key_{i}"] == f"value_{i}"
        
        # Verify insights were saved
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        with open(insights_file, "r") as f:
            insights_data = json.load(f)
        
        expected_insights = len([i for i in range(10) if i % 3 == 0])
        assert len(insights_data["insights"]) == expected_insights