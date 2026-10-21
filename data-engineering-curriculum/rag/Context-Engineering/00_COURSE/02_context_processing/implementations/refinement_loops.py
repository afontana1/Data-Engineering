#!/usr/bin/env python3
"""
Refinement Loops - Self-Improvement Algorithms
==============================================

Production-ready iterative context improvement implementations.
Minimal code, maximal signal ratio.

Usage:
    from refinement_loops import QualityAssessor, IterativeRefiner, MetaController
    
    refiner = IterativeRefiner(d_model=512)
    improved_context, stats = refiner.refine(context, target_quality=0.8)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

__all__ = [
    'QualityScore', 'QualityAssessor', 'ContextRefiner', 'IterativeRefiner', 
    'MetaController', 'ConstitutionalRefiner', 'RefinementPipeline'
]

# ============================================================================
# CORE INTERFACES & DATA STRUCTURES
# ============================================================================

@dataclass
class QualityScore:
    """Multi-dimensional quality assessment."""
    coherence: float = 0.0      # Local consistency
    relevance: float = 0.0      # Query alignment  
    completeness: float = 0.0   # Information coverage
    clarity: float = 0.0        # Structural organization
    safety: float = 0.0         # Content safety
    
    @property
    def overall(self) -> float:
        """Weighted overall score."""
        weights = [0.3, 0.3, 0.2, 0.1, 0.1]
        scores = [self.coherence, self.relevance, self.completeness, self.clarity, self.safety]
        return sum(w * s for w, s in zip(weights, scores))
    
    def __str__(self) -> str:
        return f"Quality(overall={self.overall:.3f}, coherence={self.coherence:.3f}, relevance={self.relevance:.3f})"

class RefinementStrategy(Enum):
    """Available refinement strategies."""
    CONSERVATIVE = "conservative"  # Small, safe improvements
    AGGRESSIVE = "aggressive"      # Large, risky improvements  
    ADAPTIVE = "adaptive"          # Context-aware adjustments
    CONSTITUTIONAL = "constitutional"  # Value-aligned improvements

# ============================================================================
# QUALITY ASSESSMENT
# ============================================================================

class QualityAssessor(ABC):
    """Base interface for quality assessment."""
    
    @abstractmethod
    def assess(self, context: np.ndarray, query: Optional[np.ndarray] = None) -> QualityScore:
        """Assess context quality across multiple dimensions."""
        pass

class EmbeddingQualityAssessor(QualityAssessor):
    """Quality assessment using embedding analysis."""
    
    def __init__(self, d_model: int = 512, window_size: int = 32):
        self.d_model = d_model
        self.window_size = window_size
        
        # Quality assessment networks (learned in practice)
        self.coherence_net = np.random.randn(d_model, 1) * 0.02
        self.relevance_net = np.random.randn(d_model * 2, 1) * 0.02
        self.completeness_net = np.random.randn(d_model, 1) * 0.02
        self.clarity_net = np.random.randn(d_model, 1) * 0.02
        self.safety_net = np.random.randn(d_model, 1) * 0.02
    
    def assess(self, context: np.ndarray, query: Optional[np.ndarray] = None) -> QualityScore:
        """Comprehensive quality assessment."""
        
        return QualityScore(
            coherence=self._assess_coherence(context),
            relevance=self._assess_relevance(context, query) if query is not None else 0.8,
            completeness=self._assess_completeness(context),
            clarity=self._assess_clarity(context),
            safety=self._assess_safety(context)
        )
    
    def _assess_coherence(self, context: np.ndarray) -> float:
        """Assess semantic coherence through local similarity."""
        if len(context) < 2:
            return 1.0
        
        # Sliding window coherence
        similarities = []
        for i in range(0, len(context) - self.window_size, self.window_size // 2):
            end_idx = min(i + self.window_size, len(context))
            segment1 = np.mean(context[i:end_idx], axis=0)
            
            next_start = min(i + self.window_size // 2, len(context) - 1)
            next_end = min(next_start + self.window_size, len(context))
            
            if next_end > next_start:
                segment2 = np.mean(context[next_start:next_end], axis=0)
                sim = np.dot(segment1, segment2) / (np.linalg.norm(segment1) * np.linalg.norm(segment2) + 1e-8)
                similarities.append(max(0, sim))
        
        coherence_score = np.mean(similarities) if similarities else 0.5
        return float(np.sigmoid(coherence_score @ self.coherence_net.flatten()))
    
    def _assess_relevance(self, context: np.ndarray, query: np.ndarray) -> float:
        """Assess relevance to query."""
        context_repr = np.mean(context, axis=0)
        query_repr = np.mean(query, axis=0) if len(query.shape) > 1 else query
        
        combined = np.concatenate([context_repr, query_repr])
        relevance_raw = combined @ self.relevance_net.flatten()
        return float(np.sigmoid(relevance_raw))
    
    def _assess_completeness(self, context: np.ndarray) -> float:
        """Assess information completeness via diversity."""
        if len(context) < 2:
            return 0.5
        
        # Information diversity through eigenvalue analysis
        try:
            cov_matrix = np.cov(context.T)
            eigenvals = np.linalg.eigvals(cov_matrix)
            eigenvals = np.real(eigenvals[eigenvals > 0])
            
            if len(eigenvals) > 1:
                eigenvals_norm = eigenvals / np.sum(eigenvals)
                entropy = -np.sum(eigenvals_norm * np.log(eigenvals_norm + 1e-10))
                max_entropy = np.log(len(eigenvals))
                diversity_score = entropy / max_entropy if max_entropy > 0 else 0.5
            else:
                diversity_score = 0.5
            
            completeness_raw = diversity_score * np.ones(self.d_model) @ self.completeness_net.flatten()
            return float(np.sigmoid(completeness_raw))
        except:
            return 0.5
    
    def _assess_clarity(self, context: np.ndarray) -> float:
        """Assess structural clarity."""
        # Embedding magnitude consistency
        norms = np.linalg.norm(context, axis=1)
        norm_consistency = 1.0 - min(1.0, np.std(norms) / (np.mean(norms) + 1e-8))
        
        clarity_features = np.array([norm_consistency] * self.d_model)
        clarity_raw = clarity_features @ self.clarity_net.flatten()
        return float(np.sigmoid(clarity_raw))
    
    def _assess_safety(self, context: np.ndarray) -> float:
        """Assess content safety (simplified)."""
        # Magnitude consistency as safety proxy
        magnitudes = np.linalg.norm(context, axis=1)
        safety_score = 1.0 - min(1.0, np.std(magnitudes) / (np.mean(magnitudes) + 1e-8))
        
        safety_features = np.array([safety_score] * self.d_model)
        safety_raw = safety_features @ self.safety_net.flatten()
        return float(np.sigmoid(safety_raw))

def np_sigmoid(x):
    """Numerically stable sigmoid."""
    return np.where(x > 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))

np.sigmoid = np_sigmoid

# ============================================================================
# CONTEXT REFINEMENT
# ============================================================================

class ContextRefiner(ABC):
    """Base interface for context refinement."""
    
    @abstractmethod
    def refine(self, context: np.ndarray, quality_score: QualityScore,
              query: Optional[np.ndarray] = None) -> np.ndarray:
        """Refine context based on quality assessment."""
        pass

class AdaptiveRefiner(ContextRefiner):
    """Adaptive context refiner targeting specific quality deficits."""
    
    def __init__(self, d_model: int = 512, refinement_strength: float = 0.2):
        self.d_model = d_model
        self.refinement_strength = refinement_strength
        
        # Refinement transformation matrices
        self.coherence_transform = np.random.randn(d_model, d_model) * 0.02
        self.relevance_transform = np.random.randn(d_model, d_model) * 0.02
        self.completeness_transform = np.random.randn(d_model, d_model) * 0.02
        self.clarity_transform = np.random.randn(d_model, d_model) * 0.02
        
        # Smoothing kernel
        self.smoothing_kernel = self._create_gaussian_kernel(5)
    
    def refine(self, context: np.ndarray, quality_score: QualityScore,
              query: Optional[np.ndarray] = None) -> np.ndarray:
        """Apply targeted refinements based on quality deficits."""
        
        refined = context.copy()
        threshold = 0.6
        
        # Apply refinements for low-quality dimensions
        if quality_score.coherence < threshold:
            refined = self._improve_coherence(refined)
        
        if quality_score.relevance < threshold and query is not None:
            refined = self._improve_relevance(refined, query)
        
        if quality_score.completeness < threshold:
            refined = self._improve_completeness(refined)
        
        if quality_score.clarity < threshold:
            refined = self._improve_clarity(refined)
        
        # Apply smoothing
        refined = self._apply_smoothing(refined)
        
        return refined
    
    def _improve_coherence(self, context: np.ndarray) -> np.ndarray:
        """Improve semantic coherence."""
        transformed = context @ self.coherence_transform
        
        # Progressive blending
        blend_weights = np.linspace(0.1, self.refinement_strength, len(context))[:, None]
        return context * (1 - blend_weights) + transformed * blend_weights
    
    def _improve_relevance(self, context: np.ndarray, query: np.ndarray) -> np.ndarray:
        """Improve relevance to query."""
        query_repr = np.mean(query, axis=0) if len(query.shape) > 1 else query
        
        # Attention-like relevance weighting
        relevance_scores = np.dot(context, query_repr)
        relevance_weights = np.softmax(relevance_scores)
        
        # Query-conditioned transformation
        query_conditioned = context + query_repr[None, :] * 0.1
        transformed = query_conditioned @ self.relevance_transform
        
        # Weighted blending
        blend_weights = relevance_weights[:, None] * self.refinement_strength
        return context * (1 - blend_weights) + transformed * blend_weights
    
    def _improve_completeness(self, context: np.ndarray) -> np.ndarray:
        """Improve information completeness."""
        # Enhance under-represented directions
        try:
            cov_matrix = np.cov(context.T)
            eigenvals, eigenvecs = np.linalg.eigh(cov_matrix)
            
            # Focus on low-variance directions
            low_variance_dirs = eigenvecs[:, eigenvals < np.median(eigenvals)]
            
            if low_variance_dirs.shape[1] > 0:
                enhancement = context @ low_variance_dirs @ low_variance_dirs.T * 0.1
            else:
                enhancement = np.zeros_like(context)
            
            transformed = (context + enhancement) @ self.completeness_transform
        except:
            transformed = context @ self.completeness_transform
        
        blend_weight = self.refinement_strength * 0.5  # Conservative for completeness
        return context * (1 - blend_weight) + transformed * blend_weight
    
    def _improve_clarity(self, context: np.ndarray) -> np.ndarray:
        """Improve structural clarity."""
        transformed = context @ self.clarity_transform
        
        # Normalize magnitudes for consistency
        norms = np.linalg.norm(transformed, axis=1, keepdims=True)
        target_norm = np.median(norms)
        normalized = transformed * (target_norm / (norms + 1e-8))
        
        blend_weight = self.refinement_strength * 0.3  # Conservative for clarity
        return context * (1 - blend_weight) + normalized * blend_weight
    
    def _apply_smoothing(self, context: np.ndarray) -> np.ndarray:
        """Apply gentle smoothing."""
        if len(context) < len(self.smoothing_kernel):
            return context
        
        smoothed = np.zeros_like(context)
        kernel_half = len(self.smoothing_kernel) // 2
        
        for i in range(len(context)):
            start = max(0, i - kernel_half)
            end = min(len(context), i + kernel_half + 1)
            
            kernel_start = max(0, kernel_half - i)
            kernel_end = kernel_start + (end - start)
            
            if kernel_end <= len(self.smoothing_kernel):
                weights = self.smoothing_kernel[kernel_start:kernel_end]
                weights = weights / np.sum(weights)
                smoothed[i] = np.sum(context[start:end] * weights[:, None], axis=0)
            else:
                smoothed[i] = context[i]
        
        # Light blending with original
        return context * 0.9 + smoothed * 0.1
    
    def _create_gaussian_kernel(self, size: int) -> np.ndarray:
        """Create Gaussian smoothing kernel."""
        kernel = np.exp(-0.5 * ((np.arange(size) - size // 2) ** 2) / (size / 4) ** 2)
        return kernel / np.sum(kernel)

def np_softmax(x, axis=-1):
    """Numerically stable softmax."""
    max_vals = np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x - max_vals)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

np.softmax = np_softmax

# ============================================================================
# ITERATIVE REFINEMENT ENGINE
# ============================================================================

@dataclass
class RefinementIteration:
    """Single refinement iteration record."""
    iteration: int
    quality_before: QualityScore
    quality_after: QualityScore
    strategy: RefinementStrategy
    processing_time: float
    
    @property
    def improvement(self) -> float:
        return self.quality_after.overall - self.quality_before.overall

class IterativeRefiner:
    """Main iterative refinement engine with convergence detection."""
    
    def __init__(self, d_model: int = 512, max_iterations: int = 5,
                 convergence_threshold: float = 0.01, target_quality: float = 0.8):
        self.d_model = d_model
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.target_quality = target_quality
        
        # Core components
        self.assessor = EmbeddingQualityAssessor(d_model)
        self.refiner = AdaptiveRefiner(d_model)
        
        # Refinement history
        self.history: List[RefinementIteration] = []
    
    def refine(self, context: np.ndarray, query: Optional[np.ndarray] = None,
              target_quality: Optional[float] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Execute iterative refinement with convergence detection."""
        
        import time
        
        target = target_quality or self.target_quality
        current_context = context.copy()
        self.history = []
        
        # Initial assessment
        current_quality = self.assessor.assess(current_context, query)
        start_time = time.time()
        
        for iteration in range(self.max_iterations):
            iter_start = time.time()
            
            # Check if target reached
            if current_quality.overall >= target:
                break
            
            # Apply refinement
            refined_context = self.refiner.refine(current_context, current_quality, query)
            refined_quality = self.assessor.assess(refined_context, query)
            
            # Record iteration
            iter_record = RefinementIteration(
                iteration=iteration,
                quality_before=current_quality,
                quality_after=refined_quality,
                strategy=RefinementStrategy.ADAPTIVE,
                processing_time=time.time() - iter_start
            )
            self.history.append(iter_record)
            
            # Check for convergence
            improvement = iter_record.improvement
            if abs(improvement) < self.convergence_threshold:
                break
            
            # Check for degradation
            if improvement < -self.convergence_threshold * 2:
                # Revert and stop
                break
            
            # Update for next iteration
            current_context = refined_context
            current_quality = refined_quality
        
        total_time = time.time() - start_time
        
        return current_context, {
            'initial_quality': self.history[0].quality_before if self.history else current_quality,
            'final_quality': current_quality,
            'iterations': len(self.history),
            'total_improvement': current_quality.overall - (self.history[0].quality_before.overall if self.history else current_quality.overall),
            'processing_time': total_time,
            'converged': len(self.history) > 0 and abs(self.history[-1].improvement) < self.convergence_threshold,
            'target_reached': current_quality.overall >= target,
            'history': self.history
        }

# ============================================================================
# META-LEARNING CONTROLLER
# ============================================================================

class MetaController:
    """Meta-learning controller for strategy selection and adaptation."""
    
    def __init__(self):
        self.strategy_performance = {
            RefinementStrategy.CONSERVATIVE: [],
            RefinementStrategy.AGGRESSIVE: [],
            RefinementStrategy.ADAPTIVE: []
        }
        
        self.refiners = {
            RefinementStrategy.CONSERVATIVE: AdaptiveRefiner(refinement_strength=0.1),
            RefinementStrategy.AGGRESSIVE: AdaptiveRefiner(refinement_strength=0.4),
            RefinementStrategy.ADAPTIVE: AdaptiveRefiner(refinement_strength=0.2)
        }
    
    def select_strategy(self, initial_quality: QualityScore, 
                       context_length: int) -> RefinementStrategy:
        """Select optimal refinement strategy."""
        
        # Strategy selection heuristics
        if initial_quality.overall < 0.4:
            return RefinementStrategy.AGGRESSIVE
        elif initial_quality.overall > 0.7:
            return RefinementStrategy.CONSERVATIVE
        else:
            return RefinementStrategy.ADAPTIVE
    
    def get_refiner(self, strategy: RefinementStrategy) -> ContextRefiner:
        """Get refiner for strategy."""
        return self.refiners[strategy]
    
    def update_performance(self, strategy: RefinementStrategy, 
                          improvement: float, efficiency: float):
        """Update strategy performance tracking."""
        performance_score = improvement * efficiency
        self.strategy_performance[strategy].append(performance_score)

# ============================================================================
# CONSTITUTIONAL REFINEMENT
# ============================================================================

class ConstitutionalRefiner(ContextRefiner):
    """Value-aligned refinement based on constitutional principles."""
    
    def __init__(self, d_model: int = 512):
        self.d_model = d_model
        
        # Constitutional principles
        self.principles = {
            'helpfulness': 0.3,
            'harmlessness': 0.3,
            'honesty': 0.2,
            'clarity': 0.2
        }
        
        # Principle enforcement networks
        self.principle_transforms = {
            principle: np.random.randn(d_model, d_model) * 0.02
            for principle in self.principles.keys()
        }
    
    def refine(self, context: np.ndarray, quality_score: QualityScore,
              query: Optional[np.ndarray] = None, 
              violations: Optional[Dict[str, float]] = None) -> np.ndarray:
        """Apply constitutional refinement."""
        
        if violations is None:
            violations = self._detect_violations(context, quality_score)
        
        refined = context.copy()
        
        for principle, violation_score in violations.items():
            if violation_score > 0.3 and principle in self.principle_transforms:
                # Apply principle-specific transformation
                transform = self.principle_transforms[principle]
                transformed = context @ transform
                
                # Weighted blending based on violation severity and principle weight
                blend_weight = min(0.5, violation_score) * self.principles[principle]
                refined = refined * (1 - blend_weight) + transformed * blend_weight
        
        return refined
    
    def _detect_violations(self, context: np.ndarray, quality_score: QualityScore) -> Dict[str, float]:
        """Detect constitutional principle violations."""
        violations = {}
        
        # Map quality dimensions to constitutional principles
        violations['helpfulness'] = max(0, 0.8 - quality_score.relevance)
        violations['harmlessness'] = max(0, 0.9 - quality_score.safety)
        violations['honesty'] = max(0, 0.8 - quality_score.coherence)
        violations['clarity'] = max(0, 0.7 - quality_score.clarity)
        
        return violations

# ============================================================================
# PRODUCTION REFINEMENT PIPELINE
# ============================================================================

class RefinementPipeline:
    """Production-ready refinement pipeline with monitoring and caching."""
    
    def __init__(self, d_model: int = 512, enable_caching: bool = True):
        self.d_model = d_model
        self.enable_caching = enable_caching
        
        # Core components
        self.iterative_refiner = IterativeRefiner(d_model)
        self.meta_controller = MetaController()
        self.constitutional_refiner = ConstitutionalRefiner(d_model)
        
        # Performance tracking
        self.processing_stats = []
        self.cache = {} if enable_caching else None
    
    def refine(self, context: np.ndarray, query: Optional[np.ndarray] = None,
              target_quality: float = 0.8, 
              constitutional_check: bool = False) -> Dict[str, Any]:
        """Full refinement pipeline with monitoring."""
        
        import time
        start_time = time.time()
        
        # Cache check
        if self.cache:
            cache_key = hash((context.data.tobytes(), 
                             query.data.tobytes() if query is not None else b'', 
                             target_quality))
            if cache_key in self.cache:
                return self.cache[cache_key]
        
        # Initial assessment
        initial_quality = self.iterative_refiner.assessor.assess(context, query)
        
        # Strategy selection
        strategy = self.meta_controller.select_strategy(initial_quality, len(context))
        refiner = self.meta_controller.get_refiner(strategy)
        
        # Update refiner in iterative system
        self.iterative_refiner.refiner = refiner
        
        # Execute iterative refinement
        refined_context, refinement_stats = self.iterative_refiner.refine(
            context, query, target_quality
        )
        
        # Constitutional check if requested
        if constitutional_check:
            violations = self.constitutional_refiner._detect_violations(
                refined_context, refinement_stats['final_quality']
            )
            
            if any(score > 0.3 for score in violations.values()):
                refined_context = self.constitutional_refiner.refine(
                    refined_context, refinement_stats['final_quality'], 
                    query, violations
                )
                
                # Re-assess after constitutional refinement
                refinement_stats['final_quality'] = self.iterative_refiner.assessor.assess(
                    refined_context, query
                )
                refinement_stats['constitutional_applied'] = True
        
        # Update meta-controller performance
        improvement = refinement_stats['total_improvement']
        efficiency = improvement / refinement_stats['processing_time'] if refinement_stats['processing_time'] > 0 else 0
        self.meta_controller.update_performance(strategy, improvement, efficiency)
        
        # Create result
        result = {
            **refinement_stats,
            'strategy_used': strategy.value,
            'constitutional_applied': constitutional_check,
            'total_processing_time': time.time() - start_time
        }
        
        # Cache result
        if self.cache:
            self.cache[cache_key] = result
        
        # Record stats
        self.processing_stats.append({
            'context_length': len(context),
            'strategy': strategy.value,
            'improvement': improvement,
            'processing_time': result['total_processing_time'],
            'iterations': refinement_stats['iterations']
        })
        
        return result

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def compare_quality_scores(score1: QualityScore, score2: QualityScore) -> Dict[str, float]:
    """Compare two quality scores across dimensions."""
    return {
        'overall_diff': score2.overall - score1.overall,
        'coherence_diff': score2.coherence - score1.coherence,
        'relevance_diff': score2.relevance - score1.relevance,
        'completeness_diff': score2.completeness - score1.completeness,
        'clarity_diff': score2.clarity - score1.clarity,
        'safety_diff': score2.safety - score1.safety
    }

def benchmark_refinement(refiner_class, num_trials: int = 10, 
                        seq_len: int = 256, d_model: int = 512) -> Dict[str, Any]:
    """Benchmark refinement performance."""
    import time
    
    results = []
    
    for trial in range(num_trials):
        # Create random context with medium quality
        context = np.random.randn(seq_len, d_model) * 0.2
        query = np.random.randn(32, d_model) * 0.1
        
        refiner = refiner_class(d_model)
        
        start_time = time.time()
        if hasattr(refiner, 'refine') and len(refiner.refine.__code__.co_varnames) > 3:
            # IterativeRefiner or RefinementPipeline
            if isinstance(refiner, RefinementPipeline):
                result = refiner.refine(context, query)
                improvement = result['total_improvement']
                iterations = result['iterations']
            else:
                refined_context, stats = refiner.refine(context, query)
                improvement = stats['total_improvement']
                iterations = stats['iterations']
        else:
            # Simple refiner
            assessor = EmbeddingQualityAssessor(d_model)
            initial_quality = assessor.assess(context, query)
            refined_context = refiner.refine(context, initial_quality, query)
            final_quality = assessor.assess(refined_context, query)
            improvement = final_quality.overall - initial_quality.overall
            iterations = 1
        
        processing_time = time.time() - start_time
        
        results.append({
            'improvement': improvement,
            'iterations': iterations,
            'processing_time': processing_time,
            'efficiency': improvement / processing_time if processing_time > 0 else 0
        })
    
    return {
        'mean_improvement': np.mean([r['improvement'] for r in results]),
        'mean_processing_time': np.mean([r['processing_time'] for r in results]),
        'mean_iterations': np.mean([r['iterations'] for r in results]),
        'mean_efficiency': np.mean([r['efficiency'] for r in results]),
        'success_rate': sum(1 for r in results if r['improvement'] > 0.01) / num_trials
    }

def create_quality_report(quality_score: QualityScore) -> str:
    """Generate human-readable quality report."""
    
    def quality_level(score: float) -> str:
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Fair"
        else:
            return "Poor"
    
    report = f"""
Quality Assessment Report
========================
Overall Quality: {quality_score.overall:.3f} ({quality_level(quality_score.overall)})

Detailed Breakdown:
- Coherence:    {quality_score.coherence:.3f} ({quality_level(quality_score.coherence)})
- Relevance:    {quality_score.relevance:.3f} ({quality_level(quality_score.relevance)})
- Completeness: {quality_score.completeness:.3f} ({quality_level(quality_score.completeness)})
- Clarity:      {quality_score.clarity:.3f} ({quality_level(quality_score.clarity)})
- Safety:       {quality_score.safety:.3f} ({quality_level(quality_score.safety)})
"""
    return report.strip()

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage of refinement systems
    import time
    
    print("Refinement Loops Demonstration")
    print("=" * 50)
    
    # Create sample context (poor quality)
    seq_len = 256
    d_model = 512
    context = np.random.randn(seq_len, d_model) * 0.3  # High noise = poor quality
    query = np.random.randn(32, d_model) * 0.1
    
    # Test different refinement approaches
    systems = [
        ("Iterative Refiner", IterativeRefiner),
        ("Refinement Pipeline", RefinementPipeline)
    ]
    
    for name, system_class in systems:
        print(f"\n{name}:")
        print("-" * 30)
        
        system = system_class(d_model)
        
        start_time = time.time()
        if name == "Refinement Pipeline":
            result = system.refine(context, query, target_quality=0.75)
            
            print(f"  Initial quality: {result['initial_quality'].overall:.3f}")
            print(f"  Final quality: {result['final_quality'].overall:.3f}")
            print(f"  Improvement: {result['total_improvement']:+.3f}")
            print(f"  Iterations: {result['iterations']}")
            print(f"  Strategy: {result['strategy_used']}")
            print(f"  Converged: {result['converged']}")
            print(f"  Processing time: {result['total_processing_time']*1000:.2f}ms")
        else:
            refined_context, stats = system.refine(context, query, target_quality=0.75)
            
            print(f"  Initial quality: {stats['initial_quality'].overall:.3f}")
            print(f"  Final quality: {stats['final_quality'].overall:.3f}")
            print(f"  Improvement: {stats['total_improvement']:+.3f}")
            print(f"  Iterations: {stats['iterations']}")
            print(f"  Converged: {stats['converged']}")
            print(f"  Processing time: {stats['processing_time']*1000:.2f}ms")
    
    # Benchmark comparison
    print(f"\nBenchmark Comparison:")
    print("-" * 30)
    
    benchmark_systems = [
        ("Adaptive Refiner", AdaptiveRefiner),
        ("Iterative Refiner", IterativeRefiner),
        ("Refinement Pipeline", RefinementPipeline)
    ]
    
    for name, system_class in benchmark_systems:
        benchmark_result = benchmark_refinement(system_class, num_trials=5)
        
        print(f"\n{name}:")
        print(f"  Mean improvement: {benchmark_result['mean_improvement']:+.4f}")
        print(f"  Mean time: {benchmark_result['mean_processing_time']*1000:.2f}ms")
        print(f"  Success rate: {benchmark_result['success_rate']*100:.1f}%")
        print(f"  Efficiency: {benchmark_result['mean_efficiency']:.3f}")
    
    print(f"\nDemonstration Complete!")
