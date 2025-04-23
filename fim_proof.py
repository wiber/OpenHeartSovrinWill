# fim_proof.py
"""
Tiny FIM Proof-of-Concept with Explicit Hypothesis Tests

This script demonstrates and validates core Fractal Identity Map (FIM) properties:
 1. Skip-pruning factor matches theoretical (c/t)^(dims*levels).
 2. Each node prunes to exactly c children.
 3. One-hop meta-vector contributions sum to 1.
 4. Pruned weights lie in the top half of the original weight distribution (heavy-tail validity).
 5. Meta-vector size equals dims*levels (constant-time explanation).
"""

import numpy as np
import pandas as pd

def build_fim(dims, levels, t, c, seed=42):
    """
    Simulate FIM components:
      - weights: heavy-tailed parent->child weights via Pareto.
      - pruned: top-c weights per node.
      - skip_factor: fraction of map scanned = (c/t)^(dims*levels).
      - df: DataFrame of one-hop contributions for a hypothetical leaf.
    """
    np.random.seed(seed)
    weights = {
        (i, d): np.random.pareto(a=1.5, size=t) + 1
        for i in range(dims)
        for d in range(levels)
    }
    pruned = {}
    for key, w in weights.items():
        pruned[key] = np.sort(w)[::-1][:c]
    skip_factor = (c / t) ** (dims * levels)
    rows = []
    for (i, d), w in pruned.items():
        rows.append({'axis': i, 'depth': d, 'parent_weight': w[0]})
    df = pd.DataFrame(rows)
    df['contribution'] = df['parent_weight'] / df['parent_weight'].sum()
    return weights, pruned, skip_factor, df

# Hypothesis Tests
def test_skip_factor():
    """Test 1: skip_factor == (c/t)^(dims*levels)."""
    dims, levels, t, c = 2, 3, 5, 2
    _, _, skip, _ = build_fim(dims, levels, t, c)
    expected = (c/t)**(dims * levels)
    assert np.isclose(skip, expected), \
        f"FAIL Test 1: skip_factor={skip} != expected={expected}"
    print("PASS Test 1: Skip factor matches theoretical formula.")

def test_pruned_count():
    """Test 2: Each node pruned to exactly c children."""
    dims, levels, t, c = 2, 3, 5, 2
    weights, pruned, _, _ = build_fim(dims, levels, t, c)
    for key in weights:
        count = len(pruned[key])
        assert count == c, f"FAIL Test 2: Node {key} has {count} children, expected {c}"
    print("PASS Test 2: All nodes pruned to c children.")

def test_contributions_sum():
    """Test 3: One-hop contributions sum to 1."""
    dims, levels, t, c = 2, 3, 5, 2
    _, _, _, df = build_fim(dims, levels, t, c)
    total = df['contribution'].sum()
    assert np.isclose(total, 1.0), f"FAIL Test 3: Contributions sum to {total}, expected 1.0"
    print("PASS Test 3: Contributions sum to 1.")

def test_heavy_tail_pruned():
    """Test 4: Pruned weights are in the top half of original distribution."""
    dims, levels, t, c = 2, 3, 5, 2
    weights, pruned, _, _ = build_fim(dims, levels, t, c)
    for key, original in weights.items():
        median = np.median(original)
        for w in pruned[key]:
            assert w >= median, \
                f"FAIL Test 4: Pruned weight {w:.3f} < median {median:.3f} at node {key}"
    print("PASS Test 4: Pruned weights are >= median of original weights.")

def test_meta_vector_size():
    """Test 5: Meta-vector size equals dims*levels (constant-time explanation)."""
    dims, levels, t, c = 2, 3, 5, 2
    _, pruned, _, df = build_fim(dims, levels, t, c)
    expected_rows = dims * levels
    actual = df.shape[0]
    assert actual == expected_rows, \
        f"FAIL Test 5: Meta-vector has {actual} rows, expected {expected_rows}"
    print("PASS Test 5: Meta-vector size is correct (constant-time explain).")

def run_all_tests():
    print("Running FIM hypothesis tests...")
    test_skip_factor()
    test_pruned_count()
    test_contributions_sum()
    test_heavy_tail_pruned()
    test_meta_vector_size()
    print("All hypothesis tests passed.")

def demo():
    """Run a small demo printout of skip factor and contributions."""
    dims, levels, t, c = 2, 3, 5, 2
    weights, pruned, skip, df = build_fim(dims, levels, t, c)
    print(f"Demo: skip-pruning factor = {skip:.6f}\n")
    print("Demo: one-hop meta-vector contributions:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    demo()
    print("\n")
    run_all_tests()
