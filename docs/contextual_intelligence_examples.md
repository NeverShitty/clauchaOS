# Contextual Intelligence in Action: Real Project Examples

## 🎯 How the System Reads Your Work Environment

### Project Structure Analysis
The system automatically scans:
- **Configuration files** (package.json, requirements.txt, Cargo.toml)
- **Dependency lists** (what frameworks/libraries you're using)  
- **File types** (JavaScript, Python, CSS, Markdown, etc.)
- **Directory structure** (src/, components/, tests/, docs/)
- **README content** (project type hints, API mentions)
- **Git status** (branch names, commit patterns)

### Intelligent Resource Curation
Based on this analysis, it curates help resources that are:
- **Immediately relevant** to your current work
- **Skill-appropriate** for your experience level
- **Action-oriented** (not just reference docs)
- **Personally customized** based on your past preferences

---

## 📱 Example 1: React Native Mobile App

### What the System Detects:
```bash
$ cd mobile-food-app
# System scans:
# - package.json: react-native, @react-navigation/native, redux-toolkit
# - src/components/ directory structure
# - android/ and ios/ folders
# - README mentions "food delivery mobile app"
```

### Contextual Help Menu:
```bash
$ help
╭──────────────────────────────────────────────────────╮
│  🎯 CONTEXTUAL HELP RESOURCES                        │
│  📁 ~/projects/mobile-food-app                       │
╰──────────────────────────────────────────────────────╯

React Native Resources:
  1. React Native Navigation Patterns
  2. Redux Toolkit Mobile Best Practices  
  3. iOS/Android Platform Differences Guide
  4. Mobile Performance Optimization

JavaScript Resources:
  5. Async/Await with API Calls
  6. Error Handling in Mobile Apps
  7. JavaScript Debugging on Device

Testing Resources:
  8. React Native Testing Library Guide
  9. Detox E2E Testing Setup
  10. Unit Testing Redux Logic

🔧 Quick Actions:
  r. Refresh context analysis
  a. Add custom resource for this context
  q. Back to terminal
```

### File-Specific Intelligence:
```bash
$ code src/screens/FoodListScreen.js
💡 React Native screen - consider: useFocusEffect for screen lifecycle, navigation patterns

$ vim ios/Podfile
💡 iOS dependencies - try: pod install, pod update, check for version conflicts
```

---

## 🌐 Example 2: Flask REST API Backend

### What the System Detects:
```bash
$ cd restaurant-api
# System scans:
# - requirements.txt: flask, flask-sqlalchemy, pytest, gunicorn
# - app.py with Flask routes
# - models/ directory with database schemas
# - tests/ directory with pytest files
# - README mentions "restaurant management API"
```

### Contextual Help Menu:
```bash
$ help
╭──────────────────────────────────────────────────────╮
│  🎯 CONTEXTUAL HELP RESOURCES                        │
│  📁 ~/projects/restaurant-api                        │
╰──────────────────────────────────────────────────────╯

Python Resources:
  1. Flask API Design Patterns
  2. SQLAlchemy Relationship Modeling
  3. Python Virtual Environment Best Practices
  4. Flask-Migrate Database Versioning

API Development Resources:
  5. RESTful API Design Guidelines  
  6. API Authentication with JWT
  7. Error Handling and Status Codes
  8. API Rate Limiting Strategies

Testing Resources:
  9. pytest for Flask Applications
  10. API Testing with requests library
  11. Database Testing Patterns
  12. Mock External Service Calls

Deployment Resources:
  13. Gunicorn Production Configuration
  14. Docker for Flask Applications
  15. Environment Variable Management
```

### File-Specific Intelligence:
```bash
$ code models/restaurant.py
💡 SQLAlchemy model - consider: relationship definitions, indexing, validation

$ vim tests/test_orders.py  
💡 Python test file - try: pytest -v, coverage analysis, fixture patterns