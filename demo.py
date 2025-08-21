#!/usr/bin/env python3
"""
🧠 Claude Memory System - Interactive Demo

This script provides an interactive demonstration of the Claude Memory System,
showing how to use persistent memory for AI collaboration across sessions.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text: str):
    """Print a colored header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_step(step: str, description: str):
    """Print a demo step."""
    print(f"{Colors.BOLD}{Colors.GREEN}Step {step}:{Colors.END} {Colors.CYAN}{description}{Colors.END}")

def print_success(message: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message: str):
    """Print an info message."""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def print_command(command: str):
    """Print a command to run."""
    print(f"{Colors.PURPLE}$ {command}{Colors.END}")

def wait_for_user():
    """Wait for user to press Enter."""
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

class MemorySystemDemo:
    """Interactive demo of the Claude Memory System."""
    
    def __init__(self):
        self.demo_dir = None
        self.memory_utils = None
        
    def setup_demo_environment(self):
        """Set up a temporary demo environment."""
        print_step("1", "Setting up demo environment")
        
        # Create temporary demo directory
        import tempfile
        self.demo_dir = tempfile.mkdtemp(prefix="claude_memory_demo_")
        print_info(f"Created demo directory: {self.demo_dir}")
        
        # Create memory structure
        memory_dirs = [
            "project_memory",
            "learning_memory", 
            "session_logs",
            "orc_data"
        ]
        
        for dir_name in memory_dirs:
            os.makedirs(os.path.join(self.demo_dir, dir_name))
            print_success(f"Created {dir_name}/ directory")
        
        # Copy memory utilities
        repo_root = Path(__file__).parent
        utils_src = repo_root / "utils" / "memory_utils.py"
        utils_dst = os.path.join(self.demo_dir, "memory_utils.py")
        
        import shutil
        shutil.copy(utils_src, utils_dst)
        print_success("Copied memory_utils.py")
        
        # Add to Python path and import
        sys.path.insert(0, self.demo_dir)
        
        # Patch memory utilities to use demo directory
        import memory_utils
        memory_utils.MEMORY_DIR = self.demo_dir
        memory_utils.ACTIVE_MEMORY_FILE = os.path.join(self.demo_dir, "active_memory.json")
        memory_utils.PROJECT_MEMORY_DIR = os.path.join(self.demo_dir, "project_memory")
        memory_utils.LEARNING_MEMORY_DIR = os.path.join(self.demo_dir, "learning_memory")
        memory_utils.SESSION_LOGS_DIR = os.path.join(self.demo_dir, "session_logs")
        memory_utils.ORC_DATA_DIR = os.path.join(self.demo_dir, "orc_data")
        
        self.memory_utils = memory_utils
        print_success("Memory system initialized!")
        
        wait_for_user()
    
    def demo_active_memory(self):
        """Demonstrate active memory functionality."""
        print_step("2", "Active Memory - Current Session Context")
        
        print_info("Active memory stores your current session context and preferences.")
        print_info("This is the first thing Claude checks when you start a new conversation.")
        
        # Initial session setup
        print("\n" + Colors.CYAN + "Setting up initial session context:" + Colors.END)
        
        session_data = {
            "project": "Claude Memory System Demo",
            "user": "Demo User",
            "workspace": self.demo_dir,
            "session_focus": "Learning how persistent memory transforms AI collaboration",
            "key_accomplishments": [
                "Set up memory system demo environment",
                "Understanding active memory concepts"
            ]
        }
        
        self.memory_utils.update_active_memory("current_session", session_data)
        print_success("Session context saved to active memory")
        
        # User preferences
        print("\n" + Colors.CYAN + "Setting user preferences:" + Colors.END)
        
        preferences = {
            "collaboration_style": "Interactive learning with hands-on examples",
            "technical_approach": "Learn by doing, with clear explanations",
            "communication_style": "Step-by-step with visual feedback",
            "preferred_formats": {
                "code_examples": "Python with clear comments",
                "documentation": "Markdown with examples",
                "explanations": "Detailed but accessible"
            }
        }
        
        self.memory_utils.update_active_memory("user_preferences", preferences)
        print_success("User preferences saved to active memory")
        
        # Show what's stored
        print("\n" + Colors.CYAN + "Current active memory contents:" + Colors.END)
        active_memory = self.memory_utils.get_active_memory()
        
        print(json.dumps({
            "current_session": active_memory.get("current_session", {}),
            "user_preferences": active_memory.get("user_preferences", {}),
            "last_updated": active_memory.get("last_updated", "unknown")
        }, indent=2))
        
        print_info("💡 Claude can now remember your project context and preferences!")
        wait_for_user()
    
    def demo_project_memory(self):
        """Demonstrate project-specific memory."""
        print_step("3", "Project Memory - Architecture & Decisions")
        
        print_info("Project memory stores architecture decisions, progress, and context")
        print_info("that needs to persist across multiple development sessions.")
        
        # Create comprehensive project context
        project_data = {
            "project_name": "E-commerce Platform",
            "project_type": "Full-stack web application",
            "start_date": "2024-08-01",
            "status": "Active development - Backend complete, Frontend in progress",
            "architecture": {
                "frontend": "React with TypeScript for type safety",
                "backend": "Python FastAPI with async/await",
                "database": "PostgreSQL with Redis for caching",
                "deployment": "Docker containers on AWS ECS"
            },
            "key_decisions": {
                "technology_choices": "React chosen for component reusability and ecosystem",
                "architecture_patterns": "Microservices with API Gateway for scalability",
                "database_choice": "PostgreSQL for ACID compliance in financial transactions"
            },
            "current_progress": {
                "completed_features": [
                    "User authentication with JWT",
                    "Product catalog with search",
                    "Shopping cart with Redis storage",
                    "Payment processing with Stripe",
                    "Order management system"
                ],
                "in_progress": [
                    "React frontend components",
                    "Admin dashboard",
                    "Mobile responsive design"
                ],
                "next_priorities": [
                    "Performance optimization",
                    "Comprehensive testing",
                    "Production deployment"
                ]
            },
            "integration_points": {
                "payment_processing": "Stripe API for secure transactions",
                "email_service": "SendGrid for transactional emails",
                "file_storage": "AWS S3 for product images",
                "monitoring": "Sentry for error tracking"
            },
            "testing_strategy": {
                "backend": "Pytest with 85% coverage requirement",
                "frontend": "Jest and React Testing Library",
                "integration": "Postman collection for API testing",
                "e2e": "Cypress for user workflow testing"
            }
        }
        
        print("\n" + Colors.CYAN + "Saving comprehensive project context:" + Colors.END)
        self.memory_utils.save_project_status(project_data)
        print_success("Project memory saved successfully!")
        
        # Demonstrate retrieval
        print("\n" + Colors.CYAN + "Retrieving project status:" + Colors.END)
        saved_project = self.memory_utils.get_project_status()
        
        # Show key information
        print(f"📊 Project: {saved_project['project_name']}")
        print(f"📈 Status: {saved_project['status']}")
        print(f"🏗️  Architecture: {len(saved_project['architecture'])} components defined")
        print(f"✅ Completed: {len(saved_project['current_progress']['completed_features'])} features")
        print(f"🔄 In Progress: {len(saved_project['current_progress']['in_progress'])} items")
        
        print_info("💡 Claude now knows your entire project context and can build on previous work!")
        wait_for_user()
    
    def demo_learning_memory(self):
        """Demonstrate learning and insights tracking."""
        print_step("4", "Learning Memory - Patterns & Insights")
        
        print_info("Learning memory captures effective collaboration patterns")
        print_info("and insights that improve future interactions.")
        
        # Save various insights
        insights = [
            ("Best Practices", "Test-driven development significantly improves code quality and reduces debugging time"),
            ("Architecture", "Microservices architecture provides flexibility but adds complexity - worth it for scalable systems"),
            ("Performance", "Database indexing on frequently queried fields improved response time by 60%"),
            ("Collaboration", "Regular code reviews catch issues early and improve team knowledge sharing"),
            ("Deployment", "Blue-green deployment strategy eliminates downtime during releases"),
            ("Testing", "Integration tests are more valuable than unit tests for catching real-world issues"),
            ("User Experience", "Progressive loading improves perceived performance even with slower backend"),
            ("Security", "Input validation at API gateway level prevents many common vulnerabilities")
        ]
        
        print("\n" + Colors.CYAN + "Saving collaboration insights:" + Colors.END)
        for category, insight in insights:
            self.memory_utils.save_session_insight(insight, category.lower().replace(" ", "_"))
            print(f"  📝 {category}: {insight[:60]}...")
        
        print_success(f"Saved {len(insights)} insights across {len(set(cat for cat, _ in insights))} categories")
        
        # Demonstrate insight retrieval
        print("\n" + Colors.CYAN + "Retrieving saved insights:" + Colors.END)
        all_insights = self.memory_utils.get_session_insights()
        
        for category, category_insights in all_insights.items():
            print(f"📚 {category.replace('_', ' ').title()}: {len(category_insights)} insights")
        
        # Show specific category
        print(f"\n{Colors.CYAN}Performance insights:{Colors.END}")
        perf_insights = self.memory_utils.get_session_insights("performance")
        for insight_data in perf_insights.get("performance", []):
            print(f"  💡 {insight_data['insight']}")
        
        print_info("💡 Claude learns from every project and applies insights to new challenges!")
        wait_for_user()
    
    def demo_session_logging(self):
        """Demonstrate session activity logging."""
        print_step("5", "Session Logs - Activity History")
        
        print_info("Session logs capture important milestones and activities")
        print_info("for historical reference and project documentation.")
        
        # Log various activities
        activities = [
            "Completed Claude Memory System demo setup",
            "Demonstrated active memory for session context",
            "Showed project memory for architecture persistence",
            "Captured learning insights for future reference",
            "Explored session logging capabilities"
        ]
        
        print("\n" + Colors.CYAN + "Logging session activities:" + Colors.END)
        for activity in activities:
            self.memory_utils.log_session_activity(activity, "demo_session.md")
            print(f"  📋 {activity}")
            time.sleep(0.1)  # Small delay for realism
        
        print_success("Session activities logged!")
        
        # Show log file
        log_file = os.path.join(self.demo_dir, "session_logs", "demo_session.md")
        if os.path.exists(log_file):
            print(f"\n{Colors.CYAN}Session log contents:{Colors.END}")
            with open(log_file, 'r') as f:
                content = f.read()
            print(content)
        
        print_info("💡 Perfect for tracking progress and creating project documentation!")
        wait_for_user()
    
    def demo_memory_overview(self):
        """Demonstrate memory system overview."""
        print_step("6", "Memory System Overview")
        
        print_info("The memory overview provides a complete picture of your")
        print_info("stored context, insights, and collaboration history.")
        
        print("\n" + Colors.CYAN + "Generating memory system overview:" + Colors.END)
        overview = self.memory_utils.get_memory_system_overview()
        
        # Display key metrics
        print(f"📁 Memory Directory: {overview['memory_directory']}")
        print(f"🕐 Last Updated: {overview['last_updated']}")
        
        print(f"\n📊 Storage Summary:")
        for storage_type, files in overview['files'].items():
            print(f"  {storage_type}: {len(files)} files")
        
        print(f"\n🎯 Current Session:")
        session = overview.get('current_session', {})
        print(f"  Project: {session.get('project', 'Unknown')}")
        print(f"  Focus: {session.get('session_focus', 'Not specified')}")
        print(f"  Accomplishments: {len(session.get('key_accomplishments', []))}")
        
        print(f"\n⚙️  User Preferences:")
        prefs = overview.get('user_preferences', {})
        print(f"  Style: {prefs.get('collaboration_style', 'Not specified')}")
        print(f"  Approach: {prefs.get('technical_approach', 'Not specified')}")
        
        print_info("💡 One command gives Claude complete context about your work!")
        wait_for_user()
    
    def demo_real_world_scenario(self):
        """Demonstrate a realistic usage scenario."""
        print_step("7", "Real-World Scenario - Multi-Session Project")
        
        print_info("Let's simulate how memory helps across multiple sessions:")
        print_info("Session 1: Planning → Session 2: Development → Session 3: Optimization")
        
        # Session 1: Planning
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📅 Session 1: Project Planning{Colors.END}")
        
        planning_updates = {
            "session_focus": "Project planning and architecture design",
            "current_phase": "planning",
            "decisions_made": [
                "Chose React + FastAPI tech stack",
                "Decided on microservices architecture",
                "Selected PostgreSQL for data persistence"
            ]
        }
        
        self.memory_utils.update_active_memory("current_session", planning_updates)
        self.memory_utils.save_session_insight("Microservices chosen for scalability despite added complexity", "architecture")
        print_success("Session 1 context and decisions saved")
        
        # Session 2: Development  
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🔨 Session 2: Active Development{Colors.END}")
        
        dev_updates = {
            "session_focus": "Backend API development and testing",
            "current_phase": "development",
            "progress_made": [
                "Implemented user authentication",
                "Created product catalog API",
                "Added comprehensive test suite"
            ]
        }
        
        self.memory_utils.update_active_memory("current_session", dev_updates)
        self.memory_utils.save_session_insight("Async/await pattern in FastAPI significantly improves performance under load", "performance")
        self.memory_utils.log_session_activity("Completed backend API with 85% test coverage")
        print_success("Session 2 progress and insights saved")
        
        # Session 3: Optimization
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚡ Session 3: Performance Optimization{Colors.END}")
        
        opt_updates = {
            "session_focus": "Performance optimization and production readiness",
            "current_phase": "optimization",
            "optimizations": [
                "Added Redis caching layer",
                "Optimized database queries",
                "Implemented connection pooling"
            ]
        }
        
        self.memory_utils.update_active_memory("current_session", opt_updates)
        self.memory_utils.save_session_insight("Redis caching reduced API response time from 200ms to 50ms", "performance")
        print_success("Session 3 optimizations and results saved")
        
        # Show the accumulated context
        print(f"\n{Colors.CYAN}Accumulated project knowledge:{Colors.END}")
        overview = self.memory_utils.get_memory_system_overview()
        
        # Count insights by category
        all_insights = self.memory_utils.get_session_insights()
        total_insights = sum(len(insights) for insights in all_insights.values())
        
        print(f"📚 Total insights captured: {total_insights}")
        print(f"🏗️  Architecture decisions: Documented and accessible")
        print(f"📈 Performance improvements: Tracked with metrics")
        print(f"📋 Session activities: Complete development timeline")
        
        print_info("💡 Each session builds perfectly on the previous work!")
        print_info("Claude has complete context and can continue exactly where you left off!")
        
        wait_for_user()
    
    def demo_ai_collaboration_benefits(self):
        """Show the benefits for AI collaboration."""
        print_step("8", "AI Collaboration Benefits")
        
        print_info("Here's how persistent memory transforms AI collaboration:")
        
        benefits = [
            ("🚀 Context Continuity", "No more re-explaining project details each session"),
            ("🧠 Learning Amplification", "AI learns your preferences and applies them consistently"),
            ("📈 Quality Improvement", "Decisions and insights compound over time"),
            ("⚡ Reduced Friction", "Start new sessions immediately with full context"),
            ("🎯 Focused Sessions", "Spend time on new problems, not recap"),
            ("📊 Progress Tracking", "Clear visibility into project evolution"),
            ("🔄 Pattern Recognition", "Identify what collaboration approaches work best"),
            ("🏗️  Architecture Consistency", "Maintain design decisions across development phases")
        ]
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}Key Benefits:{Colors.END}")
        for benefit, description in benefits:
            print(f"  {benefit} {description}")
            time.sleep(0.3)  # Dramatic pause
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Before Memory System:{Colors.END}")
        print("  ❌ 'Could you remind me what tech stack we're using?'")
        print("  ❌ 'What were the architectural decisions we made?'")
        print("  ❌ 'I think we discussed this optimization before...'")
        print("  ❌ Starting every session from scratch")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}With Memory System:{Colors.END}")
        print("  ✅ 'Continue optimizing the API performance we discussed'")
        print("  ✅ 'Build on the microservices architecture we designed'")
        print("  ✅ 'Apply the testing patterns that worked well before'")
        print("  ✅ Immediate continuation with full context")
        
        print_info("💡 Memory transforms AI from a tool into a true collaboration partner!")
        wait_for_user()
    
    def cleanup_demo(self):
        """Clean up demo environment."""
        print_step("9", "Demo Cleanup")
        
        print_info("Demo completed! Cleaning up temporary files...")
        
        # Show final stats
        overview = self.memory_utils.get_memory_system_overview()
        all_insights = self.memory_utils.get_session_insights()
        total_insights = sum(len(insights) for insights in all_insights.values())
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}Demo Statistics:{Colors.END}")
        print(f"  📁 Memory directory: {self.demo_dir}")
        print(f"  📚 Total insights saved: {total_insights}")
        print(f"  🗂️  File types created: {len(overview['files'])}")
        print(f"  📋 Session activities logged: Multiple entries")
        
        # Ask about cleanup
        cleanup = input(f"\n{Colors.YELLOW}Keep demo files for exploration? (y/N): {Colors.END}")
        
        if cleanup.lower() not in ['y', 'yes']:
            import shutil
            try:
                shutil.rmtree(self.demo_dir)
                print_success("Demo files cleaned up")
            except Exception as e:
                print(f"{Colors.RED}Warning: Could not clean up {self.demo_dir}: {e}{Colors.END}")
        else:
            print_info(f"Demo files preserved at: {self.demo_dir}")
            print_info("You can explore the generated memory files manually!")
    
    def run_demo(self):
        """Run the complete interactive demo."""
        print_header("🧠 CLAUDE MEMORY SYSTEM - INTERACTIVE DEMO")
        
        print(f"{Colors.BOLD}Welcome to the Claude Memory System Demo!{Colors.END}")
        print(f"{Colors.CYAN}This demonstration will show you how persistent memory")
        print(f"transforms AI collaboration from session-based to continuous.{Colors.END}")
        
        print(f"\n{Colors.YELLOW}What you'll learn:{Colors.END}")
        print("  • How to set up and use persistent memory")
        print("  • Different types of memory (active, project, learning)")
        print("  • Real-world collaboration scenarios")
        print("  • Benefits for complex, multi-session projects")
        
        start = input(f"\n{Colors.BOLD}Ready to start? (Y/n): {Colors.END}")
        if start.lower() in ['n', 'no']:
            print("Maybe next time! 👋")
            return
        
        try:
            self.setup_demo_environment()
            self.demo_active_memory()
            self.demo_project_memory()
            self.demo_learning_memory()
            self.demo_session_logging()
            self.demo_memory_overview()
            self.demo_real_world_scenario()
            self.demo_ai_collaboration_benefits()
            
            print_header("🎉 DEMO COMPLETE!")
            print(f"{Colors.BOLD}{Colors.GREEN}Congratulations!{Colors.END}")
            print(f"{Colors.CYAN}You've experienced how persistent memory transforms AI collaboration.{Colors.END}")
            print(f"\n{Colors.YELLOW}Next steps:{Colors.END}")
            print("  1. Run ./setup.sh to install the full system")
            print("  2. Customize templates for your specific projects") 
            print("  3. Start your first memory-enhanced AI session")
            print("  4. Watch your collaboration quality improve over time!")
            
            print(f"\n{Colors.PURPLE}Resources:{Colors.END}")
            print("  📖 docs/COMPLETE_GUIDE.md - Comprehensive usage guide")
            print("  🎯 docs/USE_CASES.md - Real-world examples")
            print("  🛠️  docs/QUICK_START_TEMPLATE.md - 5-minute setup")
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Demo interrupted by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Demo error: {e}{Colors.END}")
        finally:
            self.cleanup_demo()


def main():
    """Main demo entry point."""
    try:
        demo = MemorySystemDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Goodbye! 👋{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
