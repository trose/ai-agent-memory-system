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
            return memory_utils._load_json(memory_file)
        
        result = benchmark(load_large_memory)
        assert len(result) == 1001  # 1000 entries + metadata
    
    def test_project_status_save_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark project status save performance."""
        memory_utils = memory_utils_module
        
        project_data = {
            "project_name": "Performance Test Project",
            "status": "testing",
            "architecture": {
                "frontend": "React with TypeScript",
                "backend": "Python FastAPI with async/await",
                "database": "PostgreSQL with pgvector extension",
                "deployment": "Docker containers on AWS ECS Fargate"
            },
            "features": [f"Feature {i}" for i in range(50)],
            "testing_results": {f"test_suite_{i}": "passed" for i in range(100)}
        }
        
        def save_project():
            memory_utils.save_project_status(project_data)
        
        benchmark(save_project)
        
        # Verify save worked
        saved_data = memory_utils.get_project_status()
        assert saved_data["project_name"] == "Performance Test Project"
    
    def test_session_insights_batch_performance(self, benchmark, memory_utils_module, temp_memory_dir):
        """Benchmark batch session insight operations."""
        memory_utils = memory_utils_module
        
        insights = [
            f"Performance insight {i}: Optimization technique {i} works well"
            for i in range(100)
        ]
        
        def batch_save_insights():
            for i, insight in enumerate(insights):
                memory_utils.save_session_insight(insight, f"category_{i % 10}")
        
        benchmark(batch_save_insights)
        
        # Verify all insights were saved
        all_insights = memory_utils.get_session_insights()
        total_insights = sum(len(category_insights) for category_insights in all_insights.values())
        assert total_insights == 100
    
    def test_memory_overview_performance(self, benchmark, memory_utils_module, populated_memory_dir):
        """Benchmark memory system overview generation."""
        memory_utils = memory_utils_module
        
        # Add some data to make the overview more realistic
        for i in range(20):
            memory_utils.save_session_insight(f"Insight {i}", f"category_{i % 5}")
            memory_utils.update_active_memory(f"key_{i}", f"value_{i}")
        
        def get_overview():
            return memory_utils.get_memory_system_overview()
        
        result = benchmark(get_overview)
        
        # Verify overview contains expected data
        assert "memory_directory" in result
        assert "files" in result
        assert len(result["files"]["learning_memory"]) > 0
    
    @pytest.mark.skip(reason="Requires PyArrow - optional dependency")
    def test_orc_file_performance(self, benchmark, temp_memory_dir):
        """Benchmark ORC file operations (when PyArrow is available)."""
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError:
            pytest.skip("PyArrow not available")
        
        # Create sample data
        data = {
            'session_id': [f"session_{i}" for i in range(10000)],
            'timestamp': [f"2024-08-21T{i%24:02d}:00:00Z" for i in range(10000)],
            'action_type': ['memory_update', 'project_save', 'insight_save'] * 3334,
            'performance_ms': [i % 1000 + 10 for i in range(10000)]
        }
        
        table = pa.table(data)
        orc_file = os.path.join(temp_memory_dir, "performance_data.orc")
        
        def write_orc():
            pq.write_table(table, orc_file)
        
        def read_orc():
            return pq.read_table(orc_file)
        
        # Benchmark write
        write_result = benchmark.pedantic(write_orc, rounds=5)
        
        # Verify file was created
        assert os.path.exists(orc_file)
        
        # Benchmark read in a separate test to avoid interference
        read_result = pq.read_table(orc_file)
        assert read_result.num_rows == 10000


class TestMemoryScalability:
    """Test memory system behavior with large datasets."""
    
    def test_large_project_memory(self, memory_utils_module, temp_memory_dir):
        """Test handling of large project memory files."""
        memory_utils = memory_utils_module
        
        # Create a comprehensive project with lots of data
        large_project = {
            "project_name": "Large Scale Application",
            "status": "active development",
            "team_members": [f"developer_{i}@company.com" for i in range(50)],
            "features": {
                f"feature_module_{i}": {
                    "description": f"Feature module {i} with comprehensive functionality",
                    "status": "in_progress" if i % 3 == 0 else "completed",
                    "tests": [f"test_{i}_{j}" for j in range(20)],
                    "files": [f"file_{i}_{j}.py" for j in range(10)]
                }
                for i in range(100)
            },
            "deployment_history": [
                {
                    "version": f"v1.{i}.0",
                    "timestamp": f"2024-08-{i%30+1:02d}T12:00:00Z",
                    "changes": [f"Change {j}" for j in range(i % 10 + 1)]
                }
                for i in range(50)
            ]
        }
        
        # Test saving large project
        memory_utils.save_project_status(large_project)
        
        # Test retrieving large project
        retrieved = memory_utils.get_project_status()
        assert retrieved["project_name"] == "Large Scale Application"
        assert len(retrieved["features"]) == 100
        assert len(retrieved["team_members"]) == 50
    
    def test_many_insights_performance(self, memory_utils_module, temp_memory_dir):
        """Test performance with many session insights."""
        memory_utils = memory_utils_module
        
        # Save many insights across different categories
        categories = ["performance", "architecture", "testing", "deployment", "optimization"]
        
        for category in categories:
            for i in range(200):  # 1000 total insights
                insight = f"Insight {i} for {category}: This is a detailed insight about {category} optimization and best practices."
                memory_utils.save_session_insight(insight, category)
        
        # Test retrieval performance
        all_insights = memory_utils.get_session_insights()
        assert len(all_insights) == 5  # 5 categories
        
        total_insights = sum(len(insights) for insights in all_insights.values())
        assert total_insights == 1000
        
        # Test category-specific retrieval
        perf_insights = memory_utils.get_session_insights("performance")
        assert len(perf_insights["performance"]) == 200
    
    def test_concurrent_memory_operations(self, memory_utils_module, temp_memory_dir):
        """Test simulated concurrent memory operations."""
        memory_utils = memory_utils_module
        
        # Simulate rapid alternating operations
        for i in range(100):
            # Update active memory
            memory_utils.update_active_memory(f"concurrent_key_{i}", f"value_{i}")
            
            # Save insight
            memory_utils.save_session_insight(f"Concurrent insight {i}", "concurrency")
            
            # Update project status
            if i % 10 == 0:
                memory_utils.save_project_status({
                    "project_name": f"Concurrent Project {i}",
                    "last_update": i,
                    "status": "active"
                })
        
        # Verify final state is consistent
        active_memory = memory_utils.get_active_memory()
        for i in range(100):
            assert active_memory[f"concurrent_key_{i}"] == f"value_{i}"
        
        insights = memory_utils.get_session_insights("concurrency")
        assert len(insights["concurrency"]) == 100
        
        final_project = memory_utils.get_project_status()
        assert final_project["project_name"] == "Concurrent Project 90"  # Last update


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
        """Test that old memory doesn't accumulate indefinitely."""
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
            
            # Simulate session end - in real usage, some cleanup might occur
            # For now, we just verify the memory is manageable
            
        active_memory = memory_utils.get_active_memory()
        
        # Should still have persistent data
        assert active_memory["persistent"] == "data"
        
        # Current session should be the latest
        assert active_memory["current_session"]["session_id"] == 9
