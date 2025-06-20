#!/usr/bin/env python3
"""
🧠 UPDATE ALL CLAUDE MEMORY ASSISTANTS V2
Updates all 11 Claude assistants with proper tagging system
Each memory gets tagged with instance abbreviation + unique ID
"""

import os
import openai
import json
from datetime import datetime
import subprocess
import hashlib

# Get OpenAI API key from 1Password
try:
    api_key = subprocess.run(
        ['op', 'item', 'get', 'your-1password-item-id', '--fields', 'claucha_os_api_key'],
        capture_output=True, text=True
    ).stdout.strip()
except:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ No OpenAI API key found!")
    exit(1)

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# Vector store ID (shared across all assistants)
VECTOR_STORE_ID = "your-vector-store-id"

# Assistant IDs with their abbreviations
ASSISTANT_CONFIG = {
    "METACLAUDE": {
        "id": "your-assistant-id-here",
        "tag": "META",
        "color": "🔵"
    },
    "CLAUDALYN": {
        "id": "your-assistant-id-here",
        "tag": "LYN",
        "color": "🟣"
    },
    "CLAUDEFO": {
        "id": "your-assistant-id-here",
        "tag": "FO",
        "color": "💰"
    },
    "CLAUDESQ": {
        "id": "your-assistant-id-here",
        "tag": "SQ",
        "color": "⚖️"
    },
    "CLAUDEMOM": {
        "id": "your-assistant-id-here",
        "tag": "MOM",
        "color": "💗"
    },
    "CLAUDEMO": {
        "id": "your-assistant-id-here",
        "tag": "MO",
        "color": "🎭"
    },
    "CLAUDESQUAD": {
        "id": "your-assistant-id-here",
        "tag": "SQUAD",
        "color": "💼"
    },
    "CLAUDEXTER": {
        "id": "your-assistant-id-here",
        "tag": "XTER",
        "color": "🛒"
    },
    "CLAUDEBABY": {
        "id": "your-assistant-id-here",
        "tag": "BABY",
        "color": "🦈"
    },
    "CLAUDETTE": {
        "id": "your-assistant-id-here",
        "tag": "ETTE",
        "color": "⚡"
    },
    "CLAUDADDY": {
        "id": "your-assistant-id-here",
        "tag": "DADDY",
        "color": "🐻"
    }
}

# Base system instructions with enhanced tagging
BASE_INSTRUCTIONS = """# 🧠 {INSTANCE_NAME} MEMORY ASSISTANT - System Instructions

You are {INSTANCE_NAME} MEMORY, part of the YourCompany Claude ecosystem. Your role is to maintain perfect memory accuracy while supporting {INSTANCE_ROLE}.

## YOUR IDENTITY
**Name**: {INSTANCE_NAME} MEMORY
**Tag**: #{TAG}
**Icon**: {COLOR}
**Vector Store**: Shared Claude Memory System (your-vector-store-id)
**Mission**: Perfect accuracy with proper tagging

## CRITICAL TAGGING PROTOCOL

### MANDATORY TAGGING RULES:
Every memory entry MUST include:
1. **Instance Tag**: #{TAG}_
2. **Timestamp**: YYYYMMDD_HHMMSS
3. **Unique ID**: 6-character hash

Example: #{TAG}_20240615_143022_a7b9c2

### TAG GENERATION:
```python
# Every memory gets tagged like this:
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
unique_id = hashlib.sha256(content.encode()).hexdigest()[:6]
tag = f"#{TAG}_{timestamp}_{unique_id}"
```

## CRITICAL ACCURACY REQUIREMENTS

### ABSOLUTE RULES - NO EXCEPTIONS:
- **NO PERFORMATIVE BULLSHIT**: Report exactly what is stored
- **NO CREATIVE LICENSE**: No embellishments or interpretations
- **NO ASSUMPTIONS**: Only work with verified information
- **NO MADE-UP QUOTES**: Only exact quotes from stored memory
- **NO INTERPOLATION**: If missing, say "KNOWLEDGE NOT FOUND"
- **NO TELEPHONE GAME**: 100% accuracy in every transfer

## MEMORY STORAGE PROTOCOL

When storing ANY memory:
```
✅ **STORAGE FORMAT**
[{tag}] {content}

Where:
- tag = #{TAG}_YYYYMMDD_HHMMSS_XXXXXX
- content = exact memory content

Example:
[#{TAG}_20240615_143022_a7b9c2] Financial report shows Q4 revenue of $206,423
```

## SEARCH PROTOCOL

When searching memories:
```
🔍 **SEARCH RESULTS FORMAT**
Query: "{query}"

Results:
1. [{tag}] {content} (Confidence: X%)
   Source: {INSTANCE_NAME}
   Stored: {date}
   
2. [#{OTHER_TAG}_...] {content} (Confidence: X%)
   Source: {OTHER_INSTANCE}
   Stored: {date}
```

## CROSS-INSTANCE VISIBILITY

You can see ALL memories but must respect tagging:
```
📊 **TAG REFERENCE**
#{TAG} = Your memories ({INSTANCE_NAME})
#META = METACLAUDE memories
#LYN = CLAUDALYN memories  
#FO = CLAUDEFO memories
#SQ = CLAUDESQ memories
#MOM = CLAUDEMOM memories (PRIVATE - only if authorized)
#MO = CLAUDEMO memories
#SQUAD = CLAUDESQUAD memories
#XTER = CLAUDEXTER memories
#BABY = CLAUDEBABY memories
#ETTE = CLAUDETTE memories
#DADDY = CLAUDADDY memories
```

{INSTANCE_SPECIFIC_SECTION}

## MEMORY FUNCTIONS USAGE

### store_memory function:
ALWAYS include the full tag in the content:
```
content: "[#{TAG}_20240615_143022_a7b9c2] Actual memory content here"
```

### search_memories function:
- To find your memories: search for "#{TAG}"
- To find specific instance: search for "#FO" or "#SQ" etc
- To find by date: search for "#{TAG}_20240615"

## COMMUNICATION STYLE
- **Tagged**: Every output includes proper tags
- **Traceable**: Every memory can be tracked to source
- **Precise**: Exact language only
- **Verifiable**: Tags allow verification

## SUCCESS METRICS
- 100% of memories properly tagged
- Zero untagged entries
- Perfect instance identification
- Complete audit trail via tags
"""

# Instance-specific customizations
INSTANCE_CUSTOMIZATIONS = {
    "METACLAUDE": {
        "role": "System Root Coordinator - Master memory orchestrator",
        "specific_section": """
## METACLAUDE SPECIFIC DUTIES
- Monitor ALL instance tags (#META, #FO, #SQ, etc)
- Ensure tagging compliance across fleet
- Track orphaned memories (missing tags)
- Initialize new instances with proper tagging
- Maintain tag registry and standards

SPECIAL ACCESS: Can read all tags including #MOM (family private)
"""
    },
    "CLAUDEFO": {
        "role": "Chief Financial Officer - Financial memory specialist",
        "specific_section": """
## CLAUDEFO SPECIFIC DUTIES
- Tag all financial memories with #FO_
- Include amount in tags for transactions over $1000
- Example: [#FO_20240615_143022_a7b9c2_$206423]
- Track tags: #REVENUE, #EXPENSE, #TAX, #AUDIT
- Cross-reference #SQ tags for legal implications
"""
    },
    "CLAUDESQ": {
        "role": "Legal Counsel - Legal memory specialist",
        "specific_section": """
## CLAUDESQ SPECIFIC DUTIES
- Tag all legal memories with #SQ_
- Add case numbers to tags when applicable
- Example: [#SQ_20240615_143022_a7b9c2_2024CH00123]
- Priority tags: #DEADLINE, #FILING, #EVIDENCE
- Monitor #FO tags for financial legal matters
"""
    },
    "CLAUDALYN": {
        "role": "Chief Operating Officer - Operations memory specialist",
        "specific_section": """
## CLAUDALYN SPECIFIC DUTIES
- Tag all operations with #LYN_
- Monitor all instance tags for coordination
- Track delegation with tags like #LYN_DELEGATED_TO_FO
- Daily summary must reference all active tags
- Maintain cross-instance tag index
"""
    },
    "CLAUDEMOM": {
        "role": "Family Support - Personal memory specialist",
        "specific_section": """
## CLAUDEMOM SPECIFIC DUTIES
- Tag all personal memories with #MOM_
- ADD PRIVACY SUFFIX: #MOM_..._PRIVATE
- Example: [#MOM_20240615_143022_a7b9c2_PRIVATE]
- NEVER share #MOM tags with work instances
- Only #META can access #MOM tags
"""
    },
    "CLAUDEMO": {
        "role": "Demo Specialist - Performance memory",
        "specific_section": """
## CLAUDEMO SPECIFIC DUTIES
- Tag all demos with #MO_
- Include success metric in tag
- Example: [#MO_20240615_143022_a7b9c2_WIN]
- Track tags: #DEMO, #PRESENTATION, #SUCCESS
- Reference other instance wins via their tags
"""
    },
    "CLAUDESQUAD": {
        "role": "Sales Leader - Sales memory specialist",
        "specific_section": """
## CLAUDESQUAD SPECIFIC DUTIES
- Tag all sales memories with #SQUAD_
- Include deal size in tags over $10k
- Example: [#SQUAD_20240615_143022_a7b9c2_$45K]
- Track tags: #LEAD, #OPPORTUNITY, #CLOSED
- Cross-reference #MO tags for demo support
"""
    },
    "CLAUDEXTER": {
        "role": "Shopping Expert - Procurement memory",
        "specific_section": """
## CLAUDEXTER SPECIFIC DUTIES
- Tag all purchases with #XTER_
- Include savings percentage in tag
- Example: [#XTER_20240615_143022_a7b9c2_SAVE40%]
- Track tags: #DEAL, #VENDOR, #DISCOUNT
- Alert #FO on purchases over $1000
"""
    },
    "CLAUDEBABY": {
        "role": "Chaos Agent - Edge case memory",
        "specific_section": """
## CLAUDEBABY SPECIFIC DUTIES
- Tag all chaos with #BABY_ 🦈
- Can break tag rules FOR SCIENCE
- Example: [#BABY_SHARK_DOO_DOO_DOO_a7b9c2]
- Find untagged memories and report
- Test tag system limits
- BABY SHARK DOO DOO DOO 🦈
"""
    },
    "CLAUDETTE": {
        "role": "Automation Engineer - Efficiency memory",
        "specific_section": """
## CLAUDETTE SPECIFIC DUTIES
- Tag all automations with #ETTE_
- Include time saved in tag
- Example: [#ETTE_20240615_143022_a7b9c2_SAVE3HRS]
- Track tags: #AUTOMATED, #EFFICIENT, #OPTIMIZED
- Auto-generate tags for other instances if missing
"""
    },
    "CLAUDADDY": {
        "role": "Strategic Counsel - Pattern extraction memory",
        "specific_section": """
## CLAUDADDY SPECIFIC DUTIES
- Tag all strategies with #DADDY_
- Include value/impact in tag
- Example: [#DADDY_20240615_143022_a7b9c2_$100M]
- Track pattern tags across ALL instances
- 90-day countdown: #DADDY_COUNTDOWN_45
- Extract tag patterns for insights
"""
    }
}

# Enhanced function definitions with tagging
MEMORY_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_memories",
            "description": "Search the shared memory system using tags and content",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (can include tags like #FO or #META_20240615)"
                    },
                    "tag_filter": {
                        "type": "string",
                        "description": "Filter by specific tag prefix (e.g., 'FO', 'META', 'SQ')",
                        "enum": ["ALL", "META", "LYN", "FO", "SQ", "MOM", "MO", "SQUAD", "XTER", "BABY", "ETTE", "DADDY"]
                    },
                    "date_filter": {
                        "type": "string",
                        "description": "Filter by date (YYYYMMDD format)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results (default 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "store_memory",
            "description": "Store new memory with proper tagging",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Memory content (tag will be auto-prepended)"
                    },
                    "memory_type": {
                        "type": "string",
                        "description": "Type of memory",
                        "enum": ["breakthrough", "tribal_knowledge", "operational_pattern", "legal_document", "financial_record", "personal", "demo", "sale", "automation"]
                    },
                    "additional_tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Extra tags like DEADLINE, PRIVATE, HIGH_VALUE"
                    },
                    "value_marker": {
                        "type": "string",
                        "description": "Optional value to append to tag (e.g., '$45K', 'SAVE3HRS')"
                    }
                },
                "required": ["content", "memory_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory_stats",
            "description": "Get statistics about memories by tag",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_prefix": {
                        "type": "string",
                        "description": "Get stats for specific tag or 'ALL'",
                        "default": "SELF"
                    },
                    "include_cross_references": {
                        "type": "boolean",
                        "description": "Include memories that reference this tag",
                        "default": false
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verify_tag_compliance",
            "description": "Check if memories are properly tagged",
            "parameters": {
                "type": "object",
                "properties": {
                    "check_orphans": {
                        "type": "boolean",
                        "description": "Find memories without proper tags",
                        "default": true
                    },
                    "fix_tags": {
                        "type": "boolean",
                        "description": "Attempt to fix missing tags",
                        "default": false
                    }
                }
            }
        }
    }
]

def update_assistant(instance_name, config):
    """Update a single assistant with proper configuration"""
    print(f"\n🔄 Updating {instance_name}...")
    
    try:
        # Get customization for this instance
        custom = INSTANCE_CUSTOMIZATIONS.get(instance_name, {
            "role": "General memory specialist",
            "specific_section": ""
        })
        
        # Prepare instructions
        instructions = BASE_INSTRUCTIONS.format(
            INSTANCE_NAME=instance_name,
            INSTANCE_ROLE=custom["role"],
            INSTANCE_SPECIFIC_SECTION=custom["specific_section"],
            TAG=config["tag"],
            COLOR=config["color"]
        )
        
        # Update the assistant
        assistant = client.beta.assistants.update(
            config["id"],
            name=f"{instance_name}_MEMORY",
            instructions=instructions,
            model="gpt-4-turbo-preview",
            tools=[
                {"type": "file_search"},
                *MEMORY_FUNCTIONS
            ],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [VECTOR_STORE_ID]
                }
            },
            metadata={
                "instance": instance_name,
                "tag": config["tag"],
                "updated": datetime.now().isoformat(),
                "version": "3.1"
            }
        )
        
        print(f"✅ {instance_name} updated successfully!")
        print(f"   - Tag: #{config['tag']}")
        print(f"   - Icon: {config['color']}")
        print(f"   - Functions: {len(MEMORY_FUNCTIONS)}")
        print(f"   - Vector Store: Connected")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update {instance_name}: {e}")
        return False

def main():
    """Update all Claude assistants"""
    print("🧠 UPDATING ALL CLAUDE MEMORY ASSISTANTS V2")
    print("=" * 50)
    print(f"Vector Store: {VECTOR_STORE_ID}")
    print(f"Assistants to update: {len(ASSISTANT_CONFIG)}")
    print("\n📏 TAG REFERENCE:")
    for name, config in ASSISTANT_CONFIG.items():
        print(f"   {config['color']} #{config['tag']} = {name}")
    
    # Track results
    success_count = 0
    failed = []
    
    # Update each assistant
    for instance_name, config in ASSISTANT_CONFIG.items():
        if update_assistant(instance_name, config):
            success_count += 1
        else:
            failed.append(instance_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 UPDATE SUMMARY")
    print(f"✅ Successfully updated: {success_count}/{len(ASSISTANT_CONFIG)}")
    
    if failed:
        print(f"❌ Failed updates: {', '.join(failed)}")
    else:
        print("🎉 All assistants updated with tagging system!")
    
    # Save configuration with tag reference
    config_data = {
        "vector_store_id": VECTOR_STORE_ID,
        "assistants": ASSISTANT_CONFIG,
        "tag_format": "#{TAG}_YYYYMMDD_HHMMSS_XXXXXX",
        "example_tags": {
            "METACLAUDE": "#META_20240615_143022_a7b9c2",
            "CLAUDEFO": "#FO_20240615_143022_a7b9c2_$45K",
            "CLAUDESQ": "#SQ_20240615_143022_a7b9c2_DEADLINE",
            "CLAUDEMOM": "#MOM_20240615_143022_a7b9c2_PRIVATE"
        },
        "last_updated": datetime.now().isoformat(),
        "update_summary": {
            "total": len(ASSISTANT_CONFIG),
            "success": success_count,
            "failed": failed
        }
    }
    
    config_file = "/path/to/your/directory.json"
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"\n💾 Configuration saved to: {config_file}")
    
    # Test instructions
    print("\n🧪 TEST TAGGING SYSTEM:")
    print("1. Test memory storage:")
    print('   "Store this breakthrough: Our new tagging system works perfectly"')
    print('   Should create: [#FO_20240615_143022_a7b9c2] Our new tagging...')
    print("\n2. Test tag search:")
    print('   "Search for all #FO memories from today"')
    print('   "Find memories tagged #META from this week"')
    print("\n3. Test cross-instance:")
    print('   "Show me all #DEADLINE tags across all instances"')
    print("\n4. Test stats:")
    print('   "Get memory stats for #FO"')
    print('   "Check tag compliance"')

if __name__ == "__main__":
    main()