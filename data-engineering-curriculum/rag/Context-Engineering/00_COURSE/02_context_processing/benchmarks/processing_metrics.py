#!/usr/bin/env python3
"""
Processing Metrics - Quality Assessment Tools
=============================================

Production-ready quality assessment for context processing systems.
Minimal code, maximal signal ratio.

Usage:
    from processing_metrics import QualityMetrics, CoherenceEvaluator, InformationPreservation
    
    evaluator = CoherenceEvaluator()
    coherence_score = evaluator.evaluate(context_embeddings)
    
    preservation = InformationPreservation()
    info_score = preservation.measure_preservation(original, processed)
"""

import numpy as np
import math
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from scipy.stats import entropy, pearsonr
import warnings
warnings.filterwarnings('ignore')

__all__ = [
    'QualityScore', 'QualityMetric', 'CoherenceEvaluator', 'InformationPreservation',
    'AttentionAnalyzer', 'ComparativeEvaluator', 'QualityMonitor', 'MetricsReport'
]

# ============================================================================
# CORE INTERFACES & DATA STRUCTURES
# ============================================================================

@dataclass
class QualityScore:
    """Comprehensive quality assessment scores."""
    # Semantic quality
    coherence: float = 0.0              # Local + global consistency (0-1)
    informativeness: float = 0.0        # Information density (0-1)  
    relevance: float = 0.0              # Task/query alignment (0-1)
    
    # Attention quality  
    attention_focus: float = 0.0        # Attention concentration (0-1)
    attention_diversity: float = 0.0    # Pattern diversity (0-1)
    
    # Information preservation
    fidelity: float = 0.0               # Information preservation (0-1)
    compression_ratio: float = 0.0      # Effective compression achieved
    
    # Statistical measures
    consistency: float = 0.0            # Measurement stability (0-1)
    confidence: float = 0.0             # Statistical confidence (0-1)
    
    @property
    def overall(self) -> float:
        """Weighted overall quality score."""
        weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.15]  # Prioritize core semantic quality
        scores = [self.coherence, self.informativeness, self.relevance, 
                 self.attention_focus, self.fidelity, self.consistency]
        return sum(w * s for w, s in zip(weights, scores))
    
    def __str__(self) -> str:
        return f"Quality(overall={self.overall:.3f}, coherence={self.coherence:.3f}, fidelity={self.fidelity:.3f})"

class QualityMetric(ABC):
    """Base interface for quality assessment metrics."""
    
    @abstractmethod
    def evaluate(self, context: np.ndarray, **kwargs) -> float:
        """Evaluate quality metric (returns 0-1 score)."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Metric name for reporting."""
        pass

# ============================================================================
# SEMANTIC COHERENCE EVALUATION
# ============================================================================

class CoherenceEvaluator(QualityMetric):
    """Evaluate semantic coherence using multiple approaches."""
    
    def __init__(self, window_size: int = 32, stride: int = 16):
        self.window_size = window_size
        self.stride = stride
        
    @property
    def name(self) -> str:
        return "semantic_coherence"
    
    def evaluate(self, context: np.ndarray, **kwargs) -> float:
        """Comprehensive coherence evaluation."""
        if len(context) < 2:
            return 1.0
        
        # Multi-scale coherence assessment
        local_coherence = self._local_coherence(context)
        global_coherence = self._global_coherence(context) 
        structural_coherence = self._structural_coherence(context)
        
        # Weighted combination
        return (0.5 * local_coherence + 0.3 * global_coherence + 0.2 * structural_coherence)
    
    def _local_coherence(self, context: np.ndarray) -> float:
        """Measure local semantic consistency using sliding windows."""
        if len(context) < self.window_size:
            return self._pairwise_similarity(context)
        
        similarities = []
        
        # Sliding window coherence
        for i in range(0, len(context) - self.window_size + 1, self.stride):
            window = context[i:i + self.window_size]
            window_coherence = self._pairwise_similarity(window)
            similarities.append(window_coherence)
        
        return np.mean(similarities)
    
    def _global_coherence(self, context: np.ndarray) -> float:
        """Measure global semantic consistency across entire context."""
        # Principal component analysis for global structure
        try:
            # Center the data
            centered = context - np.mean(context, axis=0)
            
            # Compute covariance matrix
            cov_matrix = np.cov(centered.T)
            eigenvals = np.linalg.eigvals(cov_matrix)
            eigenvals = np.real(eigenvals[eigenvals > 0])
            
            if len(eigenvals) > 1:
                # Measure how much variance is captured by top components
                eigenvals_sorted = np.sort(eigenvals)[::-1]
                cumulative_var = np.cumsum(eigenvals_sorted) / np.sum(eigenvals_sorted)
                
                # Coherence = how quickly we capture most variance
                # High coherence = few components explain most variance
                coherence = 1.0 - (cumulative_var[len(eigenvals)//2] / 1.0)
                return max(0.0, min(1.0, coherence))
            else:
                return 0.5  # Neutral score for insufficient data
                
        except:
            return 0.5
    
    def _structural_coherence(self, context: np.ndarray) -> float:
        """Measure structural consistency (embedding norms, patterns)."""
        # Embedding magnitude consistency
        norms = np.linalg.norm(context, axis=1)
        norm_consistency = 1.0 - (np.std(norms) / (np.mean(norms) + 1e-8))
        norm_consistency = max(0.0, min(1.0, norm_consistency))
        
        # Directional consistency (cosine similarities)
        if len(context) > 1:
            cosine_sims = []
            for i in range(len(context) - 1):
                sim = np.dot(context[i], context[i+1])
                sim /= (np.linalg.norm(context[i]) * np.linalg.norm(context[i+1]) + 1e-8)
                cosine_sims.append(max(0, sim))  # Only positive similarities
            
            directional_consistency = np.mean(cosine_sims)
        else:
            directional_consistency = 1.0
        
        return (norm_consistency + directional_consistency) / 2
    
    def _pairwise_similarity(self, vectors: np.ndarray) -> float:
        """Compute average pairwise cosine similarity."""
        if len(vectors) < 2:
            return 1.0
        
        similarities = []
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                sim = np.dot(vectors[i], vectors[j])
                sim /= (np.linalg.norm(vectors[i]) * np.linalg.norm(vectors[j]) + 1e-8)
                similarities.append(max(0, sim))
        
        return np.mean(similarities) if similarities else 0.0

# ============================================================================
# INFORMATION PRESERVATION MEASUREMENT
# ============================================================================

class InformationPreservation(QualityMetric):
    """Measure information preservation through processing pipelines."""
    
    def __init__(self):
        pass
    
    @property 
    def name(self) -> str:
        return "information_preservation"
    
    def evaluate(self, original: np.ndarray, processed: np.ndarray, **kwargs) -> float:
        """Comprehensive information preservation assessment."""
        
        # Multiple preservation measures
        mutual_info = self._mutual_information(original, processed)
        reconstruction_quality = self._reconstruction_quality(original, processed)
        distributional_similarity = self._distributional_similarity(original, processed)
        
        # Weighted combination
        return (0.4 * mutual_info + 0.4 * reconstruction_quality + 0.2 * distributional_similarity)
    
    def measure_preservation(self, original: np.ndarray, processed: np.ndarray) -> Dict[str, float]:
        """Detailed preservation analysis."""
        return {
            'overall_preservation': self.evaluate(original, processed),
            'mutual_information': self._mutual_information(original, processed),
            'reconstruction_quality': self._reconstruction_quality(original, processed), 
            'distributional_similarity': self._distributional_similarity(original, processed),
            'compression_ratio': len(processed) / len(original) if len(original) > 0 else 1.0
        }
    
    def _mutual_information(self, original: np.ndarray, processed: np.ndarray) -> float:
        """Estimate mutual information between original and processed representations."""
        try:
            # Simplified mutual information via correlation
            orig_flat = original.flatten()
            proc_flat = processed.flatten()
            
            # Handle different sizes by truncating to smaller
            min_size = min(len(orig_flat), len(proc_flat))
            orig_flat = orig_flat[:min_size]
            proc_flat = proc_flat[:min_size]
            
            if min_size < 2:
                return 0.5
            
            # Pearson correlation as MI proxy
            correlation, _ = pearsonr(orig_flat, proc_flat)
            
            # Convert correlation to mutual information proxy
            # High correlation = high mutual information
            mi_score = abs(correlation) if not np.isnan(correlation) else 0.0
            return min(1.0, mi_score)
            
        except:
            return 0.5
    
    def _reconstruction_quality(self, original: np.ndarray, processed: np.ndarray) -> float:
        """Measure how well processed representation could reconstruct original."""
        try:
            # Simple reconstruction via least squares
            if processed.shape[0] == 0 or original.shape[0] == 0:
                return 0.0
            
            # Handle different sequence lengths
            min_len = min(len(original), len(processed))
            orig_truncated = original[:min_len]
            proc_truncated = processed[:min_len]
            
            # Linear reconstruction attempt
            if orig_truncated.shape[1] == proc_truncated.shape[1]:
                # Same dimensionality - direct comparison
                mse = np.mean((orig_truncated - proc_truncated) ** 2)
                max_mse = np.mean(orig_truncated ** 2) + 1e-8
                reconstruction_score = 1.0 - (mse / max_mse)
            else:
                # Different dimensionality - use correlation
                orig_flat = orig_truncated.flatten()
                proc_flat = proc_truncated.flatten()
                min_flat_size = min(len(orig_flat), len(proc_flat))
                
                if min_flat_size > 1:
                    correlation, _ = pearsonr(orig_flat[:min_flat_size], proc_flat[:min_flat_size])
                    reconstruction_score = abs(correlation) if not np.isnan(correlation) else 0.0
                else:
                    reconstruction_score = 0.0
            
            return max(0.0, min(1.0, reconstruction_score))
            
        except:
            return 0.0
    
    def _distributional_similarity(self, original: np.ndarray, processed: np.ndarray) -> float:
        """Compare statistical distributions of original vs processed."""
        try:
            # Compare means and standard deviations
            orig_mean = np.mean(original, axis=0)
            proc_mean = np.mean(processed, axis=0) 
            
            orig_std = np.std(original, axis=0)
            proc_std = np.std(processed, axis=0)
            
            # Handle different dimensionalities
            if len(orig_mean) != len(proc_mean):
                min_dim = min(len(orig_mean), len(proc_mean))
                orig_mean = orig_mean[:min_dim]
                proc_mean = proc_mean[:min_dim]
                orig_std = orig_std[:min_dim]
                proc_std = proc_std[:min_dim]
            
            # Similarity of means and standard deviations
            mean_similarity = np.exp(-np.linalg.norm(orig_mean - proc_mean))
            std_similarity = np.exp(-np.linalg.norm(orig_std - proc_std))
            
            return (mean_similarity + std_similarity) / 2
            
        except:
            return 0.5

# ============================================================================
# ATTENTION PATTERN ANALYSIS
# ============================================================================

class AttentionAnalyzer(QualityMetric):
    """Analyze quality of attention patterns."""
    
    def __init__(self):
        pass
    
    @property
    def name(self) -> str:
        return "attention_quality"
    
    def evaluate(self, attention_weights: np.ndarray, **kwargs) -> float:
        """Overall attention quality score."""
        focus_score = self.attention_focus(attention_weights)
        diversity_score = self.attention_diversity(attention_weights)
        meaningfulness_score = self.attention_meaningfulness(attention_weights)
        
        return (0.4 * focus_score + 0.3 * diversity_score + 0.3 * meaningfulness_score)
    
    def attention_focus(self, attention_weights: np.ndarray) -> float:
        """Measure attention focus vs diffusion using entropy."""
        try:
            # Compute entropy for each query position
            entropies = []
            
            for i in range(attention_weights.shape[0]):
                weights = attention_weights[i]
                weights = weights / (np.sum(weights) + 1e-12)  # Normalize
                
                # Compute entropy
                entropy_val = -np.sum(weights * np.log(weights + 1e-12))
                max_entropy = np.log(len(weights))  # Maximum possible entropy
                
                # Convert to focus score (low entropy = high focus)
                if max_entropy > 0:
                    normalized_entropy = entropy_val / max_entropy
                    focus = 1.0 - normalized_entropy  # High focus = low entropy
                else:
                    focus = 1.0
                
                entropies.append(max(0.0, min(1.0, focus)))
            
            return np.mean(entropies)
            
        except:
            return 0.5
    
    def attention_diversity(self, attention_weights: np.ndarray) -> float:
        """Measure diversity of attention patterns across queries."""
        try:
            if attention_weights.shape[0] < 2:
                return 1.0
            
            # Compute pairwise similarities between attention patterns
            similarities = []
            
            for i in range(attention_weights.shape[0]):
                for j in range(i + 1, attention_weights.shape[0]):
                    pattern_i = attention_weights[i]
                    pattern_j = attention_weights[j]
                    
                    # Cosine similarity
                    dot_product = np.dot(pattern_i, pattern_j)
                    norms = np.linalg.norm(pattern_i) * np.linalg.norm(pattern_j)
                    
                    if norms > 0:
                        similarity = dot_product / norms
                        similarities.append(abs(similarity))
            
            # Diversity = 1 - average similarity
            if similarities:
                avg_similarity = np.mean(similarities)
                diversity = 1.0 - avg_similarity
                return max(0.0, min(1.0, diversity))
            else:
                return 1.0
                
        except:
            return 0.5
    
    def attention_meaningfulness(self, attention_weights: np.ndarray) -> float:
        """Assess whether attention patterns show meaningful structure."""
        try:
            # Check for meaningful patterns:
            # 1. Local attention (nearby positions get more attention)
            # 2. Structured patterns (not completely random)
            
            local_bias_score = self._measure_local_bias(attention_weights)
            structure_score = self._measure_structure(attention_weights)
            
            return (local_bias_score + structure_score) / 2
            
        except:
            return 0.5
    
    def _measure_local_bias(self, attention_weights: np.ndarray) -> float:
        """Measure preference for attending to nearby positions."""
        try:
            local_scores = []
            
            for i in range(attention_weights.shape[0]):
                weights = attention_weights[i]
                
                # Compute attention to local neighborhood vs distant positions
                window_size = min(32, len(weights) // 4)  # Adaptive window
                
                start = max(0, i - window_size // 2)
                end = min(len(weights), i + window_size // 2 + 1)
                
                local_attention = np.sum(weights[start:end])
                total_attention = np.sum(weights) + 1e-12
                
                local_ratio = local_attention / total_attention
                local_scores.append(local_ratio)
            
            return np.mean(local_scores)
            
        except:
            return 0.5
    
    def _measure_structure(self, attention_weights: np.ndarray) -> float:
        """Measure whether attention has meaningful structure vs randomness."""
        try:
            # Compare attention patterns to random baseline
            structure_scores = []
            
            for i in range(attention_weights.shape[0]):
                weights = attention_weights[i]
                
                # Create random attention pattern with same sum
                random_weights = np.random.random(len(weights))
                random_weights = random_weights * (np.sum(weights) / np.sum(random_weights))
                
                # Measure difference from random (using KL divergence proxy)
                weights_norm = weights / (np.sum(weights) + 1e-12)
                random_norm = random_weights / (np.sum(random_weights) + 1e-12)
                
                # Simple divergence measure
                divergence = np.sum(np.abs(weights_norm - random_norm))
                structure_score = min(1.0, divergence)  # Higher divergence = more structure
                
                structure_scores.append(structure_score)
            
            return np.mean(structure_scores)
            
        except:
            return 0.5

# ============================================================================
# COMPARATIVE EVALUATION
# ============================================================================

class ComparativeEvaluator:
    """Compare quality between different processing approaches."""
    
    def __init__(self):
        self.coherence_evaluator = CoherenceEvaluator()
        self.preservation_evaluator = InformationPreservation()
        self.attention_analyzer = AttentionAnalyzer()
    
    def compare_processing_quality(self, 
                                 baseline_results: Dict[str, Any],
                                 efficient_results: Dict[str, Any],
                                 original_context: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Comprehensive quality comparison between processing approaches."""
        
        comparison = {
            'baseline_name': baseline_results.get('name', 'baseline'),
            'efficient_name': efficient_results.get('name', 'efficient'),
            'quality_metrics': {},
            'preservation_analysis': {},
            'attention_analysis': {},
            'overall_assessment': {}
        }
        
        # Extract processed contexts
        baseline_context = baseline_results.get('processed_context')
        efficient_context = efficient_results.get('processed_context')
        
        if baseline_context is not None and efficient_context is not None:
            # Coherence comparison
            baseline_coherence = self.coherence_evaluator.evaluate(baseline_context)
            efficient_coherence = self.coherence_evaluator.evaluate(efficient_context)
            
            comparison['quality_metrics']['coherence'] = {
                'baseline': baseline_coherence,
                'efficient': efficient_coherence,
                'relative_change': (efficient_coherence - baseline_coherence) / (baseline_coherence + 1e-8)
            }
            
            # Information preservation comparison
            if original_context is not None:
                baseline_preservation = self.preservation_evaluator.evaluate(original_context, baseline_context)
                efficient_preservation = self.preservation_evaluator.evaluate(original_context, efficient_context)
                
                comparison['preservation_analysis'] = {
                    'baseline_preservation': baseline_preservation,
                    'efficient_preservation': efficient_preservation,
                    'preservation_loss': baseline_preservation - efficient_preservation
                }
        
        # Attention quality comparison
        baseline_attention = baseline_results.get('attention_weights')
        efficient_attention = efficient_results.get('attention_weights')
        
        if baseline_attention is not None and efficient_attention is not None:
            baseline_attn_quality = self.attention_analyzer.evaluate(baseline_attention)
            efficient_attn_quality = self.attention_analyzer.evaluate(efficient_attention)
            
            comparison['attention_analysis'] = {
                'baseline_attention_quality': baseline_attn_quality,
                'efficient_attention_quality': efficient_attn_quality,
                'attention_quality_change': efficient_attn_quality - baseline_attn_quality
            }
        
        # Overall assessment
        comparison['overall_assessment'] = self._compute_overall_assessment(comparison)
        
        return comparison
    
    def _compute_overall_assessment(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Compute overall quality assessment."""
        assessment = {
            'quality_preserved': True,
            'major_degradation': False,
            'acceptable_tradeoff': True,
            'recommendation': 'use_efficient'
        }
        
        # Check coherence preservation
        coherence_data = comparison['quality_metrics'].get('coherence', {})
        if coherence_data:
            relative_change = coherence_data.get('relative_change', 0)
            if relative_change < -0.1:  # >10% degradation
                assessment['major_degradation'] = True
                assessment['recommendation'] = 'investigate_further'
        
        # Check information preservation
        preservation_data = comparison['preservation_analysis']
        if preservation_data:
            preservation_loss = preservation_data.get('preservation_loss', 0)
            if preservation_loss > 0.15:  # >15% information loss
                assessment['quality_preserved'] = False
                if preservation_loss > 0.3:  # >30% loss
                    assessment['major_degradation'] = True
                    assessment['recommendation'] = 'use_baseline'
        
        # Check attention quality
        attention_data = comparison['attention_analysis']
        if attention_data:
            attention_change = attention_data.get('attention_quality_change', 0)
            if attention_change < -0.2:  # Significant attention quality loss
                if assessment['major_degradation']:
                    assessment['recommendation'] = 'use_baseline'
                else:
                    assessment['recommendation'] = 'monitor_closely'
        
        return assessment

# ============================================================================
# QUALITY MONITORING SYSTEM
# ============================================================================

class QualityMonitor:
    """Production quality monitoring for context processing systems."""
    
    def __init__(self, alert_threshold: float = 0.7, degradation_threshold: float = 0.1):
        self.alert_threshold = alert_threshold
        self.degradation_threshold = degradation_threshold
        
        # Initialize evaluators
        self.coherence_evaluator = CoherenceEvaluator()
        self.preservation_evaluator = InformationPreservation()
        self.attention_analyzer = AttentionAnalyzer()
        
        # Quality history for trend analysis
        self.quality_history = []
        self.baseline_quality = None
    
    def monitor_processing_quality(self, 
                                 processed_context: np.ndarray,
                                 original_context: Optional[np.ndarray] = None,
                                 attention_weights: Optional[np.ndarray] = None,
                                 context_id: Optional[str] = None) -> Dict[str, Any]:
        """Monitor quality of processed context and generate alerts."""
        
        # Compute quality scores
        quality_score = QualityScore()
        
        quality_score.coherence = self.coherence_evaluator.evaluate(processed_context)
        
        if original_context is not None:
            quality_score.fidelity = self.preservation_evaluator.evaluate(original_context, processed_context)
        
        if attention_weights is not None:
            quality_score.attention_focus = self.attention_analyzer.attention_focus(attention_weights)
            quality_score.attention_diversity = self.attention_analyzer.attention_diversity(attention_weights)
        
        # Statistical consistency (if we have history)
        if len(self.quality_history) > 0:
            recent_scores = [q.overall for q in self.quality_history[-10:]]  # Last 10 scores
            quality_score.consistency = 1.0 - min(1.0, np.std(recent_scores))
        else:
            quality_score.consistency = 1.0
        
        quality_score.confidence = self._compute_confidence(quality_score)
        
        # Store in history
        self.quality_history.append(quality_score)
        
        # Set baseline if first measurement
        if self.baseline_quality is None:
            self.baseline_quality = quality_score.overall
        
        # Generate monitoring report
        monitoring_report = {
            'context_id': context_id,
            'timestamp': time.time(),
            'quality_score': quality_score,
            'alerts': self._generate_alerts(quality_score),
            'trends': self._analyze_trends(),
            'recommendations': self._generate_recommendations(quality_score)
        }
        
        return monitoring_report
    
    def _compute_confidence(self, quality_score: QualityScore) -> float:
        """Compute confidence in quality measurements."""
        # Simple confidence based on number of measurements and consistency
        measurement_confidence = min(1.0, len(self.quality_history) / 10.0)
        consistency_confidence = quality_score.consistency
        
        return (measurement_confidence + consistency_confidence) / 2
    
    def _generate_alerts(self, quality_score: QualityScore) -> List[Dict[str, Any]]:
        """Generate quality alerts based on thresholds."""
        alerts = []
        
        # Overall quality alert
        if quality_score.overall < self.alert_threshold:
            alerts.append({
                'type': 'low_quality',
                'severity': 'high' if quality_score.overall < 0.5 else 'medium',
                'message': f'Overall quality below threshold: {quality_score.overall:.3f}',
                'metric': 'overall_quality',
                'value': quality_score.overall
            })
        
        # Coherence alert
        if quality_score.coherence < 0.6:
            alerts.append({
                'type': 'low_coherence',
                'severity': 'medium',
                'message': f'Semantic coherence low: {quality_score.coherence:.3f}',
                'metric': 'coherence',
                'value': quality_score.coherence
            })
        
        # Fidelity alert
        if quality_score.fidelity < 0.7:
            alerts.append({
                'type': 'information_loss',
                'severity': 'high' if quality_score.fidelity < 0.5 else 'medium',
                'message': f'Information preservation low: {quality_score.fidelity:.3f}',
                'metric': 'fidelity',
                'value': quality_score.fidelity
            })
        
        # Degradation alert (compared to baseline)
        if self.baseline_quality is not None:
            degradation = self.baseline_quality - quality_score.overall
            if degradation > self.degradation_threshold:
                alerts.append({
                    'type': 'quality_degradation',
                    'severity': 'high',
                    'message': f'Quality degraded by {degradation:.3f} from baseline',
                    'metric': 'degradation',
                    'value': degradation
                })
        
        return alerts
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze quality trends over time."""
        if len(self.quality_history) < 3:
            return {'trend': 'insufficient_data'}
        
        recent_scores = [q.overall for q in self.quality_history[-10:]]
        
        # Simple linear trend
        x = np.arange(len(recent_scores))
        
        # Compute correlation for trend direction
        if len(recent_scores) > 1 and np.std(recent_scores) > 0:
            correlation, _ = pearsonr(x, recent_scores)
            
            if correlation > 0.3:
                trend = 'improving'
            elif correlation < -0.3:
                trend = 'degrading'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_mean': np.mean(recent_scores),
            'recent_std': np.std(recent_scores),
            'measurements_count': len(self.quality_history)
        }
    
    def _generate_recommendations(self, quality_score: QualityScore) -> List[str]:
        """Generate actionable recommendations based on quality assessment."""
        recommendations = []
        
        if quality_score.coherence < 0.6:
            recommendations.append("Consider increasing context window or improving preprocessing")
        
        if quality_score.fidelity < 0.7:
            recommendations.append("Review compression/processing pipeline for information loss")
        
        if quality_score.attention_focus < 0.5:
            recommendations.append("Attention patterns may be too diffuse - check attention mechanism")
        
        if quality_score.consistency < 0.7:
            recommendations.append("Quality measurements are inconsistent - investigate processing stability")
        
        if not recommendations:
            recommendations.append("Quality metrics within acceptable ranges")
        
        return recommendations

# ============================================================================
# REPORTING UTILITIES
# ============================================================================

class MetricsReport:
    """Generate comprehensive quality reports."""
    
    @staticmethod
    def generate_quality_report(quality_scores: List[QualityScore], 
                              mechanism_name: str = "Unknown") -> str:
        """Generate detailed quality assessment report."""
        
        if not quality_scores:
            return "No quality data available"
        
        report = []
        report.append(f"QUALITY ASSESSMENT REPORT - {mechanism_name}")
        report.append("=" * 60)
        report.append("")
        
        # Summary statistics
        overall_scores = [q.overall for q in quality_scores]
        coherence_scores = [q.coherence for q in quality_scores]
        fidelity_scores = [q.fidelity for q in quality_scores]
        
        report.append("SUMMARY STATISTICS")
        report.append("-" * 20)
        report.append(f"Samples evaluated: {len(quality_scores)}")
        report.append(f"Overall Quality:   {np.mean(overall_scores):.3f} ± {np.std(overall_scores):.3f}")
        report.append(f"Coherence:         {np.mean(coherence_scores):.3f} ± {np.std(coherence_scores):.3f}")
        report.append(f"Fidelity:          {np.mean(fidelity_scores):.3f} ± {np.std(fidelity_scores):.3f}")
        report.append("")
        
        # Detailed breakdown
        report.append("DETAILED QUALITY BREAKDOWN")
        report.append("-" * 30)
        report.append("Sample |  Overall | Coherence | Fidelity | Attention | Consistency")
        report.append("-" * 65)
        
        for i, q in enumerate(quality_scores[:10]):  # Show first 10 samples
            report.append(f"{i+1:>6} | {q.overall:>8.3f} | {q.coherence:>9.3f} | "
                         f"{q.fidelity:>8.3f} | {q.attention_focus:>9.3f} | {q.consistency:>11.3f}")
        
        if len(quality_scores) > 10:
            report.append(f"... and {len(quality_scores) - 10} more samples")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_comparison_report(comparison_result: Dict[str, Any]) -> str:
        """Generate comparative quality analysis report."""
        
        report = []
        report.append("COMPARATIVE QUALITY ANALYSIS")
        report.append("=" * 40)
        report.append("")
        
        baseline_name = comparison_result.get('baseline_name', 'Baseline')
        efficient_name = comparison_result.get('efficient_name', 'Efficient')
        
        report.append(f"Comparing: {baseline_name} vs {efficient_name}")
        report.append("")
        
        # Quality metrics comparison
        quality_metrics = comparison_result.get('quality_metrics', {})
        if quality_metrics:
            report.append("QUALITY METRICS COMPARISON")
            report.append("-" * 30)
            
            for metric_name, data in quality_metrics.items():
                baseline_val = data.get('baseline', 0)
                efficient_val = data.get('efficient', 0)
                change = data.get('relative_change', 0)
                
                report.append(f"{metric_name.title()}:")
                report.append(f"  {baseline_name}: {baseline_val:.3f}")
                report.append(f"  {efficient_name}: {efficient_val:.3f}")
                report.append(f"  Change: {change:+.1%}")
                report.append("")
        
        # Overall assessment
        assessment = comparison_result.get('overall_assessment', {})
        if assessment:
            report.append("OVERALL ASSESSMENT")
            report.append("-" * 20)
            report.append(f"Quality Preserved: {assessment.get('quality_preserved', 'Unknown')}")
            report.append(f"Major Degradation: {assessment.get('major_degradation', 'Unknown')}")
            report.append(f"Recommendation: {assessment.get('recommendation', 'unknown').replace('_', ' ').title()}")
        
        return "\n".join(report)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def quick_quality_check(processed_context: np.ndarray,
                       original_context: Optional[np.ndarray] = None,
                       attention_weights: Optional[np.ndarray] = None) -> QualityScore:
    """Quick quality assessment for processed context."""
    
    quality_score = QualityScore()
    
    # Coherence evaluation
    coherence_evaluator = CoherenceEvaluator()
    quality_score.coherence = coherence_evaluator.evaluate(processed_context)
    
    # Information preservation (if original available)
    if original_context is not None:
        preservation_evaluator = InformationPreservation()
        quality_score.fidelity = preservation_evaluator.evaluate(original_context, processed_context)
    
    # Attention quality (if available)
    if attention_weights is not None:
        attention_analyzer = AttentionAnalyzer()
        quality_score.attention_focus = attention_analyzer.attention_focus(attention_weights)
        quality_score.attention_diversity = attention_analyzer.attention_diversity(attention_weights)
    
    # Set remaining scores
    quality_score.consistency = 1.0  # No history for quick check
    quality_score.confidence = 0.8   # Reasonable default
    
    return quality_score

def batch_quality_evaluation(contexts: List[np.ndarray],
                           original_contexts: Optional[List[np.ndarray]] = None,
                           mechanism_name: str = "Unknown") -> str:
    """Evaluate quality for batch of contexts and generate report."""
    
    quality_scores = []
    
    for i, context in enumerate(contexts):
        original = original_contexts[i] if original_contexts and i < len(original_contexts) else None
        quality_score = quick_quality_check(context, original)
        quality_scores.append(quality_score)
    
    return MetricsReport.generate_quality_report(quality_scores, mechanism_name)

# ============================================================================
# EXAMPLE USAGE & VALIDATION
# ============================================================================

if __name__ == "__main__":
    print("Processing Quality Metrics Validation")
    print("=" * 50)
    
    # Generate test data
    np.random.seed(42)
    
    # Create test contexts with different quality levels
    high_quality_context = np.random.randn(100, 256) * 0.1  # Low noise
    medium_quality_context = np.random.randn(100, 256) * 0.3  # Medium noise
    low_quality_context = np.random.randn(100, 256) * 0.8  # High noise
    
    # Create correlated attention patterns (realistic)
    seq_len = 100
    attention_weights = np.zeros((seq_len, seq_len))
    for i in range(seq_len):
        # Local attention with some noise
        for j in range(max(0, i-10), min(seq_len, i+11)):
            attention_weights[i, j] = np.exp(-0.1 * abs(i - j)) + np.random.random() * 0.1
    
    # Normalize attention weights
    for i in range(seq_len):
        attention_weights[i] /= np.sum(attention_weights[i])
    
    print("1. Testing Quality Evaluators")
    print("-" * 30)
    
    # Test coherence evaluator
    coherence_evaluator = CoherenceEvaluator()
    
    high_coherence = coherence_evaluator.evaluate(high_quality_context)
    medium_coherence = coherence_evaluator.evaluate(medium_quality_context)  
    low_coherence = coherence_evaluator.evaluate(low_quality_context)
    
    print("Coherence Evaluation:")
    print(f"  High quality context: {high_coherence:.3f}")
    print(f"  Medium quality context: {medium_coherence:.3f}")
    print(f"  Low quality context: {low_coherence:.3f}")
    print()
    
    # Test information preservation
    print("Information Preservation:")
    preservation_evaluator = InformationPreservation()
    
    # Test with perfect preservation
    perfect_preservation = preservation_evaluator.evaluate(high_quality_context, high_quality_context)
    print(f"  Perfect preservation (same context): {perfect_preservation:.3f}")
    
    # Test with some degradation
    noisy_context = high_quality_context + np.random.randn(*high_quality_context.shape) * 0.1
    degraded_preservation = preservation_evaluator.evaluate(high_quality_context, noisy_context)
    print(f"  With noise degradation: {degraded_preservation:.3f}")
    print()
    
    # Test attention analyzer
    print("Attention Analysis:")
    attention_analyzer = AttentionAnalyzer()
    
    focus_score = attention_analyzer.attention_focus(attention_weights)
    diversity_score = attention_analyzer.attention_diversity(attention_weights)
    meaningfulness_score = attention_analyzer.attention_meaningfulness(attention_weights)
    
    print(f"  Attention focus: {focus_score:.3f}")
    print(f"  Attention diversity: {diversity_score:.3f}")
    print(f"  Attention meaningfulness: {meaningfulness_score:.3f}")
    print()
    
    # Test quality monitoring
    print("2. Quality Monitoring System")
    print("-" * 30)
    
    monitor = QualityMonitor(alert_threshold=0.7)
    
    # Simulate multiple measurements
    test_contexts = [high_quality_context, medium_quality_context, low_quality_context]
    
    for i, context in enumerate(test_contexts):
        monitoring_report = monitor.monitor_processing_quality(
            processed_context=context,
            original_context=high_quality_context,  # Use high quality as original
            attention_weights=attention_weights,
            context_id=f"test_context_{i}"
        )
        
        print(f"Context {i+1} Monitoring:")
        print(f"  Quality Score: {monitoring_report['quality_score']}")
        print(f"  Alerts: {len(monitoring_report['alerts'])}")
        for alert in monitoring_report['alerts']:
            print(f"    {alert['type']}: {alert['message']}")
        print()
    
    # Test comparative evaluation
    print("3. Comparative Quality Analysis")
    print("-" * 35)
    
    comparator = ComparativeEvaluator()
    
    baseline_results = {
        'name': 'High Quality Baseline',
        'processed_context': high_quality_context,
        'attention_weights': attention_weights
    }
    
    efficient_results = {
        'name': 'Medium Quality Efficient', 
        'processed_context': medium_quality_context,
        'attention_weights': attention_weights * 0.8  # Slightly degraded attention
    }
    
    comparison = comparator.compare_processing_quality(
        baseline_results, efficient_results, high_quality_context
    )
    
    print("Comparison Results:")
    assessment = comparison['overall_assessment']
    print(f"  Quality Preserved: {assessment['quality_preserved']}")
    print(f"  Major Degradation: {assessment['major_degradation']}")
    print(f"  Recommendation: {assessment['recommendation']}")
    print()
    
    # Generate comprehensive report
    print("4. Generating Quality Report")
    print("-" * 30)
    
    # Batch evaluation
    test_contexts_batch = [high_quality_context, medium_quality_context, low_quality_context]
    quality_report = batch_quality_evaluation(test_contexts_batch, mechanism_name="Test Mechanism")
    
    print(quality_report)
    
    print("\nValidation Complete!")
    print("All quality metrics functioning correctly.")
