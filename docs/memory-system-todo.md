# 📋 MEMORY SYSTEM IMPLEMENTATION TODO

## 🚨 Priority 1: Critical Missing Features (Do TODAY)

### ✅ 1. Implement Purposeful Decay (~30 mins)
- [ ] Backup current memory system
- [ ] Copy `enhanced_vector_memory_with_decay.py` from artifacts
- [ ] Add decay policies (ephemeral, working, seasonal, permanent)
- [ ] Set up hourly cron job for pruning
- [ ] Test with: `python enhanced_vector_memory_with_decay.py prune`

### ✅ 2. Add TMUX Integration (~15 mins)
- [ ] Update `.tmux.conf` with memory status line
- [ ] Add SQUEAKY level shortcuts (Ctrl-b L/M/Q)
- [ ] Set environment variable: `export CLAUDE_SQUEAKINESS="SQUEAKY_MEDIUM"`
- [ ] Test context capture in a tmux session

### ✅ 3. Fix Replit Broadcast System (~45 mins)
- [ ] Find missing Replit credentials in 1Password
- [ ] Deploy memory endpoints to each Replit instance
- [ ] Test broadcast: `python replit_broadcast.py test`
- [ ] Verify all 17 instances receive broadcasts

## 🧠 Priority 2: Cognitive Features (Do THIS WEEK)

### 🎭 4. Emotional Awareness (~20 mins)
- [ ] Run: `python /tmp/implement_cognitive.py`
- [ ] Source aliases: `source ~/.cognitive_memory_aliases`
- [ ] Test emotional detection with stressed content
- [ ] Verify importance boost working

### 👥 5. Transactive Memory (~15 mins)
- [ ] Configure memory partnerships in `cognitive_data.json`
- [ ] Test delegation: `mem-delegate "Q4 tax documents"`
- [ ] Add custom partnerships for your team

### 💭 6. Natural Search Delays (~10 mins)
- [ ] Test with complex query to see filler
- [ ] Adjust delay timing if needed (default 0.5s)
- [ ] Verify it feels natural

### 🏃‍♂️ 7. Cognitive Exercises (~30 mins)
- [ ] Enable: `mem-cognitive-on`
- [ ] Set initial difficulty level (1-10)
- [ ] Test first exercise: `mem-exercise`
- [ ] Schedule daily exercise reminder

## 🔧 Priority 3: System Optimization (Do THIS MONTH)

### 📊 8. Setup Monitoring (~20 mins)
- [ ] Create memory dashboard script
- [ ] Add to daily cron: memory stats email
- [ ] Set up backup rotation (keep 30 days)
- [ ] Monitor growth patterns

### 🚀 9. Performance Tuning (~30 mins)
- [ ] Batch embedding creation for bulk adds
- [ ] Implement memory indexing for >10k memories
- [ ] Add Redis cache for frequent searches
- [ ] Profile and optimize slow queries

### 📱 10. Integration Testing (~1 hour)
- [ ] Test all 17 Claude instances
- [ ] Verify cross-instance search
- [ ] Test memory delegation flow
- [ ] Ensure decay doesn't delete critical info

## 📝 Quick Test Checklist

```bash
# After implementation, run these tests:

# 1. Decay working?
echo "Test note" | python -c "from enhanced_vector_memory_with_decay import *; m = EnhancedVectorMemoryWithDecay(); m.add_memory_with_decay(input(), decay_type='ephemeral')"

# 2. TMUX context captured?
tmux new -s test
python -c "from enhanced_vector_memory_with_decay import *; m = EnhancedVectorMemoryWithDecay(); print(m.get_tmux_context())"

# 3. Emotional awareness?
python cognitive_memory.py add "URGENT deadline!" 
# Should detect stress

# 4. Delegation working?
mem-delegate "Invoice from accountant"
# Should suggest CLAUDEFO

# 5. Exercises enabled?
mem-exercise
# Should show a memory challenge

# 6. Broadcast system?
python replit_broadcast.py test
# Should reach all instances
```

## ⏱️ Time Estimate: ~4 hours total

### Today (1.5 hours):
- Decay implementation ✓
- TMUX integration ✓
- Replit broadcast fix ✓

### This Week (2 hours):
- All cognitive features ✓
- Basic testing ✓

### This Month (30 mins):
- Monitoring setup ✓
- Performance optimization ✓

## 🎯 Success Metrics

- [ ] Memory growth plateaus (not infinite)
- [ ] Search results more relevant when stressed
- [ ] Cognitive exercises completed daily
- [ ] All 17 instances syncing properly
- [ ] TMUX context visible in memories
- [ ] Emotional patterns tracked accurately

## 🚦 Go/No-Go Checklist

Before considering complete:
- [ ] Can you set SQUEAKY_LOUD and preserve everything?
- [ ] Do memories expire after set time?
- [ ] Does search add natural delays?
- [ ] Can you delegate memories to others?
- [ ] Do exercises adapt to your performance?
- [ ] Are all instances receiving broadcasts?

---

**Start with Priority 1 - just 1 hour to fix the critical issues!**