#!/usr/bin/env python3
"""
🧠 CLAUDE VECTOR MEMORY V3 - ENHANCED WITH OPENAI MEMORY ASSISTANTS
Integrates all the best features from your existing systems plus new enhancements
"""

import os
import json
import time
import random
import asyncio
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

# OpenAI imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not installed - falling back to simple embeddings")

logger = logging.getLogger(__name__)

class ClaudeVectorMemoryV3Enhanced:
    def __init__(self, base_path: str = "/path/to/your/directory"):
        self.base_path = base_path
        self.memory_dir = os.path.join(base_path, "vector_memory_v3")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Core memory files
        self.embeddings_file = os.path.join(self.memory_dir, "embeddings.json")
        self.emotional_patterns_file = os.path.join(self.memory_dir, "emotional_patterns.json")
        self.transactive_memory_file = os.path.join(self.memory_dir, "transactive_memory.json")
        self.cognitive_profile_file = os.path.join(self.memory_dir, "cognitive_profile.json")
        self.decay_log_file = os.path.join(self.memory_dir, "decay_log.json")
        self.adhd_patterns_file = os.path.join(self.memory_dir, "adhd_patterns.json")
        
        # Load data
        self.embeddings = self._load_json(self.embeddings_file)
        self.emotional_patterns = self._load_json(self.emotional_patterns_file)
        self.transactive_memory = self._load_json(self.transactive_memory_file)
        self.cognitive_profile = self._load_json(self.cognitive_profile_file)
        self.decay_log = self._load_json(self.decay_log_file)
        self.adhd_patterns = self._load_json(self.adhd_patterns_file)
        
        # Initialize profiles if new
        if not self.cognitive_profile:
            self.cognitive_profile = self._init_cognitive_profile()
        if not self.adhd_patterns:
            self.adhd_patterns = self._init_adhd_patterns()
        
        # Decay policies with ADHD awareness
        self.DECAY_POLICIES = {
            "ephemeral": 7,        # Temporary thoughts
            "working": 30,         # Active project memories
            "seasonal": 90,        # Quarterly relevance
            "annual": 365,         # Yearly cycles
            "permanent": None,     # Never decay
            "squeaky_loud": None,  # High priority preservation
            "legal": None,         # Legal/compliance
            "financial": None,     # Financial records
            "adhd_anchor": None,   # ADHD support memories - never decay
            "habit_building": 60   # Habit formation memories
        }
        
        # Emotional triggers with ADHD awareness
        self.EMOTIONAL_TRIGGERS = {
            "stress": ["deadline", "urgent", "emergency", "pressure", "overwhelmed", "stressed"],
            "joy": ["success", "achievement", "happy", "excited", "wonderful", "great", "progress"],
            "anxiety": ["worried", "nervous", "uncertain", "afraid", "concern", "anxious"],
            "frustration": ["stuck", "confused", "difficult", "problem", "issue", "broken", "blocked"],
            "pride": ["accomplished", "proud", "finished", "completed", "solved", "fixed"],
            "curiosity": ["interesting", "wonder", "how", "why", "learn", "discover"],
            "hyperfocus": ["flow", "zone", "focused", "absorbed", "deep", "intense"],
            "scattered": ["distracted", "jumping", "scattered", "unfocused", "chaotic"],
            "motivated": ["excited", "energized", "ready", "pumped", "driven"]
        }
        
        # ADHD-aware memory partnerships
        self.MEMORY_PARTNERSHIPS = {
            "technical": {
                "primary": "user",
                "backup": ["Claude", "documentation", "stackoverflow"],
                "keywords": ["code", "debug", "algorithm", "system", "technical"]
            },
            "financial": {
                "primary": "CLAUDEFO",
                "backup": ["accountant", "spouse", "quickbooks"],
                "keywords": ["tax", "invoice", "payment", "revenue", "expense"]
            },
            "legal": {
                "primary": "CLAUDESQ",
                "backup": ["lawyer", "paralegal", "case_files"],
                "keywords": ["contract", "filing", "court", "legal", "lawsuit"]
            },
            "personal": {
                "primary": "spouse",
                "backup": ["user", "CLAUDEMOM", "calendar"],
                "keywords": ["birthday", "anniversary", "family", "personal", "appointment"]
            },
            "habits": {
                "primary": "user",
                "backup": ["CLAUDETTE", "reminders", "apps"],
                "keywords": ["routine", "habit", "daily", "practice", "schedule"]
            }
        }
        
        # ADHD cognitive exercise modes
        self.ADHD_EXERCISE_MODES = {
            "memory_anchoring": {
                "description": "Create strong associations for important info",
                "adhd_benefit": "Helps with working memory challenges",
                "frequency": "per_session"
            },
            "pattern_recognition": {
                "description": "Identify patterns in chaos",
                "adhd_benefit": "Leverages ADHD pattern-matching strengths",
                "frequency": "daily"
            },
            "micro_habits": {
                "description": "Build tiny, achievable habits",
                "adhd_benefit": "Works with ADHD attention spans",
                "frequency": "multiple_daily"
            },
            "gamified_recall": {
                "description": "Memory challenges with rewards",
                "adhd_benefit": "Dopamine-driven learning",
                "frequency": "adaptive"
            },
            "context_switching": {
                "description": "Practice smooth transitions",
                "adhd_benefit": "Reduces transition friction",
                "frequency": "as_needed"
            }
        }
        
        # Squeaky preservation rules
        self.SQUEAKY_RULES = {
            "SQUEAKY_LOUD": {
                "preserve_keywords": ["legal", "financial", "emergency", "contract", "deadline", 
                                    "court", "judge", "filing", "payment", "invoice", "audit"],
                "default_decay": None,
                "min_confidence": 0.8
            },
            "SQUEAKY_MEDIUM": {
                "preserve_keywords": ["important", "meeting", "decision", "project", "milestone"],
                "default_decay": "seasonal",
                "min_confidence": 0.6
            },
            "SQUEAKY_QUIET": {
                "preserve_keywords": ["note", "idea", "thought", "maybe", "consider"],
                "default_decay": "working",
                "min_confidence": 0.4
            }
        }
        
        # Initialize OpenAI
        self.openai_client = None
        self.embedding_model = "text-embedding-3-small"
        self._init_openai()
        
        # OpenAI Assistant IDs (from your pairing file)
        self.ASSISTANT_IDS = {
            "METACLAUDE": "your-assistant-id-here",
            "CLAUDALYN": "your-assistant-id-here",
            "CLAUDEFO": "your-assistant-id-here",
            "CLAUDESQ": "your-assistant-id-here",
            "CLAUDEMOM": "your-assistant-id-here",
            "CLAUDEMO": "your-assistant-id-here",
            "CLAUDESQUAD": "your-assistant-id-here",
            "CLAUDEXTER": "your-assistant-id-here",
            "CLAUDEBABY": "your-assistant-id-here",
            "CLAUDETTE": "your-assistant-id-here",
            "CLAUDADDY": "your-assistant-id-here"
        }
        
        # Thread management
        self.threads_file = os.path.join(self.memory_dir, "assistant_threads.json")
        self.threads = self._load_json(self.threads_file)
        
        # Prune on init
        self.prune_expired_memories()
    
    def _init_cognitive_profile(self) -> Dict[str, Any]:
        """Initialize user's cognitive profile with ADHD awareness"""
        return {
            "user_id": "primary",
            "created": datetime.now().isoformat(),
            "exercise_enabled": True,
            "adhd_mode": True,
            "current_difficulty": 5,
            "comfort_zone": {
                "lower": 3,
                "upper": 7
            },
            "strengths": ["pattern_recognition", "creative_connections", "hyperfocus"],
            "areas_for_growth": ["working_memory", "task_switching", "time_awareness"],
            "exercise_history": [],
            "last_exercise": None,
            "cognitive_load": "normal",
            "preferred_modalities": ["visual", "kinesthetic", "gamified"],
            "memory_partnerships": {},
            "adhd_preferences": {
                "chunk_size": "small",
                "repetition_needed": True,
                "visual_aids": True,
                "gamification": True,
                "immediate_feedback": True
            }
        }
    
    def _init_adhd_patterns(self) -> Dict[str, Any]:
        """Initialize ADHD pattern tracking"""
        return {
            "hyperfocus_topics": {},
            "distraction_triggers": {},
            "productive_times": {},
            "energy_patterns": {},
            "transition_friction": {},
            "dopamine_responses": {},
            "successful_strategies": [],
            "habit_streaks": {}
        }
    
    def get_tmux_context(self) -> Dict[str, Any]:
        """Get current tmux session/window/pane context"""
        try:
            in_tmux = os.environ.get('TMUX', None) is not None
            
            if not in_tmux:
                return {
                    "in_tmux": False,
                    "session": None,
                    "window": None,
                    "pane": None,
                    "timestamp": datetime.now().isoformat()
                }
            
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
        env_level = os.environ.get('CLAUDE_SQUEAKINESS', '').upper()
        if env_level in ['SQUEAKY_LOUD', 'SQUEAKY_MEDIUM', 'SQUEAKY_QUIET']:
            return env_level
        
        try:
            tmux_level = subprocess.run(
                ['tmux', 'show-environment', 'CLAUDE_SQUEAKINESS'],
                capture_output=True, text=True
            ).stdout.strip().split('=')[-1].upper()
            
            if tmux_level in ['SQUEAKY_LOUD', 'SQUEAKY_MEDIUM', 'SQUEAKY_QUIET']:
                return tmux_level
        except:
            pass
        
        return 'SQUEAKY_MEDIUM'
    
    def analyze_emotional_context_with_adhd(self, content: str, context: str = "") -> Dict[str, Any]:
        """Analyze emotional triggers with ADHD awareness"""
        combined = f"{content} {context}".lower()
        
        emotional_scores = {}
        triggered_emotions = []
        
        for emotion, keywords in self.EMOTIONAL_TRIGGERS.items():
            score = sum(1 for keyword in keywords if keyword in combined)
            if score > 0:
                emotional_scores[emotion] = score
                triggered_emotions.append(emotion)
        
        # Update emotional patterns
        if triggered_emotions:
            timestamp = datetime.now().isoformat()
            date_key = timestamp[:10]
            hour_key = timestamp[11:13]
            
            if date_key not in self.emotional_patterns:
                self.emotional_patterns[date_key] = {}
            
            for emotion in triggered_emotions:
                if emotion not in self.emotional_patterns[date_key]:
                    self.emotional_patterns[date_key][emotion] = 0
                self.emotional_patterns[date_key][emotion] += 1
            
            # Track ADHD-specific patterns
            if "hyperfocus" in triggered_emotions:
                topic = self._extract_topic(content)
                if topic not in self.adhd_patterns["hyperfocus_topics"]:
                    self.adhd_patterns["hyperfocus_topics"][topic] = []
                self.adhd_patterns["hyperfocus_topics"][topic].append(timestamp)
            
            if "scattered" in triggered_emotions:
                self.adhd_patterns["distraction_triggers"][hour_key] = \
                    self.adhd_patterns["distraction_triggers"].get(hour_key, 0) + 1
        
        # Determine memory importance with ADHD considerations
        importance_boost = 0
        if "hyperfocus" in triggered_emotions:
            importance_boost = 0.4  # Hyperfocus memories are often valuable
        if "stress" in triggered_emotions or "anxiety" in triggered_emotions:
            importance_boost = 0.3
        if "motivated" in triggered_emotions or "pride" in triggered_emotions:
            importance_boost = 0.25  # Positive reinforcement important for ADHD
        
        return {
            "emotions": triggered_emotions,
            "scores": emotional_scores,
            "importance_boost": importance_boost,
            "emotional_state": self._get_current_emotional_state(),
            "adhd_state": self._get_adhd_state()
        }
    
    def _get_adhd_state(self) -> Dict[str, Any]:
        """Analyze current ADHD patterns"""
        current_hour = datetime.now().hour
        
        # Check if this is typically a productive time
        productive_score = self.adhd_patterns["productive_times"].get(str(current_hour), 0)
        distraction_score = self.adhd_patterns["distraction_triggers"].get(str(current_hour), 0)
        
        state = {
            "likely_focus_level": "high" if productive_score > distraction_score else "low",
            "recommended_chunk_size": "small" if distraction_score > 5 else "medium",
            "needs_break": (datetime.now() - datetime.fromisoformat(
                self.cognitive_profile.get("last_break", datetime.now().isoformat())
            )).seconds > 3600  # Need break every hour
        }
        
        return state
    
    def add_memory_with_cognitive_awareness(self, content: str, context: str = "",
                                          impact: str = "", memory_type: str = "general",
                                          source_instance: str = "user") -> str:
        """Add memory with emotional, transactive, and ADHD awareness"""
        
        # Analyze emotional and ADHD context
        emotional_context = self.analyze_emotional_context_with_adhd(content, context)
        
        # Identify memory ownership
        ownership = self.identify_memory_owner(content, context)
        
        # Determine decay based on multiple factors
        decay_type = self._determine_intelligent_decay(
            content, context, emotional_context, ownership
        )
        
        # Create memory ID
        memory_id = f"{memory_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get tmux context
        tmux_context = self.get_tmux_context()
        
        # Calculate expiry
        ttl_days = self.DECAY_POLICIES.get(decay_type)
        expires = None
        if ttl_days:
            expires = (datetime.now() + timedelta(days=ttl_days)).isoformat()
        
        memory = {
            "content": content,
            "context": context,
            "impact": impact,
            "created": datetime.now().isoformat(),
            "expires": expires,
            "type": memory_type,
            "decay_type": decay_type,
            "emotional_context": emotional_context,
            "ownership": ownership,
            "cognitive_load": self.cognitive_profile.get("cognitive_load", "normal"),
            "exercise_eligible": self._is_exercise_eligible(content, emotional_context),
            "tmux_context": tmux_context,
            "squeaky_level": self.get_squeaky_level(),
            "source_instance": source_instance,
            "access_count": 0,
            "last_accessed": datetime.now().isoformat()
        }
        
        # Create embedding
        embedding = self._create_embedding(content)
        
        # Store memory with embedding
        self.embeddings[memory_id] = {
            "embedding": embedding,
            "embedding_type": "openai" if self.openai_client else "simple",
            **memory
        }
        
        # Update transactive memory map
        self._update_transactive_memory(ownership, content)
        
        # Save to persistent storage
        self.save_all_data()
        
        # If OpenAI available, also save to assistant thread
        if self.openai_client and source_instance in self.ASSISTANT_IDS:
            self._save_to_assistant_thread(source_instance, memory_id, memory)
        
        logger.info(f"💭 Added memory with emotional state: {emotional_context['emotional_state']}")
        logger.info(f"👥 Memory owner: {ownership['primary']} (confidence: {ownership['confidence']:.2f})")
        logger.info(f"⏰ Decay type: {decay_type} (expires: {expires or 'never'})")
        
        return memory_id
    
    def _determine_intelligent_decay(self, content: str, context: str, 
                                   emotional_context: Dict, ownership: Dict) -> str:
        """Determine decay type based on multiple factors"""
        combined = f"{content} {context}".lower()
        
        # Check for preservation keywords
        squeaky_level = self.get_squeaky_level()
        rules = self.SQUEAKY_RULES[squeaky_level]
        
        for keyword in rules["preserve_keywords"]:
            if keyword in combined:
                if keyword in ["legal", "financial", "contract", "court", "audit"]:
                    return "legal"
                elif keyword in ["emergency", "deadline", "filing"]:
                    return "squeaky_loud"
        
        # ADHD-specific preservation
        if any(word in combined for word in ["habit", "routine", "reminder", "system"]):
            return "adhd_anchor"
        
        # High emotional importance
        if emotional_context["importance_boost"] > 0.3:
            return "seasonal"
        
        # Delegate to others
        if ownership["primary"] != "user" and ownership["confidence"] > 0.7:
            return "ephemeral"
        
        # Tmux context rules
        tmux_context = self.get_tmux_context()
        if tmux_context.get("in_tmux"):
            session = tmux_context.get("session", "").lower()
            if "legal" in session or "litigation" in session:
                return "legal"
            elif "finance" in session or "accounting" in session:
                return "financial"
            elif "temp" in session or "scratch" in session:
                return "ephemeral"
        
        # Default based on squeaky level
        return rules.get("default_decay", "working")
    
    def search_with_cognitive_context(self, query: str, include_filler: bool = True,
                                    source_instance: str = "user") -> List[Dict]:
        """Search with ADHD-aware context and natural delays"""
        
        # ADHD-friendly search feedback
        if include_filler and len(query.split()) > 3:
            adhd_state = self._get_adhd_state()
            
            if adhd_state["likely_focus_level"] == "low":
                fillers = [
                    "Let me focus on that for you...",
                    "Gathering the scattered pieces...",
                    "Pulling this together, one sec...",
                    "Let me collect those thoughts..."
                ]
            else:
                fillers = [
                    "Hmm, let me think about that for a second...",
                    "That's an interesting question, let me search my memory...",
                    "Give me a moment to recall that information...",
                    "Let me dig into that for you..."
                ]
            
            print(random.choice(fillers))
            time.sleep(0.5)  # Brief pause for realism
        
        # Check memory partnerships
        ownership = self.identify_memory_owner(query)
        
        if ownership["primary"] != source_instance and ownership["confidence"] > 0.7:
            print(f"💭 This might be something {ownership['primary']} would remember better...")
            print(f"   You might also check with: {', '.join(ownership['backup'])}")
        
        # Perform search
        results = self._vector_search_internal(query)
        
        # Boost results based on current state
        emotional_state = self._get_current_emotional_state()
        adhd_state = self._get_adhd_state()
        
        if emotional_state in ["stressed", "anxious"]:
            results = self._boost_actionable_results(results)
        
        if adhd_state["likely_focus_level"] == "low":
            # When distracted, prioritize simple, clear results
            results = self._boost_simple_results(results)
        
        # Update access times
        for result in results:
            if "id" in result:
                self._update_access_time(result["id"])
        
        return results
    
    def generate_adhd_cognitive_exercise(self) -> Optional[Dict[str, Any]]:
        """Generate brain exercise specifically designed for ADHD"""
        if not self.cognitive_profile.get("exercise_enabled", False):
            return None
        
        # Check if enough time has passed (shorter for ADHD - more frequent, smaller exercises)
        last_exercise = self.cognitive_profile.get("last_exercise")
        if last_exercise:
            last_date = datetime.fromisoformat(last_exercise.replace("Z", "+00:00"))
            if (datetime.now() - last_date).total_seconds() < 1800:  # 30 min intervals
                return None
        
        # Get current ADHD state
        adhd_state = self._get_adhd_state()
        
        # Select appropriate exercise type
        if adhd_state["likely_focus_level"] == "high":
            exercise_types = ["pattern_recognition", "memory_anchoring"]
        else:
            exercise_types = ["micro_habits", "gamified_recall"]
        
        exercise_type = random.choice(exercise_types)
        
        # Get eligible memories (prefer recent, emotionally positive ones for ADHD)
        eligible_memories = []
        for mem_id, memory in self.embeddings.items():
            if memory.get("exercise_eligible", False):
                days_old = (datetime.now() - datetime.fromisoformat(
                    memory["created"].replace("Z", "+00:00")
                )).days
                
                # ADHD benefits from more recent memories
                if 1 <= days_old <= 3:
                    # Prefer positive memories for dopamine
                    emotions = memory.get("emotional_context", {}).get("emotions", [])
                    if any(e in emotions for e in ["joy", "pride", "motivated"]):
                        eligible_memories.append((mem_id, memory, 2))  # Higher weight
                    else:
                        eligible_memories.append((mem_id, memory, 1))
        
        if not eligible_memories:
            return None
        
        # Weight selection toward positive memories
        weights = [w for _, _, w in eligible_memories]
        selected = random.choices(eligible_memories, weights=weights, k=1)[0]
        memory_id, memory, _ = selected
        
        exercise = self._create_adhd_exercise(exercise_type, memory_id, memory)
        
        # Update profile
        self.cognitive_profile["last_exercise"] = datetime.now().isoformat()
        self.cognitive_profile["exercise_history"].append(exercise)
        self.save_all_data()
        
        return exercise
    
    def _create_adhd_exercise(self, exercise_type: str, memory_id: str, 
                            memory: Dict) -> Dict[str, Any]:
        """Create ADHD-specific exercise"""
        difficulty = self.cognitive_profile.get("current_difficulty", 5)
        
        exercise = {
            "type": exercise_type,
            "memory_id": memory_id,
            "difficulty": difficulty,
            "created": datetime.now().isoformat(),
            "adhd_optimized": True
        }
        
        content = memory["content"]
        
        if exercise_type == "gamified_recall":
            # Multiple choice for quick dopamine hits
            words = content.split()
            if len(words) > 3:
                hidden_word = random.choice(words[1:-1])  # Not first or last
                options = self._generate_similar_words(hidden_word)
                
                exercise["prompt"] = f"🎮 Quick recall! Fill in the blank:\n{content.replace(hidden_word, '___')}"
                exercise["options"] = options
                exercise["answer"] = hidden_word
                exercise["reward"] = "🌟" * random.randint(1, 3)  # Visual reward
        
        elif exercise_type == "pattern_recognition":
            # Leverage ADHD pattern-matching strength
            exercise["prompt"] = f"🔍 Pattern hunt! This memory:\n'{content[:50]}...'\n\nWhat pattern or connection do you see?"
            exercise["goal"] = "Find any pattern - there's no wrong answer!"
            exercise["reward_type"] = "discovery"
        
        elif exercise_type == "micro_habits":
            # Tiny, achievable habit building
            exercise["prompt"] = f"🌱 Micro-habit moment!\nBased on: '{content[:30]}...'\n\nName ONE tiny action you could do right now (< 2 minutes)"
            exercise["goal"] = "Build momentum with tiny wins"
            exercise["timer"] = 120  # 2-minute timer
        
        elif exercise_type == "memory_anchoring":
            # Create strong associations
            exercise["prompt"] = f"⚓ Memory anchor!\n'{content}'\n\nCreate a vivid mental image or association"
            exercise["techniques"] = [
                "Visual: Picture it happening",
                "Audio: Give it a sound or rhythm",
                "Physical: Assign it a gesture",
                "Emotional: How does it feel?"
            ]
        
        return exercise
    
    def track_adhd_success(self, exercise_id: str, completed: bool, 
                         engagement_level: int, strategy_used: str = None):
        """Track what works for ADHD management"""
        if completed and engagement_level >= 7:
            if strategy_used and strategy_used not in self.adhd_patterns["successful_strategies"]:
                self.adhd_patterns["successful_strategies"].append({
                    "strategy": strategy_used,
                    "context": datetime.now().hour,
                    "success_count": 1
                })
        
        # Track productive times
        if completed:
            hour = str(datetime.now().hour)
            self.adhd_patterns["productive_times"][hour] = \
                self.adhd_patterns["productive_times"].get(hour, 0) + 1
        
        self.save_all_data()
    
    def get_memory_delegation_suggestion(self, content: str) -> Dict[str, Any]:
        """Suggest who should remember this (with ADHD awareness)"""
        ownership = self.identify_memory_owner(content)
        
        suggestion = {
            "recommendation": ownership["primary"],
            "reason": f"This appears to be {ownership['category']} information",
            "alternatives": ownership["backup"],
            "delegation_script": None,
            "adhd_support": None
        }
        
        # ADHD-specific suggestions
        if ownership["category"] in ["personal", "habits"]:
            suggestion["adhd_support"] = {
                "external_tools": ["Calendar app", "Reminder app", "Habit tracker"],
                "backup_strategy": "Set multiple reminders across different systems"
            }
        
        if ownership["primary"] != "user":
            suggestion["delegation_script"] = \
                f"Hey {ownership['primary']}, could you keep track of this? {content[:50]}..."
            suggestion["confirmation_needed"] = True  # ADHD benefit: explicit confirmation
        
        return suggestion
    
    def prune_expired_memories(self) -> int:
        """Prune expired memories with ADHD awareness"""
        logger.info("🧹 Pruning expired memories...")
        
        pruned_count = 0
        preserved_count = 0
        now = datetime.now()
        
        updated_embeddings = {}
        for memory_id, embedding_data in self.embeddings.items():
            expires = embedding_data.get("expires")
            
            if expires:
                try:
                    expiry_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                    
                    if expiry_date < now:
                        # Special preservation for ADHD support memories
                        if self._should_preserve_for_adhd(embedding_data):
                            embedding_data["preserved"] = True
                            embedding_data["preservation_reason"] = "adhd_support"
                            updated_embeddings[memory_id] = embedding_data
                            preserved_count += 1
                            logger.info(f"  🛡️  Preserved (ADHD): {embedding_data.get('content', '')[:50]}...")
                        elif self._should_preserve_general(embedding_data):
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
        self.save_all_data()
        
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
    
    def _should_preserve_for_adhd(self, memory: Dict[str, Any]) -> bool:
        """Check if memory should be preserved for ADHD support"""
        content = memory.get("content", "").lower()
        
        # Preserve habit-building memories
        adhd_keywords = ["habit", "routine", "system", "reminder", "anchor", "trick", "works for me"]
        if any(keyword in content for keyword in adhd_keywords):
            return True
        
        # Preserve highly accessed memories (indicates usefulness)
        if memory.get("access_count", 0) > 5:
            return True
        
        # Preserve memories from hyperfocus sessions
        emotions = memory.get("emotional_context", {}).get("emotions", [])
        if "hyperfocus" in emotions:
            return True
        
        return False
    
    def _should_preserve_general(self, memory: Dict[str, Any]) -> bool:
        """General preservation rules"""
        decay_type = memory.get("decay_type", "")
        if decay_type in ["permanent", "legal", "financial", "squeaky_loud", "adhd_anchor"]:
            return True
        
        current_squeaky = self.get_squeaky_level()
        if current_squeaky == "SQUEAKY_LOUD":
            return True
        
        content = memory.get("content", "").lower()
        rules = self.SQUEAKY_RULES[current_squeaky]
        
        for keyword in rules["preserve_keywords"]:
            if keyword in content:
                return True
        
        # Recently accessed
        last_accessed = memory.get("last_accessed")
        if last_accessed:
            try:
                last_date = datetime.fromisoformat(last_accessed.replace("Z", "+00:00"))
                if (datetime.now() - last_date).days < 7:
                    return True
            except:
                pass
        
        return False
    
    def get_cognitive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive cognitive and ADHD dashboard"""
        dashboard = {
            "emotional_state": self._get_current_emotional_state(),
            "adhd_state": self._get_adhd_state(),
            "cognitive_load": self.cognitive_profile.get("cognitive_load", "normal"),
            "exercise_status": {
                "enabled": self.cognitive_profile.get("exercise_enabled", False),
                "adhd_mode": self.cognitive_profile.get("adhd_mode", False),
                "current_difficulty": self.cognitive_profile.get("current_difficulty", 5),
                "comfort_zone": self.cognitive_profile.get("comfort_zone"),
                "exercises_completed": len([e for e in self.cognitive_profile.get("exercise_history", [])
                                          if e.get("completed")])
            },
            "transactive_memory": {
                "partnerships": len(self.transactive_memory),
                "primary_categories": {}
            },
            "emotional_trends": self._get_emotional_trends(),
            "adhd_insights": self._get_adhd_insights(),
            "memory_stats": self._get_memory_stats()
        }
        
        # Analyze transactive memory distribution
        for owner, data in self.transactive_memory.items():
            for category, stats in data.get("categories", {}).items():
                if category not in dashboard["transactive_memory"]["primary_categories"]:
                    dashboard["transactive_memory"]["primary_categories"][category] = {
                        "owner": owner,
                        "count": 0
                    }
                dashboard["transactive_memory"]["primary_categories"][category]["count"] += \
                    stats["count"]
        
        return dashboard
    
    def _get_adhd_insights(self) -> Dict[str, Any]:
        """Generate ADHD-specific insights"""
        insights = {
            "hyperfocus_topics": list(self.adhd_patterns.get("hyperfocus_topics", {}).keys())[:5],
            "productive_hours": [],
            "distraction_patterns": [],
            "successful_strategies": self.adhd_patterns.get("successful_strategies", [])[:3],
            "recommendations": []
        }
        
        # Find most productive hours
        productive_times = self.adhd_patterns.get("productive_times", {})
        if productive_times:
            sorted_hours = sorted(productive_times.items(), key=lambda x: x[1], reverse=True)
            insights["productive_hours"] = [h for h, _ in sorted_hours[:3]]
        
        # Current recommendations
        current_hour = datetime.now().hour
        if str(current_hour) in insights["productive_hours"]:
            insights["recommendations"].append("🎯 You're in a productive time slot - tackle challenging tasks!")
        else:
            insights["recommendations"].append("🌿 Lower focus time - perfect for routine tasks or breaks")
        
        if self._get_adhd_state()["needs_break"]:
            insights["recommendations"].append("⏰ Time for a break - movement helps reset focus!")
        
        return insights
    
    def _get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total = len(self.embeddings)
        stats = {
            "total_memories": total,
            "by_decay_type": {},
            "by_instance": {},
            "expiring_soon": 0,
            "preserved_count": 0
        }
        
        now = datetime.now()
        for memory_id, memory in self.embeddings.items():
            # Count by decay type
            decay_type = memory.get("decay_type", "unknown")
            stats["by_decay_type"][decay_type] = stats["by_decay_type"].get(decay_type, 0) + 1
            
            # Count by instance
            instance = memory.get("source_instance", "unknown")
            stats["by_instance"][instance] = stats["by_instance"].get(instance, 0) + 1
            
            # Count preserved
            if memory.get("preserved", False):
                stats["preserved_count"] += 1
            
            # Check expiring soon
            expires = memory.get("expires")
            if expires:
                try:
                    expiry_date = datetime.fromisoformat(expires.replace("Z", "+00:00"))
                    days_left = (expiry_date - now).days
                    if 0 < days_left <= 7:
                        stats["expiring_soon"] += 1
                except:
                    pass
        
        return stats
    
    # Helper methods
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            return
            
        try:
            # Try to get from 1Password first
            api_key = subprocess.run(
                ['op', 'item', 'get', 'OpenAI', '--fields', 'credential'],
                capture_output=True, text=True
            ).stdout.strip()
            
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY")
            
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
                logger.info("✅ OpenAI connection established!")
            else:
                logger.warning("⚠️  No OpenAI API key found")
        except Exception as e:
            logger.warning(f"⚠️  OpenAI initialization failed: {e}")
    
    def _create_embedding(self, text: str) -> List[float]:
        """Create embedding with OpenAI or fallback"""
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    input=text,
                    model=self.embedding_model
                )
                return response.data[0].embedding
            except Exception as e:
                logger.warning(f"OpenAI embedding failed: {e}, using fallback")
        
        return self._simple_embedding(text)
    
    def _simple_embedding(self, text: str) -> List[float]:
        """Fallback character frequency embedding"""
        embedding = [0] * 128
        for char in text.lower():
            if ord(char) < 128:
                embedding[ord(char)] += 1
        
        total = sum(embedding)
        if total > 0:
            embedding = [x / total for x in embedding]
        
        return embedding
    
    def _vector_search_internal(self, query: str, threshold: float = 0.7, 
                               limit: int = 10) -> List[Dict]:
        """Internal vector search implementation"""
        if not self.embeddings:
            return []
        
        query_embedding = np.array(self._create_embedding(query))
        
        similarities = []
        for memory_id, memory_data in self.embeddings.items():
            memory_embedding = np.array(memory_data.get("embedding", []))
            
            if len(memory_embedding) > 0 and len(query_embedding) == len(memory_embedding):
                similarity = cosine_similarity([query_embedding], [memory_embedding])[0][0]
                
                if similarity >= threshold:
                    similarities.append({
                        "id": memory_id,
                        "content": memory_data.get("content", ""),
                        "similarity": float(similarity),
                        "data": memory_data,
                        "type": memory_data.get("type", "unknown")
                    })
        
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similarities[:limit]
    
    def _save_to_assistant_thread(self, instance: str, memory_id: str, memory: Dict):
        """Save memory to OpenAI assistant thread"""
        if instance not in self.ASSISTANT_IDS:
            return
        
        try:
            # Get or create thread for this instance
            if instance not in self.threads:
                thread = self.openai_client.beta.threads.create()
                self.threads[instance] = thread.id
                self._save_json(self.threads_file, self.threads)
            
            thread_id = self.threads[instance]
            
            # Add memory to thread
            message = self.openai_client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=f"[MEMORY] {memory['content']}\nContext: {memory.get('context', '')}\nImpact: {memory.get('impact', '')}"
            )
            
            logger.info(f"💾 Saved to {instance} assistant thread")
            
        except Exception as e:
            logger.error(f"Failed to save to assistant thread: {e}")
    
    def identify_memory_owner(self, content: str, context: str = "") -> Dict[str, Any]:
        """Identify who should own this memory"""
        combined = f"{content} {context}".lower()
        
        ownership_scores = {}
        
        for category, config in self.MEMORY_PARTNERSHIPS.items():
            score = sum(1 for keyword in config["keywords"] if keyword in combined)
            if score > 0:
                ownership_scores[category] = {
                    "score": score,
                    "primary": config["primary"],
                    "backup": config["backup"]
                }
        
        if not ownership_scores:
            return {
                "category": "general",
                "primary": "user",
                "backup": ["Claude"],
                "confidence": 0.5
            }
        
        best_category = max(ownership_scores.items(), key=lambda x: x[1]["score"])
        
        return {
            "category": best_category[0],
            "primary": best_category[1]["primary"],
            "backup": best_category[1]["backup"],
            "confidence": min(best_category[1]["score"] / 3, 1.0)
        }
    
    def _update_transactive_memory(self, ownership: Dict[str, Any], content: str):
        """Update who knows what"""
        owner = ownership["primary"]
        category = ownership["category"]
        
        if owner not in self.transactive_memory:
            self.transactive_memory[owner] = {
                "categories": {},
                "last_updated": datetime.now().isoformat()
            }
        
        if category not in self.transactive_memory[owner]["categories"]:
            self.transactive_memory[owner]["categories"][category] = {
                "count": 0,
                "keywords": [],
                "last_accessed": None
            }
        
        self.transactive_memory[owner]["categories"][category]["count"] += 1
        self.transactive_memory[owner]["categories"][category]["last_accessed"] = \
            datetime.now().isoformat()
    
    def _get_current_emotional_state(self) -> str:
        """Analyze recent emotional patterns"""
        if not self.emotional_patterns:
            return "neutral"
        
        recent_dates = sorted(self.emotional_patterns.keys())[-7:]
        emotion_totals = {}
        
        for date in recent_dates:
            for emotion, count in self.emotional_patterns[date].items():
                emotion_totals[emotion] = emotion_totals.get(emotion, 0) + count
        
        if not emotion_totals:
            return "neutral"
        
        dominant = max(emotion_totals.items(), key=lambda x: x[1])[0]
        
        state_mapping = {
            "stress": "stressed",
            "anxiety": "anxious",
            "joy": "positive",
            "pride": "confident",
            "frustration": "challenged",
            "curiosity": "engaged",
            "hyperfocus": "focused",
            "scattered": "distracted",
            "motivated": "energized"
        }
        
        return state_mapping.get(dominant, "neutral")
    
    def _get_emotional_trends(self) -> Dict[str, Any]:
        """Analyze emotional patterns over time"""
        if not self.emotional_patterns:
            return {"trend": "stable", "data": {}}
        
        dates = sorted(self.emotional_patterns.keys())[-30:]
        
        trends = {}
        for date in dates:
            for emotion, count in self.emotional_patterns[date].items():
                if emotion not in trends:
                    trends[emotion] = []
                trends[emotion].append(count)
        
        trend_directions = {}
        for emotion, counts in trends.items():
            if len(counts) > 7:
                recent_avg = sum(counts[-7:]) / 7
                older_avg = sum(counts[:-7]) / len(counts[:-7])
                
                if recent_avg > older_avg * 1.2:
                    trend_directions[emotion] = "increasing"
                elif recent_avg < older_avg * 0.8:
                    trend_directions[emotion] = "decreasing"
                else:
                    trend_directions[emotion] = "stable"
        
        return {
            "trends": trend_directions,
            "raw_data": trends
        }
    
    def _extract_topic(self, content: str) -> str:
        """Extract main topic from content"""
        # Simple implementation - could be enhanced with NLP
        words = content.lower().split()
        # Remove common words
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        significant_words = [w for w in words if w not in stopwords and len(w) > 3]
        
        if significant_words:
            return significant_words[0]
        return "general"
    
    def _generate_similar_words(self, word: str) -> List[str]:
        """Generate plausible alternatives for multiple choice"""
        # In a real implementation, this could use word embeddings
        # For now, simple character manipulation
        options = [word]  # Correct answer
        
        # Add some variations
        if len(word) > 4:
            options.append(word[:-1] + "ed")
            options.append(word[:-1] + "ing")
            options.append(word + "s")
        
        # Add some random words from recent memories
        recent_words = []
        for memory in list(self.embeddings.values())[-10:]:
            content_words = memory.get("content", "").split()
            recent_words.extend([w for w in content_words if len(w) > 3])
        
        if recent_words:
            options.extend(random.sample(recent_words, min(2, len(recent_words))))
        
        # Ensure we have 4 options
        while len(options) < 4:
            options.append(f"option{len(options)}")
        
        random.shuffle(options)
        return options[:4]
    
    def _is_exercise_eligible(self, content: str, emotional_context: Dict) -> bool:
        """Determine if memory is good for exercises"""
        # For ADHD, prefer positive and actionable content
        positive_emotions = ["joy", "pride", "motivated", "curiosity"]
        if any(e in emotional_context.get("emotions", []) for e in positive_emotions):
            return True
        
        # Good for exercise if it's learnable
        exercise_keywords = ["learn", "remember", "fact", "how", "process", "step", 
                           "method", "trick", "tip", "strategy"]
        content_lower = content.lower()
        
        return any(keyword in content_lower for keyword in exercise_keywords)
    
    def _boost_actionable_results(self, results: List[Dict]) -> List[Dict]:
        """Boost actionable results when stressed"""
        action_keywords = ["todo", "action", "step", "next", "now", "deadline", "must"]
        
        for result in results:
            content = result.get("content", "").lower()
            action_score = sum(1 for keyword in action_keywords if keyword in content)
            
            if action_score > 0:
                result["similarity"] = min(1.0, result.get("similarity", 0) + (action_score * 0.1))
        
        return sorted(results, key=lambda x: x.get("similarity", 0), reverse=True)
    
    def _boost_simple_results(self, results: List[Dict]) -> List[Dict]:
        """Boost simple, clear results for low focus states"""
        for result in results:
            content = result.get("content", "")
            # Prefer shorter, clearer memories
            clarity_score = 1.0 / (1 + len(content.split()) / 20)  # Fewer words = higher score
            result["similarity"] = result.get("similarity", 0) * (0.7 + 0.3 * clarity_score)
        
        return sorted(results, key=lambda x: x.get("similarity", 0), reverse=True)
    
    def _update_access_time(self, memory_id: str):
        """Update last accessed time"""
        if memory_id in self.embeddings:
            self.embeddings[memory_id]["last_accessed"] = datetime.now().isoformat()
            self.embeddings[memory_id]["access_count"] = \
                self.embeddings[memory_id].get("access_count", 0) + 1
    
    def save_all_data(self):
        """Save all data to disk"""
        self._save_json(self.embeddings_file, self.embeddings)
        self._save_json(self.emotional_patterns_file, self.emotional_patterns)
        self._save_json(self.transactive_memory_file, self.transactive_memory)
        self._save_json(self.cognitive_profile_file, self.cognitive_profile)
        self._save_json(self.decay_log_file, self.decay_log)
        self._save_json(self.adhd_patterns_file, self.adhd_patterns)
        self._save_json(self.threads_file, self.threads)
    
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
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# CLI Interface
if __name__ == "__main__":
    import sys
    
    memory = ClaudeVectorMemoryV3Enhanced()
    
    if len(sys.argv) == 1:
        # Show dashboard
        dashboard = memory.get_cognitive_dashboard()
        print("\n🧠 COGNITIVE MEMORY DASHBOARD V3")
        print("=" * 60)
        print(f"Emotional State: {dashboard['emotional_state']}")
        print(f"ADHD Focus Level: {dashboard['adhd_state']['likely_focus_level']}")
        print(f"Cognitive Load: {dashboard['cognitive_load']}")
        
        print(f"\n📊 Memory Statistics:")
        stats = dashboard['memory_stats']
        print(f"  Total: {stats['total_memories']}")
        print(f"  Preserved: {stats['preserved_count']}")
        print(f"  Expiring Soon: {stats['expiring_soon']}")
        
        print(f"\n🎯 ADHD Insights:")
        insights = dashboard['adhd_insights']
        print(f"  Productive Hours: {', '.join(insights['productive_hours'])}")
        print(f"  Hyperfocus Topics: {', '.join(insights['hyperfocus_topics'][:3])}")
        
        if insights['recommendations']:
            print(f"\n💡 Current Recommendations:")
            for rec in insights['recommendations']:
                print(f"  {rec}")
    
    elif sys.argv[1] == "add" and len(sys.argv) >= 3:
        content = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        
        memory_id = memory.add_memory_with_cognitive_awareness(content, context)
        print(f"✅ Added memory: {memory_id}")
        
        # Check delegation
        suggestion = memory.get_memory_delegation_suggestion(content)
        if suggestion["recommendation"] != "user":
            print(f"\n💡 Suggestion: {suggestion['recommendation']} should track this")
            print(f"   Reason: {suggestion['reason']}")
            if suggestion.get("adhd_support"):
                print(f"   ADHD Support: Use {', '.join(suggestion['adhd_support']['external_tools'])}")
    
    elif sys.argv[1] == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        results = memory.search_with_cognitive_context(query)
        
        print(f"\n🔍 Results for: '{query}'")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result.get('content', '')[:100]}... ({result.get('similarity', 0):.3f})")
    
    elif sys.argv[1] == "exercise":
        exercise = memory.generate_adhd_cognitive_exercise()
        if exercise:
            print(f"\n🧠 BRAIN EXERCISE ({exercise['type']})")
            print(f"Difficulty: {exercise['difficulty']}/10")
            print(f"\n{exercise['prompt']}")
            
            if exercise.get('options'):
                print("\nOptions:")
                for i, opt in enumerate(exercise['options'], 1):
                    print(f"  {i}. {opt}")
            
            if exercise.get('timer'):
                print(f"\n⏱️ Timer: {exercise['timer']} seconds")
        else:
            print("No exercise available right now. Try again in 30 minutes!")
    
    elif sys.argv[1] == "prune":
        pruned = memory.prune_expired_memories()
        print(f"🧹 Pruned {pruned} expired memories")
    
    elif sys.argv[1] == "help":
        print("\n🧠 Claude Vector Memory V3 - Enhanced with ADHD Support")
        print("\nCommands:")
        print("  python memory.py                    # Show dashboard")
        print("  python memory.py add <content>      # Add memory")
        print("  python memory.py search <query>     # Search memories")
        print("  python memory.py exercise           # Get brain exercise")
        print("  python memory.py prune              # Clean expired memories")
        print("\nADHD Features:")
        print("  - Adaptive exercise difficulty")
        print("  - Gamified memory challenges")
        print("  - Hyperfocus tracking")
        print("  - Productive time analysis")
        print("  - External tool integration")