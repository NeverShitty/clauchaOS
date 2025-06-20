#!/usr/bin/env python3
"""
🧪 MEMORY DECAY DEMONSTRATION
Shows the difference between old and new memory systems
"""

import os
import json
from datetime import datetime, timedelta
from enhanced_vector_memory_with_decay import EnhancedVectorMemoryWithDecay

def demo_memory_decay():
    print("🧠 CLAUDE MEMORY DECAY DEMONSTRATION")
    print("=" * 50)
    
    # Initialize memory system
    memory = EnhancedVectorMemoryWithDecay()
    
    # Show current environment
    print(f"\n📊 Current Environment:")
    print(f"  SQUEAKY Level: {memory.get_squeaky_level()}")
    tmux = memory.get_tmux_context()
    if tmux.get("in_tmux"):
        print(f"  TMUX Session: {tmux['session']}")
        print(f"  TMUX Window: {tmux['window']}")
    else:
        print("  TMUX: Not in session")
    
    # Add various types of memories
    print(f"\n📝 Adding test memories...")
    
    test_memories = [
        # (content, context, decay_type, description)
        (
            "Remember to buy coffee", 
            "Shopping list", 
            "ephemeral",
            "Temporary note - expires in 7 days"
        ),
        (
            "Q1 2024 revenue target: $500K", 
            "Business planning", 
            "seasonal",
            "Quarterly info - expires in 90 days"
        ),
        (
            "TRO hearing scheduled for January 20, 2024", 
            "Your County Case 2024-CH-00123", 
            "legal",
            "Legal deadline - NEVER expires"
        ),
        (
            "Test API endpoint at localhost:3000", 
            "Development notes", 
            "ephemeral",
            "Dev note - expires in 7 days"
        ),
        (
            "YOUR_LLC 2024 tax filing complete", 
            "Financial records", 
            "financial",
            "Financial record - NEVER expires"
        ),
        (
            "Team standup moved to 10 AM", 
            "Meeting update", 
            None,  # Auto-determine
            "Auto-classified based on content"
        )
    ]
    
    added_memories = []
    for content, context, decay_type, description in test_memories:
        memory_id = memory.add_memory_with_decay(
            content=content,
            context=context,
            decay_type=decay_type
        )
        added_memories.append(memory_id)
        
        # Get the memory details
        mem_data = memory.embeddings.get(memory_id, {})
        actual_decay = mem_data.get("decay_type", "unknown")
        expires = mem_data.get("expires", "Never")
        if expires != "Never" and expires:
            try:
                exp_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                days_left = (exp_date - datetime.now()).days
                expires = f"{days_left} days"
            except:
                pass
        
        print(f"\n  ✅ Added: {content[:40]}...")
        print(f"     Type: {actual_decay} | Expires: {expires}")
        print(f"     {description}")
    
    # Show memory statistics
    print(f"\n📊 Memory Statistics:")
    stats = memory.get_memory_stats_with_decay()
    
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Preserved forever: {stats['preserved_count']}")
    print(f"\n  By decay type:")
    for decay_type, count in stats['by_decay_type'].items():
        print(f"    {decay_type}: {count}")
    
    print(f"\n  By squeaky level:")
    for level, count in stats['squeaky_distribution'].items():
        print(f"    {level}: {count}")
    
    # Demonstrate search with decay awareness
    print(f"\n🔍 Testing decay-aware search...")
    
    # Search for financial info (should always return)
    financial_results = memory.vector_search_with_decay_awareness("tax filing", include_expired=False)
    print(f"\n  Search: 'tax filing'")
    print(f"  Results: {len(financial_results)} found")
    if financial_results:
        print(f"  Top result: {financial_results[0]['content']}")
        print(f"  (This will NEVER expire - financial record)")
    
    # Simulate time passing and pruning
    print(f"\n⏰ Simulating expired memories...")
    
    # Manually expire one memory for demo
    if added_memories:
        test_id = added_memories[0]  # The coffee reminder
        if test_id in memory.embeddings:
            # Set to expired
            memory.embeddings[test_id]["expires"] = (datetime.now() - timedelta(days=1)).isoformat()
            memory.save_embeddings()
    
    # Run pruning
    print(f"\n🧹 Running pruning process...")
    pruned = memory.prune_expired_memories()
    print(f"  Pruned: {pruned} expired memories")
    
    # Show what would happen with different squeaky levels
    print(f"\n🔊 Squeaky Level Effects:")
    
    for level in ["SQUEAKY_QUIET", "SQUEAKY_MEDIUM", "SQUEAKY_LOUD"]:
        os.environ["CLAUDE_SQUEAKINESS"] = level
        rules = memory.SQUEAKY_RULES[level]
        print(f"\n  {level}:")
        print(f"    Preserve keywords: {', '.join(rules['preserve_keywords'][:3])}...")
        print(f"    Default decay: {rules['default_decay'] or 'Never'}")
        
    # Reset to original
    os.environ["CLAUDE_SQUEAKINESS"] = "SQUEAKY_MEDIUM"
    
    # Show the decay log
    if memory.decay_log:
        print(f"\n📋 Decay Log (pruned memories):")
        for memory_id, log_entry in list(memory.decay_log.items())[:3]:
            print(f"  - {log_entry['content']}")
            print(f"    Lived: {log_entry['lived_days']} days | Type: {log_entry['decay_type']}")
    
    print(f"\n✅ DEMO COMPLETE!")
    print(f"\n💡 Key Differences from Old System:")
    print("  1. Memories now expire based on content importance")
    print("  2. Legal/financial records are preserved forever")
    print("  3. TMUX context is captured for better organization")
    print("  4. Squeaky levels control preservation aggressiveness")
    print("  5. Automatic hourly pruning prevents infinite growth")

if __name__ == "__main__":
    demo_memory_decay()