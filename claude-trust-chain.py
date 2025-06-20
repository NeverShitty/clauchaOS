#!/usr/bin/env python3
"""
Claude Trust Chain - Immutable Activity & Approval Logging System

Every Claude instance has a trust score based on their chain of actions.
Every approval, rejection, and autonomous decision is permanently logged.
This creates an audit trail for legal compliance and business model transparency.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sqlite3
import threading
from enum import Enum
from dataclasses import dataclass, asdict

# ============================================================================
# TRUST EVENTS
# ============================================================================

class TrustEventType(Enum):
    # Positive events
    TASK_COMPLETED = "task_completed"
    APPROVAL_GRANTED = "approval_granted"
    REVENUE_GENERATED = "revenue_generated"
    COMPLIANCE_PASSED = "compliance_passed"
    QUALITY_CHECK_PASSED = "quality_check_passed"
    
    # Negative events
    TASK_FAILED = "task_failed"
    APPROVAL_DENIED = "approval_denied"
    ERROR_GENERATED = "error_generated"
    COMPLIANCE_VIOLATION = "compliance_violation"
    QUALITY_CHECK_FAILED = "quality_check_failed"
    
    # Neutral events
    HUMAN_OVERRIDE = "human_override"
    SYSTEM_PAUSE = "system_pause"
    CONFIGURATION_CHANGE = "configuration_change"

@dataclass
class TrustEvent:
    """Immutable trust event for the chain"""
    timestamp: float
    claude_id: str
    event_type: TrustEventType
    description: str
    impact: float  # -1.0 to 1.0
    metadata: Dict
    human_approval: Optional[bool] = None
    approval_reason: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def calculate_hash(self, previous_hash: str) -> str:
        """Calculate SHA-256 hash including previous block"""
        event_data = json.dumps(self.to_dict(), sort_keys=True)
        combined = f"{previous_hash}{event_data}"
        return hashlib.sha256(combined.encode()).hexdigest()

# ============================================================================
# TRUST CHAIN BLOCK
# ============================================================================

@dataclass
class TrustBlock:
    """Immutable block in the trust chain"""
    index: int
    timestamp: float
    events: List[TrustEvent]
    previous_hash: str
    nonce: int = 0
    
    @property
    def hash(self) -> str:
        """Calculate block hash"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'events': [e.to_dict() for e in self.events],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Simple proof of work for immutability"""
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1

# ============================================================================
# CLAUDE TRUST PROFILE
# ============================================================================

class ClaudeTrustProfile:
    """Individual trust profile for each Claude instance"""
    
    def __init__(self, claude_id: str):
        self.claude_id = claude_id
        self.trust_score = 50.0  # Start neutral
        self.total_tasks = 0
        self.successful_tasks = 0
        self.failed_tasks = 0
        self.revenue_generated = 0.0
        self.compliance_violations = 0
        self.last_activity = datetime.now()
        self.approval_history = []
        self.permission_levels = {
            'spawn_instances': False,
            'send_emails': False,
            'send_sms': False,
            'process_payments': False,
            'access_sensitive_data': False,
            'make_autonomous_decisions': False
        }
        
    def update_trust_score(self, event: TrustEvent):
        """Update trust score based on event"""
        # Base impact
        impact = event.impact * 10  # Scale to 0-100 range
        
        # Amplify negative impacts (failures hurt more than successes help)
        if impact < 0:
            impact *= 1.5
            
        # Apply trust score change with bounds
        self.trust_score = max(0, min(100, self.trust_score + impact))
        
        # Update counters
        if event.event_type == TrustEventType.TASK_COMPLETED:
            self.successful_tasks += 1
            self.total_tasks += 1
        elif event.event_type == TrustEventType.TASK_FAILED:
            self.failed_tasks += 1
            self.total_tasks += 1
        elif event.event_type == TrustEventType.REVENUE_GENERATED:
            self.revenue_generated += event.metadata.get('amount', 0)
        elif event.event_type == TrustEventType.COMPLIANCE_VIOLATION:
            self.compliance_violations += 1
            
        self.last_activity = datetime.now()
        
    def get_permission_level(self) -> str:
        """Get permission level based on trust score"""
        if self.trust_score >= 90:
            return "FULL_AUTO"
        elif self.trust_score >= 70:
            return "SUPERVISED_AUTO"
        elif self.trust_score >= 50:
            return "APPROVAL_REQUIRED"
        elif self.trust_score >= 30:
            return "LIMITED"
        else:
            return "QUARANTINED"
            
    def requires_approval(self, action_type: str) -> bool:
        """Check if action requires human approval"""
        permission_level = self.get_permission_level()
        
        # Quarantined always needs approval
        if permission_level == "QUARANTINED":
            return True
            
        # High-risk actions always need approval below 70 trust
        high_risk_actions = ['process_payments', 'access_sensitive_data']
        if action_type in high_risk_actions and self.trust_score < 70:
            return True
            
        # Check specific permissions
        if action_type in self.permission_levels:
            return not self.permission_levels[action_type]
            
        # Default to requiring approval for unknown actions
        return True

# ============================================================================
# TRUST CHAIN MANAGER
# ============================================================================

class TrustChainManager:
    """Manages the immutable trust chain for all Claude instances"""
    
    def __init__(self, db_path: str = "./claude_trust_chain.db"):
        self.db_path = db_path
        self.chain: List[TrustBlock] = []
        self.pending_events: List[TrustEvent] = []
        self.profiles: Dict[str, ClaudeTrustProfile] = {}
        self.lock = threading.Lock()
        
        # Initialize database
        self._init_database()
        
        # Load existing chain
        self._load_chain()
        
        # Start block mining thread
        self.mining_thread = threading.Thread(target=self._mining_loop, daemon=True)
        self.mining_thread.start()
        
    def _init_database(self):
        """Initialize SQLite database for persistence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Trust chain blocks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trust_blocks (
                block_index INTEGER PRIMARY KEY,
                timestamp REAL,
                events TEXT,
                previous_hash TEXT,
                block_hash TEXT,
                nonce INTEGER
            )
        ''')
        
        # Claude profiles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claude_profiles (
                claude_id TEXT PRIMARY KEY,
                trust_score REAL,
                total_tasks INTEGER,
                successful_tasks INTEGER,
                failed_tasks INTEGER,
                revenue_generated REAL,
                compliance_violations INTEGER,
                last_activity TIMESTAMP,
                permission_levels TEXT
            )
        ''')
        
        # Approval queue
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approval_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                claude_id TEXT,
                action_type TEXT,
                action_details TEXT,
                risk_level TEXT,
                status TEXT DEFAULT 'pending',
                human_decision TEXT,
                decision_reason TEXT,
                decided_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _load_chain(self):
        """Load existing chain from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT block_index, timestamp, events, previous_hash, nonce
            FROM trust_blocks
            ORDER BY block_index
        ''')
        
        for row in cursor.fetchall():
            events_data = json.loads(row[2])
            events = [TrustEvent(**event_data) for event_data in events_data]
            
            block = TrustBlock(
                index=row[0],
                timestamp=row[1],
                events=events,
                previous_hash=row[3],
                nonce=row[4]
            )
            
            self.chain.append(block)
            
        conn.close()
        
        # Create genesis block if chain is empty
        if not self.chain:
            self._create_genesis_block()
            
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_event = TrustEvent(
            timestamp=time.time(),
            claude_id="SYSTEM",
            event_type=TrustEventType.CONFIGURATION_CHANGE,
            description="Trust chain initialized",
            impact=0.0,
            metadata={"genesis": True}
        )
        
        genesis_block = TrustBlock(
            index=0,
            timestamp=time.time(),
            events=[genesis_event],
            previous_hash="0"
        )
        
        genesis_block.mine_block()
        self.chain.append(genesis_block)
        self._save_block(genesis_block)
        
    def log_event(self, event: TrustEvent) -> str:
        """Log a trust event to the chain"""
        with self.lock:
            # Update Claude profile
            if event.claude_id not in self.profiles:
                self.profiles[event.claude_id] = ClaudeTrustProfile(event.claude_id)
                
            profile = self.profiles[event.claude_id]
            profile.update_trust_score(event)
            
            # Add to pending events
            self.pending_events.append(event)
            
            # Save profile
            self._save_profile(profile)
            
            return f"Event logged for {event.claude_id}: {event.event_type.value}"
            
    def request_approval(self, claude_id: str, action_type: str, 
                        action_details: Dict) -> Tuple[bool, str]:
        """Request human approval for an action"""
        profile = self.profiles.get(claude_id)
        if not profile:
            return False, "Unknown Claude instance"
            
        # Check if approval needed
        if not profile.requires_approval(action_type):
            # Auto-approve based on trust
            self.log_event(TrustEvent(
                timestamp=time.time(),
                claude_id=claude_id,
                event_type=TrustEventType.APPROVAL_GRANTED,
                description=f"Auto-approved: {action_type}",
                impact=0.1,
                metadata={"action_type": action_type, "auto_approved": True}
            ))
            return True, "Auto-approved based on trust score"
            
        # Queue for human approval
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        risk_level = self._calculate_risk_level(action_type, action_details)
        
        cursor.execute('''
            INSERT INTO approval_queue 
            (timestamp, claude_id, action_type, action_details, risk_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            claude_id,
            action_type,
            json.dumps(action_details),
            risk_level
        ))
        
        approval_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return False, f"Queued for human approval (ID: {approval_id})"
        
    def process_human_approval(self, approval_id: int, approved: bool, 
                              reason: str) -> bool:
        """Process human approval decision"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get approval request
        cursor.execute('''
            SELECT claude_id, action_type, action_details
            FROM approval_queue
            WHERE id = ? AND status = 'pending'
        ''', (approval_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
            
        claude_id, action_type, action_details = row
        
        # Update approval
        cursor.execute('''
            UPDATE approval_queue
            SET status = ?, human_decision = ?, decision_reason = ?, decided_at = ?
            WHERE id = ?
        ''', (
            'approved' if approved else 'denied',
            'approved' if approved else 'denied',
            reason,
            datetime.now(),
            approval_id
        ))
        
        conn.commit()
        conn.close()
        
        # Log event
        self.log_event(TrustEvent(
            timestamp=time.time(),
            claude_id=claude_id,
            event_type=TrustEventType.APPROVAL_GRANTED if approved else TrustEventType.APPROVAL_DENIED,
            description=f"Human {'approved' if approved else 'denied'}: {action_type}",
            impact=0.2 if approved else -0.3,
            metadata={
                "action_type": action_type,
                "approval_id": approval_id,
                "reason": reason
            },
            human_approval=approved,
            approval_reason=reason
        ))
        
        return True
        
    def _mining_loop(self):
        """Background thread to mine blocks"""
        while True:
            time.sleep(10)  # Mine every 10 seconds
            
            with self.lock:
                if len(self.pending_events) > 0:
                    # Create new block
                    previous_hash = self.chain[-1].hash if self.chain else "0"
                    
                    new_block = TrustBlock(
                        index=len(self.chain),
                        timestamp=time.time(),
                        events=self.pending_events.copy(),
                        previous_hash=previous_hash
                    )
                    
                    new_block.mine_block()
                    self.chain.append(new_block)
                    self._save_block(new_block)
                    
                    # Clear pending events
                    self.pending_events.clear()
                    
    def _save_block(self, block: TrustBlock):
        """Save block to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        events_json = json.dumps([e.to_dict() for e in block.events])
        
        cursor.execute('''
            INSERT INTO trust_blocks 
            (block_index, timestamp, events, previous_hash, block_hash, nonce)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            block.index,
            block.timestamp,
            events_json,
            block.previous_hash,
            block.hash,
            block.nonce
        ))
        
        conn.commit()
        conn.close()
        
    def _save_profile(self, profile: ClaudeTrustProfile):
        """Save Claude profile to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO claude_profiles
            (claude_id, trust_score, total_tasks, successful_tasks, failed_tasks,
             revenue_generated, compliance_violations, last_activity, permission_levels)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile.claude_id,
            profile.trust_score,
            profile.total_tasks,
            profile.successful_tasks,
            profile.failed_tasks,
            profile.revenue_generated,
            profile.compliance_violations,
            profile.last_activity,
            json.dumps(profile.permission_levels)
        ))
        
        conn.commit()
        conn.close()
        
    def _calculate_risk_level(self, action_type: str, details: Dict) -> str:
        """Calculate risk level for an action"""
        high_risk_actions = ['process_payments', 'delete_data', 'modify_configuration']
        medium_risk_actions = ['send_emails', 'send_sms', 'spawn_instances']
        
        if action_type in high_risk_actions:
            return "HIGH"
        elif action_type in medium_risk_actions:
            return "MEDIUM"
        else:
            return "LOW"
            
    def get_trust_report(self, claude_id: str) -> Dict:
        """Get comprehensive trust report for a Claude instance"""
        profile = self.profiles.get(claude_id)
        if not profile:
            return {"error": "Unknown Claude instance"}
            
        # Get recent events
        recent_events = []
        for block in reversed(self.chain[-10:]):  # Last 10 blocks
            for event in block.events:
                if event.claude_id == claude_id:
                    recent_events.append({
                        "timestamp": datetime.fromtimestamp(event.timestamp).isoformat(),
                        "type": event.event_type.value,
                        "description": event.description,
                        "impact": event.impact
                    })
                    
        return {
            "claude_id": claude_id,
            "trust_score": profile.trust_score,
            "permission_level": profile.get_permission_level(),
            "stats": {
                "total_tasks": profile.total_tasks,
                "successful_tasks": profile.successful_tasks,
                "failed_tasks": profile.failed_tasks,
                "success_rate": profile.successful_tasks / profile.total_tasks if profile.total_tasks > 0 else 0,
                "revenue_generated": profile.revenue_generated,
                "compliance_violations": profile.compliance_violations
            },
            "permissions": profile.permission_levels,
            "last_activity": profile.last_activity.isoformat(),
            "recent_events": recent_events
        }
        
    def verify_chain_integrity(self) -> bool:
        """Verify the integrity of the entire chain"""
        if not self.chain:
            return True
            
        # Check genesis block
        if self.chain[0].previous_hash != "0":
            return False
            
        # Check all blocks
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash link
            if current_block.previous_hash != previous_block.hash:
                return False
                
            # Verify block hash
            if current_block.hash != current_block.hash:  # Recalculates
                return False
                
        return True
        
    def export_chain_audit(self, start_date: datetime = None, 
                          end_date: datetime = None) -> str:
        """Export chain audit for legal compliance"""
        audit = []
        audit.append("CLAUDE TRUST CHAIN AUDIT REPORT")
        audit.append(f"Generated: {datetime.now().isoformat()}")
        audit.append(f"Chain Integrity: {'VALID' if self.verify_chain_integrity() else 'COMPROMISED'}")
        audit.append(f"Total Blocks: {len(self.chain)}")
        audit.append("")
        
        # Filter blocks by date if specified
        blocks_to_audit = self.chain
        if start_date or end_date:
            blocks_to_audit = [
                b for b in self.chain
                if (not start_date or datetime.fromtimestamp(b.timestamp) >= start_date) and
                   (not end_date or datetime.fromtimestamp(b.timestamp) <= end_date)
            ]
            
        audit.append(f"Blocks in Range: {len(blocks_to_audit)}")
        audit.append("="*80)
        
        # Detailed block audit
        for block in blocks_to_audit:
            audit.append(f"\nBlock #{block.index}")
            audit.append(f"Timestamp: {datetime.fromtimestamp(block.timestamp).isoformat()}")
            audit.append(f"Hash: {block.hash}")
            audit.append(f"Previous Hash: {block.previous_hash}")
            audit.append(f"Events: {len(block.events)}")
            
            for event in block.events:
                audit.append(f"  - {event.timestamp}: {event.claude_id} - {event.event_type.value}")
                audit.append(f"    Description: {event.description}")
                audit.append(f"    Impact: {event.impact}")
                if event.human_approval is not None:
                    audit.append(f"    Human Approval: {event.human_approval}")
                    audit.append(f"    Reason: {event.approval_reason}")
                    
        return "\n".join(audit)

# ============================================================================
# INTEGRATION WITH CLAUDE CONTROL SYSTEM
# ============================================================================

class TrustIntegration:
    """Integrate trust chain with Claude Control System"""
    
    def __init__(self, trust_chain: TrustChainManager, controller):
        self.trust_chain = trust_chain
        self.controller = controller
        
        # Hook into controller events
        self._setup_event_hooks()
        
    def _setup_event_hooks(self):
        """Setup event listeners for controller"""
        # Listen for spawn events
        self.controller.on('spawn_attempt', self.on_spawn_attempt)
        self.controller.on('task_completed', self.on_task_completed)
        self.controller.on('task_failed', self.on_task_failed)
        self.controller.on('error_occurred', self.on_error_occurred)
        
    def on_spawn_attempt(self, data):
        """Handle spawn attempt"""
        claude_id = data.get('parent_id', 'ROOT')
        
        # Check if approval needed
        approved, message = self.trust_chain.request_approval(
            claude_id,
            'spawn_instances',
            {
                'task': data.get('task'),
                'depth': data.get('depth', 0)
            }
        )
        
        if not approved:
            # Log denial
            self.trust_chain.log_event(TrustEvent(
                timestamp=time.time(),
                claude_id=claude_id,
                event_type=TrustEventType.APPROVAL_DENIED,
                description=f"Spawn attempt denied: {message}",
                impact=-0.1,
                metadata=data
            ))
            
        return approved
        
    def on_task_completed(self, data):
        """Handle task completion"""
        self.trust_chain.log_event(TrustEvent(
            timestamp=time.time(),
            claude_id=data.get('instance_id'),
            event_type=TrustEventType.TASK_COMPLETED,
            description=f"Task completed successfully",
            impact=0.2,
            metadata=data
        ))
        
    def on_task_failed(self, data):
        """Handle task failure"""
        self.trust_chain.log_event(TrustEvent(
            timestamp=time.time(),
            claude_id=data.get('instance_id'),
            event_type=TrustEventType.TASK_FAILED,
            description=f"Task failed: {data.get('error')}",
            impact=-0.3,
            metadata=data
        ))
        
    def on_error_occurred(self, data):
        """Handle errors"""
        self.trust_chain.log_event(TrustEvent(
            timestamp=time.time(),
            claude_id=data.get('instance_id'),
            event_type=TrustEventType.ERROR_GENERATED,
            description=f"Error: {data.get('error')}",
            impact=-0.2,
            metadata=data
        ))

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Initialize trust chain
    trust_chain = TrustChainManager()
    
    # Example: Claude completes a task
    trust_chain.log_event(TrustEvent(
        timestamp=time.time(),
        claude_id="claude_001",
        event_type=TrustEventType.TASK_COMPLETED,
        description="Successfully parsed FurnishedFinder email",
        impact=0.2,
        metadata={"task": "email_parsing", "duration": 1.2}
    ))
    
    # Example: Claude generates revenue
    trust_chain.log_event(TrustEvent(
        timestamp=time.time(),
        claude_id="claude_001",
        event_type=TrustEventType.REVENUE_GENERATED,
        description="Lead converted to paying customer",
        impact=0.5,
        metadata={"amount": 1500, "customer": "lead_12345"}
    ))
    
    # Example: Request approval for sensitive action
    approved, message = trust_chain.request_approval(
        "claude_002",
        "process_payments",
        {"amount": 500, "customer": "cust_67890"}
    )
    
    print(f"Approval status: {approved}, Message: {message}")
    
    # Get trust report
    report = trust_chain.get_trust_report("claude_001")
    print(json.dumps(report, indent=2))
    
    # Export audit
    audit = trust_chain.export_chain_audit()
    print(audit)
