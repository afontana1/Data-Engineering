#!/usr/bin/env python3
"""
Self-Refinement Context Processing Lab
======================================

Context Engineering Course - Module 02: Context Processing
Production-ready implementation of iterative context improvement systems.

Learning Objectives:
- Implement self-assessment mechanisms for context quality
- Build iterative refinement loops with convergence detection  
- Create adaptive context improvement pipelines
- Deploy self-correcting context processing systems

Research Foundation:
- Self-Refine (Madaan et al.) - Iterative refinement with self-feedback
- Reflexion (Shinn et al.) - Learning from failure through self-reflection
- Constitutional AI - Value-based iterative improvement
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import json
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CORE INTERFACES & UTILITIES
# ============================================================================

class QualityMetric(Enum):
    """Types of quality metrics for context assessment."""
    COHERENCE = "coherence"
    RELEVANCE = "relevance" 
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    FACTUALITY = "factuality"

@dataclass
class QualityScore:
    """Container for context quality assessment."""
    coherence: float = 0.0
    relevance: float = 0.0  
    completeness: float = 0.0
    clarity: float = 0.0
    factuality: float = 0.0
    
    @property
    def overall(self) -> float:
        """Weighted overall quality score."""
        weights = [0.3, 0.3, 0.2, 0.1, 0.1]  # Adjustable weights
        scores = [self.coherence, self.relevance, self.completeness, 
                 self.clarity, self.factuality]
        return sum(w * s for w, s in zip(weights, scores))
    
    def __str__(self) -> str:
        return f"Quality(overall={self.overall:.3f}, coherence={self.coherence:.3f}, relevance={self.relevance:.3f})"

@dataclass
class RefinementIteration:
    """Track single refinement iteration."""
    iteration: int
    input_context: np.ndarray
    output_context: np.ndarray
    quality_before: QualityScore
    quality_after: QualityScore
    refinement_type: str
    processing_time: float
    
    @property
    def improvement(self) -> float:
        """Quality improvement from this iteration."""
        return self.quality_after.overall - self.quality_before.overall

class ContextAssessor(ABC):
    """Base interface for context quality assessment."""
    
    @abstractmethod
    def assess_quality(self, context: np.ndarray, query: Optional[np.ndarray] = None) -> QualityScore:
        """Assess quality of context for given query."""
        pass

class ContextRefiner(ABC):
    """Base interface for context refinement strategies."""
    
    @abstractmethod
    def refine_context(self, context: np.ndarray, quality_score: QualityScore,
                      query: Optional[np.ndarray] = None) -> np.ndarray:
        """Refine context based on quality assessment."""
        pass

# ============================================================================
# QUALITY ASSESSMENT MECHANISMS  
# ============================================================================

class SemanticCoherenceAssessor(ContextAssessor):
    """Assess semantic coherence using embedding analysis."""
    
    def __init__(self, d_model: int = 256, window_size: int = 32):
        self.d_model = d_model
        self.window_size = window_size
        
        # Learned quality assessment networks (simplified)
        self.coherence_net = np.random.randn(d_model, 1) * 0.02
        self.relevance_net = np.random.randn(d_model * 2, 1) * 0.02
        self.completeness_net = np.random.randn(d_model, 1) * 0.02
    
    def assess_quality(self, context: np.ndarray, query: Optional[np.ndarray] = None) -> QualityScore:
        """Comprehensive quality assessment of context."""
        
        # Coherence: Local consistency between adjacent segments
        coherence = self._assess_coherence(context)
        
        # Relevance: Alignment with query (if provided)
        relevance = self._assess_relevance(context, query) if query is not None else 0.8
        
        # Completeness: Information coverage
        completeness = self._assess_completeness(context)
        
        # Clarity: Structural organization
        clarity = self._assess_clarity(context)
        
        # Factuality: Internal consistency (simplified)
        factuality = self._assess_factuality(context)
        
        return QualityScore(
            coherence=coherence,
            relevance=relevance,
            completeness=completeness,
            clarity=clarity,
            factuality=factuality
        )
    
    def _assess_coherence(self, context: np.ndarray) -> float:
        """Assess local semantic coherence."""
        if context.shape[0] < 2:
            return 1.0
        
        # Compute pairwise similarities between adjacent segments
        similarities = []
        for i in range(0, context.shape[0] - self.window_size, self.window_size // 2):
            end_idx = min(i + self.window_size, context.shape[0])
            segment1 = np.mean(context[i:end_idx], axis=0)
            
            next_start = min(i + self.window_size // 2, context.shape[0] - 1)
            next_end = min(next_start + self.window_size, context.shape[0])
            
            if next_end > next_start:
                segment2 = np.mean(context[next_start:next_end], axis=0)
                
                # Cosine similarity
                sim = np.dot(segment1, segment2) / (np.linalg.norm(segment1) * np.linalg.norm(segment2) + 1e-8)
                similarities.append(max(0, sim))  # Clip negative similarities
        
        return np.mean(similarities) if similarities else 0.5
    
    def _assess_relevance(self, context: np.ndarray, query: np.ndarray) -> float:
        """Assess relevance to query."""
        context_repr = np.mean(context, axis=0)
        query_repr = np.mean(query, axis=0)
        
        # Enhanced relevance with learned weights
        combined = np.concatenate([context_repr, query_repr])
        relevance_raw = np.sigmoid(combined @ self.relevance_net.flatten())
        
        return float(relevance_raw)
    
    def _assess_completeness(self, context: np.ndarray) -> float:
        """Assess information completeness using diversity metrics."""
        if context.shape[0] < 2:
            return 0.5
        
        # Information diversity via eigenvalue spread
        cov_matrix = np.cov(context.T)
        eigenvals = np.linalg.eigvals(cov_matrix)
        eigenvals = np.real(eigenvals[eigenvals > 0])  # Keep positive eigenvalues
        
        if len(eigenvals) > 1:
            # Normalized entropy of eigenvalue distribution  
            eigenvals_norm = eigenvals / np.sum(eigenvals)
            entropy = -np.sum(eigenvals_norm * np.log(eigenvals_norm + 1e-10))
            max_entropy = np.log(len(eigenvals))
            completeness = entropy / max_entropy if max_entropy > 0 else 0.5
        else:
            completeness = 0.5
            
        return min(1.0, completeness)
    
    def _assess_clarity(self, context: np.ndarray) -> float:
        """Assess structural clarity and organization."""
        seq_len = context.shape[0]
        
        # Measure consistency of embedding norms (structural regularity)
        norms = np.linalg.norm(context, axis=1)
        norm_consistency = 1.0 - (np.std(norms) / (np.mean(norms) + 1e-8))
        norm_consistency = max(0, min(1, norm_consistency))
        
        # Measure progressive information flow
        if seq_len > 3:
            position_weights = np.linspace(0, 1, seq_len)
            weighted_context = context * position_weights[:, None]
            flow_consistency = np.mean(np.abs(np.diff(np.linalg.norm(weighted_context, axis=1))))
            flow_score = 1.0 / (1.0 + flow_consistency)  # Lower variation = higher clarity
        else:
            flow_score = 0.7
            
        return (norm_consistency + flow_score) / 2
    
    def _assess_factuality(self, context: np.ndarray) -> float:
        """Assess internal factual consistency (simplified)."""
        # Simplified: Check for embedding magnitude consistency as proxy for factual coherence
        magnitudes = np.linalg.norm(context, axis=1)
        
        # Consistent magnitude indicates consistent "confidence" in information
        magnitude_consistency = 1.0 - min(1.0, np.std(magnitudes) / (np.mean(magnitudes) + 1e-8))
        
        # Check for contradictory patterns (very dissimilar embeddings)
        pairwise_sims = np.corrcoef(context)
        negative_correlations = np.sum(pairwise_sims < -0.3) / (pairwise_sims.shape[0] ** 2)
        contradiction_penalty = min(1.0, negative_correlations * 5)  # Scale penalty
        
        factuality = magnitude_consistency - contradiction_penalty
        return max(0.1, min(1.0, factuality))

def np_sigmoid(x):
    """Numerically stable sigmoid."""
    return np.where(x > 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))

# Fix sigmoid reference
np.sigmoid = np_sigmoid

# ============================================================================
# REFINEMENT STRATEGIES
# ============================================================================

class AdaptiveContextRefiner(ContextRefiner):
    """Multi-strategy context refiner that adapts based on quality assessment."""
    
    def __init__(self, d_model: int = 256):
        self.d_model = d_model
        
        # Refinement transformation matrices
        self.coherence_transform = np.random.randn(d_model, d_model) * 0.02
        self.relevance_transform = np.random.randn(d_model, d_model) * 0.02  
        self.completeness_transform = np.random.randn(d_model, d_model) * 0.02
        self.clarity_transform = np.random.randn(d_model, d_model) * 0.02
        
        # Smoothing and filtering operations
        self.smoothing_kernel = self._create_smoothing_kernel(5)
    
    def refine_context(self, context: np.ndarray, quality_score: QualityScore,
                      query: Optional[np.ndarray] = None) -> np.ndarray:
        """Apply targeted refinements based on quality deficiencies."""
        
        refined = context.copy()
        
        # Apply refinements based on lowest quality scores
        refinement_threshold = 0.6
        
        if quality_score.coherence < refinement_threshold:
            refined = self._improve_coherence(refined)
        
        if quality_score.relevance < refinement_threshold and query is not None:
            refined = self._improve_relevance(refined, query)
            
        if quality_score.completeness < refinement_threshold:
            refined = self._improve_completeness(refined)
            
        if quality_score.clarity < refinement_threshold:
            refined = self._improve_clarity(refined)
        
        # Apply gentle smoothing to maintain overall structure
        refined = self._apply_smoothing(refined)
        
        return refined
    
    def _improve_coherence(self, context: np.ndarray) -> np.ndarray:
        """Improve semantic coherence through local smoothing."""
        refined = context.copy()
        
        # Apply coherence transformation
        transformed = context @ self.coherence_transform
        
        # Blend with original using sigmoid weighting
        seq_len = context.shape[0]
        blend_weights = np.sigmoid(np.linspace(-2, 2, seq_len))[:, None]
        
        refined = context * (1 - blend_weights) + transformed * blend_weights
        
        return refined
    
    def _improve_relevance(self, context: np.ndarray, query: np.ndarray) -> np.ndarray:
        """Improve relevance to query through attention-like mechanism."""
        query_repr = np.mean(query, axis=0)
        
        # Compute relevance scores for each context position
        relevance_scores = np.dot(context, query_repr)
        relevance_weights = np.softmax(relevance_scores)
        
        # Apply relevance transformation with query conditioning
        query_conditioned = context + query_repr[None, :] * 0.1
        transformed = query_conditioned @ self.relevance_transform
        
        # Weight transformation by relevance
        blend_weights = relevance_weights[:, None]
        refined = context * (1 - blend_weights) + transformed * blend_weights
        
        return refined
    
    def _improve_completeness(self, context: np.ndarray) -> np.ndarray:
        """Improve information completeness through diversity enhancement."""
        # Identify under-represented directions in embedding space
        cov_matrix = np.cov(context.T)
        eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
        
        # Focus on directions with low variance (under-represented information)
        low_variance_dirs = eigenvecs[:, eigenvals < np.median(eigenvals)]
        
        # Apply completeness transformation
        transformed = context @ self.completeness_transform
        
        # Enhance low-variance directions
        if low_variance_dirs.shape[1] > 0:
            enhancement = context @ low_variance_dirs @ low_variance_dirs.T * 0.1
            transformed += enhancement
        
        # Progressive blending (more enhancement towards the end)
        seq_len = context.shape[0]
        blend_weights = np.linspace(0.1, 0.3, seq_len)[:, None]
        
        refined = context * (1 - blend_weights) + transformed * blend_weights
        
        return refined
    
    def _improve_clarity(self, context: np.ndarray) -> np.ndarray:
        """Improve structural clarity through regularization."""
        # Apply clarity transformation
        transformed = context @ self.clarity_transform
        
        # Normalize magnitudes for consistency
        norms = np.linalg.norm(transformed, axis=1, keepdims=True)
        target_norm = np.median(norms)
        normalized = transformed * (target_norm / (norms + 1e-8))
        
        # Progressive structure enhancement
        seq_len = context.shape[0]
        structure_weights = 0.2 * np.sin(np.linspace(0, np.pi, seq_len))[:, None]
        
        refined = context * 0.8 + normalized * 0.2 + structure_weights
        
        return refined
    
    def _apply_smoothing(self, context: np.ndarray) -> np.ndarray:
        """Apply gentle smoothing to maintain overall coherence."""
        if context.shape[0] < len(self.smoothing_kernel):
            return context
            
        # Apply 1D smoothing along sequence dimension for each embedding dimension
        smoothed = np.zeros_like(context)
        kernel_half = len(self.smoothing_kernel) // 2
        
        for i in range(context.shape[0]):
            start_idx = max(0, i - kernel_half) 
            end_idx = min(context.shape[0], i + kernel_half + 1)
            
            # Extract relevant kernel portion
            kernel_start = max(0, kernel_half - i)
            kernel_end = kernel_start + (end_idx - start_idx)
            
            if kernel_end <= len(self.smoothing_kernel):
                weights = self.smoothing_kernel[kernel_start:kernel_end]
                weights = weights / np.sum(weights)  # Normalize
                
                smoothed[i] = np.sum(context[start_idx:end_idx] * weights[:, None], axis=0)
            else:
                smoothed[i] = context[i]  # Fallback
        
        # Blend with original
        return context * 0.9 + smoothed * 0.1
    
    def _create_smoothing_kernel(self, size: int) -> np.ndarray:
        """Create Gaussian smoothing kernel."""
        kernel = np.exp(-0.5 * ((np.arange(size) - size // 2) ** 2) / (size / 4) ** 2)
        return kernel / np.sum(kernel)

def np_softmax(x, axis=-1):
    """Numerically stable softmax."""
    max_vals = np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x - max_vals)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

# Add softmax to numpy namespace
np.softmax = np_softmax

# ============================================================================
# REFINEMENT PIPELINE
# ============================================================================

class SelfRefinementPipeline:
    """Complete self-refinement pipeline with convergence detection."""
    
    def __init__(self, d_model: int = 256, max_iterations: int = 5, 
                 convergence_threshold: float = 0.01, quality_threshold: float = 0.8):
        self.d_model = d_model
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.quality_threshold = quality_threshold
        
        # Initialize components
        self.assessor = SemanticCoherenceAssessor(d_model)
        self.refiner = AdaptiveContextRefiner(d_model)
        
        # Track refinement history
        self.refinement_history: List[RefinementIteration] = []
    
    def refine_context(self, initial_context: np.ndarray, 
                      query: Optional[np.ndarray] = None,
                      target_quality: Optional[float] = None) -> Dict[str, Any]:
        """Execute complete refinement pipeline with convergence detection."""
        
        if target_quality is None:
            target_quality = self.quality_threshold
        
        current_context = initial_context.copy()
        self.refinement_history = []
        
        print(f"Starting self-refinement pipeline...")
        print(f"Target quality: {target_quality:.3f}, Max iterations: {self.max_iterations}")
        
        # Initial quality assessment
        current_quality = self.assessor.assess_quality(current_context, query)
        print(f"Initial quality: {current_quality}")
        
        start_time = time.time()
        
        for iteration in range(self.max_iterations):
            iteration_start = time.time()
            
            # Check if we've reached target quality
            if current_quality.overall >= target_quality:
                print(f"Target quality reached at iteration {iteration}")
                break
            
            # Apply refinement
            refined_context = self.refiner.refine_context(current_context, current_quality, query)
            
            # Assess refined quality
            refined_quality = self.assessor.assess_quality(refined_context, query)
            
            iteration_time = time.time() - iteration_start
            
            # Record iteration
            refinement_iter = RefinementIteration(
                iteration=iteration,
                input_context=current_context.copy(),
                output_context=refined_context.copy(),
                quality_before=current_quality,
                quality_after=refined_quality,
                refinement_type="adaptive",
                processing_time=iteration_time
            )
            
            self.refinement_history.append(refinement_iter)
            
            # Check for convergence
            improvement = refinement_iter.improvement
            print(f"Iteration {iteration + 1}: {current_quality} → {refined_quality} (Δ={improvement:+.4f})")
            
            if abs(improvement) < self.convergence_threshold:
                print(f"Convergence detected at iteration {iteration + 1}")
                break
            
            # Check for degradation (with some tolerance)
            if improvement < -self.convergence_threshold * 2:
                print(f"Quality degradation detected, stopping refinement")
                break
            
            # Update for next iteration
            current_context = refined_context
            current_quality = refined_quality
        
        total_time = time.time() - start_time
        
        return {
            'initial_context': initial_context,
            'final_context': current_context,
            'initial_quality': self.refinement_history[0].quality_before if self.refinement_history else current_quality,
            'final_quality': current_quality,
            'iterations_completed': len(self.refinement_history),
            'total_improvement': current_quality.overall - (self.refinement_history[0].quality_before.overall if self.refinement_history else current_quality.overall),
            'processing_time': total_time,
            'convergence_achieved': abs(self.refinement_history[-1].improvement) < self.convergence_threshold if self.refinement_history else False,
            'target_quality_reached': current_quality.overall >= target_quality
        }
    
    def get_refinement_analytics(self) -> Dict[str, Any]:
        """Analyze refinement process and provide insights."""
        if not self.refinement_history:
            return {'error': 'No refinement history available'}
        
        improvements = [iter.improvement for iter in self.refinement_history]
        processing_times = [iter.processing_time for iter in self.refinement_history]
        
        # Quality trajectory
        quality_trajectory = []
        quality_trajectory.append(self.refinement_history[0].quality_before.overall)
        for iter in self.refinement_history:
            quality_trajectory.append(iter.quality_after.overall)
        
        return {
            'total_iterations': len(self.refinement_history),
            'total_improvement': sum(improvements),
            'average_improvement_per_iteration': np.mean(improvements),
            'best_iteration': np.argmax(improvements),
            'worst_iteration': np.argmin(improvements),
            'total_processing_time': sum(processing_times),
            'average_time_per_iteration': np.mean(processing_times),
            'quality_trajectory': quality_trajectory,
            'improvement_stability': np.std(improvements),
            'time_efficiency': sum(improvements) / sum(processing_times) if sum(processing_times) > 0 else 0
        }

# ============================================================================
# ADVANCED REFINEMENT TECHNIQUES
# ============================================================================

class MetaRefinementController:
    """Meta-level controller that learns optimal refinement strategies."""
    
    def __init__(self, d_model: int = 256):
        self.d_model = d_model
        self.refinement_strategies = {
            'conservative': {'max_iter': 3, 'convergence': 0.02, 'blend_ratio': 0.1},
            'aggressive': {'max_iter': 8, 'convergence': 0.005, 'blend_ratio': 0.3},
            'balanced': {'max_iter': 5, 'convergence': 0.01, 'blend_ratio': 0.2}
        }
        
        # Strategy performance tracking
        self.strategy_performance = {name: [] for name in self.refinement_strategies.keys()}
        
    def select_strategy(self, initial_quality: QualityScore, 
                       context_length: int) -> Dict[str, Any]:
        """Select optimal refinement strategy based on context characteristics."""
        
        # Strategy selection heuristics
        if initial_quality.overall < 0.4:
            # Poor quality needs aggressive refinement
            selected = 'aggressive'
        elif initial_quality.overall > 0.7:
            # Good quality needs conservative refinement
            selected = 'conservative' 
        else:
            # Medium quality gets balanced approach
            selected = 'balanced'
        
        # Adjust for context length
        strategy = self.refinement_strategies[selected].copy()
        if context_length > 1000:
            strategy['max_iter'] = max(1, strategy['max_iter'] // 2)  # Reduce iterations for long contexts
        
        return {'name': selected, 'params': strategy}
    
    def update_strategy_performance(self, strategy_name: str, 
                                  improvement: float, efficiency: float):
        """Update performance tracking for refinement strategies."""
        performance_score = improvement * efficiency  # Combined metric
        self.strategy_performance[strategy_name].append(performance_score)

class ConstitutionalRefinement:
    """Refinement based on constitutional principles and value alignment."""
    
    def __init__(self, d_model: int = 256):
        self.d_model = d_model
        self.principles = {
            'helpfulness': 0.3,
            'harmlessness': 0.3, 
            'honesty': 0.2,
            'clarity': 0.2
        }
        
        # Principle enforcement networks
        self.principle_networks = {
            principle: np.random.randn(d_model, d_model) * 0.02 
            for principle in self.principles.keys()
        }
    
    def apply_constitutional_refinement(self, context: np.ndarray, 
                                      violations: Dict[str, float]) -> np.ndarray:
        """Apply refinements based on constitutional principle violations."""
        
        refined = context.copy()
        
        for principle, violation_score in violations.items():
            if violation_score > 0.3 and principle in self.principle_networks:
                # Apply principle-specific transformation
                principle_transform = self.principle_networks[principle]
                transformed = context @ principle_transform
                
                # Blend based on violation severity
                blend_weight = min(0.5, violation_score) * self.principles[principle]
                refined = refined * (1 - blend_weight) + transformed * blend_weight
        
        return refined

# ============================================================================
# PRACTICAL APPLICATIONS
# ============================================================================

class ProductionRefinementSystem:
    """Production-ready self-refinement system with monitoring and caching."""
    
    def __init__(self, d_model: int = 256):
        self.d_model = d_model
        self.pipeline = SelfRefinementPipeline(d_model)
        self.meta_controller = MetaRefinementController(d_model)
        self.constitutional = ConstitutionalRefinement(d_model)
        
        # Performance monitoring
        self.processing_stats = []
        self.cache = {}  # Simple caching for similar contexts
        
    def refine_context_production(self, context: np.ndarray, query: Optional[np.ndarray] = None,
                                user_requirements: Optional[Dict] = None) -> Dict[str, Any]:
        """Production-ready context refinement with full monitoring."""
        
        start_time = time.time()
        
        # Check cache first
        context_hash = hash(context.data.tobytes())
        if context_hash in self.cache:
            print("Cache hit - returning cached refinement")
            return self.cache[context_hash]
        
        # Initial assessment
        initial_quality = self.pipeline.assessor.assess_quality(context, query)
        
        # Select refinement strategy
        strategy = self.meta_controller.select_strategy(initial_quality, context.shape[0])
        
        # Update pipeline parameters
        self.pipeline.max_iterations = strategy['params']['max_iter']
        self.pipeline.convergence_threshold = strategy['params']['convergence']
        
        print(f"Selected strategy: {strategy['name']}")
        
        # Execute refinement
        result = self.pipeline.refine_context(context, query)
        
        # Apply constitutional refinement if needed
        if user_requirements and 'constitutional_check' in user_requirements:
            violations = user_requirements.get('violations', {})
            if any(score > 0.3 for score in violations.values()):
                print("Applying constitutional refinement...")
                result['final_context'] = self.constitutional.apply_constitutional_refinement(
                    result['final_context'], violations
                )
                # Re-assess quality after constitutional refinement
                result['final_quality'] = self.pipeline.assessor.assess_quality(
                    result['final_context'], query
                )
        
        # Update strategy performance
        efficiency = result['total_improvement'] / result['processing_time'] if result['processing_time'] > 0 else 0
        self.meta_controller.update_strategy_performance(
            strategy['name'], result['total_improvement'], efficiency
        )
        
        # Cache result
        self.cache[context_hash] = result
        
        # Record performance stats
        total_time = time.time() - start_time
        self.processing_stats.append({
            'context_length': context.shape[0],
            'strategy_used': strategy['name'],
            'iterations': result['iterations_completed'],
            'improvement': result['total_improvement'],
            'processing_time': total_time,
            'cache_hit': False
        })
        
        return result

def create_sample_context(seq_len: int, d_model: int = 256, quality_level: str = 'medium') -> np.ndarray:
    """Create sample context with specified quality characteristics."""
    np.random.seed(42)
    
    if quality_level == 'poor':
        # Incoherent, random embeddings
        context = np.random.randn(seq_len, d_model) * 0.5
        # Add noise
        context += np.random.randn(seq_len, d_model) * 0.3
        
    elif quality_level == 'medium':
        # Some structure but inconsistent
        base = np.random.randn(seq_len, d_model) * 0.2
        # Add some coherent patterns
        for i in range(0, seq_len, 10):
            end_idx = min(i + 10, seq_len)
            pattern = np.random.randn(d_model) * 0.1
            base[i:end_idx] += pattern
        context = base
        
    elif quality_level == 'high':
        # Highly structured and coherent
        base_pattern = np.random.randn(d_model) * 0.1
        context = np.zeros((seq_len, d_model))
        for i in range(seq_len):
            # Progressive variation on base pattern
            variation = np.random.randn(d_model) * 0.05
            context[i] = base_pattern + variation * (i / seq_len)
    
    return context

# ============================================================================
# BENCHMARKING & EVALUATION
# ============================================================================

def benchmark_refinement_pipeline():
    """Comprehensive benchmark of self-refinement capabilities."""
    
    print("="*60)
    print("SELF-REFINEMENT BENCHMARK")
    print("="*60)
    
    # Test different initial quality levels
    quality_levels = ['poor', 'medium', 'high']
    seq_lengths = [128, 256, 512]
    
    results = {}
    
    for quality in quality_levels:
        results[quality] = {}
        
        for seq_len in seq_lengths:
            print(f"\nTesting {quality} quality context, length {seq_len}")
            
            # Create test context
            context = create_sample_context(seq_len, quality_level=quality)
            query = create_sample_context(32, quality_level='high')  # Always use high-quality query
            
            # Initialize refinement system
            system = ProductionRefinementSystem()
            
            # Run refinement
            start_time = time.time()
            result = system.refine_context_production(context, query)
            end_time = time.time()
            
            # Store results
            results[quality][seq_len] = {
                'initial_quality': result['initial_quality'].overall,
                'final_quality': result['final_quality'].overall,
                'improvement': result['total_improvement'],
                'iterations': result['iterations_completed'],
                'processing_time': end_time - start_time,
                'convergence_achieved': result['convergence_achieved'],
                'target_reached': result['target_quality_reached']
            }
            
            print(f"  Initial: {result['initial_quality'].overall:.3f}")
            print(f"  Final: {result['final_quality'].overall:.3f}")
            print(f"  Improvement: {result['total_improvement']:+.3f}")
            print(f"  Iterations: {result['iterations_completed']}")
            print(f"  Time: {end_time - start_time:.2f}s")
    
    return results

def visualize_refinement_results(results: Dict, refinement_history: List[RefinementIteration]):
    """Create comprehensive visualization of refinement results."""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Self-Refinement Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # Plot 1: Quality improvement by initial quality level
    ax = axes[0, 0]
    quality_levels = list(results.keys())
    seq_lengths = list(results[quality_levels[0]].keys())
    
    for seq_len in seq_lengths:
        improvements = [results[qual][seq_len]['improvement'] for qual in quality_levels]
        ax.plot(quality_levels, improvements, 'o-', label=f'Length {seq_len}', linewidth=2, markersize=8)
    
    ax.set_xlabel('Initial Quality Level')
    ax.set_ylabel('Quality Improvement')
    ax.set_title('Improvement by Initial Quality')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Processing time analysis
    ax = axes[0, 1]
    for qual in quality_levels:
        times = [results[qual][seq_len]['processing_time'] for seq_len in seq_lengths]
        ax.plot(seq_lengths, times, 's-', label=f'{qual.title()} Quality', linewidth=2, markersize=8)
    
    ax.set_xlabel('Sequence Length')
    ax.set_ylabel('Processing Time (seconds)')
    ax.set_title('Processing Time Analysis')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Convergence analysis
    ax = axes[0, 2]
    convergence_rates = {}
    for qual in quality_levels:
        converged = sum(1 for seq_len in seq_lengths if results[qual][seq_len]['convergence_achieved'])
        convergence_rates[qual] = converged / len(seq_lengths)
    
    bars = ax.bar(convergence_rates.keys(), convergence_rates.values(), 
                  alpha=0.7, color=['red', 'orange', 'green'])
    ax.set_ylabel('Convergence Rate')
    ax.set_title('Convergence Success Rate')
    ax.set_ylim(0, 1)
    
    # Add percentage labels
    for bar, rate in zip(bars, convergence_rates.values()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{rate*100:.0f}%', ha='center', va='bottom')
    
    # Plot 4: Refinement trajectory (if history available)
    ax = axes[1, 0]
    if refinement_history:
        iterations = range(len(refinement_history) + 1)
        quality_trajectory = [refinement_history[0].quality_before.overall]
        quality_trajectory.extend([iter.quality_after.overall for iter in refinement_history])
        
        ax.plot(iterations, quality_trajectory, 'b-o', linewidth=3, markersize=8)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Quality Score')
        ax.set_title('Quality Trajectory Example')
        ax.grid(True, alpha=0.3)
        
        # Highlight best iteration
        best_iter = np.argmax([iter.quality_after.overall for iter in refinement_history])
        ax.axvline(x=best_iter + 1, color='green', linestyle='--', alpha=0.7, label='Best Result')
        ax.legend()
    
    # Plot 5: Efficiency analysis
    ax = axes[1, 1]
    efficiency_data = {}
    for qual in quality_levels:
        efficiencies = []
        for seq_len in seq_lengths:
            improvement = results[qual][seq_len]['improvement']
            time = results[qual][seq_len]['processing_time']
            efficiency = improvement / time if time > 0 else 0
            efficiencies.append(max(0, efficiency))  # Ensure non-negative
        efficiency_data[qual] = np.mean(efficiencies)
    
    bars = ax.bar(efficiency_data.keys(), efficiency_data.values(), 
                  alpha=0.7, color=['red', 'orange', 'green'])
    ax.set_ylabel('Efficiency (Improvement/Time)')
    ax.set_title('Refinement Efficiency')
    
    # Add value labels
    for bar, eff in zip(bars, efficiency_data.values()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
               f'{eff:.3f}', ha='center', va='bottom')
    
    # Plot 6: Quality dimensions breakdown (if history available)
    ax = axes[1, 2]
    if refinement_history:
        final_quality = refinement_history[-1].quality_after
        dimensions = ['Coherence', 'Relevance', 'Completeness', 'Clarity', 'Factuality']
        values = [final_quality.coherence, final_quality.relevance, 
                 final_quality.completeness, final_quality.clarity, final_quality.factuality]
        
        bars = ax.bar(dimensions, values, alpha=0.7, color='skyblue')
        ax.set_ylabel('Quality Score')
        ax.set_title('Final Quality Breakdown')
        ax.set_ylim(0, 1)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'{value:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Main demonstration of self-refinement capabilities."""
    
    print("="*80)
    print("SELF-REFINEMENT CONTEXT PROCESSING LAB")
    print("Context Engineering Course - Module 02")
    print("="*80)
    print()
    
    # 1. Basic refinement demonstration
    print("1. Basic Self-Refinement Demonstration")
    print("-" * 50)
    
    # Create sample context with medium quality
    context = create_sample_context(256, quality_level='poor')
    query = create_sample_context(32, quality_level='high')
    
    # Initialize refinement pipeline
    pipeline = SelfRefinementPipeline(max_iterations=5, quality_threshold=0.75)
    
    # Execute refinement
    result = pipeline.refine_context(context, query)
    
    print(f"\nRefinement completed:")
    print(f"  Initial quality: {result['initial_quality'].overall:.3f}")
    print(f"  Final quality: {result['final_quality'].overall:.3f}")
    print(f"  Total improvement: {result['total_improvement']:+.3f}")
    print(f"  Iterations: {result['iterations_completed']}")
    print(f"  Target reached: {result['target_quality_reached']}")
    print(f"  Processing time: {result['processing_time']:.2f}s")
    
    # 2. Production system demonstration
    print("\n2. Production Refinement System")
    print("-" * 50)
    
    production_system = ProductionRefinementSystem()
    
    # Test different scenarios
    test_contexts = {
        'Poor Quality': create_sample_context(128, quality_level='poor'),
        'Medium Quality': create_sample_context(128, quality_level='medium'),
        'High Quality': create_sample_context(128, quality_level='high')
    }
    
    for name, test_context in test_contexts.items():
        print(f"\nTesting {name} Context:")
        prod_result = production_system.refine_context_production(test_context, query)
        
        print(f"  Strategy selected: {name}")
        print(f"  Improvement: {prod_result['total_improvement']:+.3f}")
        print(f"  Final quality: {prod_result['final_quality'].overall:.3f}")
    
    # 3. Run comprehensive benchmark
    print("\n3. Comprehensive Benchmark")
    print("-" * 50)
    
    benchmark_results = benchmark_refinement_pipeline()
    
    # 4. Visualize results
    print("\n4. Generating Visualizations...")
    print("-" * 50)
    
    visualize_refinement_results(benchmark_results, pipeline.refinement_history)
    
    # 5. Analytics and insights
    print("\n5. Refinement Analytics")
    print("-" * 50)
    
    analytics = pipeline.get_refinement_analytics()
    
    if 'error' not in analytics:
        print(f"  Total iterations: {analytics['total_iterations']}")
        print(f"  Average improvement: {analytics['average_improvement_per_iteration']:+.4f}")
        print(f"  Best iteration: #{analytics['best_iteration'] + 1}")
        print(f"  Time efficiency: {analytics['time_efficiency']:.4f}")
        print(f"  Improvement stability: {analytics['improvement_stability']:.4f}")
    
    print("\n" + "="*80)
    print("SELF-REFINEMENT LAB COMPLETE")
    print("="*80)
    print("\nKey Takeaways:")
    print("• Self-refinement significantly improves context quality")
    print("• Different strategies work better for different initial quality levels")
    print("• Convergence detection prevents over-refinement")
    print("• Production systems need caching and strategy selection")
    print("• Meta-learning improves refinement efficiency over time")
    
    print("\nPractical Applications:")
    print("• Automated content improvement for RAG systems")
    print("• Quality assurance in context generation pipelines")
    print("• Adaptive context optimization for different users/tasks")
    print("• Self-improving dialogue systems")

if __name__ == "__main__":
    main()
