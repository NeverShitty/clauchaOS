#!/usr/bin/env python3
"""
🧠 ENHANCED VECTOR MEMORY V3 - COGNITIVE & SOCIAL AWARENESS
Includes emotional learning, transactive memory, and cognitive exercise features
"""

import os
import json
import time
import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class EnhancedVectorMemoryV3:
    def __init__(self, base_path: str = "/Users/noshit/MCMANSION/AUTOMATION_LAB"):
        self.base_path = base_path
        self.memory_dir = os.path.join(base_path, "vector_memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Core memory files
        self.embeddings_file = os.path.join(self.memory_dir, "embeddings.json")
        self.emotional_patterns_file = os.path.join(self.memory_dir, "emotional_patterns.json")
        self.transactive_memory_file = os.path.join(self.memory_dir, "transactive_memory.json")
        self.cognitive_profile_file = os.path.join(self.memory_dir, "cognitive_profile.json")
        
        # Load data
        self.embeddings = self._load_json(self.embeddings_file)
        self.emotional_patterns = self._load_json(self.emotional_patterns_file)
        self.transactive_memory = self._load_json(self.transactive_memory_file)
        self.cognitive_profile = self._load_json(self.cognitive_profile_file)
        
        # Initialize cognitive profile if new
        if not self.cognitive_profile:
            self.cognitive_profile = self._init_cognitive_profile()
        
        # Emotional trigger keywords by category
        self.EMOTIONAL_TRIGGERS = {
            "stress": ["deadline", "urgent", "emergency", "pressure", "overwhelmed", "stressed"],
            "joy": ["success", "achievement", "happy", "excited", "wonderful", "great"],
            "anxiety": ["worried", "nervous", "uncertain", "afraid", "concern", "anxious"],
            "frustration": ["stuck", "confused", "difficult", "problem", "issue", "broken"],
            "pride": ["accomplished", "proud", "finished", "completed", "solved", "fixed"],
            "curiosity": ["interesting", "wonder", "how", "why", "learn", "discover"]
        }
        
        # Transactive memory patterns (who remembers what)
        self.MEMORY_PARTNERSHIPS = {
            "technical": {
                "primary": "user",
                "backup": ["Claude", "team"],
                "keywords": ["code", "debug", "algorithm", "system", "technical"]
            },
            "financial": {
                "primary": "CLAUDEFO",
                "backup": ["accountant", "spouse"],
                "keywords": ["tax", "invoice", "payment", "revenue", "expense"]
            },
            "legal": {
                "primary": "CLAUDESQ",
                "backup": ["lawyer", "paralegal"],
                "keywords": ["contract", "filing", "court", "legal", "lawsuit"]
            },
            "personal": {
                "primary": "spouse",
                "backup": ["user", "CLAUDEMOM"],
                "keywords": ["birthday", "anniversary", "family", "personal", "appointment"]
            }
        }
        
        # Cognitive exercise settings
        self.EXERCISE_MODES = {
            "memory_recall": {
                "description": "Periodically ask user to recall recent information",
                "difficulty_range": (1, 10),
                "frequency": "daily"
            },
            "association": {
                "description": "Connect new information to existing knowledge",
                "difficulty_range": (1, 10),
                "frequency": "per_session"
            },
            "elaboration": {
                "description": "Ask user to explain concepts in their own words",
                "difficulty_range": (1, 10),
                "frequency": "weekly"
            },
            "spaced_repetition": {
                "description": "Review important information at increasing intervals",
                "difficulty_range": (1, 10),
                "frequency": "adaptive"
            }
        }
        
        # Initialize OpenAI if available
        self.openai_client = None
        self._init_openai()
    
    def _init_cognitive_profile(self) -> Dict[str, Any]:
        """Initialize user's cognitive profile"""
        return {
            "user_id": "primary",
            "created": datetime.now().isoformat(),
            "exercise_enabled": False,
            "current_difficulty": 5,
            "comfort_zone": {
                "lower": 3,
                "upper": 7
            },
            "strengths": [],
            "areas_for_growth": [],
            "exercise_history": [],
            "last_exercise": None,
            "cognitive_load": "normal",  # low, normal, high
            "preferred_modalities": ["verbal", "visual"],
            "memory_partnerships": {}
        }
    
    def analyze_emotional_context(self, content: str, context: str = "") -> Dict[str, Any]:
        """Analyze emotional triggers in content"""
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
            if timestamp[:10] not in self.emotional_patterns:
                self.emotional_patterns[timestamp[:10]] = {}
            
            for emotion in triggered_emotions:
                if emotion not in self.emotional_patterns[timestamp[:10]]:
                    self.emotional_patterns[timestamp[:10]][emotion] = 0
                self.emotional_patterns[timestamp[:10]][emotion] += 1
        
        # Determine memory importance based on emotional context
        importance_boost = 0
        if "stress" in triggered_emotions or "anxiety" in triggered_emotions:
            importance_boost = 0.3  # Stressed memories often important
        if "joy" in triggered_emotions or "pride" in triggered_emotions:
            importance_boost = 0.2  # Positive achievements worth preserving
        
        return {
            "emotions": triggered_emotions,
            "scores": emotional_scores,
            "importance_boost": importance_boost,
            "emotional_state": self._get_current_emotional_state()
        }
    
    def _get_current_emotional_state(self) -> str:
        """Analyze recent emotional patterns"""
        if not self.emotional_patterns:
            return "neutral"
        
        # Look at last 7 days
        recent_dates = sorted(self.emotional_patterns.keys())[-7:]
        emotion_totals = {}
        
        for date in recent_dates:
            for emotion, count in self.emotional_patterns[date].items():
                emotion_totals[emotion] = emotion_totals.get(emotion, 0) + count
        
        if not emotion_totals:
            return "neutral"
        
        # Determine dominant emotion
        dominant = max(emotion_totals.items(), key=lambda x: x[1])[0]
        
        # Map to general state
        state_mapping = {
            "stress": "stressed",
            "anxiety": "anxious",
            "joy": "positive",
            "pride": "confident",
            "frustration": "challenged",
            "curiosity": "engaged"
        }
        
        return state_mapping.get(dominant, "neutral")
    
    def identify_memory_owner(self, content: str, context: str = "") -> Dict[str, Any]:
        """Identify who should own this memory (transactive memory)"""
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
        
        # Get highest scoring category
        best_category = max(ownership_scores.items(), key=lambda x: x[1]["score"])
        
        return {
            "category": best_category[0],
            "primary": best_category[1]["primary"],
            "backup": best_category[1]["backup"],
            "confidence": min(best_category[1]["score"] / 3, 1.0)  # Normalize confidence
        }
    
    def add_memory_with_cognitive_awareness(self, content: str, context: str = "",
                                          impact: str = "", memory_type: str = "general") -> str:
        """Add memory with emotional and transactive awareness"""
        
        # Analyze emotional context
        emotional_context = self.analyze_emotional_context(content, context)
        
        # Identify memory ownership
        ownership = self.identify_memory_owner(content, context)
        
        # Determine decay based on emotional state and ownership
        if emotional_context["importance_boost"] > 0.2:
            decay_type = "seasonal"  # Important emotional memories last longer
        elif ownership["primary"] != "user":
            decay_type = "ephemeral"  # Others will remember this
        else:
            decay_type = "working"  # Standard decay
        
        # Create memory with enhanced metadata
        memory_id = f"cognitive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        memory = {
            "content": content,
            "context": context,
            "impact": impact,
            "created": datetime.now().isoformat(),
            "type": memory_type,
            "emotional_context": emotional_context,
            "ownership": ownership,
            "decay_type": decay_type,
            "cognitive_load": self.cognitive_profile.get("cognitive_load", "normal"),
            "exercise_eligible": self._is_exercise_eligible(content, emotional_context)
        }
        
        # Store memory
        self.embeddings[memory_id] = memory
        self.save_all_data()
        
        # Update transactive memory map
        self._update_transactive_memory(ownership, content)
        
        logger.info(f"💭 Added memory with emotional state: {emotional_context['emotional_state']}")
        logger.info(f"👥 Memory owner: {ownership['primary']} (confidence: {ownership['confidence']:.2f})")
        
        return memory_id
    
    def _update_transactive_memory(self, ownership: Dict[str, Any], content: str):
        """Update who knows what in the transactive memory system"""
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
    
    def search_with_cognitive_context(self, query: str, include_filler: bool = True) -> List[Dict]:
        """Search with awareness of emotional state and memory partnerships"""
        
        if include_filler and len(query.split()) > 3:
            # Add natural filler for complex searches
            fillers = [
                "Hmm, let me think about that for a second...",
                "That's an interesting question, let me search my memory...",
                "Give me a moment to recall that information...",
                "Let me dig into that for you..."
            ]
            print(random.choice(fillers))
            time.sleep(0.5)  # Brief pause for realism
        
        # Check who might know this
        ownership = self.identify_memory_owner(query)
        
        if ownership["primary"] != "user" and ownership["confidence"] > 0.7:
            print(f"💭 This might be something {ownership['primary']} would remember better...")
        
        # Perform search
        results = self.vector_search(query)
        
        # Boost results based on current emotional state
        emotional_state = self._get_current_emotional_state()
        if emotional_state in ["stressed", "anxious"]:
            # Prioritize actionable, clear information when stressed
            results = self._boost_actionable_results(results)
        
        return results
    
    def generate_cognitive_exercise(self) -> Optional[Dict[str, Any]]:
        """Generate a brain exercise based on recent memories and user profile"""
        if not self.cognitive_profile.get("exercise_enabled", False):
            return None
        
        # Check if enough time has passed
        last_exercise = self.cognitive_profile.get("last_exercise")
        if last_exercise:
            last_date = datetime.fromisoformat(last_exercise.replace("Z", "+00:00"))
            if (datetime.now() - last_date).hours < 4:
                return None  # Don't overwhelm
        
        # Get exercise-eligible memories
        eligible_memories = []
        for mem_id, memory in self.embeddings.items():
            if memory.get("exercise_eligible", False):
                days_old = (datetime.now() - datetime.fromisoformat(
                    memory["created"].replace("Z", "+00:00")
                )).days
                
                # Good for exercise if 1-7 days old
                if 1 <= days_old <= 7:
                    eligible_memories.append((mem_id, memory))
        
        if not eligible_memories:
            return None
        
        # Select exercise type based on cognitive load
        cognitive_load = self.cognitive_profile.get("cognitive_load", "normal")
        
        if cognitive_load == "high":
            exercise_type = "simple_recall"
        elif cognitive_load == "low":
            exercise_type = "elaboration"
        else:
            exercise_type = random.choice(["memory_recall", "association"])
        
        # Generate exercise
        memory_id, memory = random.choice(eligible_memories)
        difficulty = self.cognitive_profile.get("current_difficulty", 5)
        
        exercise = {
            "type": exercise_type,
            "memory_id": memory_id,
            "difficulty": difficulty,
            "created": datetime.now().isoformat()
        }
        
        if exercise_type == "memory_recall":
            # Hide part of the information
            content = memory["content"]
            words = content.split()
            if len(words) > 5:
                hide_count = max(1, int(len(words) * (difficulty / 10)))
                hide_indices = random.sample(range(len(words)), hide_count)
                for i in hide_indices:
                    words[i] = "___"
                
                exercise["prompt"] = f"Can you recall what goes in the blanks?\n{' '.join(words)}"
                exercise["answer"] = content
        
        elif exercise_type == "association":
            exercise["prompt"] = f"This reminds me of: '{memory['content'][:30]}...'\n" \
                               f"What does this make you think of?"
            exercise["goal"] = "Connect to personal experience"
        
        elif exercise_type == "elaboration":
            exercise["prompt"] = f"In your own words, explain:\n{memory['content']}"
            exercise["goal"] = "Deepen understanding through explanation"
        
        # Update profile
        self.cognitive_profile["last_exercise"] = datetime.now().isoformat()
        self.cognitive_profile["exercise_history"].append(exercise)
        
        return exercise
    
    def adjust_cognitive_difficulty(self, exercise_id: str, success: bool, effort: int):
        """Adjust difficulty based on performance"""
        current = self.cognitive_profile.get("current_difficulty", 5)
        comfort_zone = self.cognitive_profile.get("comfort_zone", {"lower": 3, "upper": 7})
        
        if success and effort < 3:  # Too easy
            new_difficulty = min(10, current + 1)
            comfort_zone["upper"] = min(10, comfort_zone["upper"] + 0.5)
        elif not success and effort > 7:  # Too hard
            new_difficulty = max(1, current - 1)
            comfort_zone["lower"] = max(1, comfort_zone["lower"] - 0.5)
        else:  # Just right
            new_difficulty = current
        
        self.cognitive_profile["current_difficulty"] = new_difficulty
        self.cognitive_profile["comfort_zone"] = comfort_zone
        
        # Log performance
        for exercise in self.cognitive_profile["exercise_history"]:
            if exercise.get("created") == exercise_id:
                exercise["success"] = success
                exercise["effort"] = effort
                exercise["completed"] = datetime.now().isoformat()
        
        self.save_all_data()
    
    def get_memory_delegation_suggestion(self, content: str) -> Dict[str, Any]:
        """Suggest who should remember this information"""
        ownership = self.identify_memory_owner(content)
        
        suggestion = {
            "recommendation": ownership["primary"],
            "reason": f"This appears to be {ownership['category']} information",
            "alternatives": ownership["backup"],
            "delegation_script": None
        }
        
        if ownership["primary"] != "user":
            suggestion["delegation_script"] = \
                f"Hey {ownership['primary']}, could you keep track of this? {content[:50]}..."
        
        return suggestion
    
    def get_cognitive_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive cognitive and emotional dashboard"""
        dashboard = {
            "emotional_state": self._get_current_emotional_state(),
            "cognitive_load": self.cognitive_profile.get("cognitive_load", "normal"),
            "exercise_status": {
                "enabled": self.cognitive_profile.get("exercise_enabled", False),
                "current_difficulty": self.cognitive_profile.get("current_difficulty", 5),
                "comfort_zone": self.cognitive_profile.get("comfort_zone"),
                "exercises_completed": len([e for e in self.cognitive_profile.get("exercise_history", [])
                                          if e.get("completed")])
            },
            "transactive_memory": {
                "partnerships": len(self.transactive_memory),
                "primary_categories": {}
            },
            "emotional_trends": self._get_emotional_trends()
        }
        
        # Analyze transactive memory distribution
        for owner, data in self.transactive_memory.items():
            for category, stats in data["categories"].items():
                if category not in dashboard["transactive_memory"]["primary_categories"]:
                    dashboard["transactive_memory"]["primary_categories"][category] = {
                        "owner": owner,
                        "count": 0
                    }
                dashboard["transactive_memory"]["primary_categories"][category]["count"] += \
                    stats["count"]
        
        return dashboard
    
    def _get_emotional_trends(self) -> Dict[str, Any]:
        """Analyze emotional patterns over time"""
        if not self.emotional_patterns:
            return {"trend": "stable", "data": {}}
        
        # Last 30 days
        dates = sorted(self.emotional_patterns.keys())[-30:]
        
        trends = {}
        for date in dates:
            for emotion, count in self.emotional_patterns[date].items():
                if emotion not in trends:
                    trends[emotion] = []
                trends[emotion].append(count)
        
        # Simple trend analysis
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
    
    def _is_exercise_eligible(self, content: str, emotional_context: Dict) -> bool:
        """Determine if a memory is good for cognitive exercises"""
        # Don't exercise on highly emotional content
        if emotional_context.get("importance_boost", 0) > 0.25:
            return False
        
        # Good for exercise if it's factual, learnable
        exercise_keywords = ["learn", "remember", "fact", "how", "process", "step", "method"]
        content_lower = content.lower()
        
        return any(keyword in content_lower for keyword in exercise_keywords)
    
    def _boost_actionable_results(self, results: List[Dict]) -> List[Dict]:
        """Boost actionable results when user is stressed"""
        action_keywords = ["todo", "action", "step", "next", "now", "deadline", "must"]
        
        for result in results:
            content = result.get("content", "").lower()
            action_score = sum(1 for keyword in action_keywords if keyword in content)
            
            if action_score > 0:
                result["similarity"] = min(1.0, result.get("similarity", 0) + (action_score * 0.1))
        
        return sorted(results, key=lambda x: x.get("similarity", 0), reverse=True)
    
    def vector_search(self, query: str, threshold: float = 0.7, limit: int = 10) -> List[Dict]:
        """Basic vector search (implement as in V2)"""
        # Placeholder - implement full vector search
        return []
    
    def save_all_data(self):
        """Save all cognitive data"""
        self._save_json(self.embeddings_file, self.embeddings)
        self._save_json(self.emotional_patterns_file, self.emotional_patterns)
        self._save_json(self.transactive_memory_file, self.transactive_memory)
        self._save_json(self.cognitive_profile_file, self.cognitive_profile)
    
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
    
    def _init_openai(self):
        """Initialize OpenAI client if available"""
        try:
            import openai
            api_key = os.environ.get("OPENAI_API_KEY")
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
        except:
            pass


# Example usage and CLI
if __name__ == "__main__":
    import sys
    
    memory = EnhancedVectorMemoryV3()
    
    if len(sys.argv) == 1:
        # Show cognitive dashboard
        dashboard = memory.get_cognitive_dashboard()
        print("\n🧠 COGNITIVE MEMORY DASHBOARD")
        print("=" * 50)
        print(f"Emotional State: {dashboard['emotional_state']}")
        print(f"Cognitive Load: {dashboard['cognitive_load']}")
        print(f"\nTransactive Memory Partners: {dashboard['transactive_memory']['partnerships']}")
        print("\nMemory Distribution:")
        for category, data in dashboard['transactive_memory']['primary_categories'].items():
            print(f"  {category}: {data['owner']} ({data['count']} memories)")
        
        print("\nEmotional Trends:")
        for emotion, trend in dashboard['emotional_trends']['trends'].items():
            print(f"  {emotion}: {trend}")
    
    elif sys.argv[1] == "add" and len(sys.argv) >= 3:
        content = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        
        memory_id = memory.add_memory_with_cognitive_awareness(content, context)
        print(f"✅ Added memory: {memory_id}")
        
        # Check if delegation suggested
        suggestion = memory.get_memory_delegation_suggestion(content)
        if suggestion["recommendation"] != "user":
            print(f"\n💡 Suggestion: {suggestion['recommendation']} should track this")
            print(f"   Reason: {suggestion['reason']}")
    
    elif sys.argv[1] == "exercise":
        if sys.argv[2] == "enable":
            memory.cognitive_profile["exercise_enabled"] = True
            memory.save_all_data()
            print("✅ Cognitive exercises enabled!")
        elif sys.argv[2] == "generate":
            exercise = memory.generate_cognitive_exercise()
            if exercise:
                print(f"\n🧠 BRAIN EXERCISE ({exercise['type']})")
                print(f"Difficulty: {exercise['difficulty']}/10")
                print(f"\n{exercise['prompt']}")
            else:
                print("No exercise available right now. Try again later!")
    
    elif sys.argv[1] == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        results = memory.search_with_cognitive_context(query)
        
        print(f"\n🔍 Results for: '{query}'")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result.get('content', '')[:100]}...")
