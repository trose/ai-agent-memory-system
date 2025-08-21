#!/bin/bash
# AI Agent Memory System Setup Script

set -e

echo "Setting up AI Agent Memory System..."

# Create memory directory structure
echo "📁 Creating memory directory structure..."
mkdir -p ~/ai_memory/{project_memory,learning_memory,session_logs}

# Copy templates
echo "📝 Installing templates..."
cp templates/active_memory_template.json ~/ai_memory/active_memory.json
echo "   ✅ Active memory template installed"

# Copy utilities
echo "🛠️  Installing utilities..."
cp utils/memory_utils.py ~/ai_memory/
chmod +x ~/ai_memory/memory_utils.py
echo "   ✅ Memory utilities installed"

# Create initial learning memory
echo "Memory Setting up learning memory..."
cat > ~/ai_memory/learning_memory/collaboration_patterns.json << 'EOF'
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

# Create session logs README
echo "Creating session logs..."
cat > ~/ai_memory/session_logs/README.md << 'EOF'
# Session Logs

This directory contains important milestones and session records.

Use this to track:
- Major project milestones
- Important decisions made
- Key insights discovered
- Progress summaries
EOF
echo "   ✅ Session logs directory ready"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit ~/ai_memory/active_memory.json with your project details"
echo "2. Tell your AI agent: 'I've set up a memory system at ~/ai_memory/ - please use it to remember our work together'"
echo "3. Start collaborating with persistent context!"
echo ""
echo "Documentation: docs/QUICK_START_TEMPLATE.md"
echo "Utilities: ~/ai_memory/memory_utils.py"

