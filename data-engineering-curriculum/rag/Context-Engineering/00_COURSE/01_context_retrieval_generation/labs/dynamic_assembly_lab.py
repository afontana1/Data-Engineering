# Context Engineering Course - Module 01: Context Retrieval & Generation
# Lab: Dynamic Assembly - Context Orchestration
# 
# Learning Objectives:
# 1. Understand mathematical formalization of context assembly: C = A(c₁, c₂, ..., cₙ)
# 2. Implement practical assembly functions with optimization
# 3. Build component integration patterns for different use cases
# 4. Measure and evaluate assembly quality and performance
# 5. Create reusable assembly patterns for production systems

"""
Dynamic Assembly Lab: Context Orchestration
==========================================

Context Engineering Course - Module 01 Laboratory
Based on principles from Context Engineering Survey (arXiv:2507.13334)

This lab offers practical, hands-on experience with dynamic context assembly
and orchestration techniques, essential for scalable and adaptable AI systems.
Participants will explore mathematical formalisms, implement optimization-driven
assembly functions, and integrate components into robust, reusable patterns.

Learning Objectives:
- Understand mathematical formalization of context assembly: C = A(c₁, c₂, ..., cₙ)
- Implement practical assembly functions with optimization strategies
- Build component integration patterns for diverse use cases
- Measure and evaluate context assembly quality and performance
- Create reusable assembly patterns for production-grade systems

Usage:
    # For Jupyter/Colab
    %run dynamic_assembly_lab.py
    
    # For direct execution
    python dynamic_assembly_lab.py
    
    # For import
    from dynamic_assembly_lab import *
"""

import json
import time
import math
import random
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict
import hashlib

# ============================================================================
# PART 1: MATHEMATICAL FOUNDATIONS
# ============================================================================

class ComponentType(Enum):
    """Context component types following the formalization C = A(c₁, c₂, ..., c₆)"""
    INSTRUCTIONS = "c_instr"    # c₁: System instructions and rules
    KNOWLEDGE = "c_know"        # c₂: External knowledge (RAG, KG)
    TOOLS = "c_tools"          # c₃: Tool definitions and signatures
    MEMORY = "c_mem"           # c₄: Persistent memory information
    STATE = "c_state"          # c₅: Dynamic state (user, world, multi-agent)
    QUERY = "c_query"          # c₆: Immediate user request

@dataclass
class ContextComponent:
    """Individual context component with metadata and optimization info"""
    component_type: ComponentType
    content: str
    priority: float = 1.0
    token_count: int = 0
    relevance_score: float = 0.0
    source: str = ""
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.token_count == 0:
            # Simple token estimation (words * 1.3 approximation)
            self.token_count = max(1, int(len(self.content.split()) * 1.3))

@dataclass
class AssemblyConstraints:
    """Constraints for context assembly optimization"""
    max_tokens: int = 4000
    min_relevance: float = 0.1
    require_all_types: bool = False
    priority_weights: Dict[ComponentType, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.priority_weights:
            # Default priority weights
            self.priority_weights = {
                ComponentType.QUERY: 1.0,
                ComponentType.INSTRUCTIONS: 0.9,
                ComponentType.KNOWLEDGE: 0.8,
                ComponentType.TOOLS: 0.7,
                ComponentType.STATE: 0.6,
                ComponentType.MEMORY: 0.5
            }

class ContextAssembler:
    """
    Core context assembly engine implementing C = A(c₁, c₂, ..., cₙ)
    
    Mathematical Foundation:
    - Context: C = Assembly(instructions, knowledge, tools, memory, state, query)
    - Optimization: A* = arg max_A E[Reward(LLM(C), target)]
    - Constraints: |C| ≤ max_tokens, relevance ≥ min_threshold
    """
    
    def __init__(self, constraints: AssemblyConstraints = None):
        self.constraints = constraints or AssemblyConstraints()
        self.components: List[ContextComponent] = []
        self.assembly_history: List[Dict] = []
        
    def add_component(self, component: ContextComponent) -> None:
        """Add a component to the assembly pool"""
        self.components.append(component)
        
    def add_components(self, components: List[ContextComponent]) -> None:
        """Add multiple components efficiently"""
        self.components.extend(components)
    
    def calculate_mutual_information(self, comp1: ContextComponent, comp2: ContextComponent) -> float:
        """
        Approximate mutual information between components
        I(c_i; c_j) for semantic coherence optimization
        """
        # Simple approximation based on content overlap
        words1 = set(comp1.content.lower().split())
        words2 = set(comp2.content.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        # Jaccard similarity as MI approximation
        jaccard = len(intersection) / len(union) if union else 0.0
        return jaccard
    
    def calculate_component_utility(self, component: ContextComponent, 
                                  selected_components: List[ContextComponent]) -> float:
        """
        Calculate utility score for component selection
        U(c_i) = relevance * priority * novelty_bonus - redundancy_penalty
        """
        base_utility = component.relevance_score * component.priority
        
        # Novelty bonus (higher for unique information)
        novelty_bonus = 1.0
        redundancy_penalty = 0.0
        
        for selected in selected_components:
            mi = self.calculate_mutual_information(component, selected)
            redundancy_penalty += mi * 0.3  # Penalty for redundant information
            
        utility = base_utility * novelty_bonus - redundancy_penalty
        return max(0.0, utility)
    
    def greedy_assembly(self, target_query: str = "") -> Dict[str, Any]:
        """
        Greedy assembly algorithm with utility optimization
        """
        selected_components = []
        total_tokens = 0
        component_groups = defaultdict(list)
        
        # Group components by type
        for comp in self.components:
            if comp.relevance_score >= self.constraints.min_relevance:
                component_groups[comp.component_type].append(comp)
        
        # Sort components within each group by utility
        for comp_type in component_groups:
            component_groups[comp_type].sort(
                key=lambda x: self.calculate_component_utility(x, selected_components),
                reverse=True
            )
        
        # Assembly process - ensure query is always included
        assembly_order = [
            ComponentType.QUERY,
            ComponentType.INSTRUCTIONS, 
            ComponentType.KNOWLEDGE,
            ComponentType.TOOLS,
            ComponentType.STATE,
            ComponentType.MEMORY
        ]
        
        for comp_type in assembly_order:
            if comp_type not in component_groups:
                continue
                
            for component in component_groups[comp_type]:
                if total_tokens + component.token_count <= self.constraints.max_tokens:
                    utility = self.calculate_component_utility(component, selected_components)
                    if utility > 0.1:  # Minimum utility threshold
                        selected_components.append(component)
                        total_tokens += component.token_count
                
        return {
            'components': selected_components,
            'total_tokens': total_tokens,
            'efficiency_ratio': len(selected_components) / len(self.components) if self.components else 0,
            'token_utilization': total_tokens / self.constraints.max_tokens
        }
    
    def optimal_assembly_dp(self, target_query: str = "") -> Dict[str, Any]:
        """
        Dynamic programming approach for optimal component selection
        Approximation of the optimization problem with polynomial complexity
        """
        # Filter eligible components
        eligible = [c for c in self.components if c.relevance_score >= self.constraints.min_relevance]
        n = len(eligible)
        max_tokens = self.constraints.max_tokens
        
        if n == 0:
            return {'components': [], 'total_tokens': 0, 'efficiency_ratio': 0, 'token_utilization': 0}
        
        # DP table: dp[i][w] = max utility using first i components with ≤ w tokens
        dp = [[0.0 for _ in range(max_tokens + 1)] for _ in range(n + 1)]
        keep = [[False for _ in range(max_tokens + 1)] for _ in range(n + 1)]
        
        # Fill DP table
        for i in range(1, n + 1):
            component = eligible[i - 1]
            tokens = component.token_count
            utility = component.relevance_score * component.priority
            
            for w in range(max_tokens + 1):
                # Don't take current component
                dp[i][w] = dp[i-1][w]
                
                # Take current component if possible
                if tokens <= w:
                    take_utility = dp[i-1][w-tokens] + utility
                    if take_utility > dp[i][w]:
                        dp[i][w] = take_utility
                        keep[i][w] = True
        
        # Backtrack to find selected components
        selected_components = []
        w = max_tokens
        total_tokens = 0
        
        for i in range(n, 0, -1):
            if keep[i][w]:
                selected_components.append(eligible[i-1])
                total_tokens += eligible[i-1].token_count
                w -= eligible[i-1].token_count
        
        selected_components.reverse()
        
        return {
            'components': selected_components,
            'total_tokens': total_tokens,
            'efficiency_ratio': len(selected_components) / len(self.components) if self.components else 0,
            'token_utilization': total_tokens / self.constraints.max_tokens,
            'optimal_utility': dp[n][max_tokens]
        }

# ============================================================================
# PART 2: ASSEMBLY PATTERNS AND STRATEGIES
# ============================================================================

class AssemblyStrategy(Enum):
    """Different assembly strategies for various use cases"""
    GREEDY = "greedy"
    OPTIMAL_DP = "optimal_dp"
    BALANCED = "balanced"
    RELEVANCE_FIRST = "relevance_first"
    DIVERSITY_MAXIMIZING = "diversity_maximizing"

class ContextOrchestrator:
    """
    High-level orchestration layer for context assembly
    Implements various assembly strategies and patterns
    """
    
    def __init__(self):
        self.assemblers: Dict[str, ContextAssembler] = {}
        self.patterns: Dict[str, Callable] = {}
        self._register_default_patterns()
    
    def _register_default_patterns(self):
        """Register default assembly patterns"""
        self.patterns.update({
            'rag_pipeline': self._rag_pipeline_pattern,
            'agent_workflow': self._agent_workflow_pattern,
            'research_assistant': self._research_assistant_pattern,
            'code_generation': self._code_generation_pattern,
            'multi_modal': self._multi_modal_pattern
        })
    
    def create_assembler(self, name: str, constraints: AssemblyConstraints = None) -> ContextAssembler:
        """Create and register a new assembler"""
        assembler = ContextAssembler(constraints)
        self.assemblers[name] = assembler
        return assembler
    
    def _rag_pipeline_pattern(self, query: str, knowledge_docs: List[str], 
                            instructions: str = "") -> List[ContextComponent]:
        """RAG pipeline assembly pattern"""
        components = []
        
        # Query component (highest priority)
        components.append(ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"User Query: {query}",
            priority=1.0,
            relevance_score=1.0,
            source="user_input"
        ))
        
        # Instructions
        if instructions:
            components.append(ContextComponent(
                component_type=ComponentType.INSTRUCTIONS,
                content=instructions,
                priority=0.9,
                relevance_score=0.9,
                source="system"
            ))
        
        # Knowledge documents
        for i, doc in enumerate(knowledge_docs):
            relevance = 0.8 - (i * 0.1)  # Decreasing relevance
            components.append(ContextComponent(
                component_type=ComponentType.KNOWLEDGE,
                content=doc,
                priority=0.8,
                relevance_score=max(0.1, relevance),
                source=f"retrieval_doc_{i}"
            ))
        
        return components
    
    def _agent_workflow_pattern(self, task: str, available_tools: List[Dict],
                              agent_state: Dict, memory: List[str] = None) -> List[ContextComponent]:
        """Agent workflow assembly pattern"""
        components = []
        
        # Task/Query
        components.append(ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Task: {task}",
            priority=1.0,
            relevance_score=1.0
        ))
        
        # Agent instructions
        agent_instructions = """
        You are an AI agent capable of using tools to complete tasks.
        Follow these steps:
        1. Analyze the task requirements
        2. Select appropriate tools
        3. Execute actions systematically
        4. Verify results and adjust if needed
        """
        components.append(ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=agent_instructions,
            priority=0.9,
            relevance_score=0.9
        ))
        
        # Available tools
        tools_content = "Available Tools:\n" + "\n".join([
            f"- {tool['name']}: {tool.get('description', '')}" 
            for tool in available_tools
        ])
        components.append(ContextComponent(
            component_type=ComponentType.TOOLS,
            content=tools_content,
            priority=0.8,
            relevance_score=0.8
        ))
        
        # Agent state
        state_content = f"Current State: {json.dumps(agent_state, indent=2)}"
        components.append(ContextComponent(
            component_type=ComponentType.STATE,
            content=state_content,
            priority=0.7,
            relevance_score=0.7
        ))
        
        # Memory (if available)
        if memory:
            memory_content = "Previous Context:\n" + "\n".join(memory[-3:])  # Last 3 items
            components.append(ContextComponent(
                component_type=ComponentType.MEMORY,
                content=memory_content,
                priority=0.6,
                relevance_score=0.6
            ))
        
        return components
    
    def _research_assistant_pattern(self, research_query: str, papers: List[Dict],
                                  research_context: str = "") -> List[ContextComponent]:
        """Research assistant assembly pattern"""
        components = []
        
        # Research query
        components.append(ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Research Query: {research_query}",
            priority=1.0,
            relevance_score=1.0
        ))
        
        # Research methodology instructions
        research_instructions = """
        You are a research assistant. Provide:
        1. Comprehensive analysis of relevant literature
        2. Synthesis of key findings and insights
        3. Identification of research gaps
        4. Evidence-based conclusions
        5. Proper citations and references
        """
        components.append(ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=research_instructions,
            priority=0.9,
            relevance_score=0.9
        ))
        
        # Research papers as knowledge
        for i, paper in enumerate(papers):
            paper_content = f"Title: {paper.get('title', '')}\n"
            paper_content += f"Abstract: {paper.get('abstract', '')}\n"
            paper_content += f"Key Findings: {paper.get('key_findings', '')}"
            
            components.append(ContextComponent(
                component_type=ComponentType.KNOWLEDGE,
                content=paper_content,
                priority=0.8,
                relevance_score=0.8 - (i * 0.05),  # Slightly decreasing relevance
                source=f"paper_{i}"
            ))
        
        # Research context
        if research_context:
            components.append(ContextComponent(
                component_type=ComponentType.STATE,
                content=f"Research Context: {research_context}",
                priority=0.7,
                relevance_score=0.7
            ))
        
        return components
    
    def _code_generation_pattern(self, coding_request: str, existing_code: str = "",
                               documentation: str = "", requirements: List[str] = None) -> List[ContextComponent]:
        """Code generation assembly pattern"""
        components = []
        
        # Coding request
        components.append(ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Coding Request: {coding_request}",
            priority=1.0,
            relevance_score=1.0
        ))
        
        # Coding instructions
        coding_instructions = """
        You are an expert programmer. Provide:
        1. Clean, well-documented code
        2. Following best practices and conventions
        3. Proper error handling
        4. Comprehensive comments
        5. Testing considerations
        """
        components.append(ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=coding_instructions,
            priority=0.9,
            relevance_score=0.9
        ))
        
        # Existing code context
        if existing_code:
            components.append(ContextComponent(
                component_type=ComponentType.STATE,
                content=f"Existing Code:\n{existing_code}",
                priority=0.8,
                relevance_score=0.8
            ))
        
        # Documentation
        if documentation:
            components.append(ContextComponent(
                component_type=ComponentType.KNOWLEDGE,
                content=f"Documentation:\n{documentation}",
                priority=0.7,
                relevance_score=0.7
            ))
        
        # Requirements
        if requirements:
            req_content = "Requirements:\n" + "\n".join([f"- {req}" for req in requirements])
            components.append(ContextComponent(
                component_type=ComponentType.KNOWLEDGE,
                content=req_content,
                priority=0.8,
                relevance_score=0.8
            ))
        
        return components
    
    def _multi_modal_pattern(self, query: str, text_content: str = "",
                           image_descriptions: List[str] = None, 
                           audio_transcripts: List[str] = None) -> List[ContextComponent]:
        """Multi-modal assembly pattern"""
        components = []
        
        # Query
        components.append(ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Multi-modal Query: {query}",
            priority=1.0,
            relevance_score=1.0
        ))
        
        # Multi-modal instructions
        instructions = """
        You are processing multi-modal input. Consider:
        1. Relationships between different modalities
        2. Cross-modal consistency and contradictions
        3. Complementary information across modalities
        4. Unified understanding and response
        """
        components.append(ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=instructions,
            priority=0.9,
            relevance_score=0.9
        ))
        
        # Text content
        if text_content:
            components.append(ContextComponent(
                component_type=ComponentType.KNOWLEDGE,
                content=f"Text Content: {text_content}",
                priority=0.8,
                relevance_score=0.8,
                metadata={"modality": "text"}
            ))
        
        # Image descriptions
        if image_descriptions:
            for i, desc in enumerate(image_descriptions):
                components.append(ContextComponent(
                    component_type=ComponentType.KNOWLEDGE,
                    content=f"Image {i+1}: {desc}",
                    priority=0.7,
                    relevance_score=0.7,
                    metadata={"modality": "image", "index": i}
                ))
        
        # Audio transcripts
        if audio_transcripts:
            for i, transcript in enumerate(audio_transcripts):
                components.append(ContextComponent(
                    component_type=ComponentType.KNOWLEDGE,
                    content=f"Audio {i+1}: {transcript}",
                    priority=0.6,
                    relevance_score=0.6,
                    metadata={"modality": "audio", "index": i}
                ))
        
        return components
    
    def assemble_with_pattern(self, pattern_name: str, strategy: AssemblyStrategy = AssemblyStrategy.GREEDY,
                            constraints: AssemblyConstraints = None, **kwargs) -> Dict[str, Any]:
        """Assemble context using a specific pattern"""
        if pattern_name not in self.patterns:
            raise ValueError(f"Pattern '{pattern_name}' not found")
        
        # Generate components using pattern
        components = self.patterns[pattern_name](**kwargs)
        
        # Create assembler
        assembler = ContextAssembler(constraints)
        assembler.add_components(components)
        
        # Execute assembly strategy
        if strategy == AssemblyStrategy.GREEDY:
            result = assembler.greedy_assembly()
        elif strategy == AssemblyStrategy.OPTIMAL_DP:
            result = assembler.optimal_assembly_dp()
        else:
            result = assembler.greedy_assembly()  # Default fallback
        
        # Add pattern metadata
        result['pattern'] = pattern_name
        result['strategy'] = strategy.value
        result['input_components'] = len(components)
        
        return result

# ============================================================================
# PART 3: EVALUATION AND OPTIMIZATION
# ============================================================================

class AssemblyEvaluator:
    """Evaluation framework for context assembly quality"""
    
    def __init__(self):
        self.metrics = {}
    
    def evaluate_coherence(self, components: List[ContextComponent]) -> float:
        """
        Evaluate semantic coherence between components
        Based on mutual information and content similarity
        """
        if len(components) <= 1:
            return 1.0
        
        coherence_scores = []
        
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                # Calculate pairwise coherence
                words_i = set(components[i].content.lower().split())
                words_j = set(components[j].content.lower().split())
                
                if words_i and words_j:
                    intersection = words_i.intersection(words_j)
                    union = words_i.union(words_j)
                    jaccard = len(intersection) / len(union)
                    coherence_scores.append(jaccard)
        
        return np.mean(coherence_scores) if coherence_scores else 0.0
    
    def evaluate_coverage(self, components: List[ContextComponent]) -> float:
        """Evaluate coverage of different component types"""
        covered_types = set(comp.component_type for comp in components)
        total_types = len(ComponentType)
        return len(covered_types) / total_types
    
    def evaluate_efficiency(self, result: Dict[str, Any]) -> float:
        """Evaluate token efficiency and utilization"""
        token_util = result.get('token_utilization', 0)
        efficiency_ratio = result.get('efficiency_ratio', 0)
        return (token_util + efficiency_ratio) / 2
    
    def evaluate_diversity(self, components: List[ContextComponent]) -> float:
        """Evaluate information diversity across components"""
        if len(components) <= 1:
            return 1.0
        
        # Calculate content diversity using vocabulary overlap
        all_words = set()
        component_words = []
        
        for comp in components:
            words = set(comp.content.lower().split())
            component_words.append(words)
            all_words.update(words)
        
        if not all_words:
            return 0.0
        
        # Calculate diversity as inverse of average overlap
        overlaps = []
        for i in range(len(component_words)):
            for j in range(i + 1, len(component_words)):
                if component_words[i] and component_words[j]:
                    overlap = len(component_words[i].intersection(component_words[j]))
                    overlap_ratio = overlap / min(len(component_words[i]), len(component_words[j]))
                    overlaps.append(overlap_ratio)
        
        avg_overlap = np.mean(overlaps) if overlaps else 0.0
        return 1.0 - avg_overlap
    
    def comprehensive_evaluation(self, result: Dict[str, Any]) -> Dict[str, float]:
        """Comprehensive evaluation of assembly result"""
        components = result.get('components', [])
        
        metrics = {
            'coherence': self.evaluate_coherence(components),
            'coverage': self.evaluate_coverage(components),
            'efficiency': self.evaluate_efficiency(result),
            'diversity': self.evaluate_diversity(components),
            'token_utilization': result.get('token_utilization', 0),
            'component_ratio': result.get('efficiency_ratio', 0)
        }
        
        # Calculate composite score
        weights = {
            'coherence': 0.25,
            'coverage': 0.20,
            'efficiency': 0.20,
            'diversity': 0.15,
            'token_utilization': 0.10,
            'component_ratio': 0.10
        }
        
        composite_score = sum(metrics[metric] * weights[metric] for metric in weights)
        metrics['composite_score'] = composite_score
        
        return metrics

# ============================================================================
# PART 4: PRACTICAL DEMONSTRATIONS AND EXPERIMENTS
# ============================================================================

def create_sample_components() -> List[ContextComponent]:
    """Create sample components for demonstration"""
    components = []
    
    # Sample instructions
    components.append(ContextComponent(
        component_type=ComponentType.INSTRUCTIONS,
        content="You are a helpful AI assistant. Provide accurate, helpful, and well-structured responses.",
        priority=0.9,
        relevance_score=0.9,
        source="system"
    ))
    
    # Sample knowledge
    knowledge_items = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
        "Context engineering involves optimizing the information payload provided to language models.",
        "Retrieval-augmented generation combines language models with external knowledge retrieval.",
        "Dynamic programming is an optimization technique that breaks problems into overlapping subproblems."
    ]
    
    for i, knowledge in enumerate(knowledge_items):
        components.append(ContextComponent(
            component_type=ComponentType.KNOWLEDGE,
            content=knowledge,
            priority=0.8,
            relevance_score=0.8 - (i * 0.1),
            source=f"knowledge_base_{i}"
        ))
    
    # Sample tools
    tools = [
        "Calculator: Performs mathematical calculations",
        "WebSearch: Searches the internet for information",
        "CodeExecutor: Executes Python code safely",
        "FileManager: Reads and writes files"
    ]
    
    for tool in tools:
        components.append(ContextComponent(
            component_type=ComponentType.TOOLS,
            content=tool,
            priority=0.7,
            relevance_score=0.7,
            source="tool_registry"
        ))
    
    # Sample memory
    components.append(ContextComponent(
        component_type=ComponentType.MEMORY,
        content="Previous conversation: User asked about context engineering best practices.",
        priority=0.6,
        relevance_score=0.6,
        source="conversation_history"
    ))
    
    # Sample state
    components.append(ContextComponent(
        component_type=ComponentType.STATE,
        content="Current session: Research mode, focusing on technical documentation.",
        priority=0.6,
        relevance_score=0.6,
        source="session_state"
    ))
    
    return components

def demonstrate_basic_assembly():
    """Demonstrate basic context assembly functionality"""
    print("=" * 60)
    print("DEMONSTRATION 1: Basic Context Assembly")
    print("=" * 60)
    
    # Create assembler with constraints
    constraints = AssemblyConstraints(
        max_tokens=1000,
        min_relevance=0.3,
        require_all_types=False
    )
    
    assembler = ContextAssembler(constraints)
    
    # Add sample components
    components = create_sample_components()
    assembler.add_components(components)
    
    # Query component
    query = ContextComponent(
        component_type=ComponentType.QUERY,
        content="Explain the principles of dynamic context assembly in AI systems.",
        priority=1.0,
        relevance_score=1.0,
        source="user_input"
    )
    assembler.add_component(query)
    
    print(f"Input components: {len(assembler.components)}")
    print(f"Total input tokens: {sum(c.token_count for c in assembler.components)}")
    
    # Test greedy assembly
    print("\n--- Greedy Assembly ---")
    greedy_result = assembler.greedy_assembly()
    print(f"Selected components: {len(greedy_result['components'])}")
    print(f"Total tokens: {greedy_result['total_tokens']}")
    print(f"Token utilization: {greedy_result['token_utilization']:.2%}")
    
    # Test optimal assembly
    print("\n--- Optimal Assembly (Dynamic Programming) ---")
    optimal_result = assembler.optimal_assembly_dp()
    print(f"Selected components: {len(optimal_result['components'])}")
    print(f"Total tokens: {optimal_result['total_tokens']}")
    print(f"Token utilization: {optimal_result['token_utilization']:.2%}")
    print(f"Optimal utility: {optimal_result.get('optimal_utility', 0):.3f}")
    
    # Evaluate results
    evaluator = AssemblyEvaluator()
    
    print("\n--- Greedy Assembly Evaluation ---")
    greedy_metrics = evaluator.comprehensive_evaluation(greedy_result)
    for metric, value in greedy_metrics.items():
        print(f"{metric}: {value:.3f}")
    
    print("\n--- Optimal Assembly Evaluation ---")
    optimal_metrics = evaluator.comprehensive_evaluation(optimal_result)
    for metric, value in optimal_metrics.items():
        print(f"{metric}: {value:.3f}")

def demonstrate_assembly_patterns():
    """Demonstrate different assembly patterns"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 2: Assembly Patterns")
    print("=" * 60)
    
    orchestrator = ContextOrchestrator()
    constraints = AssemblyConstraints(max_tokens=1200, min_relevance=0.2)
    
    # RAG Pipeline Pattern
    print("\n--- RAG Pipeline Pattern ---")
    rag_result = orchestrator.assemble_with_pattern(
        pattern_name='rag_pipeline',
        strategy=AssemblyStrategy.GREEDY,
        constraints=constraints,
        query="What are the latest developments in transformer architectures?",
        knowledge_docs=[
            "Transformers use self-attention mechanisms for sequence modeling.",
            "Recent variants include GPT, BERT, and T5 with different training objectives.",
            "Efficient transformers like Linformer and Performer reduce computational complexity.",
            "Vision transformers adapt the architecture for image processing tasks."
        ],
        instructions="Provide a comprehensive overview based on the available documents."
    )
    
    print(f"Components: {len(rag_result['components'])}")
    print(f"Token utilization: {rag_result['token_utilization']:.2%}")
    
    # Agent Workflow Pattern
    print("\n--- Agent Workflow Pattern ---")
    agent_result = orchestrator.assemble_with_pattern(
        pattern_name='agent_workflow',
        strategy=AssemblyStrategy.GREEDY,
        constraints=constraints,
        task="Research and summarize papers on context engineering",
        available_tools=[
            {"name": "PaperSearch", "description": "Search academic papers"},
            {"name": "PDFReader", "description": "Extract text from PDF documents"},
            {"name": "Summarizer", "description": "Generate summaries of long text"}
        ],
        agent_state={"current_step": "planning", "papers_found": 0},
        memory=["Previous search: 'context engineering'", "Found 15 relevant papers"]
    )
    
    print(f"Components: {len(agent_result['components'])}")
    print(f"Token utilization: {agent_result['token_utilization']:.2%}")
    
    # Research Assistant Pattern
    print("\n--- Research Assistant Pattern ---")
    research_result = orchestrator.assemble_with_pattern(
        pattern_name='research_assistant',
        strategy=AssemblyStrategy.OPTIMAL_DP,
        constraints=constraints,
        research_query="Impact of context length on language model performance",
        papers=[
            {
                "title": "Scaling Laws for Context Length in Language Models",
                "abstract": "We investigate how performance scales with context length...",
                "key_findings": "Longer contexts improve performance but with diminishing returns."
            },
            {
                "title": "Efficient Long Context Processing in Transformers", 
                "abstract": "Novel attention mechanisms for handling long sequences...",
                "key_findings": "Sparse attention patterns reduce computational complexity."
            }
        ],
        research_context="Literature review for PhD thesis on context optimization"
    )
    
    print(f"Components: {len(research_result['components'])}")
    print(f"Token utilization: {research_result['token_utilization']:.2%}")
    
    # Evaluate all patterns
    evaluator = AssemblyEvaluator()
    
    print("\n--- Pattern Evaluation Comparison ---")
    patterns_results = {
        'RAG Pipeline': rag_result,
        'Agent Workflow': agent_result, 
        'Research Assistant': research_result
    }
    
    for pattern_name, result in patterns_results.items():
        metrics = evaluator.comprehensive_evaluation(result)
        print(f"\n{pattern_name}:")
        print(f"  Composite Score: {metrics['composite_score']:.3f}")
        print(f"  Coherence: {metrics['coherence']:.3f}")
        print(f"  Coverage: {metrics['coverage']:.3f}")
        print(f"  Efficiency: {metrics['efficiency']:.3f}")

def demonstrate_optimization_comparison():
    """Compare different optimization strategies"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 3: Optimization Strategy Comparison")
    print("=" * 60)
    
    # Create test scenario with varying constraints
    constraints_scenarios = [
        AssemblyConstraints(max_tokens=500, min_relevance=0.1),
        AssemblyConstraints(max_tokens=1000, min_relevance=0.3),
        AssemblyConstraints(max_tokens=2000, min_relevance=0.5)
    ]
    
    base_components = create_sample_components()
    
    # Add query
    query = ContextComponent(
        component_type=ComponentType.QUERY,
        content="Compare different approaches to context optimization in large language models.",
        priority=1.0,
        relevance_score=1.0
    )
    
    evaluator = AssemblyEvaluator()
    
    print("Constraint Scenario | Strategy | Components | Tokens | Composite Score")
    print("-" * 70)
    
    for i, constraints in enumerate(constraints_scenarios):
        assembler = ContextAssembler(constraints)
        assembler.add_components(base_components + [query])
        
        # Test both strategies
        greedy_result = assembler.greedy_assembly()
        optimal_result = assembler.optimal_assembly_dp()
        
        greedy_metrics = evaluator.comprehensive_evaluation(greedy_result)
        optimal_metrics = evaluator.comprehensive_evaluation(optimal_result)
        
        print(f"Scenario {i+1:2d}      | Greedy   | {len(greedy_result['components']):10d} | {greedy_result['total_tokens']:6d} | {greedy_metrics['composite_score']:13.3f}")
        print(f"Scenario {i+1:2d}      | Optimal  | {len(optimal_result['components']):10d} | {optimal_result['total_tokens']:6d} | {optimal_metrics['composite_score']:13.3f}")

def performance_benchmark():
    """Benchmark assembly performance with different scales"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 4: Performance Benchmark")
    print("=" * 60)
    
    # Test with different numbers of components
    component_counts = [10, 50, 100, 200]
    
    print("Components | Greedy Time (ms) | Optimal Time (ms) | Greedy Score | Optimal Score")
    print("-" * 80)
    
    for count in component_counts:
        # Generate components
        components = []
        for i in range(count):
            comp_type = list(ComponentType)[i % len(ComponentType)]
            components.append(ContextComponent(
                component_type=comp_type,
                content=f"Sample content for component {i} " * (5 + i % 10),
                priority=0.5 + (i % 10) * 0.05,
                relevance_score=0.3 + (i % 7) * 0.1
            ))
        
        constraints = AssemblyConstraints(max_tokens=1500, min_relevance=0.2)
        assembler = ContextAssembler(constraints)
        assembler.add_components(components)
        
        # Benchmark greedy
        start_time = time.time()
        greedy_result = assembler.greedy_assembly()
        greedy_time = (time.time() - start_time) * 1000
        
        # Benchmark optimal (with timeout for large cases)
        start_time = time.time()
        try:
            optimal_result = assembler.optimal_assembly_dp()
            optimal_time = (time.time() - start_time) * 1000
        except:
            optimal_result = greedy_result
            optimal_time = float('inf')
        
        evaluator = AssemblyEvaluator()
        greedy_score = evaluator.comprehensive_evaluation(greedy_result)['composite_score']
        optimal_score = evaluator.comprehensive_evaluation(optimal_result)['composite_score']
        
        print(f"{count:10d} | {greedy_time:15.2f} | {optimal_time:16.2f} | {greedy_score:11.3f} | {optimal_score:12.3f}")

def advanced_field_integration_demo():
    """Demonstrate advanced field theory integration concepts"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION 5: Advanced Field Integration")
    print("=" * 60)
    
    # Create components with field-theoretic properties
    components = []
    
    # Mythic attractor
    components.append(ContextComponent(
        component_type=ComponentType.KNOWLEDGE,
        content="The hero's journey represents a universal pattern of transformation and growth.",
        priority=0.8,
        relevance_score=0.7,
        metadata={"attractor_type": "mythic", "field_strength": 0.8}
    ))
    
    # Mathematical attractor
    components.append(ContextComponent(
        component_type=ComponentType.KNOWLEDGE, 
        content="Dynamic programming optimizes recursive problems through memoization.",
        priority=0.9,
        relevance_score=0.9,
        metadata={"attractor_type": "mathematical", "field_strength": 0.9}
    ))
    
    # Metaphorical attractor
    components.append(ContextComponent(
        component_type=ComponentType.INSTRUCTIONS,
        content="Think of context assembly like conducting an orchestra - each component must harmonize.",
        priority=0.7,
        relevance_score=0.6,
        metadata={"attractor_type": "metaphorical", "field_strength": 0.6}
    ))
    
    # Query with field resonance
    query = ContextComponent(
        component_type=ComponentType.QUERY,
        content="How can we create harmony between different types of knowledge in AI systems?",
        priority=1.0,
        relevance_score=1.0,
        metadata={"resonance_pattern": ["mythic", "mathematical", "metaphorical"]}
    )
    
    # Assembly with field-aware optimization
    constraints = AssemblyConstraints(max_tokens=800, min_relevance=0.3)
    assembler = ContextAssembler(constraints)
    assembler.add_components(components + [query])
    
    result = assembler.greedy_assembly()
    
    print("Field Integration Analysis:")
    print(f"Selected components: {len(result['components'])}")
    
    attractor_types = []
    for comp in result['components']:
        attractor_type = comp.metadata.get('attractor_type', 'none')
        if attractor_type != 'none':
            attractor_types.append(attractor_type)
    
    print(f"Attractor types present: {set(attractor_types)}")
    
    # Calculate field resonance
    query_resonance = query.metadata.get('resonance_pattern', [])
    field_resonance = len(set(attractor_types).intersection(set(query_resonance))) / len(query_resonance)
    print(f"Field resonance score: {field_resonance:.3f}")
    
    # Demonstrate emergent properties
    print("\nEmergent Properties:")
    total_field_strength = sum(
        comp.metadata.get('field_strength', 0) 
        for comp in result['components'] 
        if 'field_strength' in comp.metadata
    )
    print(f"Total field strength: {total_field_strength:.2f}")
    
    if total_field_strength > 2.0:
        print("Strong field emergence detected - high potential for creative synthesis")
    elif total_field_strength > 1.0:
        print("Moderate field emergence - balanced analytical and creative potential")
    else:
        print("Weak field emergence - primarily analytical processing")

# ============================================================================
# MAIN EXECUTION AND LAB RUNNER
# ============================================================================

def run_dynamic_assembly_lab():
    """Run the complete dynamic assembly laboratory"""
    print("CONTEXT ENGINEERING - DYNAMIC ASSEMBLY LABORATORY")
    print("Module 01: Context Retrieval & Generation")
    print("=" * 60)
    print("Mathematical Foundation: C = A(c₁, c₂, ..., cₙ)")
    print("Optimization Objective: A* = arg max_A E[Reward(LLM(C), target)]")
    print("=" * 60)
    
    try:
        # Run all demonstrations
        demonstrate_basic_assembly()
        demonstrate_assembly_patterns()
        demonstrate_optimization_comparison()
        performance_benchmark()
        advanced_field_integration_demo()
        
        print("\n" + "=" * 60)
        print("LABORATORY COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        print("\nKey Learning Outcomes Achieved:")
        print("✓ Mathematical formalization of context assembly")
        print("✓ Practical implementation of assembly algorithms")
        print("✓ Component integration patterns for different use cases")
        print("✓ Evaluation and optimization strategies")
        print("✓ Performance benchmarking and analysis")
        print("✓ Advanced field theory integration concepts")
        
        print("\nNext Steps:")
        print("- Experiment with custom assembly patterns")
        print("- Implement domain-specific optimization strategies")
        print("- Explore multi-objective optimization approaches")
        print("- Study the relationship between context structure and model performance")
        
    except Exception as e:
        print(f"\nLaboratory Error: {e}")
        print("Please review the implementation and try again.")

if __name__ == "__main__":
    # Run the laboratory
    run_dynamic_assembly_lab()
    
    print("\n" + "=" * 60)
    print("ADDITIONAL EXERCISES FOR STUDENTS")
    print("=" * 60)
    
    print("""
1. Implement a custom assembly pattern for your domain of interest
2. Experiment with different constraint configurations
3. Develop a multi-objective optimization approach considering both relevance and diversity
4. Create a real-time assembly system with streaming components
5. Build an adaptive assembler that learns from user feedback
6. Explore the integration of field theory concepts in practical applications
7. Design evaluation metrics specific to your use case
8. Implement cross-modal context assembly for multimodal applications
    """)
