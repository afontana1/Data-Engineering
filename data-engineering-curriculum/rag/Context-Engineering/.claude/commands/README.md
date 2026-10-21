# Context Engineering AgenticOS

> “We shape our tools and thereafter our tools shape us.” — [Marshall McLuhan](https://www.goodreads.com/quotes/350791-we-become-what-we-behold-we-shape-our-tools-and)


## [Anthropic Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) | [Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
## Overview

This directory contains a growing library of modular, customizable, and extendable agents and harnesses embedded as slash commands, forming an Agentic Operating System (AgenticOS) designed for enhancing the capabilities of [Claude Code](https://www.anthropic.com/claude-code) and other frontier systems, such as [OpenCode](https://opencode.ai/), [Amp](https://sourcegraph.com/amp), [Kiro](https://kiro.dev/), [Codex](https://openai.com/codex/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), and more. Each agent implements a standardized workflow with consistent structure, enabling sophisticated context engineering across various domains.

The operating system provides a selection of agents that serve as scaffolds for context-driven AI workflows, leveraging the latest research in cognitive tools, neural field theory, symbolic mechanisms, and quantum semantics to create more capable, interpretable, and predictable AI interactions.

```
/command Q="query" param="value" context=@file.md ...
      │
      ▼
[context]→[specialized_phase_1]→[specialized_phase_2]→...→[synthesis]→[audit/log]
        ↑___________________feedback/CI___________________|
```

## AgenticOS Library (Under Construction)

| Command | Purpose | Usage Example |
|---------|---------|---------------|
| [`alignment.agent.md`](./alignment.agent.md) | AI safety/alignment evaluation | `/alignment Q="prompt injection" model="claude-3"` |
| [`cli.agent.md`](./cli.agent.md) | Terminal workflow automation | `/cli "find all .log files" alias=logscan` |
| [`comms.agent.md`](./comms.agent.md) | Stakeholder communications | `/comms Q="major outage" audience="internal" type="crisis"` |
| [`data.agent.md`](./data.agent.md) | Data transformation and validation | `/data input="data.csv" op="validate" schema=@schema.json` |
| [`deploy.agent.md`](./deploy.agent.md) | Deployment automation | `/deploy target="app" env="staging" version="1.2.0"` |
| [`diligence.agent.md`](./diligence.agent.md) | Due diligence workflows | `/diligence target="acquisition" scope="tech" depth="full"` |
| [`doc.agent.md`](./doc.agent.md) | Documentation generation | `/doc target="api" format="markdown" scope="public"` |
| [`legal.agent.md`](./legal.agent.md) | Legal research and analysis | `/legal Q="contract review" jurisdiction="US" type="SaaS"` |
| [`lit.agent.md`](./lit.agent.md) | Literature review and writing | `/literature Q="PEMF effect" type="review" years=3` |
| [`marketing.agent.md`](./marketing.agent.md) | Marketing strategy and campaigns | `/marketing goal="lead gen" channel="email" vertical="SaaS"` |
| [`meta.agent.md`](./meta.agent.md) | Meta-level agent coordination | `/meta agents="research,data" task="market analysis"` |
| [`monitor.agent.md`](./monitor.agent.md) | System/service monitoring | `/monitor service="api" period="24h" alert=true` |
| [`optimize.agent.md`](./optimize.agent.md) | Code and process optimization | `/optimize target="foo.py" area="speed" mode="aggressive"` |
| [`research.agent.md`](./research.agent.md) | Research workflows | `/research topic="quantum computing" depth="technical"` |
| [`security.agent.md`](./security.agent.md) | Security analysis | `/security target="app" scope="full" report="detailed"` |
| [`test.agent.md`](./test.agent.md) | Test generation and execution | `/test suite="integration" mutate=true report=summary"` |

## Command Structure

Each command agent follows a standardized system prompt format with these key components:

```
/command.agent.md
├── [meta]            # Protocol version, runtime, namespaces
├── [instructions]    # Agent rules, invocation, argument mapping
├── [ascii_diagrams]  # File tree, workflow, phase flow
├── [context_schema]  # JSON/YAML: domain-specific fields
├── [workflow]        # YAML: specialized workflow phases
├── [tools]           # YAML: tool registry & control
├── [recursion]       # Python: feedback/revision loop
└── [examples]        # Markdown: sample runs, logs, usage
```

### Meta Section

The meta section defines protocol compatibility and runtime parameters:

```json
{
  "agent_protocol_version": "2.0.0",
  "prompt_style": "multimodal-markdown",
  "intended_runtime": ["Anthropic Claude", "OpenAI GPT-4o", "Agentic System"],
  "schema_compatibility": ["json", "yaml", "markdown", "python", "shell"],
  "namespaces": ["project", "user", "team", "field"],
  "audit_log": true,
  "last_updated": "2025-07-10",
  "prompt_goal": "Purpose statement for the command harness"
}
```

### Workflow Phases

Each command implements domain-specific workflow phases that systematically process inputs and generate outputs:

```yaml
phases:
  - context_mapping:
      description: |
        Parse input arguments, clarify goals, establish context.
      output: Context table, argument log, clarifications.
  
  - domain_specific_phase_1:
      description: |
        Specialized processing for the domain.
      output: Domain-specific artifacts and logs.
  
  - domain_specific_phase_2:
      description: |
        Additional domain processing.
      output: Secondary artifacts and analysis.
  
  - synthesis_phase:
      description: |
        Integrate findings and generate recommendations.
      output: Synthesis report, action items, open questions.
  
  - audit_logging:
      description: |
        Document process, decisions, and version history.
      output: Audit log, version history, unresolved issues.
```

### Tool Registry

Commands declare tool access explicitly for each phase:

```yaml
tools:
  - id: domain_specific_tool
    type: internal
    description: Tool purpose and functionality.
    input_schema: { param1: string, param2: string }
    output_schema: { result: list, metadata: dict }
    call: { protocol: /tool.function{ param1=<param1>, param2=<param2> } }
    phases: [domain_specific_phase_1, domain_specific_phase_2]
    examples: [{ input: {...}, output: {...} }]
  - id: github_issue
    type: external
    description: Create or update issues in a GitHub repo for agent workflow failures or meta-level tracking.
    input_schema: { repo: string, title: string, body: string }
    output_schema: { issue_url: string, status: string }
    endpoint: "https://api.github.com/repos/{repo}/issues"
    auth: "api_token"
    call: { protocol: /call_api{ endpoint=<endpoint>, params={repo, title, body} } }
    phases: [error_feedback_handling, audit_meta_logging]
    examples:
      - input: { repo: "team/agent-infra", title: "Meta-agent error", body: "Dependency loop detected" }
        output: { issue_url: "https://github.com/team/agent-infra/issues/45", status: "created" }
```

### Recursion Loop

Commands implement recursive self-improvement via feedback loops:

```python
def agent_cycle(context, state=None, audit_log=None, depth=0, max_depth=4):
    # Execute each phase sequentially
    for phase in workflow_phases:
        state[phase] = run_phase(phase, context, state)
    
    # Check if revision is needed and recurse if appropriate
    if depth < max_depth and needs_revision(state):
        revised_context, reason = query_for_revision(context, state)
        audit_log.append({'revision': phase, 'reason': reason, 'timestamp': get_time()})
        return agent_cycle(revised_context, state, audit_log, depth + 1, max_depth)
    else:
        state['audit_log'] = audit_log
        return state
```

## Usage Patterns

### Basic Invocation

Commands follow the slash command pattern with named arguments:

```bash
/command Q="main question" param1="value1" param2="value2"
```

### File References

Include file contents in commands using the `@` prefix:

```bash
/legal Q="contract review" context=@agreement.md
```

### Bash Command Integration

Execute bash commands and include their output using the `!` prefix:

```
/cli "commit changes" context="!git status"
```

## Theoretical Foundation

This AgenticOS operationalize several key concepts from the Context Engineering framework:

### Progressive Complexity Paradigm

```
atoms → molecules → cells → organs → neural systems → neural fields
  │        │         │        │             │              │
single    few-     memory/   multi-    cognitive tools   fields +
prompt    shot     agents    agents    prompt programs   persistence
```

### Emergent Symbolic Mechanisms (Princeton ICML, 2025)

Three-stage symbolic processing architecture:

1. **Symbol Abstraction Heads (Early Layers)** - Convert tokens to abstract variables
2. **Symbolic Induction Heads (Intermediate Layers)** - Perform sequence induction over abstract variables
3. **Retrieval Heads (Later Layers)** - Predict next token by retrieving values associated with abstract variables

### Cognitive Tools Architecture (IBM Zurich, 2025)

Structured prompt templates that encapsulate reasoning operations:

```python
def cognitive_tool_template():
    """IBM Zurich cognitive tool structure"""
    return {
        "understand": "Identify main concepts and requirements",
        "extract": "Extract relevant information from context", 
        "highlight": "Identify key properties and relationships",
        "apply": "Apply appropriate reasoning techniques",
        "validate": "Verify reasoning steps and conclusions"
    }
```

### Quantum Semantic Framework (Indiana University, 2025)

Observer-dependent meaning actualization framework where semantic interpretation emerges through dynamic interaction between expressions and interpretive contexts.

## Integration with Claude Code CLI

These commands work seamlessly with the Claude Code CLI following the Anthropic [slash command documentation](https://docs.anthropic.com/en/docs/claude-code/slash-commands).

Key features:
- **Custom command execution** via standardized interface
- **Namespacing** via subdirectories (e.g., `/domain:command`)
- **Arguments** via the `$ARGUMENTS` placeholder
- **Bash integration** using the `!` prefix
- **File references** using the `@` prefix

## Creating Custom Commands

To create your own command agent:

1. **Copy an existing template** from this directory
2. **Modify domain-specific sections** for your use case
3. **Define specialized workflow phases** tailored to your domain
4. **Register appropriate tools** for each phase
5. **Include helpful examples** and audit logging

Follow this naming convention:
- Project-specific commands: `.claude/commands/your-command.agent.md`
- Personal commands: `~/.claude/commands/your-command.agent.md`

## Implementation Strategy

These commands follow key principles:

1. **Layered Approach** - Building from foundations to advanced integration
2. **Practical Focus** - Ensuring theory has practical implementation
3. **Modular Design** - Creating composable, recombinant components
4. **Progressive Complexity** - Starting simple, adding sophistication incrementally
5. **Integration Emphasis** - Focusing on component interactions
6. **Self-Improvement** - Building systems that enhance themselves
7. **Transparency** - Maintaining understandability despite complexity
8. **Collaboration** - Designing for effective human-AI partnership
9. **Modal Flexibility** - Supporting unified understanding across modalities

## Advanced Patterns

### Field-Theoretic Dynamics

Commands can implement attractor dynamics and field resonance:

```python
def attractor_field_dynamics():
    """Shanghai AI Lab field theory framework"""
    return {
        "attractor_detection": {
            "identify_basins": "Map stable behavioral patterns",
            "measure_depth": "Quantify attractor strength",
            "track_evolution": "Monitor attractor development"
        },
        "field_resonance": {
            "resonance_patterns": "Identify coherent field oscillations",
            "coupling_strength": "Measure component interactions",
            "phase_relationships": "Track synchronization patterns"
        },
        "symbolic_residue": {
            "residue_tracking": "Monitor persistent information",
            "decay_analysis": "Study information degradation",
            "transfer_mechanisms": "Understand residue propagation"
        }
    }
```

### Memory-Reasoning Synergy

Commands can implement memory consolidation with reasoning:

```python
def mem1_consolidation():
    """Singapore-MIT MEM1 memory-reasoning synergy"""
    return {
        "analysis_stage": {
            "interaction_patterns": "Analyze memory-reasoning interactions",
            "efficiency_metrics": "Measure memory utilization",
            "bottleneck_identification": "Find performance constraints"
        },
        "consolidation_stage": {
            "selective_compression": "Compress low-value information",
            "insight_extraction": "Extract high-value patterns",
            "relationship_mapping": "Map memory element relationships"
        },
        "optimization_stage": {
            "memory_pruning": "Remove redundant information",
            "reasoning_acceleration": "Optimize for reasoning speed",
            "synergy_enhancement": "Improve memory-reasoning integration"
        }
    }
```

## Contributing

When creating new command agents:

1. Follow the established structural patterns
2. Include comprehensive documentation and examples
3. Implement appropriate audit logging and versioning
4. Test across different runtime environments
5. Consider integration with existing commands

## Future Directions

This directory will expand to include:
- Additional domain-specific command agents
- Enhanced integration with external tools and APIs
- More sophisticated feedback and recursive improvement mechanisms
- Cross-command coordination frameworks
- Advanced field-theoretic and quantum semantic implementations
- Meta-recursive frameworks for system-level emergence

---

*For more information on Context Engineering concepts and implementations, see the main [Context Engineering repository](https://github.com/davidkimai/Context-Engineering).*
