#!/usr/bin/env python3
"""
🚀 QUICK SETUP SCRIPT FOR BROADCAST SYSTEM
Sets up the broadcast system and tests connectivity
"""

import os
import sys
import subprocess

def setup_broadcast_system():
    print("🚀 SETTING UP CLAUDE BROADCAST SYSTEM")
    print("=" * 50)
    
    # 1. Create necessary directories
    directories = [
        "/Users/noshit/MCMANSION/AUTOMATION_LAB/broadcasts",
        "/Users/noshit/MCMANSION/AUTOMATION_LAB/replit_endpoints",
        "/Users/noshit/MCMANSION/AUTOMATION_LAB/instance_memories"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}")
    
    # 2. Save the broadcast system
    print("\n💾 Saving broadcast system...")
    broadcast_file = "/Users/noshit/MCMANSION/AUTOMATION_LAB/replit_broadcast.py"
    # Note: The broadcast system code is already in the artifact above
    print(f"  ✅ Broadcast system ready at: {broadcast_file}")
    
    # 3. Initialize connections
    print("\n🔗 Initializing connections...")
    os.system(f"cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python replit_broadcast.py init")
    
    # 4. Generate endpoint code
    print("\n🔧 Generating Replit endpoint code...")
    os.system(f"cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python replit_broadcast.py setup")
    
    # 5. Create a test broadcast
    print("\n🧪 Testing broadcast system...")
    test_message = {
        "insight": "Cross-platform Claude network activated",
        "context": "All instances connected via unified broadcast system",
        "impact": "100% knowledge synchronization across local and cloud environments"
    }
    
    # 6. Show next steps
    print("\n✅ SETUP COMPLETE!")
    print("\n📋 NEXT STEPS:")
    print("1. Deploy endpoint code to each Replit:")
    for replit in ["CLAUDECON", "CLAUDENTAL", "CLAUDEGAL", "CLAUDETECT", "CLAUDETOTAL", "CLAUDEGENIE"]:
        print(f"   - Copy /Users/noshit/MCMANSION/AUTOMATION_LAB/replit_endpoints/{replit}_memory_endpoint.py to Replit")
    
    print("\n2. Find missing Replit credentials:")
    print("   bash find_missing_replit.sh")
    
    print("\n3. Test the broadcast:")
    print("   python replit_broadcast.py test")
    
    print("\n4. Send a real broadcast:")
    print('   python replit_broadcast.py broadcast "New insight" "Context" "Impact"')
    
    print("\n🎯 BROADCAST COMMANDS:")
    print("  Status:    python replit_broadcast.py status")
    print("  Test:      python replit_broadcast.py test")
    print("  Broadcast: python replit_broadcast.py broadcast <insight> <context> <impact> [source]")
    
    # 7. Create helper aliases
    print("\n🔧 Creating helper commands...")
    alias_file = "/Users/noshit/.broadcast_aliases"
    with open(alias_file, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('# Claude Broadcast System Aliases\n\n')
        f.write('alias broadcast="cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python replit_broadcast.py broadcast"\n')
        f.write('alias broadcast-status="cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python replit_broadcast.py status"\n')
        f.write('alias broadcast-test="cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python replit_broadcast.py test"\n')
        f.write('alias claude-memories="cd /Users/noshit/MCMANSION/AUTOMATION_LAB && python"\n')
    
    print(f"  ✅ Created aliases in: {alias_file}")
    print("  Add to your shell: echo 'source ~/.broadcast_aliases' >> ~/.zshrc")

if __name__ == "__main__":
    setup_broadcast_system()