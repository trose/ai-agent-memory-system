# 🧠 Claude Persistent Memory System

[![GitHub release](https://img.shields.io/github/release/trose/claude-memory-system.svg)](https://github.com/trose/claude-memory-system/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/trose/claude-memory-system/workflows/🧪%20CI/CD%20Pipeline/badge.svg)](https://github.com/trose/claude-memory-system/actions)
[![Coverage](https://codecov.io/gh/trose/claude-memory-system/branch/main/graph/badge.svg)](https://codecov.io/gh/trose/claude-memory-system)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/trose/claude-memory-system/blob/main/CONTRIBUTING.md)

**Transform your AI collaboration with persistent memory across sessions**

## 🌟 **What This Solves**

Working on complex projects with Claude but losing context between sessions? This memory system provides:

- ✅ **Persistent Context** - Claude remembers your projects, decisions, and progress
- ✅ **Collaboration Learning** - Effective patterns are retained and consistently applied  
- ✅ **Reduced Friction** - No more re-explaining context or starting from scratch
- ✅ **Quality Improvement** - Consistent approaches lead to better outcomes
- ✅ **Performance Analytics** - Track what collaboration patterns work best

## 🚀 **Quick Start (5 minutes)**

### 1. Create the directory structure
```bash
mkdir -p ~/claude_memory/{project_memory,learning_memory,orc_data,session_logs}
```

### 2. Set up initial memory file
```bash
# Copy the template from quick-start-template.md
cp templates/active_memory_template.json ~/claude_memory/active_memory.json
# Edit with your project details
```

### 3. Tell Claude about it
```
I've set up a persistent memory system at ~/claude_memory/ that you can use to remember our work together across sessions. Please use this to maintain context, learn my preferences, and build on previous work.
```

**That's it!** Claude will now maintain context across all your sessions.

## 📁 **System Architecture**

```
~/claude_memory/
├── active_memory.json              # Current session context & preferences
├── project_memory/                 # Project-specific contexts
│   ├── project_alpha.json
│   └── project_beta.json
├── learning_memory/                # Collaboration patterns & insights
│   ├── collaboration_patterns.json
│   └── technical_insights.json
├── orc_data/                       # Fast analytical data (optional)
│   └── session_metrics.orc
└── session_logs/                   # Historical session records
    └── important_milestones.md
```

## 🎯 **Key Features**

### **Hybrid Storage Strategy**
- **JSON Files** → Human-readable, easily editable, immediate access
- **ORC Files** → Ultra-fast columnar retrieval for analytical queries

### **Multi-Project Support**
- Separate contexts for different projects
- Cross-project learning and pattern recognition
- Easy switching between project contexts

### **Learning Amplification**
- Captures effective collaboration patterns
- Remembers your preferences and working style
- Continuously improves interaction quality

## 📖 **Documentation**

- **[Complete Guide](docs/COMPLETE_GUIDE.md)** - Comprehensive setup and usage
- **[Quick Start Template](docs/QUICK_START_TEMPLATE.md)** - Copy-paste 5-minute setup
- **[Advanced Features](docs/ADVANCED_FEATURES.md)** - ORC analytics and power-user tools
- **[Use Cases](docs/USE_CASES.md)** - Real-world examples and success stories
- **[API Reference](docs/API_REFERENCE.md)** - Memory utilities and programmatic access

## 🎯 **Proven Results**

This system was developed and tested on a complex identity verification platform with:
- **4 Specialized AI Agents** working in sequence
- **270+ Tests** across all components  
- **Production-Ready Architecture** with comprehensive documentation
- **Seamless Handoffs** between development phases

**Result**: Each agent built perfectly on previous work with full context, creating a cohesive, production-ready system.

## 🛠 **Installation**

### **Basic Setup**
```bash
git clone https://github.com/trose/claude-memory-system.git
cd claude-memory-system
./setup.sh
```

### **Interactive Demo**
```bash
python demo.py
```
Experience the full system with a guided, interactive demonstration!

### **With Analytics Support**
```bash
# Install PyArrow for ORC file support
pip install pyarrow

# Copy advanced utilities
cp utils/memory_utils.py ~/claude_memory/
```

## 💡 **Use Cases**

- **Software Development** - Multi-session coding projects with persistent architecture context
- **Research Projects** - Long-term academic or business research with cumulative insights
- **Content Creation** - Books, courses, documentation with consistent style and progress
- **Business Strategy** - Ongoing strategic planning with decision history
- **Learning Projects** - Skill development with progress tracking and pattern recognition

## 🤝 **Contributing**

Contributions welcome! Areas of interest:
- Additional memory templates for specific project types
- Advanced analytics queries for ORC data
- Integration with popular development tools
- Performance optimizations
- New use case documentation

## 📄 **License**

MIT License - Feel free to use, modify, and share!

## 🙏 **Acknowledgments**

Developed through real-world collaboration on complex AI projects. Special thanks to users who provided feedback on effective memory patterns and performance optimization insights.

---

**Transform your AI collaboration today - your future self (and Claude) will thank you! 🧠✨**
