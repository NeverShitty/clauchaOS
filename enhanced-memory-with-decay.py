#!/usr/bin/env python3
"""
🧠 ENHANCED VECTOR MEMORY WITH PURPOSEFUL DECAY
Implements TMUX integration, decay policies, and squeaky preservation
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tiktoken
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedVectorMemoryWithDecay:
    def __init__(self, base_path: str = "/Users/noshit/MCMANSION/AUTOMATION_LAB"):
        self.base_path = base_path
        self.memory_dir = os.path.join(base_path, "vector_memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # File paths
        self.embeddings_file = os.path.join(self.memory_dir, "embeddings.json")
        self.breakthroughs_file = os.path.join(self.memory_dir, "breakthroughs.json")
        self.tribal_knowledge_file = os.path.join(self.memory_dir, "tribal_knowledge.json")
        self.decay_log_file = os.path.join(self.memory_dir, "decay_log.json")
        
        # Load existing data
        self.embeddings = self._load_json(self.embeddings_file)
        self.breakthroughs = self._load_json(self.breakthroughs_file)
        self.tribal_knowledge = self._load_json(self.tribal_knowledge_file)
        self.decay_log = self._load_json(self.decay_log_file)
        
        # Decay policies (in days)
        self.DECAY_POLICIES = {
            "ephemeral": 7,        # Temporary thoughts, quick notes
            "working": 30,         # Active project memories
            "seasonal": 90,        # Quarterly relevance
            "annual": 365,         # Yearly cycles
            "permanent": None,     # Never decay
            "squeaky_loud": None,  # Always preserve (high priority)
            "legal": None,         # Legal/compliance - never decay
            "financial": None      # Financial records - never decay
        }
        
        # Squeaky preservation rules
        self.SQUEAKY_RULES = {
            "SQUEAKY_LOUD": {
                "preserve_keywords": ["legal", "financial", "emergency", "contract", "deadline", 
                                    "court", "judge", "filing", "payment", "invoice", "audit"],
                "default_decay": None,  # Never decay by default
                "min_confidence": 0.8   # High confidence threshold
            },
            "SQUEAKY_MEDIUM": {
                "preserve_keywords": ["important", "meeting", "decision", "project", "milestone"],
                "default_decay": "seasonal",  # 90 days default
                "min_confidence": 0.6
            },
            "SQUEAKY_QUIET": {
                "preserve_keywords": ["note", "idea", "thought", "maybe", "consider"],
                "default_decay": "working",  # 30 days default
                "min_confidence": 0.4
            }
        }
        
        # Initialize OpenAI if available
        self.openai_client = None
        self.embedding_model = "text-embedding-3-small"
        self._init_openai()
        
        # Prune on init
        self.prune_expired_memories()
    
    def get_tmux_context(self) -> Dict[str, Any]:
        """Get current tmux session/window/pane context"""
        try:
            # Check if we're in a tmux session
            in_tmux = os.environ.get('TMUX', None) is not None
            
            if not in_tmux:
                return {
                    "in_tmux": False,
                    "session": None,
                    "window": None,
                    "pane": None,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Get tmux context
            session = subprocess.run(
                ['tmux', 'display-message', '-p', '#S'],
                capture_output=True, text=True
            ).stdout.strip()
            
            window = subprocess.run(
                ['tmux', 'display-message', '-p', '#W'],
                capture_output=True, text=True
            ).stdout.strip()
            
            pane = subprocess.run(
                ['tmux', 'display-message', '-p', '#P'],
                capture_output=True, text=True
            ).stdout.strip()
            
            # Get pane title (might contain project info)
            pane_title = subprocess.run(
                ['tmux', 'display-message', '-p', '#T'],
                capture_output=True, text=True
            ).stdout.strip()
            
            return {
                "in_tmux": True,
                "session": session,
                "window": window,
                "pane": pane,
                "pane_title": pane_title,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting tmux context: {e}")
            return {
                "in_tmux": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_squeaky_level(self) -> str:
        """Get current squeaky level from environment or tmux"""
        # First check environment variable
        env_level = os.environ.get('CLAUDE_SQUEAKINESS', '').upper()
        if env_level in ['SQUEAKY_LOUD', 'SQUEAKY_MEDIUM', 'SQUEAKY_QUIET']:
            return env_level
        
        # Check tmux variable
        try:
            tmux_level = subprocess.run(
                ['tmux', 'show-environment', 'CLAUDE_SQUEAKINESS'],
                capture_output=True, text=True
            ).stdout.strip().split('=')[-1].upper()
            
            if tmux_level in ['SQUEAKY_LOUD', 'SQUEAKY_MEDIUM', 'SQUEAKY_QUIET']:
                return tmux_level
        except:
            pass
        
        # Default
        return 'SQUEAKY_MEDIUM'
    
    def determine_decay_type(self, content: str, context: str = "", 
                           explicit_type: Optional[str] = None) -> Tuple[str, int]:
        """Determine appropriate decay type based on content and context"""
        if explicit_type and explicit_type in self.DECAY_POLICIES:
            return explicit_type, self.DECAY_POLICIES[explicit_type]
        
        content_lower = content.lower()
        context_lower = context.lower()
        combined = f"{content_lower} {context_lower}"
        
        # Get current squeaky level
        squeaky_level = self.get_squeaky_level()
        rules = self.SQUEAKY_RULES[squeaky_level]
        
        # Check for preservation keywords
        for keyword in rules["preserve_keywords"]:
            if keyword in combined:
                # Check if it's a high-priority keyword
                if keyword in ["legal", "financial", "contract", "court", "audit"]:
                    return "legal", None
                elif keyword in ["emergency", "deadline", "filing"]:
                    return "squeaky_loud", None
        
        # Check tmux context for project-specific rules
        tmux_context = self.get_tmux_context()
        if tmux_context.get("in_tmux"):
            session = tmux_context.get("session", "").lower()
            
            # Session-based rules
            if "legal" in session or "litigation" in session:
                return "legal", None
            elif "finance" in session or "accounting" in session:
                return "financial", None
            elif "temp" in session or "scratch" in session:
                return "ephemeral", 7
        
        # Default based on squeaky level
        default_decay = rules["default_decay"]
        if default_decay:
            return default_decay, self.DECAY_POLICIES[default_decay]
        
        return "working", 30
    
    def calculate_expiry(self, ttl_days: Optional[int]) -> Optional[str]:
        """Calculate expiry timestamp"""
        if ttl_days is None:
            return None
        return (datetime.now() + timedelta(days=ttl_days)).isoformat()
    
    def should_preserve(self, memory: Dict[str, Any]) -> bool:
        """Determine if a memory should be preserved despite expiry"""
        # Check if it's marked as permanent
        decay_type = memory.get("decay_type", "")
        if decay_type in ["permanent", "legal", "financial", "squeaky_loud"]:
            return True
        
        # Check squeaky level at time of preservation check
        current_squeaky = self.get_squeaky_level()
        
        # SQUEAKY_LOUD preserves everything
        if current_squeaky == "SQUEAKY_LOUD":
            return True
        
        # Check preservation keywords
        content = memory.get("content", "").lower()
        rules = self.SQUEAKY_RULES[current_squeaky]
        
        for keyword in rules["preserve_keywords"]:
            if keyword in content:
                return True
        
        # Check if it's been accessed recently (within 7 days)
        last_accessed = memory.get("last_accessed")
        if last_accessed:
            try:
                last_date = datetime.fromisoformat(last_accessed.replace("Z", "+00:00"))
                if (datetime.now() - last_date).days < 7:
                    return True
            except:
                pass
        
        return False
    
    def add_memory_with_decay(self, content: str, context: str = "", 
                            impact: str = "", memory_type: str = "breakthrough",
                            decay_type: Optional[str] = None) -> str:
        """Add memory with decay metadata and tmux context"""
        # Determine decay policy
        determined_decay, ttl_days = self.determine_decay_type(
            content, context, decay_type
        )
        
        # Get contexts
        tmux_context = self.get_tmux_context()
        squeaky_level = self.get_squeaky_level()
        
        # Create memory ID
        memory_id = f"{memory_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create memory object
        memory = {
            "content": content,
            "context": context,
            "impact": impact,
            "created": datetime.now().isoformat(),
            "expires": self.calculate_expiry(ttl_days),
            "decay_type": determined_decay,
            "ttl_days": ttl_days,
            "squeaky_level": squeaky_level,
            "tmux_context": tmux_context,
            "access_count": 0,
            "last_accessed": datetime.now().isoformat(),
            "preserved": determined_decay in ["permanent", "legal", "financial", "squeaky_loud"]
        }
        
        # Add to appropriate storage
        if memory_type == "breakthrough":
            self.breakthroughs[memory_id] = memory
            self.save_breakthroughs()
            logger.info(f"💡 Added breakthrough (decay: {determined_decay}, expires: {ttl_days} days)")
        
        # Create embedding
        self._create_embedding_with_metadata(memory_id, content, memory)
        
        return memory_id
    
    def prune_expired_memories(self) -> int:
        """Prune expired memories based on decay policies"""
        logger.info("🧹 Pruning expired memories...")
        
        pruned_count = 0
        preserved_count = 0
        now = datetime.now()
        
        # Prune embeddings
        updated_embeddings = {}
        for memory_id, embedding_data in self.embeddings.items():
            expires = embedding_data.get("expires") or embedding_data.get("data", {}).get("expires")
            
            if expires:
                try:
                    expiry_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                    
                    if expiry_date < now:
                        # Check if should preserve
                        if self.should_preserve(embedding_data):
                            # Update as preserved
                            embedding_data["preserved"] = True
                            embedding_data["preservation_reason"] = "squeaky_rules"
                            updated_embeddings[memory_id] = embedding_data
                            preserved_count += 1
                            logger.info(f"  🛡️  Preserved: {embedding_data.get('content', '')[:50]}...")
                        else:
                            # Log decay
                            self.decay_log[memory_id] = {
                                "content": embedding_data.get("content", "")[:100],
                                "decayed_at": now.isoformat(),
                                "decay_type": embedding_data.get("decay_type", "unknown"),
                                "lived_days": (now - datetime.fromisoformat(
                                    embedding_data.get("created", now.isoformat()).replace("Z", "+00:00")
                                )).days
                            }
                            pruned_count += 1
                            logger.info(f"  🗑️  Pruned: {embedding_data.get('content', '')[:50]}...")
                    else:
                        updated_embeddings[memory_id] = embedding_data
                except Exception as e:
                    # Keep if can't parse date
                    updated_embeddings[memory_id] = embedding_data
            else:
                # No expiry = permanent
                updated_embeddings[memory_id] = embedding_data
        
        # Update storage
        self.embeddings = updated_embeddings
        self.save_embeddings()
        
        # Save decay log
        self._save_json(self.decay_log_file, self.decay_log)
        
        logger.info(f"✅ Pruning complete: {pruned_count} pruned, {preserved_count} preserved")
        
        # Update tmux status if in tmux
        if os.environ.get('TMUX'):
            try:
                total = len(self.embeddings)
                subprocess.run([
                    'tmux', 'set-environment', '-g', 
                    f'CLAUDE_MEMORIES', str(total)
                ])
            except:
                pass
        
        return pruned_count
    
    def update_access_time(self, memory_id: str):
        """Update last accessed time when memory is retrieved"""
        if memory_id in self.embeddings:
            self.embeddings[memory_id]["last_accessed"] = datetime.now().isoformat()
            self.embeddings[memory_id]["access_count"] = \
                self.embeddings[memory_id].get("access_count", 0) + 1
    
    def get_memory_stats_with_decay(self) -> Dict[str, Any]:
        """Get memory statistics including decay information"""
        stats = {
            "total_memories": len(self.embeddings),
            "by_decay_type": {},
            "expiring_soon": [],
            "preserved_count": 0,
            "avg_ttl_days": 0,
            "squeaky_distribution": {
                "SQUEAKY_LOUD": 0,
                "SQUEAKY_MEDIUM": 0,
                "SQUEAKY_QUIET": 0
            }
        }
        
        now = datetime.now()
        ttl_sum = 0
        ttl_count = 0
        
        for memory_id, memory_data in self.embeddings.items():
            # Count by decay type
            decay_type = memory_data.get("decay_type", "unknown")
            stats["by_decay_type"][decay_type] = \
                stats["by_decay_type"].get(decay_type, 0) + 1
            
            # Count preserved
            if memory_data.get("preserved", False):
                stats["preserved_count"] += 1
            
            # Count by squeaky level
            squeaky = memory_data.get("squeaky_level", "SQUEAKY_MEDIUM")
            if squeaky in stats["squeaky_distribution"]:
                stats["squeaky_distribution"][squeaky] += 1
            
            # Check if expiring soon (within 7 days)
            expires = memory_data.get("expires")
            if expires:
                try:
                    expiry_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                    days_left = (expiry_date - now).days
                    
                    if 0 < days_left <= 7:
                        stats["expiring_soon"].append({
                            "id": memory_id,
                            "content": memory_data.get("content", "")[:50] + "...",
                            "days_left": days_left,
                            "decay_type": decay_type
                        })
                    
                    # Calculate average TTL
                    if memory_data.get("ttl_days"):
                        ttl_sum += memory_data["ttl_days"]
                        ttl_count += 1
                except:
                    pass
        
        if ttl_count > 0:
            stats["avg_ttl_days"] = round(ttl_sum / ttl_count, 1)
        
        # Sort expiring soon by days left
        stats["expiring_soon"].sort(key=lambda x: x["days_left"])
        
        return stats
    
    def _create_embedding_with_metadata(self, memory_id: str, content: str, 
                                      metadata: Dict[str, Any]):
        """Create embedding with full metadata including decay info"""
        try:
            if self.openai_client:
                # Get OpenAI embedding
                response = self.openai_client.embeddings.create(
                    input=content,
                    model=self.embedding_model
                )
                embedding = response.data[0].embedding
                embedding_type = "openai"
            else:
                # Fallback to simple embedding
                embedding = self._simple_embedding(content)
                embedding_type = "simple"
            
            # Store with metadata
            self.embeddings[memory_id] = {
                "content": content,
                "embedding": embedding,
                "embedding_type": embedding_type,
                "metadata": metadata,
                "type": "breakthrough",
                **metadata  # Include all decay metadata at top level
            }
            
            self.save_embeddings()
            
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            # Always create at least a simple embedding
            self.embeddings[memory_id] = {
                "content": content,
                "embedding": self._simple_embedding(content),
                "embedding_type": "simple",
                "metadata": metadata,
                "type": "breakthrough",
                **metadata
            }
            self.save_embeddings()
    
    def vector_search_with_decay_awareness(self, query: str, threshold: float = 0.7, 
                                          limit: int = 10, include_expired: bool = False) -> List[Dict]:
        """Search memories with decay awareness"""
        results = self.vector_search(query, threshold, limit * 2)  # Get extra to account for filtering
        
        if not include_expired:
            # Filter out expired memories unless preserved
            now = datetime.now()
            filtered_results = []
            
            for result in results:
                memory_id = result.get("id", "")
                if memory_id in self.embeddings:
                    memory_data = self.embeddings[memory_id]
                    expires = memory_data.get("expires")
                    
                    if expires:
                        try:
                            expiry_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                            if expiry_date < now and not memory_data.get("preserved", False):
                                continue  # Skip expired
                        except:
                            pass
                    
                    # Update access time
                    self.update_access_time(memory_id)
                    filtered_results.append(result)
                    
                    if len(filtered_results) >= limit:
                        break
            
            results = filtered_results
        
        return results
    
    # Include all the existing methods from EnhancedVectorMemory
    def _init_openai(self):
        """Initialize OpenAI client if available"""
        try:
            import openai
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
                logger.info("✅ OpenAI connection established!")
            else:
                logger.warning("⚠️  No OpenAI API key found")
        except ImportError:
            logger.warning("⚠️  OpenAI library not installed")
    
    def _simple_embedding(self, text: str) -> list:
        """Fallback character frequency embedding"""
        embedding = [0] * 128
        for char in text.lower():
            if ord(char) < 128:
                embedding[ord(char)] += 1
        
        # Normalize
        total = sum(embedding)
        if total > 0:
            embedding = [x / total for x in embedding]
        
        return embedding
    
    def _load_json(self, filepath: str) -> dict:
        """Load JSON file or return empty dict"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_json(self, filepath: str, data: dict):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_embeddings(self):
        """Save embeddings to file"""
        self._save_json(self.embeddings_file, self.embeddings)
    
    def save_breakthroughs(self):
        """Save breakthroughs to file"""
        self._save_json(self.breakthroughs_file, self.breakthroughs)
    
    def vector_search(self, query: str, threshold: float = 0.7, limit: int = 10) -> List[Dict]:
        """Basic vector search (called by decay-aware version)"""
        if not self.embeddings:
            return []
        
        # Get query embedding
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=query,
                    model=self.embedding_model
                )
                query_embedding = np.array(response.data[0].embedding)
                comparing_openai = True
            except:
                query_embedding = np.array(self._simple_embedding(query))
                comparing_openai = False
        else:
            query_embedding = np.array(self._simple_embedding(query))
            comparing_openai = False
        
        # Calculate similarities
        similarities = []
        for memory_id, memory_data in self.embeddings.items():
            # Skip if embedding types don't match
            if comparing_openai and memory_data.get("embedding_type") != "openai":
                continue
            if not comparing_openai and memory_data.get("embedding_type") == "openai":
                continue
            
            memory_embedding = np.array(memory_data.get("embedding", []))
            
            if len(memory_embedding) > 0:
                similarity = cosine_similarity([query_embedding], [memory_embedding])[0][0]
                
                if similarity >= threshold:
                    similarities.append({
                        "id": memory_id,
                        "content": memory_data.get("content", ""),
                        "similarity": float(similarity),
                        "data": memory_data.get("data", memory_data.get("metadata", {})),
                        "type": memory_data.get("type", "unknown")
                    })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similarities[:limit]


# CLI Interface
if __name__ == "__main__":
    import sys
    
    memory = EnhancedVectorMemoryWithDecay()
    
    if len(sys.argv) == 1:
        # Show stats
        stats = memory.get_memory_stats_with_decay()
        print("\n🧠 MEMORY SYSTEM STATUS (With Decay)")
        print("=" * 50)
        print(f"Total memories: {stats['total_memories']}")
        print(f"Preserved: {stats['preserved_count']}")
        print(f"Average TTL: {stats['avg_ttl_days']} days")
        
        print("\n📊 By Decay Type:")
        for decay_type, count in stats['by_decay_type'].items():
            print(f"  {decay_type}: {count}")
        
        print("\n🔊 By Squeaky Level:")
        for level, count in stats['squeaky_distribution'].items():
            print(f"  {level}: {count}")
        
        if stats['expiring_soon']:
            print(f"\n⏰ Expiring Soon ({len(stats['expiring_soon'])}):")
            for mem in stats['expiring_soon'][:5]:
                print(f"  - {mem['content']} ({mem['days_left']} days)")
        
        print(f"\n🗂️ Current squeaky level: {memory.get_squeaky_level()}")
        
        tmux = memory.get_tmux_context()
        if tmux.get("in_tmux"):
            print(f"📺 TMUX context: {tmux['session']}:{tmux['window']}:{tmux['pane']}")
    
    elif sys.argv[1] == "add" and len(sys.argv) >= 3:
        content = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        decay_type = sys.argv[4] if len(sys.argv) > 4 else None
        
        memory_id = memory.add_memory_with_decay(content, context, decay_type=decay_type)
        print(f"✅ Added memory: {memory_id}")
    
    elif sys.argv[1] == "prune":
        pruned = memory.prune_expired_memories()
        print(f"🧹 Pruned {pruned} expired memories")
    
    elif sys.argv[1] == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        results = memory.vector_search_with_decay_awareness(query)
        
        print(f"\n🔍 Search results for: '{query}'")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['content']} ({result['similarity']:.3f})")
