import math
import struct
from sympy import primerange
import matplotlib.pyplot as plt

def R(z, p):
    """Canonical resonance function as described in the paper."""
    return math.sin(math.pi / p) * math.cos(math.pi / (2 * p)) * math.sin(math.pi / p)

def Cn(z, n):
    """Compute the resonance cascade Cn(z) = product of R(z, pk) for k=1..n."""
    primes = list(primerange(2, 2 + 10000))  # Generate enough primes
    product = 1.0
    for i in range(n):
        product *= R(z, primes[i])
    return product

def float_to_bin64(x):
    """Convert a Python float to its IEEE-754 binary64 representation as a string of 64 bits."""
    [d] = struct.unpack(">Q", struct.pack(">d", x))
    return f"{d:064b}"

def common_bit_prefix(xs):
    """Return the length of the common bit prefix among a list of floats."""
    bins = [float_to_bin64(x) for x in xs]
    prefix_len = 0
    for bits in zip(*bins):
        if all(b == bits[0] for b in bits):
            prefix_len += 1
        else:
            break
    return prefix_len

def hamming_distance(x, y):
    """Return the Hamming distance between two floats' binary64 representations."""
    bx = float_to_bin64(x)
    by = float_to_bin64(y)
    return sum(b1 != b2 for b1, b2 in zip(bx, by))

def empirical_stability_law(epsilon):
    """Return the predicted number of stable bits for a given epsilon."""
    if epsilon == 0:
        return 64
    return 64 - int(math.floor(math.log2(1/epsilon)))

def demo_sequence_extension(z=0.5, n_start=3, n_end=30):
    """Demonstrate bitwise stability as n increases."""
    results = []
    ns = []
    vals = []
    for n in range(n_start, n_end + 1):
        val = Cn(z, n)
        results.append(val)
        ns.append(n)
        vals.append(val)
    prefix = common_bit_prefix(results)
    print(f"Common bit prefix for Cn(z) as n goes from {n_start} to {n_end}: {prefix} bits")
    for i, val in enumerate(results, n_start):
        print(f"n={i}, Cn(z)={val}, bits={float_to_bin64(val)}")
    # Visualization
    plt.figure(figsize=(8, 5))
    plt.plot(ns, vals, marker='o')
    plt.yscale('log')
    plt.xlabel('n')
    plt.ylabel('Cn(z)')
    plt.title('Cn(z) vs n (log scale)')
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.tight_layout()
    plt.show()

def demo_input_perturbation(z=0.5, n=15, delta=1e-6):
    """Demonstrate bitwise stability under small perturbations of z."""
    base = Cn(z, n)
    perturbed = Cn(z + delta, n)
    prefix = common_bit_prefix([base, perturbed])
    hamming = hamming_distance(base, perturbed)
    diff = abs(base - perturbed)
    print(f"Base: {base}, Perturbed: {perturbed}")
    print(f"Common bit prefix: {prefix} bits")
    print(f"Hamming distance: {hamming}")
    print(f"Difference: {diff}")
    print(f"Empirical law predicts ≥ {empirical_stability_law(diff)} stable bits")

if __name__ == "__main__":
    print("=== Bitwise Stability: Sequence Extension Demo ===")
    demo_sequence_extension()
    print("\n=== Bitwise Stability: Input Perturbation Demo ===")
    demo_input_perturbation()