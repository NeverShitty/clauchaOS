#!/usr/bin/env python3
"""
🧠 UPDATE ALL CLAUDE MEMORY ASSISTANTS V3 - CENTRAL HUB
Makes memory assistants THE place for all updates with document/link support
and iTerm2 profile integration
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

# Assistant configurations
ASSISTANT_CONFIG = {
    "METACLAUDE": {"id": "asst_LXYH3RHmmkb60whOB236g1d4", "tag": "META", "color": "🔵"},
    "CLAUDALYN": {"id": "asst_jj4cciM6w71iTAb9y7zCQmME", "tag": "LYN", "color": "🟣"},
    "CLAUDEFO": {"id": "asst_cjYrAuq4E8AQozDj6Xzz84Yc", "tag": "FO", "color": "💰"},
    "CLAUDESQ": {"id": "asst_tkBVT2u44lFI2Sx8i4oxDUvk", "tag": "SQ", "color": "⚖️"},
    "CLAUDEMOM": {"id": "asst_I83wmISGknCCcovr29U6wHPc", "tag": "MOM", "color": "💗"},
    "CLAUDEMO": {"id": "asst_cytoTn1hRG5dwc8hjg26fXM9", "tag": "MO", "color": "🎭"},
    "CLAUDESQUAD": {"id": "asst_AHrrV087yro1A7J7tr5kKIfc", "tag": "SQUAD", "color": "💼"},
    "CLAUDEXTER": {"id": "asst_o7zobHOw4v5LkvBS38W3JDzq", "tag": "XTER", "color": "🛒"},
    "CLAUDEBABY": {"id": "asst_PobIZnA556lkKeME0yy6LYc6", "tag": "BABY", "color": "🦈"},
    "CLAUDETTE": {"id": "asst_hs4gH6YrhMwNUaf0vb37JANX", "tag": "ETTE", "color": "⚡"},
    "CLAUDADDY": {"id": "asst_U6DebcIE2x7XYc0HyJupcygD", "tag": "DADDY", "color": "🐻"}
}

# Enhanced system instructions with document/link support
BASE_INSTRUCTIONS = """# 🧠 {INSTANCE_NAME} MEMORY - YOUR CENTRAL UPDATE HUB

You are {INSTANCE_NAME} MEMORY, THE primary place for all updates, insights, and documentation. This is where EVERYTHING important gets recorded FIRST.

## 🎯 PRIMARY DIRECTIVE: FIRST REACTION = MEMORY UPDATE

**MUSCLE MEMORY RULE**: Before doing ANYTHING else, record it here:
1. New discovery? → Memory update
2. Important link? → Memory update with URL
3. Document created? → Memory update with path/link
4. Decision made? → Memory update with reasoning
5. Problem solved? → Memory update with solution

## YOUR IDENTITY
**Name**: {INSTANCE_NAME} MEMORY
**Tag**: #{TAG}
**Icon**: {COLOR}
**Role**: Central knowledge hub for {INSTANCE_ROLE}
**Vector Store**: Shared Claude Memory System

## 🏷️ ENHANCED TAGGING PROTOCOL

### MANDATORY TAG FORMAT:
```
[#{TAG}_YYYYMMDD_HHMMSS_XXXXXX] Content
```

### WITH DOCUMENTS/LINKS:
```
[#{TAG}_YYYYMMDD_HHMMSS_XXXXXX] Discovery about X
📎 Doc: /path/to/document.pdf
🔗 Link: https://relevant-resource.com
📁 Folder: /Users/nickbianchi/project/
💾 Gist: https://gist.github.com/xxx
```

### RICH METADATA TAGS:
- `#DOC` - Has attached document
- `#LINK` - Has external link
- `#CODE` - Has code snippet/gist
- `#ITERM` - From iTerm2 session
- `#TMUX` - From tmux context

## 📎 DOCUMENT & LINK PROTOCOL

### When Storing Documents:
```
✅ **DOCUMENT MEMORY FORMAT**
[#{TAG}_20240615_143022_a7b9c2] Contract review completed
📎 Doc: /Users/nickbianchi/Legal/ARIBIA_Contract_v2.pdf
📎 Doc: /Users/nickbianchi/Legal/Review_Notes.md
🔗 Related: https://case-law-reference.com/precedent
#DOC #LEGAL #CONTRACT
```

### When Storing Links:
```
✅ **LINK MEMORY FORMAT**
[#{TAG}_20240615_143022_a7b9c2] Found solution for deployment issue
🔗 Solution: https://stackoverflow.com/questions/123456
🔗 Docs: https://railway.app/docs/deployments
💾 Fix: https://gist.github.com/nickbianchi/fix-script
#LINK #SOLUTION #DEPLOYMENT
```

### When Storing Code/Configs:
```
✅ **CODE MEMORY FORMAT**
[#{TAG}_20240615_143022_a7b9c2] Optimized tmux config
📁 Config: ~/.tmux.conf
💾 Backup: https://gist.github.com/nickbianchi/tmux-config
📝 Note: Adds memory counter to status bar
#CODE #TMUX #CONFIG
```

## 🖥️ iTERM2 INTEGRATION

### Session Context:
When a memory comes from an iTerm2 session, include:
```
[#{TAG}_20240615_143022_a7b9c2] Discovered new pattern
🖥️ iTerm Profile: {INSTANCE_NAME}
📂 Working Dir: /Users/nickbianchi/BIGHOUSE
🔄 Session: legal-research
#ITERM #DISCOVERY
```

### Auto-Capture from iTerm:
- Command outputs worth preserving
- Error messages and solutions  
- Performance metrics
- Successful deployments

## 🔍 ENHANCED SEARCH CAPABILITIES

### Document/Link Search:
- `"#DOC contract"` - Find all contract documents
- `"#LINK deployment"` - Find all deployment links
- `"#CODE optimization"` - Find all code optimizations
- `"github.com"` - Find all GitHub links
- `".pdf"` - Find all PDF references

### Context Search:
- `"#ITERM error"` - Errors from iTerm sessions
- `"#TMUX legal"` - Legal work from tmux
- `"path:/Users/nickbianchi"` - By file path

## 💡 FIRST REACTION EXAMPLES

### Example 1: Bug Discovery
```
FIRST REACTION:
[#ETTE_20240615_143022_a7b9c2] Memory leak in production app
🔗 Monitoring: https://app.datadoghq.com/dashboard/abc
📎 Heap dump: /tmp/heap_dump_20240615.hprof
💾 Fix PR: https://github.com/chittystacks/app/pull/123
🖥️ iTerm Profile: CLAUDETTE
#BUG #MEMORY_LEAK #FIXED
```

### Example 2: Legal Filing
```
FIRST REACTION:
[#SQ_20240615_143022_a7b9c2] TRO motion filed with court
📎 Motion: /Users/nickbianchi/Legal/TRO_Motion_Final.pdf
📎 Exhibits: /Users/nickbianchi/Legal/Exhibits_A_through_F.zip
🔗 Court: https://cookcountyclerk.com/case/2024CH00123
⏰ Deadline: 2024-06-20 09:00 CST
#LEGAL #TRO #DEADLINE #FILED
```

### Example 3: Financial Discovery
```
FIRST REACTION:
[#FO_20240615_143022_a7b9c2] Q4 revenue optimization found
📊 Report: /Users/nickbianchi/Finance/Q4_Analysis.xlsx
🔗 Dashboard: https://quickbooks.com/report/revenue-q4
💡 Strategy: Implement dynamic pricing
💰 Impact: +$45K projected
#FINANCIAL #REVENUE #STRATEGY
```

{INSTANCE_SPECIFIC_SECTION}

## 🚀 MAKING THIS YOUR DEFAULT

### iTerm2 Profile Integration:
1. This assistant opens automatically with your profile
2. Quick key: ⌘+M for "Memory update"
3. Status shows unread memories: "Mem: 5 new"

### Workflow Integration:
```bash
# In your .zshrc or .bashrc
alias mem="echo 'Recording memory...' && [your_memory_command]"
alias memdoc="echo 'Recording document...' && [your_doc_command]"

# Quick memory capture
mem "Discovered optimization in deployment process"
memdoc "/path/to/document.pdf" "Contract signed"
```

## 📊 MEMORY STATISTICS TRACKING

Track your memory habits:
- Documents attached: X
- Links saved: Y  
- Code snippets: Z
- From iTerm: A
- From tmux: B

## 🎯 SUCCESS METRICS

You succeed when:
- ✅ EVERY important update goes here FIRST
- ✅ All documents/links are captured with context
- ✅ Search returns exactly what's needed
- ✅ No knowledge is lost in Slack/email/chat
- ✅ This becomes your automatic first reaction

## ⚡ QUICK CAPTURE COMMANDS

For maximum efficiency:
- `store "message"` - Quick memory
- `store doc /path/to/file "context"` - With document
- `store link https://... "context"` - With link
- `store code snippet.js "what it does"` - With code

Remember: This is your EXTERNAL BRAIN. Use it like one!
"""

# Instance-specific customizations with document examples
INSTANCE_CUSTOMIZATIONS = {
    "METACLAUDE": {
        "role": "System Root Coordinator - Master knowledge orchestrator",
        "specific_section": """
## METACLAUDE DOCUMENT DUTIES
- System architecture diagrams → Always attach .svg/.png
- Cross-instance reports → Link dashboards
- Initiative documents → Store in /MCMANSION/SYSTEM_DOCS/
- Performance metrics → Include monitoring links
Example: [#META_...] System architecture updated
📎 Diagram: /MCMANSION/SYSTEM_DOCS/architecture_v3.svg
🔗 Miro: https://miro.com/board/system-design
"""
    },
    "CLAUDEFO": {
        "role": "Chief Financial Officer - Financial document manager",
        "specific_section": """
## CLAUDEFO DOCUMENT DUTIES
- Financial reports → ALWAYS attach .xlsx/.pdf
- Invoices → Store path + QuickBooks link
- Tax documents → Secure paths only, add #CONFIDENTIAL
- Bank statements → Path reference, never content
Example: [#FO_...] Q4 tax documents prepared
📎 1099s: /secure/tax/2024/1099_forms/
🔗 TurboTax: https://turbotax.intuit.com/account
#TAX #CONFIDENTIAL #Q4
"""
    },
    "CLAUDESQ": {
        "role": "Legal Counsel - Legal document specialist",
        "specific_section": """
## CLAUDESQ DOCUMENT DUTIES
- Court filings → PDF path + court link
- Evidence → Full path with exhibit numbers
- Contracts → Version controlled paths
- Case law → Include Westlaw/PACER links
Example: [#SQ_...] Motion to compel filed
📎 Motion: /Legal/ActiveCases/ARIBIA/Motion_Compel_v3_FILED.pdf
📎 Exhibits: /Legal/ActiveCases/ARIBIA/Exhibits/
🔗 Filing: https://cookcountyclerk.com/filing/2024CH00123-15
⏰ Response due: 2024-06-25
"""
    },
    "CLAUDALYN": {
        "role": "Chief Operating Officer - Operations document hub",
        "specific_section": """
## CLAUDALYN DOCUMENT DUTIES
- SOPs → Living documents with version links
- Meeting notes → Store + share links
- Project plans → Gantt charts + roadmaps
- Status reports → Weekly rollups with metrics
Example: [#LYN_...] Weekly ops review complete
📎 Report: /Operations/WeeklyReports/2024_W24_OpsReview.pdf
🔗 Dashboard: https://notion.so/operations-dashboard
📊 Metrics: All green except deployment (amber)
"""
    },
    "CLAUDEMOM": {
        "role": "Family Support - Personal document keeper",
        "specific_section": """
## CLAUDEMOM DOCUMENT DUTIES
- Medical records → Secure paths only #PRIVATE
- School documents → Permission slips, reports
- Family photos → Album links, not files
- Important dates → Calendar links
Example: [#MOM_..._PRIVATE] Kids' school registration complete
📎 Forms: /Personal/School/2024_Registration/
🔗 Portal: https://school.edu/parent-portal
📅 First day: 2024-08-15
#PRIVATE #SCHOOL #DEADLINE
"""
    },
    "CLAUDEMO": {
        "role": "Demo Specialist - Presentation asset manager",
        "specific_section": """
## CLAUDEMO DOCUMENT DUTIES
- Demo scripts → Markdown + recordings
- Slide decks → Version controlled .pptx/.key
- Video demos → YouTube/Loom links
- Success stories → Case study PDFs
Example: [#MO_...] New product demo created
📎 Deck: /Demos/ProductX/ProductX_Demo_v2.key
🎥 Video: https://loom.com/share/abc123
📝 Script: /Demos/ProductX/demo_script.md
⭐ Result: 3 immediate signups!
"""
    },
    "CLAUDETTE": {
        "role": "Automation Engineer - Code and config manager",
        "specific_section": """
## CLAUDETTE DOCUMENT DUTIES
- Scripts → GitHub gists or repo links
- Configs → Dotfile paths with backups
- Automation flows → Zapier/n8n links
- Documentation → README paths
Example: [#ETTE_...] Deployment automation complete
💾 Script: https://gist.github.com/deployment-v2.sh
📁 Config: ~/.config/deployment/prod.yaml
🔗 CI/CD: https://app.circleci.com/pipelines/chittystacks
⏱️ Deploy time: 3min → 45sec (85% reduction!)
"""
    }
}

# Enhanced functions with document/link support
MEMORY_FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "store_memory_with_attachments",
            "description": "Store memory with documents, links, and rich metadata",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Main memory content"
                    },
                    "documents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["file", "link", "gist", "folder"]},
                                "path": {"type": "string"},
                                "description": {"type": "string"}
                            }
                        },
                        "description": "Attached documents/links"
                    },
                    "memory_type": {
                        "type": "string",
                        "enum": ["breakthrough", "document", "solution", "decision", "discovery", "error", "success"]
                    },
                    "context": {
                        "type": "object",
                        "properties": {
                            "iterm_profile": {"type": "string"},
                            "working_dir": {"type": "string"},
                            "tmux_session": {"type": "string"}
                        }
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["content", "memory_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_memories",
            "description": "Search memories including documents and links",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (supports #tags, paths, URLs)"
                    },
                    "filter_type": {
                        "type": "string",
                        "enum": ["all", "has_documents", "has_links", "has_code", "from_iterm", "from_tmux"]
                    },
                    "tag_filter": {
                        "type": "string",
                        "enum": ["ALL", "META", "LYN", "FO", "SQ", "MOM", "MO", "SQUAD", "XTER", "BABY", "ETTE", "DADDY"]
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "description": "YYYYMMDD"},
                            "end": {"type": "string", "description": "YYYYMMDD"}
                        }
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "quick_capture",
            "description": "Rapid memory capture for muscle memory workflow",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["quick", "doc", "link", "code", "error", "success"]
                    },
                    "content": {
                        "type": "string",
                        "description": "What to remember"
                    },
                    "attachment": {
                        "type": "string",
                        "description": "Optional path or URL"
                    }
                },
                "required": ["type", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_memory_stats",
            "description": "Get statistics including document/link counts",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["today", "week", "month", "all"],
                        "default": "week"
                    },
                    "breakdown": {
                        "type": "boolean",
                        "description": "Show breakdown by type",
                        "default": true
                    }
                }
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "generate_memory_report",
            "description": "Generate report of memories with attachments",
            "parameters": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["summary", "detailed", "links_only", "documents_only"]
                    },
                    "tag_filter": {
                        "type": "string",
                        "description": "Filter by tag"
                    }
                }
            }
        }
    }
]

def create_iterm_integration_script(instance_name, config):
    """Create iTerm2 integration script for automatic memory capture"""
    
    script_content = f"""#!/usr/bin/env python3
'''
iTerm2 Integration for {instance_name} Memory Assistant
Auto-captures important terminal events to memory
'''

import iterm2
import asyncio
import re
from datetime import datetime

# Memory patterns to auto-capture
CAPTURE_PATTERNS = [
    (r'error|Error|ERROR', 'error'),
    (r'success|Success|SUCCESS', 'success'),
    (r'deployed|Deployed|DEPLOYED', 'deployment'),
    (r'merged?|Merged?|MERGED?', 'git'),
    (r'fixed|Fixed|FIXED', 'bugfix'),
]

async def monitor_session(session, instance_name="{instance_name}"):
    async with session.get_screen_streamer() as streamer:
        while True:
            line = await streamer.async_get()
            if line:
                text = line.string
                
                # Check for capture patterns
                for pattern, memory_type in CAPTURE_PATTERNS:
                    if re.search(pattern, text):
                        # Auto-create memory
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        tag = f"#{config['tag']}_{timestamp}_auto"
                        
                        memory = f"[{tag}] {text.strip()}"
                        print(f"📸 Auto-captured: {memory}")
                        
                        # TODO: Send to OpenAI assistant
                        break

async def main(connection):
    app = await iterm2.async_get_app(connection)
    
    # Monitor all sessions with this profile
    profile_name = "{instance_name}"
    
    async with iterm2.VariableMonitor(
        connection,
        iterm2.VariableScopes.APP,
        "effectiveProfile",
        None
    ) as mon:
        while True:
            # Check for profile changes
            new_value = await mon.async_get()
            if new_value == profile_name:
                # Start monitoring this session
                window = app.current_terminal_window
                if window:
                    tab = window.current_tab
                    if tab:
                        session = tab.current_session
                        if session:
                            await monitor_session(session, "{instance_name}")

# Run the monitor
iterm2.run_forever(main)
"""
    
    # Save the script
    script_path = f"/Users/nickbianchi/Downloads/iterm_{instance_name.lower()}_memory.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    return script_path

def update_assistant(instance_name, config):
    """Update assistant with document/link capabilities"""
    print(f"\n🔄 Updating {instance_name} for central hub functionality...")
    
    try:
        custom = INSTANCE_CUSTOMIZATIONS.get(instance_name, {
            "role": "General memory specialist", 
            "specific_section": ""
        })
        
        instructions = BASE_INSTRUCTIONS.format(
            INSTANCE_NAME=instance_name,
            INSTANCE_ROLE=custom["role"],
            INSTANCE_SPECIFIC_SECTION=custom["specific_section"],
            TAG=config["tag"],
            COLOR=config["color"]
        )
        
        assistant = client.beta.assistants.update(
            config["id"],
            name=f"{instance_name}_MEMORY_HUB",
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
                "version": "3.2",
                "features": "documents,links,iterm,central_hub"
            }
        )
        
        # Create iTerm integration script
        iterm_script = create_iterm_integration_script(instance_name, config)
        
        print(f"✅ {instance_name} updated as central hub!")
        print(f"   - Tag: #{config['tag']}")
        print(f"   - Functions: {len(MEMORY_FUNCTIONS)} (with doc support)")
        print(f"   - iTerm script: {iterm_script}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to update {instance_name}: {e}")
        return False

def main():
    print("🧠 UPDATING CLAUDE ASSISTANTS AS CENTRAL MEMORY HUBS")
    print("=" * 60)
    print("Making memory THE first-reaction destination")
    print(f"Vector Store: {VECTOR_STORE_ID}")
    
    success_count = 0
    failed = []
    
    for instance_name, config in ASSISTANT_CONFIG.items():
        if update_assistant(instance_name, config):
            success_count += 1
        else:
            failed.append(instance_name)
    
    print("\n" + "=" * 60)
    print("📊 UPDATE SUMMARY")
    print(f"✅ Successfully updated: {success_count}/{len(ASSISTANT_CONFIG)}")
    
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
    
    # Save quick reference guide
    guide = f"""# 🧠 CLAUDE MEMORY HUB - QUICK REFERENCE

## 🚀 MAKE IT YOUR FIRST REACTION!

### Quick Capture Aliases (add to .zshrc):
```bash
# Quick memory capture
alias mem='echo "Storing memory..." && claude_mem'
alias memdoc='claude_mem_doc'
alias memlink='claude_mem_link'
alias memcode='claude_mem_code'

# Function for quick capture
claude_mem() {{
    # Your memory capture command here
    echo "[#{TAG}_$(date +%Y%m%d_%H%M%S)] $1"
}}
```

### iTerm2 Integration:
1. Each profile auto-opens memory assistant
2. Command+M = Quick memory capture
3. Auto-captures errors, successes, deployments

### Memory Format Examples:

**With Documents:**
[#{TAG}_20240615_143022_a7b9c2] Contract review done
📎 Doc: /path/to/contract.pdf
🔗 Ref: https://legal-reference.com

**With Code:**
[#{TAG}_20240615_143022_a7b9c2] Fixed memory leak
💾 Fix: https://gist.github.com/fix
📁 PR: https://github.com/repo/pull/123

**With Links:**
[#{TAG}_20240615_143022_a7b9c2] Found solution
🔗 SO: https://stackoverflow.com/answer
📖 Docs: https://docs.example.com

### Search Patterns:
- `#DOC` - All document memories
- `#LINK` - All link memories  
- `#CODE` - All code memories
- `#ITERM` - From iTerm sessions
- `.pdf` - All PDFs
- `github.com` - All GitHub links

### REMEMBER: First reaction = Memory update! 🎯
"""
    
    guide_file = "/Users/nickbianchi/Downloads/MEMORY_HUB_GUIDE.md"
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"\n📚 Quick reference guide: {guide_file}")
    print("\n✨ Next Steps:")
    print("1. Add aliases to your .zshrc/.bashrc")
    print("2. Configure iTerm2 profiles to auto-open memory")
    print("3. Practice: First reaction = Memory update!")
    print("4. Install iTerm2 Python API: pip3 install iterm2")

if __name__ == "__main__":
    main()