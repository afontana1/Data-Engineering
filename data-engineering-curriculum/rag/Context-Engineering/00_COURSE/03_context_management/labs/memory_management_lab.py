"""
Memory Management Lab - Context Engineering
==========================================

A comprehensive implementation of memory hierarchies and context management
for large language model applications. This lab provides both educational
demonstrations and production-ready components for managing context windows,
memory hierarchies, and performance optimization.

Mathematical Foundation:
    Context Assembly: C = A(c_instr, c_know, c_tools, c_mem, c_state, c_query)
    Memory Optimization: M* = argmax_M E[Reward(LLM(C_M), target)] s.t. |C| ≤ L_max

Authors: Context Engineering Research Group
License: MIT
"""

import json
import time
import hashlib
import threading
from abc import ABC, abstractmethod
from collections import defaultdict, OrderedDict
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from datetime import datetime, timedelta
import heapq
import pickle
import gzip
import sys
from contextlib import contextmanager


# =============================================================================
# Core Memory Abstractions
# =============================================================================

@dataclass
class MemoryEntry:
    """Fundamental unit of memory storage with metadata."""
    content: str
    timestamp: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    priority: float = 1.0
    size_bytes: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.size_bytes == 0:
            self.size_bytes = sys.getsizeof(self.content)
        if self.last_accessed is None:
            self.last_accessed = self.timestamp
    
    def access(self) -> None:
        """Update access statistics."""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def decay_priority(self, decay_rate: float = 0.95) -> None:
        """Apply temporal decay to priority."""
        self.priority *= decay_rate
    
    def compute_score(self, query_embedding: Optional[List[float]] = None) -> float:
        """Compute relevance score for retrieval."""
        # Basic scoring combining recency, frequency, and priority
        recency_score = 1.0 / (1.0 + (datetime.now() - self.last_accessed).total_seconds() / 3600)
        frequency_score = min(self.access_count / 10.0, 1.0)  # Normalize to [0,1]
        
        base_score = (recency_score * 0.4 + frequency_score * 0.3 + self.priority * 0.3)
        
        # TODO: Add semantic similarity if query_embedding provided
        return base_score


class MemoryInterface(ABC):
    """Abstract interface for memory systems."""
    
    @abstractmethod
    def store(self, key: str, entry: MemoryEntry) -> bool:
        """Store a memory entry."""
        pass
    
    @abstractmethod
    def retrieve(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry."""
        pass
    
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, MemoryEntry]]:
        """Search for relevant memories."""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Return current memory usage in bytes."""
        pass
    
    @abstractmethod
    def cleanup(self) -> int:
        """Clean up expired/low-priority memories. Returns bytes freed."""
        pass


# =============================================================================
# Memory Layer Implementations
# =============================================================================

class WorkingMemory(MemoryInterface):
    """
    High-speed, limited capacity memory for immediate context.
    Implements LRU eviction with priority considerations.
    """
    
    def __init__(self, max_size_bytes: int = 50000, max_entries: int = 100):
        self.max_size_bytes = max_size_bytes
        self.max_entries = max_entries
        self.memory: OrderedDict[str, MemoryEntry] = OrderedDict()
        self.current_size = 0
        self._lock = threading.RLock()
    
    def store(self, key: str, entry: MemoryEntry) -> bool:
        """Store entry with LRU eviction."""
        with self._lock:
            # Remove if already exists (for update)
            if key in self.memory:
                old_entry = self.memory.pop(key)
                self.current_size -= old_entry.size_bytes
            
            # Check if we need to evict
            while (self.current_size + entry.size_bytes > self.max_size_bytes or
                   len(self.memory) >= self.max_entries):
                if not self.memory:
                    return False  # Can't fit even with empty memory
                self._evict_lru()
            
            # Store new entry
            self.memory[key] = entry
            self.current_size += entry.size_bytes
            return True
    
    def retrieve(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve and mark as recently used."""
        with self._lock:
            if key in self.memory:
                entry = self.memory.pop(key)  # Remove from current position
                entry.access()
                self.memory[key] = entry  # Add to end (most recent)
                return entry
            return None
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, MemoryEntry]]:
        """Simple substring search with scoring."""
        with self._lock:
            results = []
            query_lower = query.lower()
            
            for key, entry in self.memory.items():
                if query_lower in entry.content.lower():
                    score = entry.compute_score()
                    results.append((score, key, entry))
            
            # Sort by score descending and return top results
            results.sort(reverse=True, key=lambda x: x[0])
            return [(key, entry) for _, key, entry in results[:limit]]
    
    def size(self) -> int:
        return self.current_size
    
    def cleanup(self) -> int:
        """Remove entries with very low priority."""
        with self._lock:
            initial_size = self.current_size
            to_remove = []
            
            for key, entry in self.memory.items():
                if entry.priority < 0.1:  # Very low priority threshold
                    to_remove.append(key)
            
            for key in to_remove:
                entry = self.memory.pop(key)
                self.current_size -= entry.size_bytes
            
            return initial_size - self.current_size
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if self.memory:
            key, entry = self.memory.popitem(last=False)
            self.current_size -= entry.size_bytes


class LongTermMemory(MemoryInterface):
    """
    Large capacity memory with persistent storage and compression.
    Implements importance-based retention and semantic organization.
    """
    
    def __init__(self, max_size_bytes: int = 10_000_000, persistence_file: Optional[str] = None):
        self.max_size_bytes = max_size_bytes
        self.persistence_file = persistence_file
        self.memory: Dict[str, MemoryEntry] = {}
        self.current_size = 0
        self.importance_index = []  # Min-heap for eviction by importance
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        self._lock = threading.RLock()
        
        # Load from persistence if available
        if persistence_file:
            self._load_from_disk()
    
    def store(self, key: str, entry: MemoryEntry) -> bool:
        """Store with importance-based eviction."""
        with self._lock:
            # Remove if already exists
            if key in self.memory:
                old_entry = self.memory.pop(key)
                self.current_size -= old_entry.size_bytes
                self._remove_from_indices(key, old_entry)
            
            # Evict low-importance entries if needed
            while self.current_size + entry.size_bytes > self.max_size_bytes:
                if not self._evict_lowest_importance():
                    return False
            
            # Store entry
            self.memory[key] = entry
            self.current_size += entry.size_bytes
            
            # Update indices
            heapq.heappush(self.importance_index, (entry.priority, key))
            for tag in entry.tags:
                self.tag_index[tag].append(key)
            
            # Persist if configured
            if self.persistence_file and len(self.memory) % 100 == 0:  # Batch persist
                self._save_to_disk()
            
            return True
    
    def retrieve(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve without affecting storage order."""
        with self._lock:
            entry = self.memory.get(key)
            if entry:
                entry.access()
            return entry
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, MemoryEntry]]:
        """Advanced search with tag-based and content-based matching."""
        with self._lock:
            results = []
            query_lower = query.lower()
            query_tags = set(query.split())  # Simple tag extraction
            
            for key, entry in self.memory.items():
                score = 0.0
                
                # Content matching
                if query_lower in entry.content.lower():
                    score += 0.5
                
                # Tag matching
                tag_overlap = len(query_tags.intersection(set(entry.tags)))
                if tag_overlap > 0:
                    score += 0.3 * (tag_overlap / len(query_tags))
                
                # Importance and recency
                score += entry.compute_score() * 0.2
                
                if score > 0:
                    results.append((score, key, entry))
            
            # Sort by score and return top results
            results.sort(reverse=True, key=lambda x: x[0])
            return [(key, entry) for _, key, entry in results[:limit]]
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[Tuple[str, MemoryEntry]]:
        """Search specifically by tags."""
        with self._lock:
            candidate_keys = set()
            for tag in tags:
                candidate_keys.update(self.tag_index.get(tag, []))
            
            results = []
            for key in candidate_keys:
                if key in self.memory:
                    entry = self.memory[key]
                    tag_score = len(set(tags).intersection(set(entry.tags))) / len(tags)
                    total_score = tag_score * 0.7 + entry.compute_score() * 0.3
                    results.append((total_score, key, entry))
            
            results.sort(reverse=True, key=lambda x: x[0])
            return [(key, entry) for _, key, entry in results[:limit]]
    
    def size(self) -> int:
        return self.current_size
    
    def cleanup(self) -> int:
        """Remove expired and low-importance entries."""
        with self._lock:
            initial_size = self.current_size
            cutoff_time = datetime.now() - timedelta(days=30)  # 30-day expiry
            to_remove = []
            
            for key, entry in self.memory.items():
                # Remove very old, unused entries
                if (entry.last_accessed < cutoff_time and 
                    entry.access_count < 3 and 
                    entry.priority < 0.2):
                    to_remove.append(key)
            
            for key in to_remove:
                self._remove_entry(key)
            
            freed = initial_size - self.current_size
            
            # Persist changes
            if self.persistence_file and freed > 0:
                self._save_to_disk()
            
            return freed
    
    def _evict_lowest_importance(self) -> bool:
        """Evict the lowest importance entry."""
        while self.importance_index:
            priority, key = heapq.heappop(self.importance_index)
            if key in self.memory:
                self._remove_entry(key)
                return True
        return False
    
    def _remove_entry(self, key: str) -> None:
        """Remove entry and clean up indices."""
        if key in self.memory:
            entry = self.memory.pop(key)
            self.current_size -= entry.size_bytes
            self._remove_from_indices(key, entry)
    
    def _remove_from_indices(self, key: str, entry: MemoryEntry) -> None:
        """Clean up tag indices."""
        for tag in entry.tags:
            if key in self.tag_index[tag]:
                self.tag_index[tag].remove(key)
                if not self.tag_index[tag]:
                    del self.tag_index[tag]
    
    def _save_to_disk(self) -> None:
        """Persist memory to disk with compression."""
        if not self.persistence_file:
            return
        
        try:
            data = {
                'memory': {k: asdict(v) for k, v in self.memory.items()},
                'tag_index': dict(self.tag_index),
                'timestamp': datetime.now().isoformat()
            }
            
            with gzip.open(self.persistence_file, 'wt', encoding='utf-8') as f:
                json.dump(data, f, default=str)
        except Exception as e:
            print(f"Failed to save memory to disk: {e}")
    
    def _load_from_disk(self) -> None:
        """Load memory from disk."""
        if not self.persistence_file:
            return
        
        try:
            with gzip.open(self.persistence_file, 'rt', encoding='utf-8') as f:
                data = json.load(f)
            
            # Reconstruct memory entries
            for key, entry_data in data.get('memory', {}).items():
                # Convert timestamp strings back to datetime
                entry_data['timestamp'] = datetime.fromisoformat(entry_data['timestamp'])
                if entry_data.get('last_accessed'):
                    entry_data['last_accessed'] = datetime.fromisoformat(entry_data['last_accessed'])
                
                entry = MemoryEntry(**entry_data)
                self.memory[key] = entry
                self.current_size += entry.size_bytes
                
                # Rebuild indices
                heapq.heappush(self.importance_index, (entry.priority, key))
                for tag in entry.tags:
                    self.tag_index[tag].append(key)
                    
        except Exception as e:
            print(f"Failed to load memory from disk: {e}")


# =============================================================================
# Hierarchical Memory System
# =============================================================================

class HierarchicalMemorySystem:
    """
    Multi-layer memory system combining working memory, long-term memory,
    and external knowledge retrieval with intelligent promotion/demotion.
    """
    
    def __init__(self,
                 working_memory_size: int = 50000,
                 long_term_memory_size: int = 10_000_000,
                 persistence_file: Optional[str] = None,
                 external_retriever: Optional[Callable] = None):
        
        self.working_memory = WorkingMemory(working_memory_size)
        self.long_term_memory = LongTermMemory(long_term_memory_size, persistence_file)
        self.external_retriever = external_retriever
        
        # Statistics
        self.stats = {
            'working_memory_hits': 0,
            'long_term_memory_hits': 0,
            'external_retrieval_calls': 0,
            'promotions': 0,
            'demotions': 0
        }
        
        self._lock = threading.RLock()
    
    def store(self, key: str, content: str, tags: List[str] = None, priority: float = 1.0) -> bool:
        """Store content in appropriate memory layer."""
        if tags is None:
            tags = []
        
        entry = MemoryEntry(
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            tags=tags
        )
        
        # Always try working memory first for immediate access
        success = self.working_memory.store(key, entry)
        
        # Also store in long-term memory if important enough
        if priority > 0.5 or len(tags) > 0:
            self.long_term_memory.store(key, entry)
        
        return success
    
    def retrieve(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve from memory hierarchy with automatic promotion."""
        with self._lock:
            # Check working memory first
            entry = self.working_memory.retrieve(key)
            if entry:
                self.stats['working_memory_hits'] += 1
                return entry
            
            # Check long-term memory
            entry = self.long_term_memory.retrieve(key)
            if entry:
                self.stats['long_term_memory_hits'] += 1
                
                # Promote to working memory if frequently accessed
                if entry.access_count > 3 or entry.priority > 0.7:
                    self.working_memory.store(key, entry)
                    self.stats['promotions'] += 1
                
                return entry
            
            return None
    
    def search(self, query: str, limit: int = 10, include_external: bool = False) -> List[Tuple[str, MemoryEntry]]:
        """Comprehensive search across all memory layers."""
        results = []
        
        # Search working memory
        wm_results = self.working_memory.search(query, limit)
        results.extend(wm_results)
        
        # Search long-term memory
        ltm_limit = max(0, limit - len(wm_results))
        if ltm_limit > 0:
            ltm_results = self.long_term_memory.search(query, ltm_limit)
            
            # Filter out duplicates from working memory
            wm_keys = {key for key, _ in wm_results}
            ltm_filtered = [(key, entry) for key, entry in ltm_results if key not in wm_keys]
            results.extend(ltm_filtered)
        
        # External retrieval if enabled and needed
        if include_external and self.external_retriever and len(results) < limit:
            try:
                external_limit = limit - len(results)
                external_results = self.external_retriever(query, external_limit)
                self.stats['external_retrieval_calls'] += 1
                
                # Convert external results to memory entries and store
                for ext_key, ext_content in external_results:
                    ext_entry = MemoryEntry(
                        content=ext_content,
                        timestamp=datetime.now(),
                        priority=0.3,  # Lower priority for external content
                        tags=['external']
                    )
                    self.long_term_memory.store(ext_key, ext_entry)
                    results.append((ext_key, ext_entry))
                    
            except Exception as e:
                print(f"External retrieval failed: {e}")
        
        return results[:limit]
    
    def optimize(self) -> Dict[str, int]:
        """Optimize memory usage and return statistics."""
        with self._lock:
            # Cleanup both layers
            wm_freed = self.working_memory.cleanup()
            ltm_freed = self.long_term_memory.cleanup()
            
            # Apply priority decay to prevent stale high-priority entries
            for entry in self.long_term_memory.memory.values():
                if entry.last_accessed < datetime.now() - timedelta(days=7):
                    entry.decay_priority()
            
            # Demote rarely accessed entries from working memory
            to_demote = []
            for key, entry in self.working_memory.memory.items():
                if (entry.access_count < 2 and 
                    entry.last_accessed < datetime.now() - timedelta(hours=6)):
                    to_demote.append(key)
            
            for key in to_demote:
                entry = self.working_memory.memory.get(key)
                if entry:
                    # Move to long-term memory
                    self.long_term_memory.store(key, entry)
                    # Remove from working memory (will be handled by normal eviction)
                    self.stats['demotions'] += 1
            
            return {
                'working_memory_freed': wm_freed,
                'long_term_memory_freed': ltm_freed,
                'demotions': len(to_demote),
                'working_memory_size': self.working_memory.size(),
                'long_term_memory_size': self.long_term_memory.size(),
                'working_memory_entries': len(self.working_memory.memory),
                'long_term_memory_entries': len(self.long_term_memory.memory)
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Return comprehensive memory system statistics."""
        return {
            **self.stats,
            'working_memory_utilization': self.working_memory.size() / self.working_memory.max_size_bytes,
            'long_term_memory_utilization': self.long_term_memory.size() / self.long_term_memory.max_size_bytes,
            'total_memory_entries': len(self.working_memory.memory) + len(self.long_term_memory.memory),
            'hit_rate': (self.stats['working_memory_hits'] + self.stats['long_term_memory_hits']) / 
                       max(1, sum(self.stats[k] for k in ['working_memory_hits', 'long_term_memory_hits', 'external_retrieval_calls']))
        }


# =============================================================================
# Context Window Manager
# =============================================================================

class ContextWindowManager:
    """
    Manages context window constraints with intelligent content selection,
    compression, and assembly optimization.
    """
    
    def __init__(self,
                 max_tokens: int = 4000,
                 memory_system: Optional[HierarchicalMemorySystem] = None,
                 tokenizer: Optional[Callable] = None):
        
        self.max_tokens = max_tokens
        self.memory_system = memory_system or HierarchicalMemorySystem()
        
        # Default tokenizer (simple word-based approximation)
        self.tokenizer = tokenizer or (lambda text: len(text.split()) * 1.3)
        
        # Reserved token allocations
        self.token_allocations = {
            'system_instructions': 0.15,  # 15% for system prompts
            'user_query': 0.20,          # 20% for user input
            'retrieved_context': 0.50,   # 50% for retrieved information
            'response_buffer': 0.15      # 15% reserved for response
        }
        
        self.assembly_history = []
    
    def assemble_context(self,
                        system_instructions: str = "",
                        user_query: str = "",
                        additional_context: List[str] = None,
                        memory_query: Optional[str] = None,
                        prioritize_recency: bool = True) -> Dict[str, Any]:
        """
        Assemble optimal context within token constraints.
        
        Returns:
            Dict containing assembled context, metadata, and statistics
        """
        
        if additional_context is None:
            additional_context = []
        
        # Calculate token budgets
        budgets = {
            component: int(self.max_tokens * allocation)
            for component, allocation in self.token_allocations.items()
        }
        
        # Start assembly
        context_components = {}
        token_usage = {}
        
        # 1. System instructions (highest priority)
        if system_instructions:
            truncated_instructions = self._truncate_to_tokens(
                system_instructions, budgets['system_instructions']
            )
            context_components['system_instructions'] = truncated_instructions
            token_usage['system_instructions'] = self.tokenizer(truncated_instructions)
        
        # 2. User query (highest priority)
        truncated_query = self._truncate_to_tokens(user_query, budgets['user_query'])
        context_components['user_query'] = truncated_query
        token_usage['user_query'] = self.tokenizer(truncated_query)
        
        # 3. Retrieved context from memory
        retrieved_content = []
        if memory_query or user_query:
            search_query = memory_query or user_query
            memory_results = self.memory_system.search(
                search_query, limit=20, include_external=True
            )
            
            # Sort by relevance and recency if requested
            if prioritize_recency:
                memory_results.sort(
                    key=lambda x: x[1].last_accessed, reverse=True
                )
            
            # Add retrieved content within budget
            available_tokens = budgets['retrieved_context']
            for key, entry in memory_results:
                entry_tokens = self.tokenizer(entry.content)
                if entry_tokens <= available_tokens:
                    retrieved_content.append(entry.content)
                    available_tokens -= entry_tokens
                else:
                    # Try to fit a truncated version
                    truncated = self._truncate_to_tokens(entry.content, available_tokens)
                    if truncated:
                        retrieved_content.append(truncated)
                    break
        
        # 4. Additional context
        for context_item in additional_context:
            item_tokens = self.tokenizer(context_item)
            if item_tokens <= budgets['retrieved_context'] - token_usage.get('retrieved_context', 0):
                retrieved_content.append(context_item)
                
        context_components['retrieved_context'] = "\n\n".join(retrieved_content)
        token_usage['retrieved_context'] = self.tokenizer(context_components['retrieved_context'])
        
        # Assemble final context
        final_context = self._assemble_final_context(context_components)
        final_token_count = self.tokenizer(final_context)
        
        # Store assembly for analysis
        assembly_record = {
            'timestamp': datetime.now(),
            'token_usage': token_usage,
            'final_token_count': final_token_count,
            'efficiency': final_token_count / self.max_tokens,
            'components_used': list(context_components.keys()),
            'memory_results_count': len(memory_results) if 'memory_results' in locals() else 0
        }
        self.assembly_history.append(assembly_record)
        
        return {
            'context': final_context,
            'components': context_components,
            'token_usage': token_usage,
            'total_tokens': final_token_count,
            'available_tokens': self.max_tokens - final_token_count,
            'efficiency': final_token_count / self.max_tokens,
            'assembly_record': assembly_record
        }
    
    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Intelligently truncate text to fit token budget."""
        if self.tokenizer(text) <= max_tokens:
            return text
        
        # Simple truncation by sentences to maintain coherence
        sentences = text.split('. ')
        result = ""
        
        for sentence in sentences:
            test_result = result + sentence + ". "
            if self.tokenizer(test_result) <= max_tokens:
                result = test_result
            else:
                break
        
        return result.strip()
    
    def _assemble_final_context(self, components: Dict[str, str]) -> str:
        """Assemble components into final context string."""
        parts = []
        
        if components.get('system_instructions'):
            parts.append(f"# System Instructions\n{components['system_instructions']}")
        
        if components.get('retrieved_context'):
            parts.append(f"# Relevant Context\n{components['retrieved_context']}")
        
        if components.get('user_query'):
            parts.append(f"# User Query\n{components['user_query']}")
        
        return "\n\n".join(parts)
    
    def optimize_allocations(self, history_window: int = 100) -> Dict[str, float]:
        """
        Optimize token allocations based on usage history.
        
        Returns updated allocation ratios.
        """
        if len(self.assembly_history) < 10:
            return self.token_allocations
        
        # Analyze recent usage patterns
        recent_history = self.assembly_history[-history_window:]
        
        # Calculate average usage per component
        avg_usage = {}
        for component in self.token_allocations.keys():
            usage_values = [
                record['token_usage'].get(component, 0) 
                for record in recent_history
            ]
            avg_usage[component] = sum(usage_values) / len(usage_values) if usage_values else 0
        
        # Adjust allocations based on actual usage
        total_avg = sum(avg_usage.values())
        if total_avg > 0:
            # Calculate new allocations with some smoothing
            smoothing_factor = 0.7  # 70% new, 30% old
            
            for component in self.token_allocations.keys():
                observed_ratio = avg_usage[component] / total_avg
                current_ratio = self.token_allocations[component]
                
                # Apply smoothed update
                self.token_allocations[component] = (
                    smoothing_factor * observed_ratio + 
                    (1 - smoothing_factor) * current_ratio
                )
            
            # Normalize to ensure sum equals 1.0
            total_allocation = sum(self.token_allocations.values())
            if total_allocation > 0:
                for component in self.token_allocations.keys():
                    self.token_allocations[component] /= total_allocation
        
        return self.token_allocations.copy()
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Return performance metrics for the context manager."""
        if not self.assembly_history:
            return {}
        
        recent_records = self.assembly_history[-50:]  # Last 50 assemblies
        
        return {
            'average_efficiency': sum(r['efficiency'] for r in recent_records) / len(recent_records),
            'average_token_usage': sum(r['final_token_count'] for r in recent_records) / len(recent_records),
            'token_waste': sum(max(0, self.max_tokens - r['final_token_count']) for r in recent_records) / len(recent_records),
            'memory_utilization': sum(r['memory_results_count'] for r in recent_records) / len(recent_records),
            'current_allocations': self.token_allocations.copy(),
            'total_assemblies': len(self.assembly_history)
        }


# =============================================================================
# Performance Monitoring and Analytics
# =============================================================================

class MemoryPerformanceMonitor:
    """Real-time performance monitoring for memory systems."""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'memory_utilization': 0.9,
            'hit_rate': 0.7,
            'avg_response_time': 0.1  # seconds
        }
        self.monitoring_active = False
        self._monitor_thread = None
    
    @contextmanager
    def measure_operation(self, operation_name: str):
        """Context manager for measuring operation performance."""
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            metrics = {
                'operation': operation_name,
                'duration': end_time - start_time,
                'memory_delta': end_memory - start_memory,
                'timestamp': datetime.now()
            }
            
            self.metrics_history.append(metrics)
            
            # Keep only recent metrics
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-500:]
    
    def start_monitoring(self, memory_system: HierarchicalMemorySystem, 
                        interval: float = 10.0):
        """Start continuous monitoring of memory system."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    stats = memory_system.get_statistics()
                    
                    # Check for alerts
                    self._check_alerts(stats)
                    
                    # Store metrics
                    metrics = {
                        'timestamp': datetime.now(),
                        'memory_stats': stats,
                        'system_memory': self._get_memory_usage()
                    }
                    self.metrics_history.append(metrics)
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(interval)
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        self.monitoring_active = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes."""
        # This is a simplified implementation
        # In practice, you might use psutil or similar
        return sys.getsizeof(self.metrics_history)
    
    def _check_alerts(self, stats: Dict[str, Any]):
        """Check if any metrics exceed alert thresholds."""
        alerts = []
        
        # Memory utilization alerts
        wm_util = stats.get('working_memory_utilization', 0)
        ltm_util = stats.get('long_term_memory_utilization', 0)
        
        if wm_util > self.alert_thresholds['memory_utilization']:
            alerts.append(f"Working memory utilization high: {wm_util:.1%}")
        
        if ltm_util > self.alert_thresholds['memory_utilization']:
            alerts.append(f"Long-term memory utilization high: {ltm_util:.1%}")
        
        # Hit rate alerts
        hit_rate = stats.get('hit_rate', 1.0)
        if hit_rate < self.alert_thresholds['hit_rate']:
            alerts.append(f"Memory hit rate low: {hit_rate:.1%}")
        
        # Log alerts
        for alert in alerts:
            print(f"ALERT: {alert}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive performance report."""
        if not self.metrics_history:
            return "No performance data available."
        
        # Analyze recent metrics
        recent_metrics = [m for m in self.metrics_history 
                         if isinstance(m.get('memory_stats'), dict)][-50:]
        
        if not recent_metrics:
            return "No memory statistics available."
        
        # Calculate averages
        avg_hit_rate = sum(m['memory_stats']['hit_rate'] for m in recent_metrics) / len(recent_metrics)
        avg_wm_util = sum(m['memory_stats']['working_memory_utilization'] for m in recent_metrics) / len(recent_metrics)
        avg_ltm_util = sum(m['memory_stats']['long_term_memory_utilization'] for m in recent_metrics) / len(recent_metrics)
        
        # Operation timing analysis
        operation_metrics = [m for m in self.metrics_history 
                           if 'operation' in m and 'duration' in m]
        
        operation_stats = {}
        if operation_metrics:
            operations = defaultdict(list)
            for metric in operation_metrics[-100:]:  # Last 100 operations
                operations[metric['operation']].append(metric['duration'])
            
            for op, durations in operations.items():
                operation_stats[op] = {
                    'avg_duration': sum(durations) / len(durations),
                    'max_duration': max(durations),
                    'call_count': len(durations)
                }
        
        # Build report
        report = f"""
Memory System Performance Report
===============================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Memory Utilization:
  Working Memory: {avg_wm_util:.1%}
  Long-term Memory: {avg_ltm_util:.1%}
  
Performance Metrics:
  Average Hit Rate: {avg_hit_rate:.1%}
  Total Memory Entries: {recent_metrics[-1]['memory_stats']['total_memory_entries']}

Operation Performance:"""
        
        for op, stats in operation_stats.items():
            report += f"""
  {op}:
    Average Duration: {stats['avg_duration']:.3f}s
    Max Duration: {stats['max_duration']:.3f}s
    Call Count: {stats['call_count']}"""
        
        return report


# =============================================================================
# Educational Demonstrations and Examples
# =============================================================================

def demo_basic_memory_hierarchy():
    """Demonstrate basic memory hierarchy functionality."""
    print("=== Memory Hierarchy Demonstration ===")
    
    # Create memory system
    memory_system = HierarchicalMemorySystem(
        working_memory_size=1000,  # Small for demo
        long_term_memory_size=5000
    )
    
    # Store some content
    memory_system.store("concept1", "Context engineering is the optimization of information payloads", 
                       tags=["context", "engineering"], priority=0.9)
    memory_system.store("concept2", "Memory hierarchies manage different types of information", 
                       tags=["memory", "hierarchy"], priority=0.7)
    memory_system.store("temp_note", "Temporary working note", priority=0.1)
    
    print(f"Initial stats: {memory_system.get_statistics()}")
    
    # Retrieve content
    result = memory_system.retrieve("concept1")
    print(f"Retrieved concept1: {result.content[:50]}...")
    
    # Search functionality
    search_results = memory_system.search("memory hierarchy")
    print(f"Search results for 'memory hierarchy': {len(search_results)} found")
    
    # Optimization
    optimization_stats = memory_system.optimize()
    print(f"Optimization results: {optimization_stats}")


def demo_context_window_management():
    """Demonstrate context window management and optimization."""
    print("\n=== Context Window Management Demonstration ===")
    
    # Create context manager with small window for demo
    context_manager = ContextWindowManager(max_tokens=200)
    
    # Store some context in memory
    context_manager.memory_system.store(
        "background_info",
        "Large language models require careful context management to operate within token limits while maintaining coherence.",
        tags=["llm", "context"], priority=0.8
    )
    
    # Assemble context
    result = context_manager.assemble_context(
        system_instructions="You are a helpful assistant focused on context engineering.",
        user_query="How can I optimize context windows for better performance?",
        memory_query="context optimization"
    )
    
    print(f"Final context length: {result['total_tokens']} tokens")
    print(f"Efficiency: {result['efficiency']:.1%}")
    print(f"Token usage: {result['token_usage']}")
    
    # Show optimization over time
    for i in range(5):
        result = context_manager.assemble_context(
            system_instructions="Brief instructions",
            user_query=f"Query number {i+1} about context engineering",
            memory_query="context"
        )
    
    optimized_allocations = context_manager.optimize_allocations()
    print(f"Optimized allocations: {optimized_allocations}")


def benchmark_memory_performance():
    """Benchmark memory system performance."""
    print("\n=== Memory Performance Benchmark ===")
    
    memory_system = HierarchicalMemorySystem()
    monitor = MemoryPerformanceMonitor()
    
    # Benchmark storage
    print("Benchmarking storage operations...")
    with monitor.measure_operation("bulk_storage"):
        for i in range(100):
            memory_system.store(
                f"entry_{i}",
                f"This is test content number {i} for benchmarking memory performance.",
                tags=[f"test_{i%10}", "benchmark"],
                priority=i / 100.0
            )
    
    # Benchmark retrieval
    print("Benchmarking retrieval operations...")
    with monitor.measure_operation("bulk_retrieval"):
        for i in range(50):
            memory_system.retrieve(f"entry_{i}")
    
    # Benchmark search
    print("Benchmarking search operations...")
    with monitor.measure_operation("bulk_search"):
        for i in range(20):
            memory_system.search(f"test content {i}")
    
    # Generate performance report
    report = monitor.generate_report()
    print(report)


# =============================================================================
# Main Execution and Testing
# =============================================================================

if __name__ == "__main__":
    """
    Run demonstrations and tests when script is executed directly.
    This makes the module both importable and executable.
    """
    
    print("Context Engineering Memory Management Lab")
    print("=" * 50)
    
    # Run demonstrations
    demo_basic_memory_hierarchy()
    demo_context_window_management()
    benchmark_memory_performance()
    
    print("\n=== Lab Complete ===")
    print("This module can be imported in Jupyter/Colab with:")
    print("from memory_management_lab import HierarchicalMemorySystem, ContextWindowManager")


# =============================================================================
# Quick Start Functions for Jupyter/Colab
# =============================================================================

def quick_start_memory_system():
    """Quick start function for Jupyter/Colab users."""
    return HierarchicalMemorySystem(
        working_memory_size=50000,
        long_term_memory_size=1_000_000,
        persistence_file="memory_cache.gz"
    )

def quick_start_context_manager(memory_system=None):
    """Quick start function for context management."""
    if memory_system is None:
        memory_system = quick_start_memory_system()
    
    return ContextWindowManager(
        max_tokens=4000,
        memory_system=memory_system
    )

# Export key classes for easy importing
__all__ = [
    'MemoryEntry',
    'WorkingMemory', 
    'LongTermMemory',
    'HierarchicalMemorySystem',
    'ContextWindowManager',
    'MemoryPerformanceMonitor',
    'quick_start_memory_system',
    'quick_start_context_manager'
]
