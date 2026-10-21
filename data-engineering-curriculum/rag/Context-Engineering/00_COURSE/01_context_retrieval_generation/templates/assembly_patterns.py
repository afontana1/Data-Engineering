# Context Engineering Course - Module 01: Context Retrieval & Generation
# Assembly Patterns - Production-Ready Context Assembly Implementations
# 
# Mathematical Foundation: C = A(c₁, c₂, ..., cₙ) with optimization and pattern composition
# Research Grounding: Based on systematic analysis of 1400+ papers (arXiv:2507.13334v1)
# 
# This module provides production-ready implementations of context assembly patterns
# for enterprise deployment, research applications, and educational purposes.

import abc
import asyncio
import hashlib
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Set
from functools import wraps, lru_cache
import threading
from collections import defaultdict, deque
import numpy as np

# Compatibility imports for optional dependencies
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# ============================================================================
# CORE PATTERN INFRASTRUCTURE
# ============================================================================

class PatternType(Enum):
    """Enumeration of supported assembly pattern types"""
    BASIC_RAG = "basic_rag"
    ENHANCED_RAG = "enhanced_rag"
    AGENT_WORKFLOW = "agent_workflow"
    RESEARCH_ASSISTANT = "research_assistant"
    MULTI_MODAL = "multi_modal"
    CONVERSATIONAL = "conversational"
    HIERARCHICAL = "hierarchical"
    GRAPH_ENHANCED = "graph_enhanced"
    FIELD_THEORETIC = "field_theoretic"
    META_RECURSIVE = "meta_recursive"
    PRODUCTION_PIPELINE = "production_pipeline"

class ComponentType(Enum):
    """Context component types from mathematical formalization"""
    INSTRUCTIONS = "c_instr"    # c₁: System instructions and rules
    KNOWLEDGE = "c_know"        # c₂: External knowledge (RAG, KG)
    TOOLS = "c_tools"          # c₃: Tool definitions and signatures
    MEMORY = "c_mem"           # c₄: Persistent memory information
    STATE = "c_state"          # c₅: Dynamic state (user, world, multi-agent)
    QUERY = "c_query"          # c₆: Immediate user request

@dataclass
class ContextComponent:
    """Individual context component with optimization metadata"""
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
            # Improved token estimation using more accurate approximation
            self.token_count = max(1, int(len(self.content.split()) * 1.3))

@dataclass
class AssemblyResult:
    """Result of context assembly with comprehensive metadata"""
    components: List[ContextComponent]
    total_tokens: int
    assembly_time: float
    pattern_used: str
    optimization_strategy: str
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def assembled_context(self) -> str:
        """Generate the final assembled context string"""
        return "\n\n".join([comp.content for comp in self.components])

@dataclass
class PatternConfiguration:
    """Configuration for assembly patterns with optimization parameters"""
    max_tokens: int = 4000
    min_relevance: float = 0.1
    optimization_strategy: str = "greedy"
    enable_caching: bool = True
    parallel_processing: bool = False
    quality_threshold: float = 0.7
    custom_weights: Dict[ComponentType, float] = field(default_factory=dict)
    performance_targets: Dict[str, float] = field(default_factory=dict)

# ============================================================================
# ABSTRACT BASE PATTERN CLASS
# ============================================================================

class AssemblyPattern(abc.ABC):
    """
    Abstract base class for all context assembly patterns
    
    Implements the mathematical foundation: C = A(c₁, c₂, ..., cₙ)
    with pattern-specific optimization strategies and quality metrics.
    """
    
    def __init__(self, config: PatternConfiguration = None):
        self.config = config or PatternConfiguration()
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._cache = {}
        self._performance_metrics = defaultdict(list)
        self._lock = threading.Lock()
        
        # Initialize optional services
        self._redis_client = None
        if REDIS_AVAILABLE and self.config.enable_caching:
            try:
                self._redis_client = redis.Redis(decode_responses=True)
            except:
                self.logger.warning("Redis not available, using in-memory cache")
    
    @abc.abstractmethod
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        """
        Core assembly method that must be implemented by each pattern
        
        Args:
            query: User query or request
            components: Available context components
            **kwargs: Pattern-specific parameters
            
        Returns:
            AssemblyResult with optimized context and metadata
        """
        pass
    
    @abc.abstractmethod
    def get_pattern_type(self) -> PatternType:
        """Return the pattern type identifier"""
        pass
    
    def optimize_components(self, components: List[ContextComponent], 
                          query: str) -> List[ContextComponent]:
        """
        Base optimization logic for component selection and ranking
        
        Mathematical basis: Utility optimization with constraints
        U(c_i) = relevance * priority * novelty - redundancy_penalty
        """
        if not components:
            return []
        
        # Calculate relevance scores if not provided
        for comp in components:
            if comp.relevance_score == 0.0:
                comp.relevance_score = self._calculate_relevance(comp, query)
        
        # Sort by utility score
        optimized = sorted(
            components,
            key=lambda c: self._calculate_utility(c, components),
            reverse=True
        )
        
        # Apply constraints
        selected = []
        total_tokens = 0
        
        for comp in optimized:
            if (total_tokens + comp.token_count <= self.config.max_tokens and
                comp.relevance_score >= self.config.min_relevance):
                selected.append(comp)
                total_tokens += comp.token_count
            
            if total_tokens >= self.config.max_tokens * 0.95:  # Leave some buffer
                break
        
        return selected
    
    def _calculate_relevance(self, component: ContextComponent, query: str) -> float:
        """Calculate relevance score between component and query"""
        # Simple keyword-based relevance (can be enhanced with embeddings)
        query_words = set(query.lower().split())
        comp_words = set(component.content.lower().split())
        
        if not query_words or not comp_words:
            return 0.0
        
        intersection = query_words.intersection(comp_words)
        union = query_words.union(comp_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_utility(self, component: ContextComponent, 
                          all_components: List[ContextComponent]) -> float:
        """Calculate utility score for component selection"""
        base_utility = component.relevance_score * component.priority
        
        # Apply custom weights if provided
        type_weight = self.config.custom_weights.get(component.component_type, 1.0)
        
        return base_utility * type_weight
    
    def _cache_key(self, query: str, components: List[ContextComponent]) -> str:
        """Generate cache key for assembly results"""
        content_hash = hashlib.md5(
            (query + str([c.content for c in components])).encode()
        ).hexdigest()
        return f"{self.get_pattern_type().value}:{content_hash}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[AssemblyResult]:
        """Retrieve cached assembly result"""
        if not self.config.enable_caching:
            return None
        
        # Try Redis first, then in-memory cache
        if self._redis_client:
            try:
                cached = self._redis_client.get(cache_key)
                if cached:
                    return AssemblyResult(**json.loads(cached))
            except:
                pass
        
        return self._cache.get(cache_key)
    
    def _cache_result(self, cache_key: str, result: AssemblyResult):
        """Cache assembly result"""
        if not self.config.enable_caching:
            return
        
        # Cache in Redis with TTL
        if self._redis_client:
            try:
                self._redis_client.setex(
                    cache_key, 
                    3600,  # 1 hour TTL
                    json.dumps(result.__dict__, default=str)
                )
            except:
                pass
        
        # Cache in memory (with size limit)
        with self._lock:
            if len(self._cache) > 1000:  # Simple LRU
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            self._cache[cache_key] = result
    
    def _record_performance(self, metric_name: str, value: float):
        """Record performance metrics for monitoring"""
        with self._lock:
            self._performance_metrics[metric_name].append({
                'value': value,
                'timestamp': time.time()
            })
            
            # Keep only recent metrics (last 1000 entries)
            if len(self._performance_metrics[metric_name]) > 1000:
                self._performance_metrics[metric_name] = \
                    self._performance_metrics[metric_name][-1000:]
    
    def get_performance_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get performance statistics"""
        with self._lock:
            stats = {}
            for metric, values in self._performance_metrics.items():
                if values:
                    recent_values = [v['value'] for v in values[-100:]]  # Last 100
                    stats[metric] = {
                        'mean': np.mean(recent_values),
                        'median': np.median(recent_values),
                        'std': np.std(recent_values),
                        'min': np.min(recent_values),
                        'max': np.max(recent_values),
                        'count': len(values)
                    }
            return stats

# ============================================================================
# BASIC RAG PATTERNS
# ============================================================================

class BasicRAGPattern(AssemblyPattern):
    """
    Basic RAG pattern implementation
    
    Mathematical formulation: C = A(c_instr, top_k_retrieval(query, KB), c_query)
    Optimization: Greedy selection with relevance ranking
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.BASIC_RAG
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        start_time = time.time()
        cache_key = self._cache_key(query, components)
        
        # Check cache first
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            self._record_performance("cache_hit_rate", 1.0)
            return cached_result
        
        self._record_performance("cache_hit_rate", 0.0)
        
        # Ensure we have a query component
        query_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"User Query: {query}",
            priority=1.0,
            relevance_score=1.0,
            source="user_input"
        )
        
        # Add basic instructions if not present
        has_instructions = any(c.component_type == ComponentType.INSTRUCTIONS 
                             for c in components)
        if not has_instructions:
            instruction_component = ContextComponent(
                component_type=ComponentType.INSTRUCTIONS,
                content="You are a helpful AI assistant. Use the provided context to answer the user's question accurately and concisely. If the context doesn't contain enough information, acknowledge this limitation.",
                priority=0.9,
                relevance_score=0.9,
                source="default_instructions"
            )
            components = [instruction_component] + components
        
        # Optimize component selection
        optimized_components = self.optimize_components(components, query)
        
        # Assembly order: Instructions -> Knowledge -> Query
        ordered_components = []
        
        # Add instructions first
        for comp in optimized_components:
            if comp.component_type == ComponentType.INSTRUCTIONS:
                ordered_components.append(comp)
        
        # Add knowledge components
        for comp in optimized_components:
            if comp.component_type == ComponentType.KNOWLEDGE:
                ordered_components.append(comp)
        
        # Add query last
        ordered_components.append(query_component)
        
        assembly_time = time.time() - start_time
        
        # Calculate quality metrics
        quality_metrics = self._calculate_quality_metrics(ordered_components, query)
        
        result = AssemblyResult(
            components=ordered_components,
            total_tokens=sum(c.token_count for c in ordered_components),
            assembly_time=assembly_time,
            pattern_used=self.get_pattern_type().value,
            optimization_strategy="greedy_relevance",
            quality_metrics=quality_metrics,
            metadata={
                "component_count": len(ordered_components),
                "knowledge_sources": len([c for c in ordered_components 
                                        if c.component_type == ComponentType.KNOWLEDGE])
            }
        )
        
        # Cache result
        self._cache_result(cache_key, result)
        
        # Record performance metrics
        self._record_performance("assembly_time", assembly_time)
        self._record_performance("token_count", result.total_tokens)
        self._record_performance("quality_score", quality_metrics.get("overall_quality", 0.0))
        
        return result
    
    def _calculate_quality_metrics(self, components: List[ContextComponent], 
                                 query: str) -> Dict[str, float]:
        """Calculate quality metrics for the assembled context"""
        if not components:
            return {"overall_quality": 0.0}
        
        # Coverage: percentage of component types present
        present_types = set(c.component_type for c in components)
        coverage = len(present_types) / len(ComponentType)
        
        # Relevance: average relevance score
        relevance_scores = [c.relevance_score for c in components if c.relevance_score > 0]
        avg_relevance = np.mean(relevance_scores) if relevance_scores else 0.0
        
        # Token efficiency: information density
        total_tokens = sum(c.token_count for c in components)
        token_efficiency = min(1.0, total_tokens / self.config.max_tokens)
        
        # Overall quality (weighted combination)
        overall_quality = (0.4 * avg_relevance + 0.3 * coverage + 0.3 * token_efficiency)
        
        return {
            "coverage": coverage,
            "avg_relevance": avg_relevance,
            "token_efficiency": token_efficiency,
            "overall_quality": overall_quality
        }

class EnhancedRAGPattern(BasicRAGPattern):
    """
    Enhanced RAG with reranking and query expansion
    
    Mathematical formulation: C = A(c_instr, rerank(expand(query), candidates), c_query)
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.ENHANCED_RAG
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        # Query expansion
        expanded_queries = self._expand_query(query, **kwargs)
        
        # Enhanced component scoring with multiple query variants
        for component in components:
            scores = []
            for expanded_query in [query] + expanded_queries:
                score = self._calculate_relevance(component, expanded_query)
                scores.append(score)
            component.relevance_score = max(scores)  # Best match across variants
        
        # Reranking with diversity consideration
        components = self._rerank_with_diversity(components, query)
        
        # Use parent assembly logic with enhanced components
        return super().assemble(query, components, **kwargs)
    
    def _expand_query(self, query: str, **kwargs) -> List[str]:
        """Expand query with synonyms and related terms"""
        # Simple expansion (can be enhanced with LLM-based expansion)
        expansions = []
        
        # Add question variations
        if "?" not in query:
            expansions.append(f"What is {query}?")
            expansions.append(f"How does {query} work?")
            expansions.append(f"Explain {query}")
        
        # Add keyword variations (simplified)
        words = query.split()
        if len(words) > 1:
            # Reorder words
            expansions.append(" ".join(reversed(words)))
        
        return expansions[:3]  # Limit expansions
    
    def _rerank_with_diversity(self, components: List[ContextComponent], 
                              query: str) -> List[ContextComponent]:
        """Rerank components considering both relevance and diversity"""
        if len(components) <= 3:
            return sorted(components, key=lambda c: c.relevance_score, reverse=True)
        
        # Maximal Marginal Relevance (MMR) approximation
        selected = []
        remaining = components.copy()
        
        # Select highest relevance first
        remaining.sort(key=lambda c: c.relevance_score, reverse=True)
        selected.append(remaining.pop(0))
        
        # MMR selection for remaining components
        lambda_param = 0.7  # Balance between relevance and diversity
        
        while remaining and len(selected) < 10:  # Limit selection
            best_score = -1
            best_component = None
            best_index = -1
            
            for i, component in enumerate(remaining):
                # Relevance score
                relevance = component.relevance_score
                
                # Diversity score (inverse of max similarity to selected)
                max_similarity = 0
                for selected_comp in selected:
                    similarity = self._calculate_similarity(component, selected_comp)
                    max_similarity = max(max_similarity, similarity)
                
                diversity = 1 - max_similarity
                
                # MMR score
                mmr_score = lambda_param * relevance + (1 - lambda_param) * diversity
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_component = component
                    best_index = i
            
            if best_component:
                selected.append(remaining.pop(best_index))
            else:
                break
        
        return selected + remaining  # Add any remaining components
    
    def _calculate_similarity(self, comp1: ContextComponent, 
                            comp2: ContextComponent) -> float:
        """Calculate similarity between two components"""
        words1 = set(comp1.content.lower().split())
        words2 = set(comp2.content.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

# ============================================================================
# AGENT WORKFLOW PATTERNS
# ============================================================================

class AgentWorkflowPattern(AssemblyPattern):
    """
    Agent-oriented assembly pattern for tool-augmented reasoning
    
    Mathematical formulation: C = A(c_instr, c_tools, c_state, planning_component)
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.AGENT_WORKFLOW
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        start_time = time.time()
        
        # Extract agent-specific parameters
        available_tools = kwargs.get("available_tools", [])
        agent_state = kwargs.get("agent_state", {})
        task_complexity = kwargs.get("task_complexity", "medium")
        
        # Build agent instructions
        agent_instructions = self._build_agent_instructions(
            query, available_tools, task_complexity
        )
        
        # Create structured components
        structured_components = []
        
        # Add agent instructions
        structured_components.append(ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=agent_instructions,
            priority=1.0,
            relevance_score=1.0,
            source="agent_system"
        ))
        
        # Add tools information
        if available_tools:
            tools_content = self._format_tools(available_tools)
            structured_components.append(ContextComponent(
                component_type=ComponentType.TOOLS,
                content=tools_content,
                priority=0.9,
                relevance_score=0.9,
                source="tool_registry"
            ))
        
        # Add current state
        if agent_state:
            state_content = f"Current State:\n{json.dumps(agent_state, indent=2)}"
            structured_components.append(ContextComponent(
                component_type=ComponentType.STATE,
                content=state_content,
                priority=0.8,
                relevance_score=0.8,
                source="agent_state"
            ))
        
        # Add relevant knowledge components
        knowledge_components = [c for c in components 
                              if c.component_type == ComponentType.KNOWLEDGE]
        relevant_knowledge = self.optimize_components(knowledge_components, query)
        structured_components.extend(relevant_knowledge)
        
        # Add memory if available
        memory_components = [c for c in components 
                           if c.component_type == ComponentType.MEMORY]
        if memory_components:
            # Select most recent and relevant memory
            memory_components.sort(key=lambda c: c.timestamp, reverse=True)
            structured_components.extend(memory_components[:2])  # Last 2 memory items
        
        # Add the task/query
        task_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Task: {query}",
            priority=1.0,
            relevance_score=1.0,
            source="user_task"
        )
        structured_components.append(task_component)
        
        # Final optimization within token limits
        final_components = self._optimize_agent_components(structured_components)
        
        assembly_time = time.time() - start_time
        
        result = AssemblyResult(
            components=final_components,
            total_tokens=sum(c.token_count for c in final_components),
            assembly_time=assembly_time,
            pattern_used=self.get_pattern_type().value,
            optimization_strategy="agent_workflow",
            quality_metrics=self._calculate_agent_quality_metrics(final_components),
            metadata={
                "tools_available": len(available_tools),
                "state_complexity": len(str(agent_state)),
                "task_complexity": task_complexity
            }
        )
        
        return result
    
    def _build_agent_instructions(self, query: str, available_tools: List[Dict], 
                                task_complexity: str) -> str:
        """Build comprehensive agent instructions"""
        base_instructions = """You are an intelligent AI agent capable of reasoning and using tools to complete tasks.

Your reasoning process should follow these steps:
1. **Task Analysis**: Break down the task into clear, manageable steps
2. **Tool Selection**: Choose appropriate tools based on the task requirements
3. **Action Planning**: Plan the sequence of actions and tool usage
4. **Execution**: Perform actions systematically, checking results
5. **Verification**: Validate results and adjust if needed
6. **Completion**: Provide a comprehensive summary of what was accomplished"""
        
        # Add complexity-specific guidance
        if task_complexity == "simple":
            complexity_guidance = """
Focus on direct, efficient solutions. Minimize tool usage and provide clear, concise results."""
        elif task_complexity == "complex":
            complexity_guidance = """
This is a complex task requiring careful planning and multiple steps. Break it down systematically,
use multiple tools if necessary, and provide detailed reasoning for each step."""
        else:  # medium
            complexity_guidance = """
Approach this task methodically. Use tools as needed and provide clear reasoning."""
        
        # Add tool-specific guidance
        tool_guidance = ""
        if available_tools:
            tool_names = [tool.get("name", "Unknown") for tool in available_tools]
            tool_guidance = f"""
Available tools: {', '.join(tool_names)}
Choose tools carefully based on their capabilities and the task requirements."""
        
        return f"{base_instructions}\n{complexity_guidance}\n{tool_guidance}"
    
    def _format_tools(self, available_tools: List[Dict]) -> str:
        """Format tool information for context"""
        if not available_tools:
            return "No tools available."
        
        formatted_tools = ["Available Tools:"]
        for tool in available_tools:
            name = tool.get("name", "Unknown")
            description = tool.get("description", "No description available")
            parameters = tool.get("parameters", {})
            
            tool_info = f"\n**{name}**"
            tool_info += f"\nDescription: {description}"
            
            if parameters:
                tool_info += f"\nParameters: {json.dumps(parameters, indent=2)}"
            
            formatted_tools.append(tool_info)
        
        return "\n".join(formatted_tools)
    
    def _optimize_agent_components(self, components: List[ContextComponent]) -> List[ContextComponent]:
        """Optimize components specifically for agent workflows"""
        # Ensure critical components are preserved
        critical_types = {ComponentType.INSTRUCTIONS, ComponentType.QUERY}
        critical_components = [c for c in components if c.component_type in critical_types]
        
        # Other components can be optimized
        other_components = [c for c in components if c.component_type not in critical_types]
        
        # Calculate available token budget after critical components
        critical_tokens = sum(c.token_count for c in critical_components)
        available_tokens = self.config.max_tokens - critical_tokens
        
        # Optimize other components within remaining budget
        optimized_others = []
        current_tokens = 0
        
        # Sort other components by priority and relevance
        other_components.sort(
            key=lambda c: c.priority * c.relevance_score, 
            reverse=True
        )
        
        for component in other_components:
            if current_tokens + component.token_count <= available_tokens:
                optimized_others.append(component)
                current_tokens += component.token_count
        
        return critical_components + optimized_others
    
    def _calculate_agent_quality_metrics(self, components: List[ContextComponent]) -> Dict[str, float]:
        """Calculate quality metrics specific to agent workflows"""
        # Check presence of essential components
        has_instructions = any(c.component_type == ComponentType.INSTRUCTIONS for c in components)
        has_tools = any(c.component_type == ComponentType.TOOLS for c in components)
        has_state = any(c.component_type == ComponentType.STATE for c in components)
        has_query = any(c.component_type == ComponentType.QUERY for c in components)
        
        completeness = sum([has_instructions, has_tools, has_state, has_query]) / 4.0
        
        # Calculate token utilization
        total_tokens = sum(c.token_count for c in components)
        token_utilization = min(1.0, total_tokens / self.config.max_tokens)
        
        # Agent-specific quality score
        agent_quality = (0.5 * completeness + 0.3 * token_utilization + 0.2 * 1.0)  # Baseline
        
        return {
            "completeness": completeness,
            "token_utilization": token_utilization,
            "agent_quality": agent_quality,
            "has_instructions": float(has_instructions),
            "has_tools": float(has_tools),
            "has_state": float(has_state)
        }

# ============================================================================
# ADVANCED PATTERNS
# ============================================================================

class HierarchicalRAGPattern(AssemblyPattern):
    """
    Hierarchical RAG pattern (RAPTOR-style) with multi-level retrieval
    
    Mathematical formulation: C = A(instructions, ∪ᵢ level_i_retrieval(query, hierarchy), query)
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.HIERARCHICAL
    
    def __init__(self, config: PatternConfiguration = None):
        super().__init__(config)
        self.hierarchy_levels = 3
        self.level_weights = [0.5, 0.3, 0.2]  # Weights for different hierarchy levels
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        start_time = time.time()
        
        # Build hierarchy from components
        hierarchy = self._build_component_hierarchy(components)
        
        # Multi-level retrieval
        selected_components = []
        
        for level, level_components in enumerate(hierarchy):
            if level < len(self.level_weights):
                # Calculate how many components to select from this level
                level_budget = int(self.config.max_tokens * self.level_weights[level] / 200)  # Rough estimate
                
                # Score and select components from this level
                for comp in level_components:
                    comp.relevance_score = self._calculate_relevance(comp, query)
                
                level_selected = sorted(
                    level_components, 
                    key=lambda c: c.relevance_score, 
                    reverse=True
                )[:level_budget]
                
                selected_components.extend(level_selected)
        
        # Add instructions and query
        instructions = ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content="Analyze the provided hierarchical information to answer the query. Consider both high-level summaries and detailed information.",
            priority=1.0,
            relevance_score=1.0,
            source="hierarchical_instructions"
        )
        
        query_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Query: {query}",
            priority=1.0,
            relevance_score=1.0,
            source="user_query"
        )
        
        # Final assembly with token optimization
        all_components = [instructions] + selected_components + [query_component]
        final_components = self._optimize_hierarchical_assembly(all_components)
        
        assembly_time = time.time() - start_time
        
        return AssemblyResult(
            components=final_components,
            total_tokens=sum(c.token_count for c in final_components),
            assembly_time=assembly_time,
            pattern_used=self.get_pattern_type().value,
            optimization_strategy="hierarchical_multi_level",
            quality_metrics=self._calculate_hierarchical_quality(final_components, hierarchy),
            metadata={
                "hierarchy_levels": len(hierarchy),
                "level_distribution": [len(level) for level in hierarchy]
            }
        )
    
    def _build_component_hierarchy(self, components: List[ContextComponent]) -> List[List[ContextComponent]]:
        """Build hierarchy of components (simplified clustering)"""
        hierarchy = [[] for _ in range(self.hierarchy_levels)]
        
        # Simple hierarchy based on content length and specificity
        for component in components:
            if component.component_type == ComponentType.KNOWLEDGE:
                content_length = len(component.content)
                
                if content_length < 100:  # Short, specific content
                    hierarchy[0].append(component)  # Detailed level
                elif content_length < 500:  # Medium content
                    hierarchy[1].append(component)  # Summary level  
                else:  # Long content
                    hierarchy[2].append(component)  # Overview level
            else:
                # Non-knowledge components go to detailed level
                hierarchy[0].append(component)
        
        return hierarchy
    
    def _optimize_hierarchical_assembly(self, components: List[ContextComponent]) -> List[ContextComponent]:
        """Optimize assembly while preserving hierarchical structure"""
        # Separate by component type
        instructions = [c for c in components if c.component_type == ComponentType.INSTRUCTIONS]
        knowledge = [c for c in components if c.component_type == ComponentType.KNOWLEDGE]
        queries = [c for c in components if c.component_type == ComponentType.QUERY]
        others = [c for c in components if c not in instructions + knowledge + queries]
        
        # Calculate token budget
        fixed_tokens = sum(c.token_count for c in instructions + queries)
        available_tokens = self.config.max_tokens - fixed_tokens
        
        # Optimize knowledge components within budget
        current_tokens = 0
        selected_knowledge = []
        
        for component in sorted(knowledge, key=lambda c: c.relevance_score, reverse=True):
            if current_tokens + component.token_count <= available_tokens:
                selected_knowledge.append(component)
                current_tokens += component.token_count
        
        return instructions + selected_knowledge + others + queries
    
    def _calculate_hierarchical_quality(self, components: List[ContextComponent], 
                                      hierarchy: List[List[ContextComponent]]) -> Dict[str, float]:
        """Calculate quality metrics for hierarchical assembly"""
        # Level coverage: how many hierarchy levels are represented
        represented_levels = 0
        for level in hierarchy:
            if any(comp in components for comp in level):
                represented_levels += 1
        
        level_coverage = represented_levels / len(hierarchy) if hierarchy else 0.0
        
        # Hierarchical balance: distribution across levels
        level_counts = []
        for level in hierarchy:
            count = sum(1 for comp in level if comp in components)
            level_counts.append(count)
        
        total_selected = sum(level_counts)
        if total_selected > 0:
            level_entropy = -sum(
                (count / total_selected) * np.log(count / total_selected + 1e-10)
                for count in level_counts if count > 0
            )
            hierarchical_balance = level_entropy / np.log(len(hierarchy))  # Normalized
        else:
            hierarchical_balance = 0.0
        
        return {
            "level_coverage": level_coverage,
            "hierarchical_balance": hierarchical_balance,
            "total_components": len(components),
            "hierarchy_quality": (level_coverage + hierarchical_balance) / 2
        }

class GraphEnhancedRAGPattern(AssemblyPattern):
    """
    Graph-enhanced RAG pattern with knowledge graph integration
    
    Mathematical formulation: C = A(instructions, graph_traverse(entities, KG), vector_retrieve(query), query)
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.GRAPH_ENHANCED
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        start_time = time.time()
        
        # Extract entities from query
        entities = self._extract_entities(query)
        
        # Graph traversal (simulated)
        graph_components = self._simulate_graph_traversal(entities, components, kwargs)
        
        # Vector retrieval
        vector_components = [c for c in components if c.component_type == ComponentType.KNOWLEDGE]
        for comp in vector_components:
            comp.relevance_score = self._calculate_relevance(comp, query)
        
        # Fusion of graph and vector results
        fused_components = self._fuse_graph_vector_results(
            graph_components, vector_components, query
        )
        
        # Add instructions
        instructions = ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content="Use both the structured knowledge graph information and the retrieved documents to provide a comprehensive answer. Consider relationships between entities and concepts.",
            priority=1.0,
            relevance_score=1.0,
            source="graph_instructions"
        )
        
        # Add query
        query_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Query: {query}\nIdentified entities: {', '.join(entities)}",
            priority=1.0,
            relevance_score=1.0,
            source="user_query"
        )
        
        # Final assembly
        all_components = [instructions] + fused_components + [query_component]
        final_components = self.optimize_components(all_components, query)
        
        assembly_time = time.time() - start_time
        
        return AssemblyResult(
            components=final_components,
            total_tokens=sum(c.token_count for c in final_components),
            assembly_time=assembly_time,
            pattern_used=self.get_pattern_type().value,
            optimization_strategy="graph_vector_fusion",
            quality_metrics=self._calculate_graph_quality(final_components, entities),
            metadata={
                "entities_found": len(entities),
                "graph_components": len(graph_components),
                "vector_components": len(vector_components)
            }
        )
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract entities from query (simplified NER)"""
        # Simple entity extraction based on capitalization and common patterns
        import re
        
        # Find capitalized words (potential proper nouns)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', query)
        
        # Find quoted phrases
        quoted = re.findall(r'"([^"]*)"', query)
        
        # Find common entity patterns
        dates = re.findall(r'\b\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b', query)
        
        entities = list(set(capitalized + quoted + dates))
        return entities[:10]  # Limit to top 10 entities
    
    def _simulate_graph_traversal(self, entities: List[str], 
                                components: List[ContextComponent],
                                kwargs: Dict) -> List[ContextComponent]:
        """Simulate knowledge graph traversal (simplified)"""
        graph_components = []
        
        # Mock graph data (in real implementation, this would query a KG)
        mock_relationships = {
            "related_to": 0.8,
            "part_of": 0.9,
            "similar_to": 0.6,
            "caused_by": 0.7
        }
        
        for entity in entities:
            # Create mock graph component for each entity
            relationships = []
            for rel_type, confidence in mock_relationships.items():
                if entity.lower() in ["ai", "machine learning", "neural network"]:
                    relationships.append(f"{entity} {rel_type} artificial intelligence (confidence: {confidence})")
            
            if relationships:
                graph_content = f"Knowledge Graph - Entity: {entity}\nRelationships:\n" + "\n".join(relationships)
                
                graph_component = ContextComponent(
                    component_type=ComponentType.KNOWLEDGE,
                    content=graph_content,
                    priority=0.8,
                    relevance_score=0.8,
                    source="knowledge_graph",
                    metadata={"entity": entity, "relationship_count": len(relationships)}
                )
                graph_components.append(graph_component)
        
        return graph_components
    
    def _fuse_graph_vector_results(self, graph_components: List[ContextComponent],
                                 vector_components: List[ContextComponent],
                                 query: str) -> List[ContextComponent]:
        """Fuse graph and vector retrieval results"""
        # Score all components
        all_components = graph_components + vector_components
        
        for comp in all_components:
            base_score = comp.relevance_score
            
            # Boost graph components that mention query entities
            if comp.source == "knowledge_graph":
                entity_boost = 0.1 if any(entity.lower() in comp.content.lower() 
                                       for entity in query.split()) else 0.0
                comp.relevance_score = min(1.0, base_score + entity_boost)
        
        # Select top components with diversity
        fused = sorted(all_components, key=lambda c: c.relevance_score, reverse=True)
        
        # Ensure mix of graph and vector components
        selected = []
        graph_count = 0
        vector_count = 0
        max_graph = 3
        max_vector = 5
        
        for comp in fused:
            if comp.source == "knowledge_graph" and graph_count < max_graph:
                selected.append(comp)
                graph_count += 1
            elif comp.source != "knowledge_graph" and vector_count < max_vector:
                selected.append(comp)
                vector_count += 1
            
            if len(selected) >= 8:  # Limit total selection
                break
        
        return selected
    
    def _calculate_graph_quality(self, components: List[ContextComponent], 
                               entities: List[str]) -> Dict[str, float]:
        """Calculate quality metrics for graph-enhanced assembly"""
        # Entity coverage: how many identified entities are covered
        entity_coverage = 0
        for entity in entities:
            if any(entity.lower() in comp.content.lower() for comp in components):
                entity_coverage += 1
        
        entity_coverage_ratio = entity_coverage / len(entities) if entities else 0.0
        
        # Graph component ratio
        graph_components = [c for c in components if c.source == "knowledge_graph"]
        graph_ratio = len(graph_components) / len(components) if components else 0.0
        
        # Relationship density (from graph components)
        total_relationships = 0
        for comp in graph_components:
            if "relationship_count" in comp.metadata:
                total_relationships += comp.metadata["relationship_count"]
        
        relationship_density = total_relationships / len(graph_components) if graph_components else 0.0
        
        return {
            "entity_coverage": entity_coverage_ratio,
            "graph_ratio": graph_ratio,
            "relationship_density": relationship_density,
            "graph_quality": (entity_coverage_ratio + graph_ratio) / 2
        }

# ============================================================================
# FIELD THEORY PATTERNS
# ============================================================================

class FieldTheoreticPattern(AssemblyPattern):
    """
    Field-theoretic assembly pattern with semantic attractors and resonance
    
    Mathematical formulation: ∇²φ = ρ(attractors, boundaries, resonance)
    """
    
    def get_pattern_type(self) -> PatternType:
        return PatternType.FIELD_THEORETIC
    
    def __init__(self, config: PatternConfiguration = None):
        super().__init__(config)
        self.attractor_types = {
            "mythic": 0.8,
            "mathematical": 0.9,
            "metaphorical": 0.6,
            "narrative": 0.7,
            "symbolic": 0.5
        }
        self.field_strength = 1.0
        self.resonance_threshold = 0.6
    
    def assemble(self, query: str, components: List[ContextComponent], 
                **kwargs) -> AssemblyResult:
        start_time = time.time()
        
        # Identify semantic attractors in query and components
        query_attractors = self._identify_attractors(query)
        
        # Calculate field dynamics for each component
        field_components = []
        for component in components:
            component_attractors = self._identify_attractors(component.content)
            field_strength = self._calculate_field_strength(query_attractors, component_attractors)
            resonance = self._calculate_resonance(query_attractors, component_attractors)
            
            if resonance >= self.resonance_threshold:
                component.relevance_score = field_strength * resonance
                component.metadata.update({
                    "attractors": component_attractors,
                    "field_strength": field_strength,
                    "resonance": resonance
                })
                field_components.append(component)
        
        # Cross-pollination: enhance components with attractor interactions
        field_components = self._apply_cross_pollination(field_components)
        
        # Boundary tuning: adjust component boundaries for optimal field dynamics
        field_components = self._tune_boundaries(field_components, query_attractors)
        
        # Field assembly with emergence optimization
        assembled_components = self._assemble_field_components(field_components, query)
        
        # Add field-aware instructions
        field_instructions = self._generate_field_instructions(query_attractors)
        instructions_component = ContextComponent(
            component_type=ComponentType.INSTRUCTIONS,
            content=field_instructions,
            priority=1.0,
            relevance_score=1.0,
            source="field_instructions"
        )
        
        # Add query with field context
        query_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Query: {query}\nSemantic Attractors: {', '.join(query_attractors)}",
            priority=1.0,
            relevance_score=1.0,
            source="field_query"
        )
        
        final_components = [instructions_component] + assembled_components + [query_component]
        
        assembly_time = time.time() - start_time
        
        return AssemblyResult(
            components=final_components,
            total_tokens=sum(c.token_count for c in final_components),
            assembly_time=assembly_time,
            pattern_used=self.get_pattern_type().value,
            optimization_strategy="field_theoretic_resonance",
            quality_metrics=self._calculate_field_quality(final_components, query_attractors),
            metadata={
                "query_attractors": query_attractors,
                "field_strength": self.field_strength,
                "resonance_threshold": self.resonance_threshold,
                "emergent_properties": self._detect_emergence(final_components)
            }
        )
    
    def _identify_attractors(self, text: str) -> List[str]:
        """Identify semantic attractors in text"""
        attractors = []
        text_lower = text.lower()
        
        # Mythic attractors
        mythic_keywords = ["hero", "journey", "transformation", "quest", "wisdom", "power"]
        if any(keyword in text_lower for keyword in mythic_keywords):
            attractors.append("mythic")
        
        # Mathematical attractors
        math_keywords = ["algorithm", "optimization", "function", "equation", "proof", "theorem"]
        if any(keyword in text_lower for keyword in math_keywords):
            attractors.append("mathematical")
        
        # Metaphorical attractors
        metaphor_keywords = ["like", "as if", "similar to", "reminds", "metaphor", "analogy"]
        if any(keyword in text_lower for keyword in metaphor_keywords):
            attractors.append("metaphorical")
        
        # Narrative attractors
        narrative_keywords = ["story", "narrative", "once", "then", "sequence", "timeline"]
        if any(keyword in text_lower for keyword in narrative_keywords):
            attractors.append("narrative")
        
        # Symbolic attractors
        symbolic_keywords = ["symbol", "represent", "meaning", "significance", "stands for"]
        if any(keyword in text_lower for keyword in symbolic_keywords):
            attractors.append("symbolic")
        
        return list(set(attractors))
    
    def _calculate_field_strength(self, query_attractors: List[str], 
                                component_attractors: List[str]) -> float:
        """Calculate field strength between query and component attractors"""
        if not query_attractors or not component_attractors:
            return 0.1  # Minimum field strength
        
        # Calculate attractor overlap
        common_attractors = set(query_attractors).intersection(set(component_attractors))
        
        if not common_attractors:
            return 0.2  # Low field strength for non-overlapping attractors
        
        # Weight by attractor strengths
        strength = 0.0
        for attractor in common_attractors:
            strength += self.attractor_types.get(attractor, 0.5)
        
        return min(1.0, strength / len(common_attractors))
    
    def _calculate_resonance(self, query_attractors: List[str], 
                           component_attractors: List[str]) -> float:
        """Calculate resonance between attractor fields"""
        if not query_attractors or not component_attractors:
            return 0.0
        
        # Harmonic resonance calculation
        total_resonance = 0.0
        total_pairs = 0
        
        for q_attractor in query_attractors:
            for c_attractor in component_attractors:
                if q_attractor == c_attractor:
                    # Perfect resonance for identical attractors
                    total_resonance += 1.0
                else:
                    # Partial resonance for compatible attractors
                    compatibility = self._attractor_compatibility(q_attractor, c_attractor)
                    total_resonance += compatibility
                total_pairs += 1
        
        return total_resonance / total_pairs if total_pairs > 0 else 0.0
    
    def _attractor_compatibility(self, attractor1: str, attractor2: str) -> float:
        """Calculate compatibility between different attractor types"""
        compatibility_matrix = {
            ("mythic", "narrative"): 0.8,
            ("mythic", "symbolic"): 0.7,
            ("mathematical", "symbolic"): 0.6,
            ("metaphorical", "narrative"): 0.7,
            ("metaphorical", "symbolic"): 0.8,
            ("narrative", "symbolic"): 0.6
        }
        
        pair = tuple(sorted([attractor1, attractor2]))
        return compatibility_matrix.get(pair, 0.3)  # Default compatibility
    
    def _apply_cross_pollination(self, components: List[ContextComponent]) -> List[ContextComponent]:
        """Apply cross-pollination between attractor fields"""
        for i, comp1 in enumerate(components):
            for j, comp2 in enumerate(components[i+1:], i+1):
                attractors1 = comp1.metadata.get("attractors", [])
                attractors2 = comp2.metadata.get("attractors", [])
                
                # Check for cross-pollination potential
                if attractors1 and attractors2:
                    compatibility = max(
                        self._attractor_compatibility(a1, a2)
                        for a1 in attractors1 for a2 in attractors2
                    )
                    
                    if compatibility > 0.6:
                        # Boost relevance through cross-pollination
                        boost = compatibility * 0.1
                        comp1.relevance_score = min(1.0, comp1.relevance_score + boost)
                        comp2.relevance_score = min(1.0, comp2.relevance_score + boost)
                        
                        # Add cross-pollination metadata
                        comp1.metadata["cross_pollination"] = comp1.metadata.get("cross_pollination", [])
                        comp1.metadata["cross_pollination"].append({
                            "with_component": j,
                            "compatibility": compatibility
                        })
        
        return components
    
    def _tune_boundaries(self, components: List[ContextComponent], 
                        query_attractors: List[str]) -> List[ContextComponent]:
        """Tune component boundaries for optimal field dynamics"""
        for component in components:
            component_attractors = component.metadata.get("attractors", [])
            
            # Adaptive boundary tuning based on attractor alignment
            alignment = len(set(query_attractors).intersection(set(component_attractors)))
            max_alignment = max(len(query_attractors), len(component_attractors))
            
            if max_alignment > 0:
                boundary_permeability = alignment / max_alignment
                
                # Adjust component priority based on boundary permeability
                component.priority *= (1 + boundary_permeability * 0.5)
                component.metadata["boundary_permeability"] = boundary_permeability
        
        return components
    
    def _assemble_field_components(self, components: List[ContextComponent], 
                                 query: str) -> List[ContextComponent]:
        """Assemble components using field optimization"""
        # Sort by field strength and resonance
        components.sort(
            key=lambda c: (
                c.metadata.get("field_strength", 0) * 
                c.metadata.get("resonance", 0) * 
                c.priority
            ),
            reverse=True
        )
        
        # Select components with field dynamics consideration
        selected = []
        total_tokens = 0
        current_field_strength = 0.0
        
        for component in components:
            if total_tokens + component.token_count <= self.config.max_tokens:
                selected.append(component)
                total_tokens += component.token_count
                current_field_strength += component.metadata.get("field_strength", 0)
                
                # Field saturation check
                if current_field_strength >= 3.0:  # Field saturation threshold
                    break
        
        return selected
    
    def _generate_field_instructions(self, query_attractors: List[str]) -> str:
        """Generate field-aware instructions"""
        base_instructions = """You are operating within a semantic field framework. Consider the harmonic resonance between different conceptual attractors when formulating your response."""
        
        if query_attractors:
            attractor_guidance = f"""
The query exhibits the following semantic attractors: {', '.join(query_attractors)}

Respond in a way that:
1. Honors the attractor dynamics present in the query
2. Creates harmonic resonance with the identified attractors
3. Allows for emergent properties to arise from attractor interactions
4. Maintains field coherence while enabling creative synthesis"""
        else:
            attractor_guidance = """
No strong attractors detected. Maintain open field dynamics and allow natural emergence."""
        
        return base_instructions + attractor_guidance
    
    def _detect_emergence(self, components: List[ContextComponent]) -> Dict[str, Any]:
        """Detect emergent properties in assembled field"""
        all_attractors = []
        for component in components:
            attractors = component.metadata.get("attractors", [])
            all_attractors.extend(attractors)
        
        # Attractor diversity
        unique_attractors = list(set(all_attractors))
        attractor_diversity = len(unique_attractors)
        
        # Cross-pollination events
        cross_pollination_events = 0
        for component in components:
            events = component.metadata.get("cross_pollination", [])
            cross_pollination_events += len(events)
        
        # Field coherence
        field_strengths = [
            component.metadata.get("field_strength", 0) 
            for component in components
        ]
        field_coherence = np.std(field_strengths) if field_strengths else 0.0
        
        return {
            "attractor_diversity": attractor_diversity,
            "cross_pollination_events": cross_pollination_events,
            "field_coherence": 1.0 / (1.0 + field_coherence),  # Inverse of standard deviation
            "emergence_potential": min(1.0, attractor_diversity * 0.2 + cross_pollination_events * 0.1)
        }
    
    def _calculate_field_quality(self, components: List[ContextComponent], 
                               query_attractors: List[str]) -> Dict[str, float]:
        """Calculate field-specific quality metrics"""
        # Attractor coverage
        component_attractors = []
        for component in components:
            attractors = component.metadata.get("attractors", [])
            component_attractors.extend(attractors)
        
        covered_attractors = set(query_attractors).intersection(set(component_attractors))
        attractor_coverage = len(covered_attractors) / len(query_attractors) if query_attractors else 0.0
        
        # Field harmony (resonance distribution)
        resonance_values = [
            component.metadata.get("resonance", 0) 
            for component in components
        ]
        field_harmony = np.mean(resonance_values) if resonance_values else 0.0
        
        # Emergence metrics
        emergence_data = self._detect_emergence(components)
        emergence_score = emergence_data.get("emergence_potential", 0.0)
        
        return {
            "attractor_coverage": attractor_coverage,
            "field_harmony": field_harmony,
            "emergence_score": emergence_score,
            "field_quality": (attractor_coverage + field_harmony + emergence_score) / 3
        }

# ============================================================================
# PATTERN REGISTRY AND FACTORY
# ============================================================================

class PatternRegistry:
    """Registry for managing and instantiating assembly patterns"""
    
    def __init__(self):
        self._patterns = {}
        self._register_default_patterns()
    
    def _register_default_patterns(self):
        """Register default pattern implementations"""
        self._patterns.update({
            PatternType.BASIC_RAG: BasicRAGPattern,
            PatternType.ENHANCED_RAG: EnhancedRAGPattern,
            PatternType.AGENT_WORKFLOW: AgentWorkflowPattern,
            PatternType.HIERARCHICAL: HierarchicalRAGPattern,
            PatternType.GRAPH_ENHANCED: GraphEnhancedRAGPattern,
            PatternType.FIELD_THEORETIC: FieldTheoreticPattern
        })
    
    def register_pattern(self, pattern_type: PatternType, pattern_class: type):
        """Register a custom pattern implementation"""
        if not issubclass(pattern_class, AssemblyPattern):
            raise ValueError("Pattern class must inherit from AssemblyPattern")
        
        self._patterns[pattern_type] = pattern_class
    
    def create_pattern(self, pattern_type: PatternType, 
                      config: PatternConfiguration = None) -> AssemblyPattern:
        """Create and configure a pattern instance"""
        if pattern_type not in self._patterns:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        pattern_class = self._patterns[pattern_type]
        return pattern_class(config)
    
    def list_patterns(self) -> List[PatternType]:
        """List available pattern types"""
        return list(self._patterns.keys())

# ============================================================================
# INTELLIGENT PATTERN SELECTION
# ============================================================================

class PatternSelector:
    """Intelligent pattern selection based on query analysis"""
    
    def __init__(self, registry: PatternRegistry):
        self.registry = registry
        self.selection_rules = self._build_selection_rules()
    
    def _build_selection_rules(self) -> List[Dict]:
        """Build pattern selection rules"""
        return [
            {
                "conditions": ["tools" in "keywords", "agent" in "keywords", "action" in "keywords"],
                "pattern": PatternType.AGENT_WORKFLOW,
                "confidence": 0.9
            },
            {
                "conditions": ["hierarchy" in "keywords", "levels" in "keywords", "summary" in "keywords"],
                "pattern": PatternType.HIERARCHICAL,
                "confidence": 0.8
            },
            {
                "conditions": ["entity" in "keywords", "relationship" in "keywords", "graph" in "keywords"],
                "pattern": PatternType.GRAPH_ENHANCED,
                "confidence": 0.8
            },
            {
                "conditions": ["metaphor" in "keywords", "symbolic" in "keywords", "emergence" in "keywords"],
                "pattern": PatternType.FIELD_THEORETIC,
                "confidence": 0.7
            },
            {
                "conditions": ["rerank" in "keywords", "diversity" in "keywords", "enhanced" in "keywords"],
                "pattern": PatternType.ENHANCED_RAG,
                "confidence": 0.7
            },
            {
                "conditions": ["simple" in "keywords", "basic" in "keywords"],
                "pattern": PatternType.BASIC_RAG,
                "confidence": 0.9
            }
        ]
    
    def select_pattern(self, query: str, components: List[ContextComponent], 
                      **kwargs) -> Tuple[PatternType, float]:
        """Select optimal pattern based on query and context analysis"""
        query_lower = query.lower()
        
        # Analyze query characteristics
        query_features = self._analyze_query(query, components, **kwargs)
        
        # Apply selection rules
        pattern_scores = defaultdict(float)
        
        for rule in self.selection_rules:
            score = self._evaluate_rule(rule, query_features)
            if score > 0:
                pattern_scores[rule["pattern"]] += score * rule["confidence"]
        
        # Add component-based scoring
        component_scores = self._analyze_components(components)
        for pattern, score in component_scores.items():
            pattern_scores[pattern] += score
        
        # Add context-based scoring
        context_scores = self._analyze_context(**kwargs)
        for pattern, score in context_scores.items():
            pattern_scores[pattern] += score
        
        # Select best pattern
        if pattern_scores:
            best_pattern = max(pattern_scores.items(), key=lambda x: x[1])
            return best_pattern
        else:
            # Default fallback
            return PatternType.BASIC_RAG, 0.5
    
    def _analyze_query(self, query: str, components: List[ContextComponent], 
                      **kwargs) -> Dict[str, Any]:
        """Analyze query characteristics for pattern selection"""
        query_lower = query.lower()
        
        features = {
            "keywords": query_lower.split(),
            "length": len(query),
            "complexity": self._estimate_complexity(query),
            "question_type": self._identify_question_type(query),
            "entities": self._count_entities(query),
            "temporal_indicators": self._has_temporal_indicators(query)
        }
        
        return features
    
    def _estimate_complexity(self, query: str) -> float:
        """Estimate query complexity"""
        factors = [
            len(query.split()) / 10.0,  # Length factor
            query.count("?") / 3.0,  # Multiple questions
            query.count("and") / 2.0,  # Conjunctions
            query.count("or") / 2.0,  # Disjunctions
        ]
        return min(1.0, sum(factors))
    
    def _identify_question_type(self, query: str) -> str:
        """Identify the type of question"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["what", "who", "where", "when"]):
            return "factual"
        elif any(word in query_lower for word in ["how", "why"]):
            return "explanatory"
        elif any(word in query_lower for word in ["compare", "analyze", "evaluate"]):
            return "analytical"
        elif any(word in query_lower for word in ["create", "generate", "build"]):
            return "creative"
        else:
            return "general"
    
    def _count_entities(self, query: str) -> int:
        """Count potential entities in query"""
        import re
        # Simple entity counting based on capitalization
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', query)
        return len(capitalized)
    
    def _has_temporal_indicators(self, query: str) -> bool:
        """Check for temporal indicators in query"""
        temporal_words = ["recent", "latest", "current", "now", "today", "yesterday", "timeline"]
        return any(word in query.lower() for word in temporal_words)
    
    def _analyze_components(self, components: List[ContextComponent]) -> Dict[PatternType, float]:
        """Analyze components to suggest suitable patterns"""
        scores = defaultdict(float)
        
        # Count component types
        type_counts = defaultdict(int)
        for component in components:
            type_counts[component.component_type] += 1
        
        # Pattern suggestions based on component types
        if type_counts[ComponentType.TOOLS] > 0:
            scores[PatternType.AGENT_WORKFLOW] += 0.3
        
        if type_counts[ComponentType.KNOWLEDGE] > 5:
            scores[PatternType.HIERARCHICAL] += 0.2
            scores[PatternType.ENHANCED_RAG] += 0.2
        
        if type_counts[ComponentType.MEMORY] > 0:
            scores[PatternType.AGENT_WORKFLOW] += 0.1
        
        # Check for graph-like metadata
        graph_indicators = 0
        for component in components:
            if any(keyword in component.content.lower() 
                  for keyword in ["entity", "relationship", "connected", "network"]):
                graph_indicators += 1
        
        if graph_indicators > 0:
            scores[PatternType.GRAPH_ENHANCED] += 0.3
        
        return scores
    
    def _analyze_context(self, **kwargs) -> Dict[PatternType, float]:
        """Analyze context parameters for pattern suggestions"""
        scores = defaultdict(float)
        
        if "available_tools" in kwargs and kwargs["available_tools"]:
            scores[PatternType.AGENT_WORKFLOW] += 0.4
        
        if "task_complexity" in kwargs:
            complexity = kwargs["task_complexity"]
            if complexity == "complex":
                scores[PatternType.HIERARCHICAL] += 0.2
                scores[PatternType.ENHANCED_RAG] += 0.2
        
        if "domain" in kwargs:
            domain = kwargs["domain"].lower()
            if domain in ["research", "academic"]:
                scores[PatternType.HIERARCHICAL] += 0.2
            elif domain in ["creative", "artistic"]:
                scores[PatternType.FIELD_THEORETIC] += 0.3
        
        return scores
    
    def _evaluate_rule(self, rule: Dict, query_features: Dict) -> float:
        """Evaluate a selection rule against query features"""
        keywords = query_features.get("keywords", [])
        
        # Simple keyword matching (can be enhanced with more sophisticated NLP)
        matches = 0
        for condition in rule["conditions"]:
            condition_keywords = condition.split()
            if any(keyword in keywords for keyword in condition_keywords):
                matches += 1
        
        return matches / len(rule["conditions"]) if rule["conditions"] else 0.0

# ============================================================================
# PRODUCTION ASSEMBLY ORCHESTRATOR
# ============================================================================

class ProductionAssemblyOrchestrator:
    """
    Production-ready orchestrator for context assembly patterns
    
    Provides high-level interface with monitoring, caching, and optimization
    """
    
    def __init__(self, config: PatternConfiguration = None):
        self.config = config or PatternConfiguration()
        self.registry = PatternRegistry()
        self.selector = PatternSelector(self.registry)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Performance monitoring
        self.metrics = defaultdict(list)
        self._lock = threading.Lock()
        
        # Pattern cache for frequently used patterns
        self.pattern_cache = {}
    
    async def assemble_async(self, query: str, components: List[ContextComponent], 
                           pattern_type: Optional[PatternType] = None,
                           **kwargs) -> AssemblyResult:
        """Asynchronous context assembly"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.assemble, query, components, pattern_type, **kwargs
        )
    
    def assemble(self, query: str, components: List[ContextComponent], 
                pattern_type: Optional[PatternType] = None,
                **kwargs) -> AssemblyResult:
        """
        Main assembly interface with intelligent pattern selection
        
        Args:
            query: User query or request
            components: Available context components
            pattern_type: Optional pattern override
            **kwargs: Additional pattern-specific parameters
            
        Returns:
            AssemblyResult with optimized context and comprehensive metadata
        """
        start_time = time.time()
        
        try:
            # Pattern selection
            if pattern_type is None:
                selected_pattern_type, confidence = self.selector.select_pattern(
                    query, components, **kwargs
                )
                self.logger.info(f"Auto-selected pattern: {selected_pattern_type.value} "
                               f"(confidence: {confidence:.2f})")
            else:
                selected_pattern_type = pattern_type
                confidence = 1.0
            
            # Get or create pattern instance
            pattern = self._get_pattern_instance(selected_pattern_type)
            
            # Execute assembly
            result = pattern.assemble(query, components, **kwargs)
            
            # Add orchestrator metadata
            result.metadata.update({
                "pattern_selection_confidence": confidence,
                "auto_selected": pattern_type is None,
                "orchestrator_version": "1.0.0"
            })
            
            # Record metrics
            total_time = time.time() - start_time
            self._record_metric("total_assembly_time", total_time)
            self._record_metric("pattern_usage", selected_pattern_type.value)
            self._record_metric("success_rate", 1.0)
            
            self.logger.info(f"Assembly completed in {total_time:.3f}s using {selected_pattern_type.value}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Assembly failed: {str(e)}")
            self._record_metric("success_rate", 0.0)
            
            # Return fallback result
            fallback_result = self._create_fallback_result(query, components)
            return fallback_result
    
    def _get_pattern_instance(self, pattern_type: PatternType) -> AssemblyPattern:
        """Get cached or create new pattern instance"""
        if pattern_type not in self.pattern_cache:
            self.pattern_cache[pattern_type] = self.registry.create_pattern(
                pattern_type, self.config
            )
        
        return self.pattern_cache[pattern_type]
    
    def _create_fallback_result(self, query: str, 
                              components: List[ContextComponent]) -> AssemblyResult:
        """Create fallback result when assembly fails"""
        # Simple fallback: return basic components with query
        fallback_components = components[:3]  # Limit to first 3 components
        
        query_component = ContextComponent(
            component_type=ComponentType.QUERY,
            content=f"Query: {query}",
            priority=1.0,
            relevance_score=1.0,
            source="fallback"
        )
        
        fallback_components.append(query_component)
        
        return AssemblyResult(
            components=fallback_components,
            total_tokens=sum(c.token_count for c in fallback_components),
            assembly_time=0.0,
            pattern_used="fallback",
            optimization_strategy="emergency_fallback",
            quality_metrics={"fallback": True},
            metadata={"is_fallback": True}
        )
    
    def _record_metric(self, metric_name: str, value: Any):
        """Record performance metric"""
        with self._lock:
            self.metrics[metric_name].append({
                "value": value,
                "timestamp": time.time()
            })
            
            # Keep only recent metrics
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-1000:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        with self._lock:
            report = {
                "total_assemblies": len(self.metrics.get("total_assembly_time", [])),
                "success_rate": np.mean([m["value"] for m in self.metrics.get("success_rate", [])]),
                "average_assembly_time": np.mean([m["value"] for m in self.metrics.get("total_assembly_time", [])]),
                "pattern_usage": self._calculate_pattern_usage(),
                "performance_trends": self._calculate_performance_trends()
            }
            
            return report
    
    def _calculate_pattern_usage(self) -> Dict[str, int]:
        """Calculate pattern usage statistics"""
        pattern_counts = defaultdict(int)
        for metric in self.metrics.get("pattern_usage", []):
            pattern_counts[metric["value"]] += 1
        return dict(pattern_counts)
    
    def _calculate_performance_trends(self) -> Dict[str, float]:
        """Calculate performance trends"""
        trends = {}
        
        # Assembly time trend
        assembly_times = [m["value"] for m in self.metrics.get("total_assembly_time", [])]
        if len(assembly_times) > 10:
            recent_avg = np.mean(assembly_times[-10:])
            overall_avg = np.mean(assembly_times)
            trends["assembly_time_trend"] = (recent_avg - overall_avg) / overall_avg
        
        return trends

# ============================================================================
# USAGE EXAMPLE AND TESTING
# ============================================================================

def demo_assembly_patterns():
    """Demonstrate assembly pattern usage"""
    print("Context Engineering - Assembly Patterns Demo")
    print("=" * 50)
    
    # Create orchestrator
    config = PatternConfiguration(
        max_tokens=2000,
        min_relevance=0.3,
        enable_caching=True
    )
    orchestrator = ProductionAssemblyOrchestrator(config)
    
    # Sample components
    components = [
        ContextComponent(
            component_type=ComponentType.KNOWLEDGE,
            content="Context engineering involves optimizing information payloads for large language models through systematic assembly of relevant components.",
            relevance_score=0.9,
            source="knowledge_base"
        ),
        ContextComponent(
            component_type=ComponentType.KNOWLEDGE,
            content="RAG systems combine retrieval mechanisms with generation capabilities to provide more accurate and contextual responses.",
            relevance_score=0.8,
            source="knowledge_base"
        ),
        ContextComponent(
            component_type=ComponentType.TOOLS,
            content="Available tools: web_search, calculator, document_reader",
            relevance_score=0.7,
            source="tool_registry"
        )
    ]
    
    # Test different queries and pattern selection
    test_queries = [
        "Explain context engineering principles",
        "How can I use tools to solve complex problems?",
        "Analyze the relationship between RAG and context optimization"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 30)
        
        result = orchestrator.assemble(query, components)
        
        print(f"Pattern used: {result.pattern_used}")
        print(f"Components: {len(result.components)}")
        print(f"Total tokens: {result.total_tokens}")
        print(f"Assembly time: {result.assembly_time:.3f}s")
        print(f"Quality score: {result.quality_metrics.get('overall_quality', 'N/A')}")
    
    # Performance report
    print("\n" + "=" * 50)
    print("Performance Report:")
    print("=" * 50)
    
    report = orchestrator.get_performance_report()
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run demo
    demo_assembly_patterns()
