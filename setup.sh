#!/bin/bash
# Claude Memory System Setup Script

set -e

echo "🧠 Setting up Claude Memory System..."

# Create memory directory structure
echo "📁 Creating memory directory structure..."
mkdir -p ~/claude_memory/{project_memory,learning_memory,orc_data,session_logs}

# Copy templates
echo "📝 Installing templates..."
cp templates/active_memory_template.json ~/claude_memory/active_memory.json
echo "   ✅ Active memory template installed"

# Copy utilities
echo "🛠️  Installing utilities..."
cp utils/memory_utils.py ~/claude_memory/
chmod +x ~/claude_memory/memory_utils.py
echo "   ✅ Memory utilities installed"

# Create initial learning memory
echo "🧠 Setting up learning memory..."
cat > ~/claude_memory/learning_memory/collaboration_patterns.json << 'EOF'
{
  "effective_patterns": {
    "session_continuity": {
      "pattern": "Using persistent memory for context retention",
      "effectiveness": "High",
      "description": "Maintaining project context across sessions eliminates repetitive explanations"
    }
  },
  "user_preferences": {
    "discovered_patterns": []
  }
}
EOF
echo "   ✅ Learning memory initialized"

# Create ORC data README
echo "📊 Setting up analytics..."
cp docs/ORC_SETUP.md ~/claude_memory/orc_data/README.md 2>/dev/null || cat > ~/claude_memory/orc_data/README.md << 'EOF'
# ORC Data for Fast Analytics

This directory is ready for ORC files when PyArrow is installed:

```bash
pip install pyarrow
```

Then use the memory utilities to create analytical datasets for fast querying.
EOF
echo "   ✅ Analytics directory ready"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit ~/claude_memory/active_memory.json with your project details"
echo "2. Tell Claude: 'I've set up a memory system at ~/claude_memory/ - please use it to remember our work together'"
echo "3. Start collaborating with persistent context!"
echo ""
echo "📖 Documentation: docs/QUICK_START_TEMPLATE.md"
echo "🛠️  Utilities: ~/claude_memory/memory_utils.py"
echo ""
echo "Happy collaborating! 🚀"
