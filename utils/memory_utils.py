#!/usr/bin/env python3
"""
Claude Memory Management Utilities

Provides tools for managing persistent memory data across sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

MEMORY_DIR = Path.home() / "claude_memory"

def update_active_memory(key: str, value: Any) -> None:
    """Update a key in active memory."""
    memory_file = MEMORY_DIR / "active_memory.json"
    
    if memory_file.exists():
        with open(memory_file, 'r') as f:
            memory = json.load(f)
    else:
        memory = {}
    
    memory[key] = value
    memory["last_updated"] = datetime.utcnow().isoformat()
    
    with open(memory_file, 'w') as f:
        json.dump(memory, f, indent=2)

def get_active_memory(key: str = None) -> Any:
    """Get active memory data."""
    memory_file = MEMORY_DIR / "active_memory.json"
    
    if not memory_file.exists():
        return None
    
    with open(memory_file, 'r') as f:
        memory = json.load(f)
    
    return memory.get(key) if key else memory

def save_session_insight(insight: str, category: str = "general") -> None:
    """Save a new insight from the current session."""
    insights_file = MEMORY_DIR / "learning_memory" / "session_insights.json"
    
    if insights_file.exists():
        with open(insights_file, 'r') as f:
            insights = json.load(f)
    else:
        insights = {"insights": []}
    
    new_insight = {
        "timestamp": datetime.utcnow().isoformat(),
        "category": category,
        "insight": insight
    }
    
    insights["insights"].append(new_insight)
    
    with open(insights_file, 'w') as f:
        json.dump(insights, f, indent=2)

def get_project_context(project_name: str = None) -> Dict[str, Any]:
    """Get project context from memory."""
    if project_name:
        project_file = MEMORY_DIR / "project_memory" / f"{project_name.lower().replace(' ', '_')}.json"
    else:
        # Get the current project from active memory
        active = get_active_memory()
        if active and "current_session" in active:
            project_name = active["current_session"].get("project", "")
            project_file = MEMORY_DIR / "project_memory" / f"{project_name.lower().replace(' ', '_')}.json"
        else:
            return {}
    
    if project_file.exists():
        with open(project_file, 'r') as f:
            return json.load(f)
    return {}

def create_orc_data(data: List[Dict], filename: str) -> None:
    """Create ORC file for analytical data (requires pyarrow)."""
    try:
        import pyarrow as pa
        import pyarrow.orc as orc
        import pandas as pd
        
        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)
        
        orc_file = MEMORY_DIR / "orc_data" / f"{filename}.orc"
        with open(orc_file, 'wb') as f:
            orc.write_table(table, f)
        
        print(f"ORC file created: {orc_file}")
        
    except ImportError:
        print("PyArrow not available. Install with: pip install pyarrow")
        # Fallback to JSON
        json_file = MEMORY_DIR / "orc_data" / f"{filename}_fallback.json"
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Fallback JSON created: {json_file}")

def memory_summary() -> Dict[str, Any]:
    """Get a summary of all memory data."""
    summary = {
        "memory_directory": str(MEMORY_DIR),
        "last_updated": datetime.utcnow().isoformat(),
        "files": {}
    }
    
    for category_dir in ["project_memory", "learning_memory", "orc_data", "session_logs"]:
        category_path = MEMORY_DIR / category_dir
        if category_path.exists():
            files = list(category_path.glob("*"))
            summary["files"][category_dir] = [str(f.name) for f in files]
    
    # Add active memory status
    active = get_active_memory()
    if active:
        summary["current_session"] = active.get("current_session", {})
        summary["user_preferences"] = active.get("user_preferences", {})
    
    return summary

if __name__ == "__main__":
    print("Claude Memory System")
    print("===================")
    print(json.dumps(memory_summary(), indent=2))
