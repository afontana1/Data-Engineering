#!/usr/bin/env python3
"""
Long Context Evaluation - Performance Measurement
=================================================

Benchmarking system for long context processing.
Minimal code, maximal signal ratio.

Usage:
    from long_context_evaluation import PerformanceBenchmark, ScalabilityAnalyzer
    
    benchmark = PerformanceBenchmark()
    results = benchmark.evaluate_attention_mechanisms(seq_lengths=[512, 1024, 2048])
    
    analyzer = ScalabilityAnalyzer()
    report = analyzer.generate_report(results)
"""

import numpy as np
import time
import psutil
import os
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import gc

__all__ = [
    'BenchmarkResult', 'PerformanceMetrics', 'MemoryProfiler', 'PerformanceBenchmark',
    'ScalabilityAnalyzer', 'QualityEvaluator', 'ComparisonReport'
]

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics for attention mechanisms."""
    mechanism_name: str
    sequence_length: int
    
    # Timing metrics
    forward_time_ms: float
    memory_peak_mb: float
    memory_allocated_mb: float
    
    # Computational metrics
    operations_count: int
    memory_complexity: str  # O(n²), O(n√n), etc.
    theoretical_ops: int
    
    # Efficiency metrics
    throughput_tokens_per_sec: float
    memory_efficiency: float  # vs baseline
    computational_efficiency: float  # actual vs theoretical
    
    # Quality metrics (optional)
    attention_entropy: Optional[float] = None
    output_norm: Optional[float] = None
    sparsity: Optional[float] = None
    
    def __post_init__(self):
        """Calculate derived metrics."""
        if self.forward_time_ms > 0:
            self.throughput_tokens_per_sec = (self.sequence_length * 1000) / self.forward_time_ms
        else:
            self.throughput_tokens_per_sec = 0.0

@dataclass
class BenchmarkResult:
    """Complete benchmark results for a single mechanism."""
    mechanism_name: str
    metrics: List[PerformanceMetrics]
    configuration: Dict[str, Any]
    timestamp: float
    
    @property
    def sequence_lengths(self) -> List[int]:
        return [m.sequence_length for m in self.metrics]
    
    @property
    def forward_times(self) -> List[float]:
        return [m.forward_time_ms for m in self.metrics]
    
    @property
    def memory_peaks(self) -> List[float]:
        return [m.memory_peak_mb for m in self.metrics]
    
    @property
    def throughputs(self) -> List[float]:
        return [m.throughput_tokens_per_sec for m in self.metrics]

# ============================================================================
# MEMORY PROFILING
# ============================================================================

class MemoryProfiler:
    """Accurate memory usage profiling for attention mechanisms."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = 0
        self.peak_memory = 0
        
    def start_profiling(self):
        """Start memory profiling session."""
        gc.collect()  # Clean up before measurement
        self.baseline_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = self.baseline_memory
        
    def update_peak(self):
        """Update peak memory if current usage is higher."""
        current_memory = self.process.memory_info().rss / 1024 / 1024
        self.peak_memory = max(self.peak_memory, current_memory)
        
    def get_metrics(self) -> Tuple[float, float]:
        """Get memory metrics: (peak_mb, allocated_mb)."""
        self.update_peak()
        allocated = self.peak_memory - self.baseline_memory
        return self.peak_memory, max(0, allocated)

# ============================================================================
# PERFORMANCE BENCHMARK
# ============================================================================

class PerformanceBenchmark:
    """Comprehensive performance benchmarking suite."""
    
    def __init__(self, d_model: int = 512, num_heads: int = 8, warmup_runs: int = 3):
        self.d_model = d_model
        self.num_heads = num_heads
        self.warmup_runs = warmup_runs
        self.memory_profiler = MemoryProfiler()
        
    def evaluate_attention_mechanism(self, 
                                   attention_class: type,
                                   sequence_lengths: List[int],
                                   num_trials: int = 5,
                                   **mechanism_kwargs) -> BenchmarkResult:
        """Evaluate single attention mechanism across sequence lengths."""
        
        mechanism_name = attention_class.__name__
        metrics = []
        
        print(f"Benchmarking {mechanism_name}...")
        
        for seq_len in sequence_lengths:
            print(f"  Testing sequence length: {seq_len:,}")
            
            # Skip if sequence is too large for mechanism
            if self._should_skip_sequence(mechanism_name, seq_len):
                print(f"    Skipped (too large for {mechanism_name})")
                continue
            
            # Run benchmark for this sequence length
            seq_metrics = self._benchmark_sequence_length(
                attention_class, seq_len, num_trials, **mechanism_kwargs
            )
            
            if seq_metrics:
                metrics.append(seq_metrics)
                print(f"    Time: {seq_metrics.forward_time_ms:.2f}ms, "
                      f"Memory: {seq_metrics.memory_peak_mb:.1f}MB, "
                      f"Throughput: {seq_metrics.throughput_tokens_per_sec:.0f} tokens/sec")
        
        return BenchmarkResult(
            mechanism_name=mechanism_name,
            metrics=metrics,
            configuration={
                'd_model': self.d_model,
                'num_heads': self.num_heads,
                'num_trials': num_trials,
                **mechanism_kwargs
            },
            timestamp=time.time()
        )
    
    def _benchmark_sequence_length(self, 
                                  attention_class: type,
                                  seq_len: int,
                                  num_trials: int,
                                  **mechanism_kwargs) -> Optional[PerformanceMetrics]:
        """Benchmark specific sequence length."""
        
        try:
            # Initialize mechanism
            mechanism = attention_class(
                d_model=self.d_model, 
                num_heads=self.num_heads,
                **mechanism_kwargs
            )
            
            # Create test data
            x = np.random.randn(seq_len, self.d_model) * 0.1
            
            # Warmup runs
            for _ in range(self.warmup_runs):
                try:
                    _ = mechanism(x)
                except:
                    pass
            
            # Benchmark runs
            times = []
            memory_peaks = []
            memory_allocations = []
            attention_entropies = []
            output_norms = []
            sparsities = []
            
            for trial in range(num_trials):
                # Memory profiling
                self.memory_profiler.start_profiling()
                
                # Time the forward pass
                start_time = time.perf_counter()
                output, info = mechanism(x)
                end_time = time.perf_counter()
                
                # Record metrics
                forward_time = (end_time - start_time) * 1000  # milliseconds
                peak_mb, allocated_mb = self.memory_profiler.get_metrics()
                
                times.append(forward_time)
                memory_peaks.append(peak_mb)
                memory_allocations.append(allocated_mb)
                
                # Quality metrics
                if 'attention_weights' in info:
                    entropy = self._compute_attention_entropy(info['attention_weights'])
                    attention_entropies.append(entropy)
                
                output_norms.append(np.linalg.norm(output))
                sparsities.append(info.get('sparsity', 1.0))
            
            # Aggregate metrics
            mean_time = np.mean(times)
            mean_memory_peak = np.mean(memory_peaks)
            mean_memory_allocated = np.mean(memory_allocations)
            
            # Computational complexity analysis
            operations_count = self._estimate_operations(mechanism_class=attention_class, seq_len=seq_len)
            memory_complexity = self._get_memory_complexity(attention_class.__name__)
            theoretical_ops = seq_len * seq_len * self.d_model  # Standard attention baseline
            
            return PerformanceMetrics(
                mechanism_name=attention_class.__name__,
                sequence_length=seq_len,
                forward_time_ms=mean_time,
                memory_peak_mb=mean_memory_peak,
                memory_allocated_mb=mean_memory_allocated,
                operations_count=operations_count,
                memory_complexity=memory_complexity,
                theoretical_ops=theoretical_ops,
                throughput_tokens_per_sec=(seq_len * 1000) / mean_time if mean_time > 0 else 0,
                memory_efficiency=theoretical_ops / max(1, operations_count),
                computational_efficiency=theoretical_ops / max(1, operations_count),
                attention_entropy=np.mean(attention_entropies) if attention_entropies else None,
                output_norm=np.mean(output_norms),
                sparsity=np.mean(sparsities) if sparsities else None
            )
            
        except Exception as e:
            print(f"    Error benchmarking {attention_class.__name__}: {e}")
            return None
    
    def evaluate_multiple_mechanisms(self, 
                                   mechanisms_config: Dict[str, Dict[str, Any]],
                                   sequence_lengths: List[int],
                                   num_trials: int = 5) -> Dict[str, BenchmarkResult]:
        """Evaluate multiple attention mechanisms."""
        
        results = {}
        
        for mechanism_name, config in mechanisms_config.items():
            attention_class = config['class']
            mechanism_kwargs = config.get('kwargs', {})
            
            result = self.evaluate_attention_mechanism(
                attention_class=attention_class,
                sequence_lengths=sequence_lengths,
                num_trials=num_trials,
                **mechanism_kwargs
            )
            
            results[mechanism_name] = result
        
        return results
    
    def _should_skip_sequence(self, mechanism_name: str, seq_len: int) -> bool:
        """Determine if sequence is too large for mechanism."""
        # Conservative limits to avoid memory issues
        if mechanism_name == "StandardAttention" and seq_len > 2048:
            return True
        if seq_len > 50000:  # Very large sequences
            return True
        return False
    
    def _estimate_operations(self, mechanism_class: type, seq_len: int) -> int:
        """Estimate computational operations for mechanism."""
        class_name = mechanism_class.__name__
        
        if class_name == "StandardAttention":
            return seq_len * seq_len * self.d_model  # O(n²)
        elif class_name == "SparseAttention":
            sparsity = 0.1  # Estimated sparsity
            return int(seq_len * seq_len * self.d_model * sparsity)  # O(n²) * sparsity
        elif class_name == "StreamingAttention":
            cache_size = getattr(mechanism_class, 'cache_size', 1024)
            return seq_len * min(cache_size, seq_len) * self.d_model  # O(n) for large sequences
        elif class_name == "FlashAttention":
            return seq_len * seq_len * self.d_model  # Same ops, different memory pattern
        else:
            return seq_len * seq_len * self.d_model  # Default to O(n²)
    
    def _get_memory_complexity(self, mechanism_name: str) -> str:
        """Get memory complexity notation for mechanism."""
        complexity_map = {
            "StandardAttention": "O(n²)",
            "SparseAttention": "O(n√n)",
            "StreamingAttention": "O(1)",
            "FlashAttention": "O(n)",
            "CrossModalAttention": "O(n²)"
        }
        return complexity_map.get(mechanism_name, "O(n²)")
    
    def _compute_attention_entropy(self, attention_weights: np.ndarray) -> float:
        """Compute attention entropy (measure of focus)."""
        # Avoid log(0) with small epsilon
        safe_weights = attention_weights + 1e-12
        entropy = -np.sum(attention_weights * np.log(safe_weights), axis=-1)
        return float(np.mean(entropy))

# ============================================================================
# SCALABILITY ANALYZER
# ============================================================================

class ScalabilityAnalyzer:
    """Analyze scalability characteristics of attention mechanisms."""
    
    def __init__(self):
        self.complexity_patterns = {
            "O(1)": lambda n: np.ones_like(n),
            "O(n)": lambda n: n,
            "O(n√n)": lambda n: n * np.sqrt(n),
            "O(n²)": lambda n: n * n,
            "O(n³)": lambda n: n * n * n
        }
    
    def analyze_scaling_behavior(self, results: Dict[str, BenchmarkResult]) -> Dict[str, Dict[str, Any]]:
        """Analyze scaling behavior of different mechanisms."""
        
        analysis = {}
        
        for mechanism_name, result in results.items():
            if not result.metrics:
                continue
            
            seq_lengths = np.array(result.sequence_lengths)
            times = np.array(result.forward_times)
            memory_usage = np.array(result.memory_peaks)
            
            analysis[mechanism_name] = {
                'time_scaling': self._fit_complexity_curve(seq_lengths, times),
                'memory_scaling': self._fit_complexity_curve(seq_lengths, memory_usage),
                'efficiency_analysis': self._analyze_efficiency(result),
                'scalability_score': self._compute_scalability_score(result)
            }
        
        return analysis
    
    def _fit_complexity_curve(self, seq_lengths: np.ndarray, values: np.ndarray) -> Dict[str, float]:
        """Fit complexity curves to observed data."""
        if len(seq_lengths) < 2:
            return {'best_fit': 'insufficient_data', 'r_squared': 0.0}
        
        best_fit = None
        best_r_squared = -1
        
        for complexity_name, complexity_func in self.complexity_patterns.items():
            try:
                # Generate theoretical curve
                theoretical = complexity_func(seq_lengths)
                
                # Normalize both curves
                if np.max(theoretical) > 0:
                    theoretical_norm = theoretical / np.max(theoretical)
                    values_norm = values / np.max(values) if np.max(values) > 0 else values
                    
                    # Compute R-squared
                    ss_res = np.sum((values_norm - theoretical_norm) ** 2)
                    ss_tot = np.sum((values_norm - np.mean(values_norm)) ** 2)
                    r_squared = 1 - (ss_res / (ss_tot + 1e-10))
                    
                    if r_squared > best_r_squared:
                        best_r_squared = r_squared
                        best_fit = complexity_name
                
            except:
                continue
        
        return {
            'best_fit': best_fit or 'unknown',
            'r_squared': max(0.0, best_r_squared)
        }
    
    def _analyze_efficiency(self, result: BenchmarkResult) -> Dict[str, float]:
        """Analyze efficiency characteristics."""
        if not result.metrics:
            return {}
        
        # Efficiency trends
        throughputs = result.throughputs
        memory_peaks = result.memory_peaks
        
        throughput_trend = self._compute_trend(throughputs)
        memory_trend = self._compute_trend(memory_peaks)
        
        return {
            'throughput_trend': throughput_trend,  # Positive = improving with scale
            'memory_trend': memory_trend,          # Negative = better (less memory growth)
            'peak_throughput': max(throughputs) if throughputs else 0,
            'memory_efficiency': min(memory_peaks) / max(memory_peaks) if memory_peaks else 1.0
        }
    
    def _compute_scalability_score(self, result: BenchmarkResult) -> float:
        """Compute overall scalability score (0-100)."""
        if not result.metrics:
            return 0.0
        
        # Factors contributing to scalability
        throughput_consistency = 1.0 - (np.std(result.throughputs) / (np.mean(result.throughputs) + 1e-10))
        memory_efficiency = 1.0 / (1.0 + np.mean(result.memory_peaks) / 1000)  # Normalize by GB
        
        # Complexity penalty
        complexity_penalty = {
            "O(1)": 0.0, "O(n)": 0.1, "O(n√n)": 0.3, "O(n²)": 0.6, "O(n³)": 0.9
        }
        
        first_metric = result.metrics[0]
        penalty = complexity_penalty.get(first_metric.memory_complexity, 0.5)
        
        # Combined score
        score = (throughput_consistency * 0.4 + memory_efficiency * 0.4 + (1 - penalty) * 0.2) * 100
        return max(0.0, min(100.0, score))
    
    def _compute_trend(self, values: List[float]) -> float:
        """Compute trend direction (-1 to 1, where 1 is strong positive trend)."""
        if len(values) < 2:
            return 0.0
        
        # Simple linear trend
        x = np.arange(len(values))
        y = np.array(values)
        
        # Correlation coefficient as trend measure
        if np.std(x) > 0 and np.std(y) > 0:
            correlation = np.corrcoef(x, y)[0, 1]
            return correlation if not np.isnan(correlation) else 0.0
        else:
            return 0.0

# ============================================================================
# QUALITY EVALUATOR
# ============================================================================

class QualityEvaluator:
    """Evaluate quality preservation in efficient attention mechanisms."""
    
    def __init__(self, d_model: int = 512):
        self.d_model = d_model
    
    def compare_attention_quality(self, 
                                baseline_class: type,
                                efficient_class: type,
                                sequence_lengths: List[int],
                                num_samples: int = 10) -> Dict[str, Any]:
        """Compare attention quality between baseline and efficient mechanisms."""
        
        quality_comparisons = []
        
        for seq_len in sequence_lengths:
            print(f"Comparing quality at sequence length {seq_len}")
            
            seq_comparisons = []
            
            for sample in range(num_samples):
                # Generate test data
                x = np.random.randn(seq_len, self.d_model) * 0.1
                
                try:
                    # Baseline mechanism
                    baseline = baseline_class(self.d_model)
                    baseline_output, baseline_info = baseline(x)
                    
                    # Efficient mechanism  
                    efficient = efficient_class(self.d_model)
                    efficient_output, efficient_info = efficient(x)
                    
                    # Quality comparison
                    comparison = self._compare_outputs(
                        baseline_output, efficient_output,
                        baseline_info, efficient_info
                    )
                    
                    comparison['sequence_length'] = seq_len
                    seq_comparisons.append(comparison)
                    
                except Exception as e:
                    print(f"  Error in comparison: {e}")
                    continue
            
            if seq_comparisons:
                # Aggregate comparisons for this sequence length
                quality_comparisons.append({
                    'sequence_length': seq_len,
                    'output_similarity': np.mean([c['output_similarity'] for c in seq_comparisons]),
                    'attention_similarity': np.mean([c['attention_similarity'] for c in seq_comparisons if c['attention_similarity'] is not None]),
                    'quality_preservation': np.mean([c['quality_preservation'] for c in seq_comparisons]),
                    'samples_compared': len(seq_comparisons)
                })
        
        return {
            'comparisons': quality_comparisons,
            'baseline_mechanism': baseline_class.__name__,
            'efficient_mechanism': efficient_class.__name__,
            'overall_quality_preservation': np.mean([c['quality_preservation'] for c in quality_comparisons]) if quality_comparisons else 0.0
        }
    
    def _compare_outputs(self, 
                        baseline_output: np.ndarray,
                        efficient_output: np.ndarray,
                        baseline_info: Dict,
                        efficient_info: Dict) -> Dict[str, Any]:
        """Compare outputs from two attention mechanisms."""
        
        # Output similarity (cosine similarity)
        baseline_flat = baseline_output.flatten()
        efficient_flat = efficient_output.flatten()
        
        dot_product = np.dot(baseline_flat, efficient_flat)
        norms_product = np.linalg.norm(baseline_flat) * np.linalg.norm(efficient_flat)
        output_similarity = dot_product / (norms_product + 1e-10)
        
        # Attention pattern similarity (if available)
        attention_similarity = None
        if 'attention_weights' in baseline_info and 'attention_weights' in efficient_info:
            baseline_attn = baseline_info['attention_weights'].flatten()
            efficient_attn = efficient_info['attention_weights'].flatten()
            
            # Handle different sizes (e.g., sparse vs full attention)
            min_size = min(len(baseline_attn), len(efficient_attn))
            baseline_attn = baseline_attn[:min_size]
            efficient_attn = efficient_attn[:min_size]
            
            if min_size > 0:
                attn_dot = np.dot(baseline_attn, efficient_attn)
                attn_norms = np.linalg.norm(baseline_attn) * np.linalg.norm(efficient_attn)
                attention_similarity = attn_dot / (attn_norms + 1e-10)
        
        # Quality preservation score
        quality_preservation = output_similarity
        if attention_similarity is not None:
            quality_preservation = (output_similarity + attention_similarity) / 2
        
        return {
            'output_similarity': float(output_similarity),
            'attention_similarity': float(attention_similarity) if attention_similarity is not None else None,
            'quality_preservation': float(quality_preservation)
        }

# ============================================================================
# COMPARISON REPORT GENERATOR
# ============================================================================

class ComparisonReport:
    """Generate comprehensive comparison reports."""
    
    @staticmethod
    def generate_performance_report(results: Dict[str, BenchmarkResult]) -> str:
        """Generate detailed performance report."""
        
        report = []
        report.append("LONG CONTEXT PERFORMANCE EVALUATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Summary statistics
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 20)
        
        for name, result in results.items():
            if result.metrics:
                avg_throughput = np.mean(result.throughputs)
                max_seq_len = max(result.sequence_lengths)
                avg_memory = np.mean(result.memory_peaks)
                
                report.append(f"{name}:")
                report.append(f"  Average Throughput: {avg_throughput:,.0f} tokens/sec")
                report.append(f"  Max Sequence Length: {max_seq_len:,} tokens") 
                report.append(f"  Average Memory Usage: {avg_memory:.1f} MB")
                report.append(f"  Complexity: {result.metrics[0].memory_complexity}")
                report.append("")
        
        # Detailed breakdown
        report.append("DETAILED PERFORMANCE BREAKDOWN")
        report.append("-" * 35)
        report.append("")
        
        for name, result in results.items():
            report.append(f"{name} Performance Analysis:")
            report.append("  Seq Length | Time (ms) | Memory (MB) | Throughput (tok/sec)")
            report.append("  " + "-" * 55)
            
            for metric in result.metrics:
                report.append(f"  {metric.sequence_length:>9,} | "
                            f"{metric.forward_time_ms:>8.2f} | "
                            f"{metric.memory_peak_mb:>10.1f} | "
                            f"{metric.throughput_tokens_per_sec:>15,.0f}")
            
            report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_scalability_report(analysis: Dict[str, Dict[str, Any]]) -> str:
        """Generate scalability analysis report."""
        
        report = []
        report.append("SCALABILITY ANALYSIS REPORT")
        report.append("=" * 40)
        report.append("")
        
        for mechanism_name, analysis_data in analysis.items():
            report.append(f"{mechanism_name} Scalability Analysis:")
            report.append("-" * (len(mechanism_name) + 22))
            
            # Time scaling
            time_scaling = analysis_data['time_scaling']
            report.append(f"Time Complexity: {time_scaling['best_fit']} "
                         f"(R² = {time_scaling['r_squared']:.3f})")
            
            # Memory scaling
            memory_scaling = analysis_data['memory_scaling']
            report.append(f"Memory Complexity: {memory_scaling['best_fit']} "
                         f"(R² = {memory_scaling['r_squared']:.3f})")
            
            # Efficiency analysis
            efficiency = analysis_data['efficiency_analysis']
            report.append(f"Throughput Trend: {efficiency['throughput_trend']:+.3f}")
            report.append(f"Peak Throughput: {efficiency['peak_throughput']:,.0f} tokens/sec")
            report.append(f"Memory Efficiency: {efficiency['memory_efficiency']:.3f}")
            
            # Overall score
            score = analysis_data['scalability_score']
            report.append(f"Scalability Score: {score:.1f}/100")
            report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_comparison_table(results: Dict[str, BenchmarkResult]) -> str:
        """Generate side-by-side comparison table."""
        
        # Find common sequence lengths
        all_seq_lens = set()
        for result in results.values():
            all_seq_lens.update(result.sequence_lengths)
        
        common_seq_lens = sorted(all_seq_lens)
        mechanisms = list(results.keys())
        
        # Create comparison table
        table = []
        table.append("PERFORMANCE COMPARISON TABLE")
        table.append("=" * 50)
        table.append("")
        
        # Header
        header = "Seq Length | " + " | ".join(f"{name[:12]:>12s}" for name in mechanisms)
        table.append(header)
        table.append("-" * len(header))
        
        # Rows for each sequence length
        for seq_len in common_seq_lens:
            row_parts = [f"{seq_len:>9,}"]
            
            for mechanism_name in mechanisms:
                result = results[mechanism_name]
                # Find metric for this sequence length
                metric = None
                for m in result.metrics:
                    if m.sequence_length == seq_len:
                        metric = m
                        break
                
                if metric:
                    # Show throughput in tokens/sec
                    throughput = f"{metric.throughput_tokens_per_sec:>10,.0f}t/s"
                else:
                    throughput = f"{'N/A':>12s}"
                
                row_parts.append(throughput)
            
            table.append(" | ".join(row_parts))
        
        return "\n".join(table)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def quick_benchmark(attention_classes: List[type], 
                   sequence_lengths: List[int] = [256, 512, 1024],
                   d_model: int = 512) -> Dict[str, BenchmarkResult]:
    """Quick benchmark for multiple attention mechanisms."""
    
    benchmark = PerformanceBenchmark(d_model=d_model)
    
    mechanisms_config = {}
    for attention_class in attention_classes:
        mechanisms_config[attention_class.__name__] = {
            'class': attention_class,
            'kwargs': {}
        }
    
    return benchmark.evaluate_multiple_mechanisms(
        mechanisms_config=mechanisms_config,
        sequence_lengths=sequence_lengths,
        num_trials=3
    )

def save_benchmark_results(results: Dict[str, BenchmarkResult], filename: str):
    """Save benchmark results to JSON file."""
    
    # Convert to serializable format
    serializable_results = {}
    
    for name, result in results.items():
        serializable_results[name] = {
            'mechanism_name': result.mechanism_name,
            'configuration': result.configuration,
            'timestamp': result.timestamp,
            'metrics': []
        }
        
        for metric in result.metrics:
            serializable_results[name]['metrics'].append({
                'mechanism_name': metric.mechanism_name,
                'sequence_length': metric.sequence_length,
                'forward_time_ms': metric.forward_time_ms,
                'memory_peak_mb': metric.memory_peak_mb,
                'memory_allocated_mb': metric.memory_allocated_mb,
                'operations_count': metric.operations_count,
                'memory_complexity': metric.memory_complexity,
                'theoretical_ops': metric.theoretical_ops,
                'throughput_tokens_per_sec': metric.throughput_tokens_per_sec,
                'memory_efficiency': metric.memory_efficiency,
                'computational_efficiency': metric.computational_efficiency,
                'attention_entropy': metric.attention_entropy,
                'output_norm': metric.output_norm,
                'sparsity': metric.sparsity
            })
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2)

def load_benchmark_results(filename: str) -> Dict[str, BenchmarkResult]:
    """Load benchmark results from JSON file."""
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    results = {}
    
    for name, result_data in data.items():
        metrics = []
        for metric_data in result_data['metrics']:
            metrics.append(PerformanceMetrics(**metric_data))
        
        results[name] = BenchmarkResult(
            mechanism_name=result_data['mechanism_name'],
            metrics=metrics,
            configuration=result_data['configuration'],
            timestamp=result_data['timestamp']
        )
    
    return results

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Import attention mechanisms (assuming they're available)
    try:
        from attention_mechanisms import StandardAttention, SparseAttention, StreamingAttention
        
        print("Long Context Performance Evaluation")
        print("=" * 50)
        
        # Quick benchmark
        attention_classes = [StandardAttention, SparseAttention, StreamingAttention]
        sequence_lengths = [128, 256, 512, 1024]
        
        print("\nRunning comprehensive benchmark...")
        results = quick_benchmark(attention_classes, sequence_lengths)
        
        # Performance report
        print("\n" + ComparisonReport.generate_performance_report(results))
        
        # Scalability analysis
        analyzer = ScalabilityAnalyzer()
        scalability_analysis = analyzer.analyze_scaling_behavior(results)
        print("\n" + ComparisonReport.generate_scalability_report(scalability_analysis))
        
        # Comparison table
        print("\n" + ComparisonReport.generate_comparison_table(results))
        
        # Quality evaluation (comparing sparse vs standard)
        print("\nEvaluating quality preservation...")
        quality_evaluator = QualityEvaluator()
        quality_results = quality_evaluator.compare_attention_quality(
            StandardAttention, SparseAttention, [256, 512], num_samples=3
        )
        
        print(f"\nQuality Preservation Analysis:")
        print(f"Baseline: {quality_results['baseline_mechanism']}")
        print(f"Efficient: {quality_results['efficient_mechanism']}")
        print(f"Overall Quality Preservation: {quality_results['overall_quality_preservation']:.3f}")
        
        for comp in quality_results['comparisons']:
            print(f"  Seq {comp['sequence_length']:>4}: "
                  f"Output similarity: {comp['output_similarity']:.3f}, "
                  f"Quality: {comp['quality_preservation']:.3f}")
        
        # Save results
        print("\nSaving benchmark results...")
        save_benchmark_results(results, "benchmark_results.json")
        print("Results saved to benchmark_results.json")
        
    except ImportError:
        print("Attention mechanisms not available. Running with mock data...")
        
        # Create mock benchmark results for demonstration
        from dataclasses import replace
        
        mock_results = {}
        mechanisms = ["StandardAttention", "SparseAttention", "StreamingAttention"]
        seq_lengths = [256, 512, 1024]
        
        for mech in mechanisms:
            metrics = []
            for seq_len in seq_lengths:
                # Mock performance data
                base_time = seq_len * 0.001  # Base time scaling
                if mech == "StandardAttention":
                    time_ms = base_time * seq_len  # O(n²)
                    memory_mb = seq_len * seq_len * 0.000004  # O(n²) memory
                elif mech == "SparseAttention":
                    time_ms = base_time * np.sqrt(seq_len)  # O(n√n)
                    memory_mb = seq_len * np.sqrt(seq_len) * 0.000004
                else:  # StreamingAttention
                    time_ms = base_time  # O(1) time for large sequences
                    memory_mb = 50  # Constant memory
                
                metrics.append(PerformanceMetrics(
                    mechanism_name=mech,
                    sequence_length=seq_len,
                    forward_time_ms=time_ms,
                    memory_peak_mb=memory_mb,
                    memory_allocated_mb=memory_mb * 0.8,
                    operations_count=int(seq_len * seq_len),
                    memory_complexity="O(n²)" if "Standard" in mech else "O(n√n)" if "Sparse" in mech else "O(1)",
                    theoretical_ops=seq_len * seq_len * 512,
                    throughput_tokens_per_sec=0,  # Will be calculated
                    memory_efficiency=1.0,
                    computational_efficiency=1.0
                ))
            
            mock_results[mech] = BenchmarkResult(
                mechanism_name=mech,
                metrics=metrics,
                configuration={'d_model': 512, 'num_heads': 8},
                timestamp=time.time()
            )
        
        print("Mock Benchmark Results:")
        print("=" * 30)
        print(ComparisonReport.generate_performance_report(mock_results))
        print(ComparisonReport.generate_comparison_table(mock_results))
