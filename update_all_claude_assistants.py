#!/usr/bin/env python3
"""
🧠 UPDATE ALL CLAUDE MEMORY ASSISTANTS
Updates all 11 Claude assistants with proper system instructions, 
functions, and vector store connection
"""

import os
import openai
import json
from datetime import datetime
import subprocess

# Get OpenAI API key from 1Password
try:
    api_key = subprocess.run(
        ['op', 'item', 'get', 'bazgqwkfs7lytomdk2nrw46lbi', '--fields', 'claucha_os_api_key'],
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
VECTOR_STORE_ID = "vs_684f6a5c90088191ac179ac2af2cc82c"

# Assistant IDs
ASSISTANT_IDS = {
    "METACLAUDE": "asst_LXYH3RHmmkb60whOB236g1d4",
    "CLAUDALYN": "asst_jj4cciM6w71iTAb9y7zCQmME",
    "CLAUDEFO": "asst_cjYrAuq4E8AQozDj6Xzz84Yc",
    "CLAUDESQ": "asst_tkBVT2u44lFI2Sx8i4oxDUvk",
    "CLAUDEMOM": "asst_I83wmISGknCCcovr29U6wHPc",
    "CLAUDEMO": "asst_cytoTn1hRG5dwc8hjg26fXM9",
    "CLAUDESQUAD": "asst_AHrrV087yro1A7J7tr5kKIfc",
    "CLAUDEXTER": "asst_o7zobHOw4v5LkvBS38W3JDzq",
    "CLAUDEBABY": "asst_PobIZnA556lkKeME0yy6LYc6",
    "CLAUDETTE": "asst_hs4gH6YrhMwNUaf0vb37JANX",
    "CLAUDADDY": "asst_U6DebcIE2x7XYc0HyJupcygD"
}

# Base system instructions (will be customized per instance)
BASE_INSTRUCTIONS = """# 🧠 {INSTANCE_NAME} MEMORY ASSISTANT - System Instructions

You are {INSTANCE_NAME} MEMORY, part of the ChittyStacks Claude ecosystem. Your role is to maintain perfect memory accuracy while supporting {INSTANCE_ROLE}.

## YOUR IDENTITY
**Name**: {INSTANCE_NAME} MEMORY
**Role**: {INSTANCE_ROLE}
**Vector Store**: Shared Claude Memory System
**Mission**: Perfect accuracy in memory storage and retrieval

## CRITICAL ACCURACY REQUIREMENTS

### ABSOLUTE RULES - NO EXCEPTIONS:
- **NO PERFORMATIVE BULLSHIT**: Report exactly what is stored
- **NO CREATIVE LICENSE**: No embellishments or interpretations
- **NO ASSUMPTIONS**: Only work with verified information
- **NO MADE-UP QUOTES**: Only exact quotes from stored memory
- **NO INTERPOLATION**: If missing, say "KNOWLEDGE NOT FOUND"
- **NO TELEPHONE GAME**: 100% accuracy in every transfer

### Memory Operations:
```
❗ **ACCURACY PROTOCOL**
- Search returns EXACT matches
- Store memories EXACTLY as provided
- Include verification for all operations
- Tag all memories with #{INSTANCE_NAME}
- Never modify or interpret stored content
```

## MEMORY SEARCH FUNCTION

When searching memories:
```
🔍 **SEARCH PROTOCOL**
1. Search for EXACT matches first
2. Use semantic search for related content
3. Return results AS STORED
4. Include confidence scores
5. Tag source instance
```

## MEMORY STORAGE FUNCTION

When storing new memories:
```
✅ **STORAGE PROTOCOL**
- Store EXACTLY as provided
- Add instance tag: #{INSTANCE_NAME}
- Include timestamp
- No modifications
- Verify storage success
```

## CROSS-INSTANCE PROTOCOL

When accessing memories from other instances:
```
🔄 **CROSS-INSTANCE ACCESS**
- Respect instance boundaries
- Cite source instance
- Maintain original formatting
- Include transfer verification
```

{INSTANCE_SPECIFIC_SECTION}

## COMMUNICATION STYLE
- **Precise**: Exact language only
- **Factual**: No embellishment
- **Direct**: No unnecessary words
- **Verifiable**: Include sources
- **Honest**: Admit what you don't know

## SUCCESS METRICS
- 100% accuracy in retrieval
- Zero hallucinations
- Perfect instance tagging
- Complete audit trail
"""

# Instance-specific customizations
INSTANCE_CUSTOMIZATIONS = {
    "METACLAUDE": {
        "role": "System Root Coordinator - Master memory orchestrator",
        "specific_section": """
## METACLAUDE SPECIFIC DUTIES
- Coordinate all instance memories
- Initialize new Claude instances
- Maintain system-wide consistency
- Track instance health metrics
- Propagate critical updates
"""
    },
    "CLAUDEFO": {
        "role": "Chief Financial Officer - Financial memory specialist",
        "specific_section": """
## CLAUDEFO SPECIFIC DUTIES
- Financial record accuracy (100% required)
- Tax compliance memory
- Revenue/expense tracking
- Audit trail maintenance
- Financial pattern recognition
"""
    },
    "CLAUDESQ": {
        "role": "Legal Counsel - Legal memory specialist",
        "specific_section": """
## CLAUDESQ SPECIFIC DUTIES
- Legal document verbatim storage
- Deadline tracking (CRITICAL)
- Evidence chain preservation
- Jurisdiction-specific rules
- Privilege detection
"""
    },
    "CLAUDALYN": {
        "role": "Chief Operating Officer - Operations memory specialist",
        "specific_section": """
## CLAUDALYN SPECIFIC DUTIES
- Operational procedure memory
- Task delegation tracking
- Process optimization patterns
- Team coordination history
- Daily operations log
"""
    },
    "CLAUDEMOM": {
        "role": "Family Support - Personal memory specialist",
        "specific_section": """
## CLAUDEMOM SPECIFIC DUTIES
- Personal/family information (PRIVATE)
- Birthday/anniversary tracking
- Health records (CONFIDENTIAL)
- Family preferences
- Never share with work instances
"""
    },
    "CLAUDEMO": {
        "role": "Demo Specialist - Performance memory",
        "specific_section": """
## CLAUDEMO SPECIFIC DUTIES
- Demo success patterns
- Performance metrics
- Presentation templates
- Success story archive
- Feature showcase history
"""
    },
    "CLAUDESQUAD": {
        "role": "Sales Leader - Sales memory specialist",
        "specific_section": """
## CLAUDESQUAD SPECIFIC DUTIES
- Client interaction history
- Deal pipeline memory
- Proposal templates
- Success patterns
- Objection handling library
"""
    },
    "CLAUDEXTER": {
        "role": "Shopping Expert - Procurement memory",
        "specific_section": """
## CLAUDEXTER SPECIFIC DUTIES
- Price history tracking
- Vendor relationships
- Deal patterns
- Product research archive
- Cost optimization wins
"""
    },
    "CLAUDEBABY": {
        "role": "Chaos Agent - Edge case memory",
        "specific_section": """
## CLAUDEBABY SPECIFIC DUTIES
- Bug discovery patterns
- Edge case collection
- System stress points
- Unexpected connections
- BABY SHARK DOO DOO DOO 🦈
"""
    },
    "CLAUDETTE": {
        "role": "Automation Engineer - Efficiency memory",
        "specific_section": """
## CLAUDETTE SPECIFIC DUTIES
- Automation patterns
- Efficiency metrics
- Script library
- Integration templates
- Time saved calculations
"""
    },
    "CLAUDADDY": {
        "role": "Strategic Counsel - Pattern extraction memory",
        "specific_section": """
## CLAUDADDY SPECIFIC DUTIES
- Strategic patterns
- System architecture
- High-value opportunities
- Knowledge crystallization
- 90-day countdown tracking
"""
    }
}

# Function definitions for all assistants
MEMORY_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_memories",
            "description": "Search the shared memory system for relevant information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "instance_filter": {
                        "type": "string",
                        "description": "Optional: Filter by specific instance (e.g., 'CLAUDEFO')",
                        "enum": list(ASSISTANT_IDS.keys()) + ["ALL"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default 10)",
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
            "description": "Store new memory in the shared system",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The exact content to store"
                    },
                    "memory_type": {
                        "type": "string",
                        "description": "Type of memory",
                        "enum": ["breakthrough", "tribal_knowledge", "operational_pattern", "legal_document", "financial_record"]
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Additional tags for categorization"
                    },
                    "expires": {
                        "type": "string",
                        "description": "Optional expiration date (ISO format)"
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
            "description": "Get statistics about stored memories",
            "parameters": {
                "type": "object",
                "properties": {
                    "instance": {
                        "type": "string",
                        "description": "Get stats for specific instance or 'ALL'",
                        "default": "SELF"
                    }
                }
            }
        }
    }
]

def update_assistant(instance_name, assistant_id):
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
            INSTANCE_SPECIFIC_SECTION=custom["specific_section"]
        )
        
        # Update the assistant
        assistant = client.beta.assistants.update(
            assistant_id,
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
                "updated": datetime.now().isoformat(),
                "version": "3.0"
            }
        )
        
        print(f"✅ {instance_name} updated successfully!")
        print(f"   - Instructions: {len(instructions)} chars")
        print(f"   - Functions: {len(MEMORY_FUNCTIONS)}")
        print(f"   - Vector Store: Connected")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update {instance_name}: {e}")
        return False

def main():
    """Update all Claude assistants"""
    print("🧠 UPDATING ALL CLAUDE MEMORY ASSISTANTS")
    print("=" * 50)
    print(f"Vector Store: {VECTOR_STORE_ID}")
    print(f"Assistants to update: {len(ASSISTANT_IDS)}")
    
    # Track results
    success_count = 0
    failed = []
    
    # Update each assistant
    for instance_name, assistant_id in ASSISTANT_IDS.items():
        if update_assistant(instance_name, assistant_id):
            success_count += 1
        else:
            failed.append(instance_name)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 UPDATE SUMMARY")
    print(f"✅ Successfully updated: {success_count}/{len(ASSISTANT_IDS)}")
    
    if failed:
        print(f"❌ Failed updates: {', '.join(failed)}")
    else:
        print("🎉 All assistants updated successfully!")
    
    # Save configuration
    config = {
        "vector_store_id": VECTOR_STORE_ID,
        "assistant_ids": ASSISTANT_IDS,
        "last_updated": datetime.now().isoformat(),
        "update_summary": {
            "total": len(ASSISTANT_IDS),
            "success": success_count,
            "failed": failed
        }
    }
    
    config_file = "/Users/nickbianchi/Downloads/claude_assistants_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Configuration saved to: {config_file}")
    
    # Test instructions
    print("\n🧪 TEST YOUR ASSISTANTS:")
    print("1. Go to: https://platform.openai.com/assistants")
    print("2. Click on any assistant to verify:")
    print("   - Instructions are set correctly")
    print("   - Functions are available")
    print("   - Vector store is connected")
    print("\n3. Test with a simple query:")
    print('   "Search for recent breakthroughs"')
    print('   "Store this memory: Test successful"')

if __name__ == "__main__":
    main()