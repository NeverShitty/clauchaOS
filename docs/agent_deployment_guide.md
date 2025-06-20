# Chitty Stacks Agent Deployment Guide

## Prerequisites

### 1Password CLI Setup
```bash
# Install 1Password CLI
brew install --cask 1password-cli

# Authenticate and configure vault
op signin --account chitty-stacks.1password.com
op vault list
```

### Claude Code CLI Installation
```bash
# Install Claude Code (research preview)
curl -L https://claude.ai/cli/install.sh | bash
claude-code --version
```

### API Key Configuration in 1Password
```bash
# Store OpenAI API key
op item create --category=login \
  --title="OpenAI API" \
  --vault="chitty-stacks-prod" \
  --field="credential,password,$(cat openai_key.txt)"

# Store additional secrets
op item create --category=database \
  --title="PostgreSQL Production" \
  --vault="chitty-stacks-prod" \
  --field="credential,password,postgresql://user:pass@host:5432/db"
```

## Agent Specialization Matrix

| Agent | Model | Use Case | Temperature | Your County Focus |
|-------|-------|----------|-------------|-------------------|
| legal-counsel | GPT-4 Turbo | Motion drafting, case analysis | 0.1 | Illinois civil procedure |
| compliance-auditor | GPT-4 | Regulatory adherence | 0.05 | Evidence rules compliance |
| evidence-validator | GPT-4 Turbo | Blockchain verification | 0.1 | Chain of custody |
| contract-analyzer | GPT-4 | Smart contract security | 0.2 | Legal enforceability |
| property-assessor | GPT-4 Vision | 3D scan analysis | 0.3 | Condition documentation |
| blockchain-optimizer | GPT-4 Turbo | Gas optimization | 0.2 | Transaction efficiency |
| performance-monitor | GPT-3.5 Turbo 16K | System metrics | 0.1 | Infrastructure scaling |
| security-scanner | GPT-4 | Vulnerability assessment | 0.1 | PII protection |

## Execution Examples

### Evidence Chain Analysis
```bash
# Analyze evidence for specific legal case
./chitty-orchestrator.sh evidence "/cases/2024-CV-1234/exhibits/property-scan-20241201.ipfs"

# Expected output:
# - Blockchain hash verification
# - IPFS content integrity check
# - Your County admissibility assessment
# - Chain of custody validation
```

### Smart Contract Security Review
```bash
# Review ChittyPropertyNFT contract
./chitty-orchestrator.sh contract "./packages/blockchain/contracts/ChittyPropertyNFT.sol"

# Agent coordination flow:
# 1. contract-analyzer: Security vulnerability scan
# 2. legal-counsel: Legal enforceability review  
# 3. blockchain-optimizer: Gas optimization recommendations
# 4. Claudaddy: Strategic synthesis
# 5. Claudalyn: Quality assurance validation
```

### Compliance Audit Execution
```bash
# Full system compliance audit
./chitty-orchestrator.sh audit "cook-county-evidence-standards"

# Multi-agent parallel execution:
# - compliance-auditor: Regulatory gap analysis
# - security-scanner: Data protection assessment
# - performance-monitor: System capacity review
# - evidence-validator: Blockchain integrity audit
```

## Coordination Protocols

### Claudaddy (Strategic Orchestrator)
- **Role**: Task decomposition and resource allocation
- **Model**: Claude-3 Opus
- **Responsibilities**:
  - Multi-agent task distribution
  - Conflict resolution between agent outputs
  - Strategic decision synthesis
  - Risk assessment coordination

### Claudalyn (Operational Assistant)  
- **Role**: Execution monitoring and quality assurance
- **Model**: Claude-3 Sonnet
- **Responsibilities**:
  - Agent output validation
  - Report generation oversight
  - Compliance verification
  - Performance monitoring

## Integration Points

### Database Integration
```bash
# Query optimization through performance-monitor
export DATABASE_URL="$(op read 'op://chitty-stacks-prod/postgres/credential')"
./chitty-orchestrator.sh optimize "evidence-retrieval-queries"
```

### Blockchain Integration
```bash
# Smart contract deployment optimization
export ETHEREUM_RPC_URL="$(op read 'op://chitty-stacks-prod/ethereum-rpc/credential')"
./chitty-orchestrator.sh contract "deployment-gas-optimization"
```

### Legal Document Processing
```bash
# Process legal pleadings through legal-counsel agent
./chitty-orchestrator.sh evidence "./legal-docs/motion-summary-judgment.pdf"
```

## Output Specifications

### Evidence Analysis Report Structure
```markdown
# Evidence Analysis Report
- **Blockchain Verification**: Pass/Fail with transaction hashes
- **IPFS Integrity**: Content hash validation results  
- **Your County Compliance**: Admissibility assessment
- **Chain of Custody**: Documentation completeness score
- **Recommendations**: Court-ready action items
```

### Performance Optimization Report
```markdown  
# System Optimization Report
- **Database Query Performance**: Execution time improvements
- **Smart Contract Gas Costs**: Before/after optimization metrics
- **Infrastructure Scaling**: Resource allocation recommendations
- **Security Posture**: Vulnerability remediation priorities
```

## Monitoring & Alerting

### Agent Performance Metrics
```bash
# Monitor agent response times and accuracy
tail -f ./logs/agent-performance.log

# Key metrics:
# - API response latency
# - Token consumption rates  
# - Output quality scores
# - Error rates by agent type
```

### Compliance Dashboard
```bash
# Real-time compliance monitoring
./chitty-orchestrator.sh audit "continuous-monitoring"

# Automated alerts for:
# - Evidence chain breaks
# - Regulatory compliance gaps
# - Security vulnerabilities
# - Performance degradation
```

## Advanced Configuration

### Custom Agent Deployment
```json
{
  "custom-agents": {
    "cook-county-specialist": {
      "model": "gpt-4-turbo",
      "system_prompt": "Expert in Your County Illinois local rules, specialized in real estate litigation and evidence authentication.",
      "temperature": 0.05,
      "max_tokens": 4096
    }
  }
}
```

### Parallel Processing Optimization
```bash
# Configure concurrent agent execution
export MAX_PARALLEL_AGENTS=8
export AGENT_TIMEOUT=300
export RETRY_ATTEMPTS=3
```

This orchestration system provides enterprise-grade multi-agent coordination specifically optimized for legal compliance and operational efficiency within the Chitty Stacks ecosystem.