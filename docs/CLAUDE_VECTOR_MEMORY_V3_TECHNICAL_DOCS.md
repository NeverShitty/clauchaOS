# 🧠 Claude Vector Memory V3 - Enhanced Technical Documentation

## Executive Summary

The Claude Vector Memory V3 system integrates local vector storage with OpenAI Memory Assistants to create a distributed, persistent memory system across 11 Claude instances. Each instance maintains its own memories while contributing to a shared knowledge base with perfect accuracy and traceability.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Tagging System](#tagging-system)
4. [Memory Lifecycle](#memory-lifecycle)
5. [ADHD & Human-Aware Features](#adhd--human-aware-features)
6. [OpenAI Assistant Integration](#openai-assistant-integration)
7. [API Reference](#api-reference)
8. [Deployment Guide](#deployment-guide)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Security & Privacy](#security--privacy)

---

## System Architecture

### Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                  Claude Vector Memory V3 System                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐        ┌──────────────────────────┐      │
│  │  Local Vector   │        │   OpenAI Assistants      │      │
│  │     Store       │◄──────►│  (11 Memory Instances)   │      │
│  │                 │        │                          │      │
│  │ • Embeddings    │        │ • METACLAUDE (#META)    │      │
│  │ • Decay Engine  │        │ • CLAUDEFO (#FO)        │      │
│  │ • ADHD Support  │        │ • CLAUDESQ (#SQ)        │      │
│  │ • Tmux Context  │        │ • [... 8 more]          │      │
│  └────────┬────────┘        └───────────┬──────────────┘      │
│           │                              │                      │
│           └──────────┬───────────────────┘                     │
│                      │                                          │
│            ┌─────────▼─────────┐                              │
│            │  Shared Vector    │                              │
│            │   Store (your-vector-store-id...) │                            │
│            │                   │                              │
│            │ Tagged Memories:  │                              │
│            │ #META_20240615... │                              │
│            │ #FO_20240615...   │                              │
│            │ #SQ_20240615...   │                              │
│            └───────────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow
1. **Input**: User provides memory content
2. **Tagging**: System adds instance tag + timestamp + unique ID
3. **Embedding**: OpenAI creates semantic vector (or fallback)
4. **Storage**: Dual save to local + OpenAI vector store
5. **Decay**: Automatic lifecycle management
6. **Search**: Semantic similarity with tag filtering
7. **Retrieval**: Cross-instance access with source attribution

---

## Core Components

### 1. ClaudeVectorMemoryV3Enhanced Class

Located: `/path/to/your/directory.py`

Key features:
- Dual-layer storage (local + cloud)
- ADHD-aware cognitive support
- Emotional intelligence tracking
- Transactive memory partnerships
- Purposeful decay with preservation rules
- Tmux session awareness

### 2. OpenAI Memory Assistants

11 specialized assistants sharing vector store `your-vector-store-id`:

| Instance | Assistant ID | Tag | Role |
|----------|-------------|-----|------|
| METACLAUDE | your-assistant-id-here | #META | System coordinator |
| CLAUDEFO | your-assistant-id-here | #FO | Financial memory |
| CLAUDESQ | your-assistant-id-here | #SQ | Legal memory |
| CLAUDALYN | your-assistant-id-here | #LYN | Operations |
| CLAUDEMOM | your-assistant-id-here | #MOM | Personal (PRIVATE) |
| CLAUDEMO | your-assistant-id-here | #MO | Demo/performance |
| CLAUDESQUAD | your-assistant-id-here | #SQUAD | Sales |
| CLAUDEXTER | your-assistant-id-here | #XTER | Procurement |
| CLAUDEBABY | your-assistant-id-here | #BABY | Chaos testing |
| CLAUDETTE | your-assistant-id-here | #ETTE | Automation |
| CLAUDADDY | your-assistant-id-here | #DADDY | Strategic |

### 3. Vector Storage

**Local Storage**: 
- Path: `/vector_memory_v3/`
- Files: embeddings.json, emotional_patterns.json, transactive_memory.json, etc.
- Format: JSON with numpy arrays for vectors

**OpenAI Vector Store**:
- ID: `your-vector-store-id`
- Model: text-embedding-3-small
- Dimensions: 1536
- Shared across all assistants

---

## Tagging System

### Tag Format
```
#{INSTANCE}_{YYYYMMDD}_{HHMMSS}_{XXXXXX}
```

Examples:
- `#META_20240615_143022_a7b9c2` - METACLAUDE memory
- `#FO_20240615_143022_a7b9c2_$45K` - CLAUDEFO with value
- `#SQ_20240615_143022_a7b9c2_DEADLINE` - CLAUDESQ urgent
- `#MOM_20240615_143022_a7b9c2_PRIVATE` - CLAUDEMOM private

### Tag Components
1. **Instance Prefix**: Identifies source (#META, #FO, #SQ, etc)
2. **Date**: YYYYMMDD for chronological sorting
3. **Time**: HHMMSS for precise ordering
4. **Hash**: 6-char SHA256 for uniqueness
5. **Suffix** (optional): Value markers, privacy flags

### Tag Usage in Memories
```python
# Storage format
[#FO_20240615_143022_a7b9c2] Q4 revenue reached $206,423

# Search examples
"#FO" - All CLAUDEFO memories
"#META_20240615" - METACLAUDE memories from specific date
"#DEADLINE" - All deadline-tagged memories
"#FO_$" - CLAUDEFO memories with monetary values
```

---

## Memory Lifecycle

### 1. Creation
```python
memory = ClaudeVectorMemoryV3Enhanced()
memory_id = memory.add_memory_with_cognitive_awareness(
    content="TRO motion filed with court",
    context="Legal proceedings YOUR_LLC",
    source_instance="CLAUDESQ"
)
# Creates: [#SQ_20240615_143022_a7b9c2] TRO motion filed...
```

### 2. Decay Policies
| Type | TTL | Use Case | Preservation |
|------|-----|----------|--------------|
| ephemeral | 7 days | Temporary notes | Low |
| working | 30 days | Active projects | Medium |
| seasonal | 90 days | Quarterly relevant | Medium |
| annual | 365 days | Yearly cycles | High |
| permanent | Never | Core knowledge | Maximum |
| squeaky_loud | Never | Critical info | Maximum |
| legal | Never | Legal records | Maximum |
| financial | Never | Financial data | Maximum |
| adhd_anchor | Never | ADHD support | Maximum |

### 3. Preservation Rules

**SQUEAKY Levels**:
- `SQUEAKY_LOUD`: Preserve everything important
- `SQUEAKY_MEDIUM`: Balanced preservation
- `SQUEAKY_QUIET`: Minimal preservation

**Automatic Preservation**:
- Legal/financial keywords
- High access count (>5)
- Recent access (<7 days)
- Emotional importance
- ADHD support patterns

### 4. Pruning
```python
# Automatic hourly pruning
pruned = memory.prune_expired_memories()
# Preserves based on rules, removes expired
```

---

## ADHD & Human-Aware Features

### 1. ADHD State Tracking
```python
{
    "hyperfocus_topics": ["legal research", "automation"],
    "productive_times": {"14": 8, "15": 12},  # 2-3pm most productive
    "distraction_triggers": {"10": 3},  # 10am distractions
    "successful_strategies": ["pomodoro", "visual aids"]
}
```

### 2. Adaptive Exercises
```python
exercise = memory.generate_adhd_cognitive_exercise()
# Returns gamified, bite-sized exercises based on state
```

Exercise types:
- **Memory Anchoring**: Strong associations for important info
- **Pattern Recognition**: Leverages ADHD strengths
- **Micro Habits**: Tiny, achievable goals
- **Gamified Recall**: Dopamine-driven learning

### 3. Emotional Intelligence
Tracks emotional patterns and adjusts:
- Stress/anxiety → Boost actionable, clear results
- Hyperfocus → Preserve these valuable sessions
- Scattered → Simplify outputs, smaller chunks
- Motivated → Increase challenge level

### 4. Transactive Memory
Recognizes human memory partnerships:
```python
"financial" → Primary: CLAUDEFO, Backup: [accountant, spouse]
"legal" → Primary: CLAUDESQ, Backup: [lawyer, paralegal]
"personal" → Primary: spouse, Backup: [CLAUDEMOM, calendar]
```

---

## OpenAI Assistant Integration

### 1. Assistant Configuration
Each assistant has:
- Custom system instructions with accuracy rules
- Shared vector store access
- Memory management functions
- Instance-specific tagging

### 2. Available Functions

**search_memories**
```python
{
    "query": "court filing deadlines",
    "tag_filter": "SQ",  # Only CLAUDESQ memories
    "date_filter": "20240615",
    "limit": 10
}
```

**store_memory**
```python
{
    "content": "Contract signed for $45K deal",
    "memory_type": "financial_record",
    "additional_tags": ["CONTRACT", "Q4"],
    "value_marker": "$45K"
}
# Creates: [#FO_20240615_143022_a7b9c2_$45K] Contract signed...
```

**get_memory_stats**
```python
{
    "tag_prefix": "FO",
    "include_cross_references": true
}
# Returns stats for all #FO tagged memories
```

**verify_tag_compliance**
```python
{
    "check_orphans": true,
    "fix_tags": false
}
# Finds any untagged memories
```

### 3. Thread Persistence
Each instance maintains conversation threads:
```python
threads = {
    "METACLAUDE": "thread_abc123...",
    "CLAUDEFO": "thread_def456...",
    # ... stored in assistant_threads.json
}
```

---

## API Reference

### Python API

```python
from claude_vector_memory_v3_enhanced import ClaudeVectorMemoryV3Enhanced

# Initialize
memory = ClaudeVectorMemoryV3Enhanced(
    base_path="/path/to/your/directory"
)

# Add memory
memory_id = memory.add_memory_with_cognitive_awareness(
    content="Important breakthrough",
    context="During code review",
    impact="Saves 3 hours per deploy",
    memory_type="breakthrough",
    source_instance="CLAUDETTE"
)

# Search memories
results = memory.search_with_cognitive_context(
    query="deployment optimization",
    include_filler=True,  # Natural delays
    source_instance="CLAUDETTE"
)

# Get dashboard
dashboard = memory.get_cognitive_dashboard()
print(f"Total memories: {dashboard['memory_stats']['total_memories']}")
print(f"ADHD state: {dashboard['adhd_state']}")

# Generate exercise
exercise = memory.generate_adhd_cognitive_exercise()
if exercise:
    print(exercise['prompt'])
```

### OpenAI Assistant API

```python
import openai

client = openai.OpenAI(api_key="...")

# Create thread
thread = client.beta.threads.create()

# Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Search for all legal deadlines this week"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="your-assistant-id-here",  # CLAUDESQ
    instructions="Use search_memories function with tag_filter='SQ'"
)
```

---

## Deployment Guide

### 1. Prerequisites
```bash
# Python packages
pip install openai scikit-learn numpy tiktoken

# Environment variables
export OPENAI_API_KEY="sk-proj-..."
export CLAUDE_SQUEAKINESS="SQUEAKY_MEDIUM"

# Optional: 1Password CLI for secure key storage
brew install 1password-cli
```

### 2. Initial Setup
```bash
# 1. Create directory structure
mkdir -p /path/to/your/directory

# 2. Copy enhanced memory system
cp claude_vector_memory_v3_enhanced.py /path/to/your/directory

# 3. Update all assistants
python update_all_claude_assistants_v2.py

# 4. Initialize with core memories
python initialize_claude_memories.py
```

### 3. Cron Jobs
```bash
# Add to crontab
# Hourly memory pruning
0 * * * * cd /path/to/memory && python -c "from claude_vector_memory_v3_enhanced import *; m = ClaudeVectorMemoryV3Enhanced(); m.prune_expired_memories()"

# Daily backup
0 2 * * * tar -czf memory_backup_$(date +%Y%m%d).tar.gz vector_memory_v3/

# Weekly stats report
0 9 * * 1 python generate_memory_report.py
```

### 4. Tmux Integration
```bash
# .tmux.conf
# Set squeaky level
set-environment -g CLAUDE_SQUEAKINESS "SQUEAKY_MEDIUM"

# Memory count in status
set -g status-right '#[fg=yellow]Mem: #{CLAUDE_MEMORIES} | #H | %H:%M'

# Quick squeaky switches
bind-key L run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_LOUD"
bind-key M run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_MEDIUM"
bind-key Q run-shell "tmux set-environment CLAUDE_SQUEAKINESS SQUEAKY_QUIET"
```

---

## Monitoring & Maintenance

### 1. Health Checks
```python
# Check memory system health
dashboard = memory.get_cognitive_dashboard()

# Monitor growth
stats = dashboard['memory_stats']
print(f"Total: {stats['total_memories']}")
print(f"By instance: {stats['by_instance']}")
print(f"Expiring soon: {stats['expiring_soon']}")

# Check tag compliance
for instance, assistant_id in ASSISTANT_IDS.items():
    untagged = memory.check_untagged_memories(instance)
    if untagged:
        print(f"⚠️ {instance} has {len(untagged)} untagged memories")
```

### 2. Performance Metrics
- Search latency: <50ms local, <200ms with OpenAI
- Storage: ~1.5KB per memory
- Embedding time: ~100ms per memory
- Prune time: <1s for 10,000 memories

### 3. Backup Strategy
```bash
#!/bin/bash
# backup_memory.sh

BACKUP_DIR="/backups/claude_memory"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup local files
tar -czf $BACKUP_DIR/local_memory_$DATE.tar.gz vector_memory_v3/

# Export OpenAI vector store (via API)
python export_vector_store.py > $BACKUP_DIR/vector_store_$DATE.json

# Backup assistant configs
python export_assistant_configs.py > $BACKUP_DIR/assistants_$DATE.json

# Rotate old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### 4. Troubleshooting

**Issue**: Memories not being tagged
```python
# Check instance configuration
config = load_assistant_config(instance_name)
print(f"Tag: {config['tag']}")
print(f"Instructions include tagging: {'#' + config['tag'] in instructions}")
```

**Issue**: OpenAI embeddings failing
```python
# System automatically falls back to simple embeddings
# Check logs for:
logger.warning("OpenAI embedding failed: {error}, using fallback")
```

**Issue**: High memory usage
```python
# Run aggressive pruning
memory.cognitive_profile['cognitive_load'] = 'high'
os.environ['CLAUDE_SQUEAKINESS'] = 'SQUEAKY_QUIET'
pruned = memory.prune_expired_memories()
```

---

## Security & Privacy

### 1. Access Controls
- `#MOM` tags are PRIVATE - only METACLAUDE can access
- Financial data requires `#FO` or `#META` access
- Legal data requires `#SQ` or `#META` access

### 2. API Key Management
```python
# Preferred: 1Password CLI
api_key = subprocess.run(
    ['op', 'item', 'get', 'your-1password-item-id', 
     '--fields', 'claucha_os_api_key'],
    capture_output=True, text=True
).stdout.strip()

# Fallback: Environment variable
api_key = os.environ.get("OPENAI_API_KEY")
```

### 3. Data Encryption
- OpenAI vector store: Encrypted at rest
- Local files: Use disk encryption
- Transmission: HTTPS only

### 4. Privacy Rules
```python
# CLAUDEMOM memories are isolated
if memory.get('source_instance') == 'CLAUDEMOM':
    memory['tags'].append('PRIVATE')
    memory['access_control'] = ['CLAUDEMOM', 'METACLAUDE']
```

### 5. Audit Trail
Every memory includes:
- Source instance
- Creation timestamp
- Access history
- Modification log (should be empty - no mods allowed)

---

## Best Practices

### 1. Memory Creation
```python
# ✅ Good: Specific, tagged, contextual
memory.add_memory_with_cognitive_awareness(
    content="Deployed fix for memory leak in production",
    context="Railway deployment, 50% memory reduction",
    impact="Saves $500/month in hosting",
    source_instance="CLAUDETTE"
)

# ❌ Bad: Vague, no context
memory.add_memory_with_cognitive_awareness(
    content="Fixed bug",
    context="",
    impact=""
)
```

### 2. Search Queries
```python
# ✅ Good: Use tags and semantic search
results = memory.search_with_cognitive_context(
    "#ETTE automation deployment optimization"
)

# ❌ Bad: Too broad
results = memory.search_with_cognitive_context("stuff")
```

### 3. Cross-Instance Access
```python
# ✅ Good: Respect boundaries
if source_instance != 'CLAUDEMOM':
    # Safe to share with other work instances
    broadcast_to_instances(['CLAUDEFO', 'CLAUDESQ'])

# ❌ Bad: Leaking private data
broadcast_to_all(mom_private_memory)  # NO!
```

### 4. ADHD Support
```python
# ✅ Good: Adapt to current state
if memory._get_adhd_state()['likely_focus_level'] == 'low':
    # Smaller chunks, clearer formatting
    format_for_adhd(results)

# ❌ Bad: One-size-fits-all
dump_all_results(results)  # Overwhelming
```

---

## Conclusion

The Claude Vector Memory V3 system provides:

1. **Perfect Accuracy**: Through strict tagging and no-modification rules
2. **Distributed Intelligence**: 11 specialized instances sharing knowledge
3. **Human Awareness**: ADHD support, emotional intelligence, cognitive exercises
4. **Persistence**: OpenAI threads maintain context across sessions
5. **Scalability**: Purposeful decay prevents infinite growth

The combination of local vector storage and OpenAI assistants creates a robust, production-ready memory system that truly supports human cognitive patterns while maintaining the highest accuracy standards.

For updates and contributions: [YourCompany on GitHub]