# Claude Memory System - Technical Documentation
*Version 2.0 - With Purposeful Decay & TMUX Integration*

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Concepts](#core-concepts)
4. [Installation & Setup](#installation--setup)
5. [API Reference](#api-reference)
6. [Configuration](#configuration)
7. [Usage Examples](#usage-examples)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Performance & Scaling](#performance--scaling)

---

## System Overview

The Claude Memory System is a distributed, decay-aware memory management platform designed for the Claude AI assistant ecosystem. It provides semantic memory storage with intelligent lifecycle management, ensuring relevant information persists while ephemeral data naturally decays.

### Key Features
- **Dual-layer architecture**: Local vector storage + OpenAI persistent threads
- **Purposeful decay**: Automatic expiration based on content importance
- **TMUX integration**: Context-aware memory tagging
- **Squeaky preservation**: Priority-based retention policies
- **Cross-instance broadcasting**: Synchronized knowledge across 17 Claude instances
- **Semantic search**: Understanding-based retrieval, not keyword matching

### System Stats
- **Active Instances**: 17 (11 local + 6 Replit)
- **Memory Capacity**: Unlimited (vector-based)
- **Search Latency**: <50ms local, <200ms with OpenAI
- **Decay Policies**: 8 configurable types
- **API Cost**: ~$5-10/month

---

## Architecture

### Component Overview
```
┌─────────────────────────────────────────────────────────┐
│                   Claude Memory System                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐        ┌──────────────────┐      │
│  │  Local Vector   │        │  OpenAI Thread   │      │
│  │     Store       │◄──────►│    Storage       │      │
│  └────────┬────────┘        └──────────────────┘      │
│           │                                             │
│  ┌────────▼────────┐        ┌──────────────────┐      │
│  │  Decay Engine   │        │  TMUX Context    │      │
│  │                 │◄──────►│    Manager       │      │
│  └────────┬────────┘        └──────────────────┘      │
│           │                                             │
│  ┌────────▼────────┐        ┌──────────────────┐      │
│  │ Squeaky Rules   │        │  Broadcast Hub   │      │
│  │    Engine       │◄──────►│                  │      │
│  └─────────────────┘        └──────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Data Flow
1. **Input**: Memory content + context enters system
2. **Classification**: Decay engine determines retention policy
3. **Storage**: Dual-layer save (local + cloud)
4. **Broadcast**: Relevant memories propagated to other instances
5. **Decay**: Automatic pruning based on policies
6. **Retrieval**: Semantic search with decay awareness

### File Structure
```
/Users/noshit/YOUR_PROJECT_DIR/automation_lab/
├── enhanced_vector_memory.py          # Core memory engine
├── memory_connector.py                # OpenAI integration
├── vector_memory/
│   ├── embeddings.json               # Vector embeddings
│   ├── breakthroughs.json           # Breakthrough memories
│   ├── tribal_knowledge.json        # Persistent knowledge
│   └── decay_log.json              # Pruned memory log
├── instance_memory_assistants.json   # Instance configurations
├── memory_backups/                  # Automated backups
├── broadcasts/                      # Broadcast logs
└── replit_endpoints/               # Replit API endpoints
```

---

## Core Concepts

### 1. Purposeful Decay

Memories are assigned decay policies based on content and context:

| Decay Type | TTL (days) | Use Case |
|------------|------------|----------|
| ephemeral | 7 | Temporary notes, quick thoughts |
| working | 30 | Active project memories |
| seasonal | 90 | Quarterly relevant information |
| annual | 365 | Yearly cycles, recurring events |
| permanent | ∞ | Never decay |
| squeaky_loud | ∞ | High-priority, always preserve |
| legal | ∞ | Legal/compliance records |
| financial | ∞ | Financial records |

### 2. Squeaky Levels

Environmental awareness for preservation priorities:

#### SQUEAKY_LOUD 🔊
- **Preserves**: Everything marked important
- **Keywords**: legal, financial, emergency, contract, deadline
- **Default decay**: None (permanent)
- **Use case**: Critical operations, legal matters

#### SQUEAKY_MEDIUM 🔔
- **Preserves**: Project-relevant information
- **Keywords**: important, meeting, decision, milestone
- **Default decay**: 90 days
- **Use case**: Standard operations

#### SQUEAKY_QUIET 🔇
- **Preserves**: Minimal set
- **Keywords**: note, idea, thought
- **Default decay**: 30 days
- **Use case**: Development, testing

### 3. TMUX Integration

Automatic context capture from terminal environment:

```python
{
    "in_tmux": true,
    "session": "legal-research",
    "window": "contracts",
    "pane": "2",
    "pane_title": "ARIBIA-TRO-Motion",
    "timestamp": "2024-01-15T10:30:00"
}
```

### 4. Memory Types

#### Embeddings
- Semantic vectors for similarity search
- OpenAI text-embedding-3-small or fallback
- Metadata includes decay and context

#### Breakthroughs
- Significant discoveries or insights
- Higher preservation priority
- Cross-instance broadcast enabled

#### Tribal Knowledge
- Institutional memory
- Never decays
- Shared across all instances

---

## Installation & Setup

### Prerequisites
```bash
# Required
python 3.8+
pip install openai scikit-learn numpy tiktoken

# Optional but recommended
tmux 3.0+
1password-cli
```

### Environment Variables
```bash
# ~/.zshrc or ~/.bashrc
export OPENAI_API_KEY="sk-..."
export CLAUDE_SQUEAKINESS="SQUEAKY_MEDIUM"  # or LOUD/QUIET
export CLAUDE_MEMORY_PATH="/Users/noshit/YOUR_PROJECT_DIR/automation_lab"
```

### Initial Setup
```bash
# 1. Clone the repository
cd /Users/noshit/YOUR_PROJECT_DIR/automation_lab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize memory system
python initialize_core_memories.py

# 4. Set up decay policies
python enhanced_vector_memory.py prune

# 5. Configure TMUX (optional)
echo "set -g status-right '#[fg=yellow]Mem: #{CLAUDE_MEMORIES} | %H:%M'" >> ~/.tmux.conf
```

### Cron Jobs
```bash
# Add to crontab
# Hourly pruning
0 * * * * cd /Users/noshit/YOUR_PROJECT_DIR/automation_lab && python enhanced_vector_memory.py prune

# Daily backup
0 2 * * * /Users/noshit/YOUR_PROJECT_DIR/automation_lab/daily_memory_backup.sh

# Weekly stats report
0 9 * * 1 cd /Users/noshit/YOUR_PROJECT_DIR/automation_lab && python memory_manager.py > weekly_report.txt
```

---

## API Reference

### Core Classes

#### EnhancedVectorMemoryWithDecay

Main memory management class with decay support.

```python
from enhanced_vector_memory import EnhancedVectorMemoryWithDecay

memory = EnhancedVectorMemoryWithDecay(base_path="/path/to/memory")
```

##### Methods

###### add_memory_with_decay()
```python
memory_id = memory.add_memory_with_decay(
    content="TRO motion filed with Your County court",
    context="Legal proceedings for YOUR_LLC",
    impact="Critical deadline for hearing",
    memory_type="breakthrough",
    decay_type="legal"  # Optional, auto-determined if not specified
)
```

###### vector_search_with_decay_awareness()
```python
results = memory.vector_search_with_decay_awareness(
    query="court filings",
    threshold=0.7,
    limit=10,
    include_expired=False  # Exclude expired memories
)
```

###### prune_expired_memories()
```python
pruned_count = memory.prune_expired_memories()
# Returns number of memories pruned
```

###### get_tmux_context()
```python
context = memory.get_tmux_context()
# Returns: {"in_tmux": true, "session": "legal", "window": "research", ...}
```

###### get_squeaky_level()
```python
level = memory.get_squeaky_level()
# Returns: "SQUEAKY_LOUD" | "SQUEAKY_MEDIUM" | "SQUEAKY_QUIET"
```

### Broadcast System

#### ReplitBroadcastSystem

Manages cross-instance memory synchronization.

```python
from replit_broadcast import ReplitBroadcastSystem

broadcaster = ReplitBroadcastSystem()
```

##### Methods

###### broadcast_memory()
```python
results = broadcaster.broadcast_memory(
    memory_data={
        "insight": "New legal precedent found",
        "context": "Illinois eviction law",
        "impact": "Changes TRO strategy"
    },
    source_instance="CLAUDESQ"
)
```

### Memory Assistants

Instance-specific memory interfaces.

```python
from create_instance_memory_assistants import InstanceMemoryAssistant

claudefo = InstanceMemoryAssistant("CLAUDEFO", "financial_operations")
```

---

## Configuration

### decay_config.json
```json
{
  "policies": {
    "ephemeral": 7,
    "working": 30,
    "seasonal": 90,
    "annual": 365,
    "permanent": null,
    "legal": null,
    "financial": null
  },
  "squeaky_rules": {
    "SQUEAKY_LOUD": {
      "preserve_keywords": ["legal", "financial", "emergency"],
      "default_decay": null
    },
    "SQUEAKY_MEDIUM": {
      "preserve_keywords": ["important", "meeting", "project"],
      "default_decay": "seasonal"
    },
    "SQUEAKY_QUIET": {
      "preserve_keywords": ["note", "idea"],
      "default_decay": "working"
    }
  }
}
```

### TMUX Configuration
```bash
# ~/.tmux.conf
# Set default squeaky level
set-environment -g CLAUDE_SQUEAKINESS "SQUEAKY_MEDIUM"

# Add memory count to status
set -g status-right '#[fg=yellow]Mem: #{CLAUDE_MEMORIES} | Squeaky: #{CLAUDE_SQUEAKINESS} | %H:%M'

# Project-specific overrides
bind-key L run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_LOUD"
bind-key M run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_MEDIUM"
bind-key Q run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_QUIET"
```

---

## Usage Examples

### 1. Legal Document Processing
```bash
# Set high preservation for legal session
tmux new -s legal-work
export CLAUDE_SQUEAKINESS="SQUEAKY_LOUD"

# Add legal memory (never decays)
python -c "
from enhanced_vector_memory import EnhancedVectorMemoryWithDecay
m = EnhancedVectorMemoryWithDecay()
m.add_memory_with_decay(
    'TRO hearing scheduled for Jan 20',
    'Your County Case 2024-CH-00123',
    decay_type='legal'
)
"
```

### 2. Development Notes
```bash
# Ephemeral session for testing
tmux new -s dev-scratch
export CLAUDE_SQUEAKINESS="SQUEAKY_QUIET"

# Add temporary note (7-day decay)
python -c "
from enhanced_vector_memory import EnhancedVectorMemoryWithDecay
m = EnhancedVectorMemoryWithDecay()
m.add_memory_with_decay(
    'Test API endpoint at localhost:3000',
    'Development testing',
    decay_type='ephemeral'
)
"
```

### 3. Financial Analysis
```python
# Python script for financial memory
from enhanced_vector_memory import EnhancedVectorMemoryWithDecay

memory = EnhancedVectorMemoryWithDecay()

# Add financial record (permanent)
memory.add_memory_with_decay(
    content="Q4 2024 rental income: $206,423.02",
    context="YOUR_LLC financial audit",
    impact="Validated for tax filing",
    decay_type="financial"
)

# Search financial memories
results = memory.vector_search_with_decay_awareness(
    "rental income 2024",
    include_expired=True  # Include all financial records
)
```

### 4. Cross-Instance Broadcast
```python
from replit_broadcast import ReplitBroadcastSystem

broadcaster = ReplitBroadcastSystem()

# Legal discovery broadcasts to all instances
broadcaster.broadcast_memory(
    memory_data={
        "insight": "Moskalets interference documented: $18,539 damages",
        "context": "TRO evidence package",
        "impact": "Critical for emergency motion"
    },
    source_instance="CLAUDESQ"
)
```

---

## Maintenance

### Daily Tasks
1. **Automatic Pruning**: Runs hourly via cron
2. **Backup**: Daily at 2 AM
3. **Status Check**: Monitor via TMUX status bar

### Weekly Tasks
```bash
# 1. Review decay log
python -c "
import json
with open('vector_memory/decay_log.json') as f:
    log = json.load(f)
print(f'Decayed this week: {len(log)} memories')
"

# 2. Analyze growth patterns
python memory_manager.py growth 7

# 3. Check instance health
python memory_manager.py stats
```

### Monthly Tasks
```bash
# 1. Full backup
python memory_manager.py backup monthly_$(date +%Y%m)

# 2. Analyze preservation effectiveness
python analyze_preservation.py

# 3. Optimize embeddings
python optimize_vectors.py
```

### Emergency Procedures

#### Memory Corruption
```bash
# 1. Stop all operations
pkill -f "python.*memory"

# 2. Restore from backup
cd memory_backups
tar -xzf daily_$(date +%Y%m%d).tar.gz
cp -r daily_*/vector_memory/* ../vector_memory/

# 3. Verify integrity
python verify_memory_integrity.py
```

#### Runaway Growth
```bash
# Aggressive pruning
python -c "
from enhanced_vector_memory import EnhancedVectorMemoryWithDecay
m = EnhancedVectorMemoryWithDecay()
# Override squeaky level temporarily
import os
os.environ['CLAUDE_SQUEAKINESS'] = 'SQUEAKY_QUIET'
m.prune_expired_memories()
"
```

---

## Troubleshooting

### Common Issues

#### 1. OpenAI API Errors
**Symptom**: Falling back to simple embeddings
```bash
# Check API key
echo $OPENAI_API_KEY

# Test connection
python -c "import openai; print(openai.OpenAI().models.list())"

# Solution: Fallback is automatic, but fix API key for better results
```

#### 2. TMUX Context Not Captured
**Symptom**: All memories show "in_tmux": false
```bash
# Verify TMUX environment
echo $TMUX

# Check TMUX version (needs 3.0+)
tmux -V

# Solution: Ensure running inside TMUX session
```

#### 3. Memories Not Decaying
**Symptom**: Storage growing infinitely
```bash
# Check cron job
crontab -l | grep prune

# Run manual prune with debug
python enhanced_vector_memory.py prune

# Check squeaky level
echo $CLAUDE_SQUEAKINESS
```

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

from enhanced_vector_memory import EnhancedVectorMemoryWithDecay
memory = EnhancedVectorMemoryWithDecay()
```

---

## Performance & Scaling

### Current Performance
- **Search latency**: 10-50ms (local), 100-200ms (with OpenAI)
- **Memory overhead**: ~1.5KB per memory
- **Embedding time**: ~100ms per memory (with OpenAI)
- **Prune time**: <1s for 10,000 memories

### Scaling Considerations

#### At 10,000 memories
- Storage: ~15MB
- Search time: ~100ms
- Monthly cost: ~$1

#### At 100,000 memories
- Storage: ~150MB
- Search time: ~500ms (consider indexing)
- Monthly cost: ~$10

#### At 1,000,000 memories
- Consider PostgreSQL with pgvector
- Implement sharding by instance
- Use dedicated vector database (Pinecone, Weaviate)

### Optimization Tips
1. **Batch embeddings**: Process multiple memories together
2. **Cache frequent searches**: Redis for common queries
3. **Partition by time**: Separate active/archive storage
4. **Compress old memories**: gzip memories older than 1 year

---

## Appendix

### A. Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | OpenAI API key | None |
| CLAUDE_SQUEAKINESS | Preservation level | SQUEAKY_MEDIUM |
| CLAUDE_MEMORY_PATH | Base directory | /Users/noshit/YOUR_PROJECT_DIR/automation_lab |
| CLAUDE_DECAY_DAYS | Default decay | 30 |

### B. File Formats

#### embeddings.json
```json
{
  "memory_id": {
    "content": "Memory content",
    "embedding": [0.123, -0.456, ...],
    "embedding_type": "openai",
    "created": "2024-01-15T10:30:00",
    "expires": "2024-04-15T10:30:00",
    "decay_type": "seasonal",
    "squeaky_level": "SQUEAKY_MEDIUM",
    "tmux_context": {...},
    "preserved": false
  }
}
```

### C. Recovery Scripts
Available in `/Users/noshit/YOUR_PROJECT_DIR/automation_lab/recovery/`:
- `restore_from_backup.sh`
- `verify_memory_integrity.py`
- `emergency_prune.py`
- `rebuild_embeddings.py`

---

*Last Updated: January 2024*
*Version: 2.0*
*Maintainer: METACLAUDE System Root*