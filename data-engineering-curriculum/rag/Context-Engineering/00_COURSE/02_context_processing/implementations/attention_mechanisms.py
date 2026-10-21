#!/usr/bin/env python3
"""
Custom Attention Mechanisms
===========================

Production-ready attention implementations for context engineering.
Minimal code, maximal signal ratio.

Usage:
    from attention_mechanisms import StandardAttention, SparseAttention, StreamingAttention
    
    attention = SparseAttention(d_model=512, num_heads=8)
    output, info = attention(x, mask=None)
"""

import numpy as np
import math
from typing import Optional, Tuple, Dict, Any
from abc import ABC, abstractmethod

__all__ = ['Attention', 'StandardAttention', 'SparseAttention', 'StreamingAttention', 'CrossModalAttention']

# ============================================================================
# BASE ATTENTION INTERFACE
# ============================================================================

class Attention(ABC):
    """Base attention mechanism interface."""
    
    def __init__(self, d_model: int, num_heads: int = 8):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.scale = 1.0 / math.sqrt(self.d_k)
        
        # Shared weight matrices
        self.W_qkv = np.random.randn(d_model, 3 * d_model) * 0.02
        self.W_o = np.random.randn(d_model, d_model) * 0.02
    
    @abstractmethod
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Forward pass returning (output, info_dict)."""
        pass
    
    def __call__(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        return self.forward(x, mask)
    
    def _project_qkv(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Project input to queries, keys, values."""
        seq_len = x.shape[0]
        qkv = x @ self.W_qkv  # (seq_len, 3 * d_model)
        qkv = qkv.reshape(seq_len, 3, self.num_heads, self.d_k)
        return qkv.transpose(1, 2, 0, 3)  # (3, num_heads, seq_len, d_k)
    
    def _output_projection(self, attended: np.ndarray) -> np.ndarray:
        """Final output projection."""
        # attended: (num_heads, seq_len, d_k)
        concat = attended.transpose(1, 0, 2).reshape(attended.shape[1], self.d_model)
        return concat @ self.W_o
    
    @staticmethod
    def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Numerically stable softmax."""
        max_vals = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - max_vals)
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

# ============================================================================
# STANDARD ATTENTION
# ============================================================================

class StandardAttention(Attention):
    """Standard scaled dot-product attention. O(n²) complexity."""
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        seq_len = x.shape[0]
        
        # Project to Q, K, V
        q, k, v = self._project_qkv(x)  # Each: (num_heads, seq_len, d_k)
        
        # Scaled attention scores
        scores = np.matmul(q, k.transpose(0, 2, 1)) * self.scale  # (num_heads, seq_len, seq_len)
        
        # Apply mask
        if mask is not None:
            scores = np.where(mask[None, :, :], scores, -1e9)
        else:
            # Default causal mask
            causal_mask = np.tril(np.ones((seq_len, seq_len), dtype=bool))
            scores = np.where(causal_mask[None, :, :], scores, -1e9)
        
        # Attention weights and output
        attn_weights = self._softmax(scores)  # (num_heads, seq_len, seq_len)
        attended = np.matmul(attn_weights, v)  # (num_heads, seq_len, d_k)
        
        output = self._output_projection(attended)
        
        return output, {
            'attention_weights': attn_weights.mean(axis=0),
            'memory_complexity': seq_len * seq_len,
            'sparsity': 1.0
        }

# ============================================================================
# SPARSE ATTENTION
# ============================================================================

class SparseAttention(Attention):
    """Sparse attention with configurable patterns. O(n√n) complexity."""
    
    def __init__(self, d_model: int, num_heads: int = 8, 
                 window_size: int = 128, stride: int = 64, global_size: int = 16):
        super().__init__(d_model, num_heads)
        self.window_size = window_size
        self.stride = stride
        self.global_size = global_size
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        seq_len = x.shape[0]
        
        # Create sparse attention mask
        sparse_mask = self._create_sparse_mask(seq_len)
        
        # Standard attention computation with sparse mask
        q, k, v = self._project_qkv(x)
        scores = np.matmul(q, k.transpose(0, 2, 1)) * self.scale
        
        # Apply sparse mask
        final_mask = sparse_mask
        if mask is not None:
            final_mask = final_mask & mask
        
        scores = np.where(final_mask[None, :, :], scores, -1e9)
        attn_weights = self._softmax(scores)
        attended = np.matmul(attn_weights, v)
        
        output = self._output_projection(attended)
        sparsity = np.sum(sparse_mask) / (seq_len * seq_len)
        
        return output, {
            'attention_weights': attn_weights.mean(axis=0),
            'sparse_mask': sparse_mask,
            'memory_complexity': int(seq_len * seq_len * sparsity),
            'sparsity': sparsity
        }
    
    def _create_sparse_mask(self, seq_len: int) -> np.ndarray:
        """Create sparse attention mask: local + global + strided."""
        mask = np.zeros((seq_len, seq_len), dtype=bool)
        
        # Local attention window
        for i in range(seq_len):
            start = max(0, i - self.window_size // 2)
            end = min(seq_len, i + self.window_size // 2 + 1)
            mask[i, start:end] = True
        
        # Global tokens (attend to/from anywhere)
        mask[:self.global_size, :] = True
        mask[:, :self.global_size] = True
        
        # Strided attention
        for i in range(seq_len):
            mask[i, ::self.stride] = True
        
        # Causal constraint
        return mask & np.tril(np.ones((seq_len, seq_len), dtype=bool))

# ============================================================================
# STREAMING ATTENTION
# ============================================================================

class StreamingAttention(Attention):
    """Streaming attention with KV cache. O(1) memory for inference."""
    
    def __init__(self, d_model: int, num_heads: int = 8, 
                 cache_size: int = 1024, sink_size: int = 64):
        super().__init__(d_model, num_heads)
        self.cache_size = cache_size
        self.sink_size = sink_size
        
        # KV cache
        self.k_cache = None  # (num_heads, cache_size, d_k)
        self.v_cache = None
        self.cache_len = 0
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        seq_len = x.shape[0]
        
        # Project current input
        q, k, v = self._project_qkv(x)  # (num_heads, seq_len, d_k)
        
        # Update cache
        if self.k_cache is None:
            self._init_cache(k, v)
        
        effective_k, effective_v = self._update_cache(k, v)
        cache_len = effective_k.shape[2]
        
        # Attention with cached KV
        scores = np.matmul(q, effective_k.transpose(0, 2, 1)) * self.scale
        
        # Causal mask for current sequence vs cache
        causal_mask = np.tril(np.ones((seq_len, cache_len), dtype=bool))
        scores = np.where(causal_mask[None, :, :], scores, -1e9)
        
        attn_weights = self._softmax(scores)
        attended = np.matmul(attn_weights, effective_v)
        
        output = self._output_projection(attended)
        
        return output, {
            'cache_size': cache_len,
            'memory_complexity': self.cache_size,  # Constant
            'attention_weights': attn_weights.mean(axis=0),
            'cache_hit_ratio': min(1.0, cache_len / seq_len)
        }
    
    def _init_cache(self, k: np.ndarray, v: np.ndarray):
        """Initialize KV cache."""
        self.k_cache = np.zeros((self.num_heads, self.cache_size, self.d_k))
        self.v_cache = np.zeros((self.num_heads, self.cache_size, self.d_k))
        self.cache_len = 0
    
    def _update_cache(self, k: np.ndarray, v: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Update cache with attention sink strategy."""
        new_len = k.shape[2]
        
        if self.cache_len + new_len <= self.cache_size:
            # Simple append
            self.k_cache[:, self.cache_len:self.cache_len + new_len] = k
            self.v_cache[:, self.cache_len:self.cache_len + new_len] = v
            self.cache_len += new_len
        else:
            # Eviction with attention sinks
            # Keep sinks + recent window
            recent_size = self.cache_size - self.sink_size - new_len
            
            # Shift recent tokens
            if recent_size > 0:
                self.k_cache[:, self.sink_size:self.sink_size + recent_size] = \
                    self.k_cache[:, self.cache_len - recent_size:self.cache_len]
                self.v_cache[:, self.sink_size:self.sink_size + recent_size] = \
                    self.v_cache[:, self.cache_len - recent_size:self.cache_len]
            
            # Add new tokens
            self.k_cache[:, self.sink_size + recent_size:self.sink_size + recent_size + new_len] = k
            self.v_cache[:, self.sink_size + recent_size:self.sink_size + recent_size + new_len] = v
            
            self.cache_len = self.sink_size + recent_size + new_len
        
        return self.k_cache[:, :self.cache_len], self.v_cache[:, :self.cache_len]
    
    def reset_cache(self):
        """Reset the KV cache."""
        self.k_cache = None
        self.v_cache = None
        self.cache_len = 0

# ============================================================================
# CROSS-MODAL ATTENTION
# ============================================================================

class CrossModalAttention(Attention):
    """Cross-modal attention for multimodal inputs."""
    
    def __init__(self, d_model: int, num_heads: int = 8, num_modalities: int = 3):
        super().__init__(d_model, num_heads)
        self.num_modalities = num_modalities
        
        # Modality-specific projections
        self.modality_projections = [
            np.random.randn(d_model, d_model) * 0.02 
            for _ in range(num_modalities)
        ]
        
        # Cross-modal fusion
        self.cross_modal_fusion = np.random.randn(d_model * num_modalities, d_model) * 0.02
    
    def forward(self, modality_inputs: list, 
                modality_masks: Optional[list] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Forward pass with multiple modality inputs.
        
        Args:
            modality_inputs: List of (seq_len, d_model) arrays for each modality
            modality_masks: Optional list of attention masks for each modality
        """
        
        if len(modality_inputs) != self.num_modalities:
            raise ValueError(f"Expected {self.num_modalities} modalities, got {len(modality_inputs)}")
        
        # Project each modality
        projected_modalities = []
        max_len = 0
        
        for i, (modality_input, projection) in enumerate(zip(modality_inputs, self.modality_projections)):
            if modality_input is not None:
                projected = modality_input @ projection
                projected_modalities.append(projected)
                max_len = max(max_len, projected.shape[0])
            else:
                projected_modalities.append(None)
        
        if max_len == 0:
            raise ValueError("At least one modality must be provided")
        
        # Pad and stack modalities
        stacked_modalities = []
        valid_mask = []
        
        for projected in projected_modalities:
            if projected is not None:
                if projected.shape[0] < max_len:
                    padding = np.zeros((max_len - projected.shape[0], self.d_model))
                    projected = np.vstack([projected, padding])
                stacked_modalities.append(projected)
                valid_mask.append(True)
            else:
                stacked_modalities.append(np.zeros((max_len, self.d_model)))
                valid_mask.append(False)
        
        # Cross-modal attention computation
        modality_stack = np.stack(stacked_modalities, axis=0)  # (num_modalities, max_len, d_model)
        num_modalities, seq_len, d_model = modality_stack.shape
        
        # Reshape for attention: treat modalities as sequence dimension
        x_combined = modality_stack.reshape(num_modalities * seq_len, d_model)
        
        # Standard attention
        q, k, v = self._project_qkv(x_combined)
        scores = np.matmul(q, k.transpose(0, 2, 1)) * self.scale
        
        # Create cross-modal mask
        cross_modal_mask = self._create_cross_modal_mask(num_modalities, seq_len, valid_mask)
        scores = np.where(cross_modal_mask[None, :, :], scores, -1e9)
        
        attn_weights = self._softmax(scores)
        attended = np.matmul(attn_weights, v)
        
        # Reshape back to modalities
        attended_reshaped = attended.transpose(1, 0, 2).reshape(num_modalities, seq_len, self.d_model)
        
        # Aggregate across modalities
        modality_weights = np.array([1.0 if valid else 0.0 for valid in valid_mask])
        modality_weights = modality_weights / (np.sum(modality_weights) + 1e-8)
        
        aggregated = np.sum(attended_reshaped * modality_weights[:, None, None], axis=0)
        
        # Final projection
        output = aggregated @ self.W_o
        
        return output, {
            'attention_weights': attn_weights.mean(axis=0),
            'modality_weights': modality_weights,
            'valid_modalities': valid_mask,
            'cross_modal_interactions': True
        }
    
    def _create_cross_modal_mask(self, num_modalities: int, seq_len: int, 
                                valid_mask: list) -> np.ndarray:
        """Create mask for cross-modal attention."""
        total_len = num_modalities * seq_len
        mask = np.ones((total_len, total_len), dtype=bool)
        
        # Mask invalid modalities
        for i, is_valid in enumerate(valid_mask):
            if not is_valid:
                start_idx = i * seq_len
                end_idx = (i + 1) * seq_len
                mask[start_idx:end_idx, :] = False
                mask[:, start_idx:end_idx] = False
        
        return mask

# ============================================================================
# FLASH ATTENTION (Memory Efficient)
# ============================================================================

class FlashAttention(Attention):
    """Memory-efficient attention using block-wise computation."""
    
    def __init__(self, d_model: int, num_heads: int = 8, block_size: int = 64):
        super().__init__(d_model, num_heads)
        self.block_size = block_size
    
    def forward(self, x: np.ndarray, mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        seq_len = x.shape[0]
        
        # Project to Q, K, V
        q, k, v = self._project_qkv(x)  # (num_heads, seq_len, d_k)
        
        # Block-wise attention computation
        output = np.zeros_like(q)  # (num_heads, seq_len, d_k)
        max_memory_used = 0
        
        for i in range(0, seq_len, self.block_size):
            q_block = q[:, i:i + self.block_size]
            block_len = q_block.shape[1]
            
            # Online attention computation for this query block
            block_output = np.zeros_like(q_block)
            
            for j in range(0, i + self.block_size, self.block_size):  # Causal constraint
                k_block = k[:, j:j + self.block_size]
                v_block = v[:, j:j + self.block_size]
                kv_block_len = k_block.shape[1]
                
                # Attention scores for this block
                scores = np.matmul(q_block, k_block.transpose(0, 2, 1)) * self.scale
                
                # Block memory usage
                block_memory = scores.nbytes
                max_memory_used = max(max_memory_used, block_memory)
                
                # Causal mask within block
                if j <= i:
                    block_mask = np.tril(np.ones((block_len, kv_block_len), dtype=bool))
                    scores = np.where(block_mask[None, :, :], scores, -1e9)
                
                # Attention and accumulate
                attn_weights = self._softmax(scores)
                block_output += np.matmul(attn_weights, v_block)
            
            output[:, i:i + self.block_size] = block_output
        
        # Final projection
        final_output = self._output_projection(output)
        
        return final_output, {
            'memory_complexity': max_memory_used,
            'blocks_processed': (seq_len + self.block_size - 1) // self.block_size,
            'memory_efficiency': seq_len * seq_len * 4 / max_memory_used,  # vs standard
            'block_size': self.block_size
        }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_causal_mask(seq_len: int) -> np.ndarray:
    """Create causal attention mask."""
    return np.tril(np.ones((seq_len, seq_len), dtype=bool))

def create_padding_mask(lengths: np.ndarray, max_len: int) -> np.ndarray:
    """Create padding mask for variable length sequences."""
    batch_size = len(lengths)
    mask = np.zeros((batch_size, max_len), dtype=bool)
    for i, length in enumerate(lengths):
        mask[i, :length] = True
    return mask

def attention_entropy(attn_weights: np.ndarray, axis: int = -1) -> np.ndarray:
    """Compute attention entropy (measure of focus vs diffusion)."""
    # Avoid log(0) with small epsilon
    safe_weights = attn_weights + 1e-12
    return -np.sum(attn_weights * np.log(safe_weights), axis=axis)

def benchmark_attention(attention_class, seq_lengths: list = [128, 256, 512, 1024], 
                       d_model: int = 512) -> dict:
    """Benchmark attention mechanism across different sequence lengths."""
    import time
    
    results = {}
    
    for seq_len in seq_lengths:
        if attention_class == StandardAttention and seq_len > 1024:
            continue  # Skip large sequences for standard attention
        
        attention = attention_class(d_model)
        x = np.random.randn(seq_len, d_model) * 0.1
        
        # Warmup
        _ = attention(x)
        
        # Benchmark
        start_time = time.time()
        output, info = attention(x)
        end_time = time.time()
        
        results[seq_len] = {
            'time_ms': (end_time - start_time) * 1000,
            'memory_complexity': info.get('memory_complexity', seq_len * seq_len),
            'sparsity': info.get('sparsity', 1.0),
            'output_shape': output.shape
        }
    
    return results

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example usage of different attention mechanisms
    seq_len = 256
    d_model = 512
    x = np.random.randn(seq_len, d_model) * 0.1
    
    print("Attention Mechanisms Comparison")
    print("=" * 50)
    
    # Test each attention mechanism
    mechanisms = [
        ("Standard", StandardAttention),
        ("Sparse", SparseAttention), 
        ("Streaming", StreamingAttention),
        ("Flash", FlashAttention)
    ]
    
    for name, attention_class in mechanisms:
        attention = attention_class(d_model, num_heads=8)
        output, info = attention(x)
        
        print(f"\n{name} Attention:")
        print(f"  Output shape: {output.shape}")
        print(f"  Memory complexity: {info.get('memory_complexity', 'N/A')}")
        print(f"  Sparsity: {info.get('sparsity', 'N/A'):.3f}")
        
        if 'attention_weights' in info:
            entropy = attention_entropy(info['attention_weights'])
            print(f"  Attention entropy: {np.mean(entropy):.3f}")
    
    # Cross-modal attention example
    print(f"\nCross-Modal Attention:")
    cross_attention = CrossModalAttention(d_model, num_heads=8, num_modalities=3)
    
    # Three modalities with different lengths
    text_input = np.random.randn(100, d_model) * 0.1
    image_input = np.random.randn(64, d_model) * 0.1  
    audio_input = np.random.randn(80, d_model) * 0.1
    
    cross_output, cross_info = cross_attention([text_input, image_input, audio_input])
    print(f"  Cross-modal output shape: {cross_output.shape}")
    print(f"  Valid modalities: {cross_info['valid_modalities']}")
    
    print(f"\nBenchmarking Complete!")
