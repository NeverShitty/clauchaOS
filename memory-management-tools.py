#!/usr/bin/env python3
"""
🧠 MEMORY MANAGEMENT TOOLS
Pruning, stats, and backup utilities for the Claude memory system
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any
import subprocess
from enhanced_vector_memory import EnhancedVectorMemory

class MemoryManager:
    def __init__(self):
        self.memory = EnhancedVectorMemory()
        self.base_path = "/Users/noshit/MCMANSION/AUTOMATION_LAB"
        
    def prune_old_memories(self, days: int = 90) -> Dict[str, Any]:
        """Remove memories older than X days to prevent infinite growth"""
        print(f"🧹 PRUNING MEMORIES OLDER THAN {days} DAYS...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        pruned_count = 0
        kept_count = 0
        
        # Create a new dict for memories to keep
        updated_embeddings = {}
        updated_breakthroughs = {}
        
        # Check embeddings
        for memory_id, memory_data in self.memory.embeddings.items():
            # Get timestamp from metadata or data
            timestamp_str = (
                memory_data.get("metadata", {}).get("timestamp") or
                memory_data.get("timestamp") or
                memory_data.get("data", {}).get("timestamp")
            )
            
            if timestamp_str:
                try:
                    memory_date = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    if memory_date > cutoff_date:
                        updated_embeddings[memory_id] = memory_data
                        kept_count += 1
                    else:
                        pruned_count += 1
                        print(f"  🗑️  Pruning: {memory_data.get('content', '')[:50]}...")
                except:
                    # Keep if we can't parse the date
                    updated_embeddings[memory_id] = memory_data
                    kept_count += 1
            else:
                # Keep memories without timestamps (legacy)
                updated_embeddings[memory_id] = memory_data
                kept_count += 1
        
        # Check breakthroughs
        for breakthrough_id, breakthrough_data in self.memory.breakthroughs.items():
            timestamp_str = breakthrough_data.get("timestamp", "")
            if timestamp_str:
                try:
                    breakthrough_date = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    if breakthrough_date > cutoff_date:
                        updated_breakthroughs[breakthrough_id] = breakthrough_data
                except:
                    updated_breakthroughs[breakthrough_id] = breakthrough_data
            else:
                updated_breakthroughs[breakthrough_id] = breakthrough_data
        
        # Backup before pruning
        backup_path = f"{self.base_path}/memory_backups/pre_prune_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_path, exist_ok=True)
        
        # Save current state to backup
        shutil.copy2(
            f"{self.base_path}/vector_memory/embeddings.json",
            f"{backup_path}/embeddings.json"
        )
        shutil.copy2(
            f"{self.base_path}/vector_memory/breakthroughs.json",
            f"{backup_path}/breakthroughs.json"
        )
        
        # Update the memory system
        self.memory.embeddings = updated_embeddings
        self.memory.breakthroughs = updated_breakthroughs
        
        # Save pruned data
        self.memory.save_embeddings()
        self.memory.save_breakthroughs()
        
        results = {
            "pruned": pruned_count,
            "kept": kept_count,
            "total_before": pruned_count + kept_count,
            "total_after": kept_count,
            "backup_location": backup_path,
            "cutoff_date": cutoff_date.isoformat()
        }
        
        print(f"\n✅ PRUNING COMPLETE!")
        print(f"  Removed: {pruned_count} memories")
        print(f"  Kept: {kept_count} memories")
        print(f"  Backup: {backup_path}")
        
        return results
    
    def get_memory_stats(self, instance: str = None) -> Dict[str, Any]:
        """Get detailed memory statistics for all or specific instance"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "total_embeddings": len(self.memory.embeddings),
            "total_breakthroughs": len(self.memory.breakthroughs),
            "total_tribal_knowledge": len(self.memory.tribal_knowledge),
            "by_instance": {},
            "by_type": {
                "breakthrough": 0,
                "tribal_knowledge": 0,
                "cd2h_finding": 0,
                "other": 0
            },
            "by_embedding_type": {
                "openai": 0,
                "simple": 0
            },
            "top_instances": [],
            "memory_health": {}
        }
        
        # Count by instance
        instance_counts = {}
        for embedding_data in self.memory.embeddings.values():
            inst = embedding_data.get("metadata", {}).get("instance", "UNKNOWN")
            instance_counts[inst] = instance_counts.get(inst, 0) + 1
            
            # Count by type
            mem_type = embedding_data.get("type", "other")
            if mem_type in stats["by_type"]:
                stats["by_type"][mem_type] += 1
            else:
                stats["by_type"]["other"] += 1
            
            # Count by embedding type
            emb_type = embedding_data.get("embedding_type", "simple")
            if emb_type in stats["by_embedding_type"]:
                stats["by_embedding_type"][emb_type] += 1
        
        stats["by_instance"] = instance_counts
        stats["top_instances"] = sorted(
            instance_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Calculate health metrics
        total = stats["total_embeddings"]
        if total > 0:
            stats["memory_health"] = {
                "openai_coverage": round((stats["by_embedding_type"]["openai"] / total) * 100, 1),
                "breakthrough_ratio": round((stats["by_type"]["breakthrough"] / total) * 100, 1),
                "avg_memories_per_instance": round(total / max(len(instance_counts), 1), 1)
            }
        
        # Filter by instance if requested
        if instance:
            stats["filtered_instance"] = instance
            stats["instance_memories"] = instance_counts.get(instance, 0)
            stats["instance_percentage"] = round(
                (instance_counts.get(instance, 0) / total) * 100, 1
            ) if total > 0 else 0
        
        return stats
    
    def create_memory_dashboard(self) -> str:
        """Create a visual memory dashboard"""
        stats = self.get_memory_stats()
        
        dashboard = f"""
🧠 CLAUDE MEMORY SYSTEM DASHBOARD
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

📊 OVERALL STATISTICS
  Total Memories: {stats['total_embeddings']:,}
  Breakthroughs: {stats['total_breakthroughs']:,}
  Tribal Knowledge: {stats['total_tribal_knowledge']:,}

🏆 TOP INSTANCES BY MEMORY COUNT
"""
        for instance, count in stats['top_instances']:
            percentage = (count / stats['total_embeddings']) * 100 if stats['total_embeddings'] > 0 else 0
            bar = "█" * int(percentage / 2)
            dashboard += f"  {instance:12} {bar} {count:3} ({percentage:.1f}%)\n"
        
        dashboard += f"""
💾 MEMORY TYPES
  Breakthroughs:     {stats['by_type']['breakthrough']:4} ({stats['memory_health'].get('breakthrough_ratio', 0):.1f}%)
  Tribal Knowledge:  {stats['by_type']['tribal_knowledge']:4}
  CD2H Findings:     {stats['by_type']['cd2h_finding']:4}
  Other:             {stats['by_type']['other']:4}

🔧 EMBEDDING QUALITY
  OpenAI Embeddings: {stats['by_embedding_type']['openai']:4} ({stats['memory_health'].get('openai_coverage', 0):.1f}%)
  Simple Embeddings: {stats['by_embedding_type']['simple']:4}

📈 SYSTEM HEALTH
  OpenAI Coverage:        {stats['memory_health'].get('openai_coverage', 0):.1f}%
  Avg Memories/Instance:  {stats['memory_health'].get('avg_memories_per_instance', 0):.1f}
  Breakthrough Ratio:     {stats['memory_health'].get('breakthrough_ratio', 0):.1f}%

🌐 INSTANCE DISTRIBUTION
"""
        
        # Show all instances
        all_instances = sorted(stats['by_instance'].items())
        for instance, count in all_instances:
            dashboard += f"  {instance:15} {count:4} memories\n"
        
        return dashboard
    
    def backup_memory_system(self, backup_name: str = None) -> str:
        """Create a complete backup of the memory system"""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = f"{self.base_path}/memory_backups/{backup_name}"
        os.makedirs(backup_path, exist_ok=True)
        
        print(f"💾 BACKING UP MEMORY SYSTEM TO: {backup_path}")
        
        # Files to backup
        backup_files = [
            ("vector_memory/embeddings.json", "embeddings.json"),
            ("vector_memory/breakthroughs.json", "breakthroughs.json"),
            ("vector_memory/tribal_knowledge.json", "tribal_knowledge.json"),
            ("instance_memory_assistants.json", "instance_memory_assistants.json"),
            ("enhanced_vector_memory.py", "enhanced_vector_memory.py"),
            ("memory_connector.py", "memory_connector.py")
        ]
        
        backed_up = []
        for source, dest in backup_files:
            source_path = f"{self.base_path}/{source}"
            dest_path = f"{backup_path}/{dest}"
            
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                backed_up.append(dest)
                print(f"  ✅ {source}")
            else:
                print(f"  ⏭️  {source} (not found)")
        
        # Create backup metadata
        metadata = {
            "backup_name": backup_name,
            "timestamp": datetime.now().isoformat(),
            "stats": self.get_memory_stats(),
            "files_backed_up": backed_up,
            "backup_location": backup_path
        }
        
        with open(f"{backup_path}/backup_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create restore script
        restore_script = f"""#!/bin/bash
# Restore script for backup: {backup_name}
# Created: {datetime.now().isoformat()}

echo "🔄 RESTORING MEMORY SYSTEM FROM: {backup_name}"
echo "⚠️  This will overwrite current memory data. Continue? (y/n)"
read -r response

if [[ "$response" == "y" ]]; then
    # Backup current state first
    echo "💾 Backing up current state..."
    mkdir -p "{self.base_path}/memory_backups/pre_restore_$(date +%Y%m%d_%H%M%S)"
    cp -r "{self.base_path}/vector_memory/" "{self.base_path}/memory_backups/pre_restore_$(date +%Y%m%d_%H%M%S)/"
    
    # Restore from backup
    echo "📥 Restoring from backup..."
"""
        
        for source, dest in backup_files:
            restore_script += f'    cp "{backup_path}/{dest}" "{self.base_path}/{source}"\n'
        
        restore_script += """    
    echo "✅ Restore complete!"
else
    echo "❌ Restore cancelled."
fi
"""
        
        restore_script_path = f"{backup_path}/restore.sh"
        with open(restore_script_path, "w") as f:
            f.write(restore_script)
        os.chmod(restore_script_path, 0o755)
        
        print(f"\n✅ BACKUP COMPLETE!")
        print(f"  Location: {backup_path}")
        print(f"  Files: {len(backed_up)}")
        print(f"  Restore: bash {restore_script_path}")
        
        return backup_path
    
    def analyze_memory_growth(self, days: int = 30) -> Dict[str, Any]:
        """Analyze memory growth patterns over time"""
        print(f"📈 ANALYZING MEMORY GROWTH OVER {days} DAYS...")
        
        growth_data = {
            "period_days": days,
            "daily_growth": {},
            "instance_growth": {},
            "projected_growth": {}
        }
        
        # Group memories by day
        for memory_data in self.memory.embeddings.values():
            timestamp_str = (
                memory_data.get("metadata", {}).get("timestamp") or
                memory_data.get("timestamp") or
                memory_data.get("data", {}).get("timestamp")
            )
            
            if timestamp_str:
                try:
                    memory_date = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    day_key = memory_date.strftime("%Y-%m-%d")
                    
                    if day_key not in growth_data["daily_growth"]:
                        growth_data["daily_growth"][day_key] = 0
                    growth_data["daily_growth"][day_key] += 1
                    
                    # Track by instance
                    instance = memory_data.get("metadata", {}).get("instance", "UNKNOWN")
                    if instance not in growth_data["instance_growth"]:
                        growth_data["instance_growth"][instance] = {}
                    if day_key not in growth_data["instance_growth"][instance]:
                        growth_data["instance_growth"][instance][day_key] = 0
                    growth_data["instance_growth"][instance][day_key] += 1
                    
                except:
                    pass
        
        # Calculate growth rate
        if growth_data["daily_growth"]:
            total_memories = sum(growth_data["daily_growth"].values())
            active_days = len(growth_data["daily_growth"])
            avg_daily_growth = total_memories / active_days if active_days > 0 else 0
            
            growth_data["summary"] = {
                "total_memories_period": total_memories,
                "active_days": active_days,
                "avg_daily_growth": round(avg_daily_growth, 2),
                "projected_monthly": round(avg_daily_growth * 30, 0),
                "projected_yearly": round(avg_daily_growth * 365, 0)
            }
            
            # Calculate storage projections
            avg_memory_size = 1.5  # KB per memory (estimate)
            growth_data["projected_growth"] = {
                "monthly_storage_mb": round((avg_daily_growth * 30 * avg_memory_size) / 1024, 2),
                "yearly_storage_mb": round((avg_daily_growth * 365 * avg_memory_size) / 1024, 2),
                "api_cost_monthly": round(avg_daily_growth * 30 * 0.0001, 2),  # $0.0001 per embedding
                "api_cost_yearly": round(avg_daily_growth * 365 * 0.0001, 2)
            }
        
        return growth_data

# CLI Interface
if __name__ == "__main__":
    import sys
    
    manager = MemoryManager()
    
    if len(sys.argv) == 1:
        # Show dashboard by default
        print(manager.create_memory_dashboard())
        
    elif sys.argv[1] == "stats":
        # Detailed stats
        if len(sys.argv) > 2:
            stats = manager.get_memory_stats(instance=sys.argv[2])
        else:
            stats = manager.get_memory_stats()
        print(json.dumps(stats, indent=2))
        
    elif sys.argv[1] == "prune":
        # Prune old memories
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        results = manager.prune_old_memories(days=days)
        
    elif sys.argv[1] == "backup":
        # Create backup
        backup_name = sys.argv[2] if len(sys.argv) > 2 else None
        backup_path = manager.backup_memory_system(backup_name=backup_name)
        
    elif sys.argv[1] == "growth":
        # Analyze growth
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        growth = manager.analyze_memory_growth(days=days)
        
        print(f"\n📊 MEMORY GROWTH ANALYSIS ({days} days)")
        print("=" * 50)
        
        if "summary" in growth:
            print(f"Total memories added: {growth['summary']['total_memories_period']}")
            print(f"Average daily growth: {growth['summary']['avg_daily_growth']}")
            print(f"Projected monthly: {growth['summary']['projected_monthly']}")
            print(f"Projected yearly: {growth['summary']['projected_yearly']}")
            
            print(f"\n💾 STORAGE PROJECTIONS")
            print(f"Monthly: {growth['projected_growth']['monthly_storage_mb']} MB")
            print(f"Yearly: {growth['projected_growth']['yearly_storage_mb']} MB")
            
            print(f"\n💰 API COST PROJECTIONS")
            print(f"Monthly: ${growth['projected_growth']['api_cost_monthly']}")
            print(f"Yearly: ${growth['projected_growth']['api_cost_yearly']}")
        
    else:
        print("🧠 MEMORY MANAGEMENT TOOLS")
        print("\nUsage:")
        print("  python memory_manager.py                    # Show dashboard")
        print("  python memory_manager.py stats [instance]   # Detailed statistics")
        print("  python memory_manager.py prune [days]       # Prune old memories")
        print("  python memory_manager.py backup [name]      # Create backup")
        print("  python memory_manager.py growth [days]      # Analyze growth patterns")
