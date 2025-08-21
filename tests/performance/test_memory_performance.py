"""
Performance tests for memory system operations.
"""
import os
import json
import tempfile
import pytest
from pathlib import Path


class TestMemoryPerformance:
    """Performance benchmarks for memory operations."""
    
    def test_active_memory_update_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark active memory update performance."""
        memory_utils = memory_utils_module
        
        def update_memory():
            memory_utils.update_active_memory("test_key", "test_value")
        
        result = benchmark(update_memory)
        
        # Verify the operation worked
        assert memory_utils.get_active_memory("test_key") == "test_value"
    
    def test_large_memory_load_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark loading large memory files."""
        memory_utils = memory_utils_module
        
        # Create a large memory file
        large_data = {
            f"key_{i}": f"value_{i}_{'x' * 100}" for i in range(1000)
        }
        large_data["metadata"] = {"size": "large", "entries": 1000}
        
        memory_file = os.path.join(temp_memory_dir, "large_memory.json")
        with open(memory_file, "w") as f:
            json.dump(large_data, f)
        
        def load_large_memory():
            with open(memory_file, 'r') as f:
                return json.load(f)
        
        result = benchmark(load_large_memory)
        assert len(result) == 1001  # 1000 entries + metadata
    
    def test_session_insights_batch_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark batch session insight operations."""
        memory_utils = memory_utils_module
        
        # Clear any existing insights file and directory
        learning_dir = os.path.join(temp_memory_dir, "learning_memory")
        if os.path.exists(learning_dir):
            import shutil
            shutil.rmtree(learning_dir)
        
        insights = [
            f"Performance insight {i}: Optimization technique {i} works well"
            for i in range(100)
        ]
        
        def batch_save_insights():
            for i, insight in enumerate(insights):
                memory_utils.save_session_insight(insight, f"category_{i % 10}")
        
        benchmark(batch_save_insights)
        
        # Verify insights were saved (benchmark runs multiple times, so just check file exists)
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        assert os.path.exists(insights_file)
        
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        # Benchmark runs multiple times, so we have more than 100 insights
        assert len(all_insights["insights"]) >= 100
    
    def test_memory_overview_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark memory system overview generation."""
        memory_utils = memory_utils_module
        
        # Add some data to make the overview more realistic
        for i in range(20):
            memory_utils.save_session_insight(f"Insight {i}", f"category_{i % 5}")
            memory_utils.update_active_memory(f"key_{i}", f"value_{i}")
        
        def get_overview():
            return memory_utils.memory_summary()
        
        result = benchmark(get_overview)
        
        # Verify overview contains expected data
        assert "memory_directory" in result
        assert "files" in result


class TestMemoryScalability:
    """Test memory system behavior with large datasets."""
    
    def test_large_active_memory(self, memory_utils_module, temp_memory_dir):
        """Test handling of large active memory data."""
        memory_utils = memory_utils_module
        
        # Create large active memory
        for i in range(1000):
            memory_utils.update_active_memory(f"large_key_{i}", f"large_value_{i}_{'x' * 50}")
        
        # Test retrieval performance
        all_memory = memory_utils.get_active_memory()
        assert len([k for k in all_memory.keys() if k.startswith("large_key_")]) == 1000
        
        # Test specific key retrieval
        result = memory_utils.get_active_memory("large_key_500")
        assert "large_value_500" in result
    
    def test_many_insights_performance(self, memory_utils_module, temp_memory_dir):
        """Test performance with many session insights."""
        memory_utils = memory_utils_module
        
        # Save many insights across different categories
        categories = ["performance", "architecture", "testing", "deployment", "optimization"]
        
        for category in categories:
            for i in range(200):  # 1000 total insights
                insight = f"Insight {i} for {category}: This is a detailed insight about {category} optimization and best practices."
                memory_utils.save_session_insight(insight, category)
        
        # Test that file was created and contains data
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        assert os.path.exists(insights_file)
        
        with open(insights_file, 'r') as f:
            all_insights = json.load(f)
        assert len(all_insights["insights"]) == 1000
    
    def test_concurrent_memory_operations(self, memory_utils_module, temp_memory_dir):
        """Test simulated concurrent memory operations."""
        memory_utils = memory_utils_module
        
        # Simulate rapid alternating operations
        for i in range(100):
            # Update active memory
            memory_utils.update_active_memory(f"concurrent_key_{i}", f"value_{i}")
            
            # Save insight
            memory_utils.save_session_insight(f"Concurrent insight {i}", "concurrency")
        
        # Verify final state is consistent
        active_memory = memory_utils.get_active_memory()
        for i in range(100):
            assert active_memory[f"concurrent_key_{i}"] == f"value_{i}"
        
        # Verify insights were saved
        insights_file = os.path.join(temp_memory_dir, "learning_memory", "session_insights.json")
        with open(insights_file, 'r') as f:
            insights_data = json.load(f)
        assert len(insights_data["insights"]) == 100


class TestMemoryEfficiency:
    """Test memory usage efficiency of the system."""
    
    def test_json_file_size_efficiency(self, memory_utils_module, temp_memory_dir):
        """Test that JSON files don't grow unnecessarily large."""
        memory_utils = memory_utils_module
        
        # Create baseline memory
        memory_utils.update_active_memory("baseline", "test")
        
        baseline_file = os.path.join(temp_memory_dir, "active_memory.json")
        baseline_size = os.path.getsize(baseline_file)
        
        # Add incremental data
        for i in range(50):
            memory_utils.update_active_memory(f"key_{i}", f"value_{i}")
        
        final_size = os.path.getsize(baseline_file)
        
        # File should grow proportionally, not exponentially
        size_ratio = final_size / baseline_size
        assert size_ratio < 100  # Should not grow by more than 100x for 50 entries
        
        # Verify data integrity
        all_data = memory_utils.get_active_memory()
        assert len([k for k in all_data.keys() if k.startswith("key_")]) == 50
    
    def test_memory_cleanup_behavior(self, memory_utils_module, temp_memory_dir):
        """Test that memory handles multiple updates efficiently."""
        memory_utils = memory_utils_module
        
        # Create initial state
        memory_utils.update_active_memory("persistent", "data")
        
        # Simulate multiple session cycles
        for session in range(10):
            # Add session-specific data
            memory_utils.update_active_memory("current_session", {
                "session_id": session,
                "temp_data": [f"temp_{i}" for i in range(100)]
            })
        
        active_memory = memory_utils.get_active_memory()
        
        # Should still have persistent data
        assert active_memory["persistent"] == "data"
        
        # Current session should be the latest
        assert active_memory["current_session"]["session_id"] == 9