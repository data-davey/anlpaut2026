# Vector Similarity: A Reference Guide
*Cosine Similarity, Dot Product, and Unit Normalisation*

---

## 1. Cosine Similarity

Cosine similarity measures the angle between two vectors, returning a value between -1 and 1:

$$\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \times \|\mathbf{B}\|}$$

Expanded:

$$\cos(\theta) = \frac{\sum A_i \times B_i}{\sqrt{\sum A_i^2} \times \sqrt{\sum B_i^2}}$$

| Part | Meaning |
|------|---------|
| Numerator (A · B) | Dot product — multiply corresponding elements and sum them |
| Denominator (‖A‖ × ‖B‖) | Product of each vector's L2 norm (Euclidean length) |

### Range

| Score | Meaning |
|-------|---------|
| 1 | Identical direction — same semantic meaning |
| 0 | Orthogonal — no similarity |
| -1 | Opposite direction |

> **Why cosine similarity works well for text:** it ignores vector magnitude and only measures the angle between vectors. A short and a long document covering the same topic will have similar directions in embedding space, even if their magnitudes differ.

---

## 2. Dot Product Similarity

Dot product similarity is the numerator of cosine similarity, without normalisation:

$$\text{sim}(\mathbf{A}, \mathbf{B}) = \mathbf{A} \cdot \mathbf{B} = \sum A_i \times B_i$$

The relationship between the two:

$$\text{dot product} = \cos(\theta) \times \|\mathbf{A}\| \times \|\mathbf{B}\|$$

Dot product captures both **direction** (angle) and **magnitude**, whereas cosine similarity captures direction only.

| | Cosine Similarity | Dot Product |
|---|---|---|
| Normalised vectors | Same result | Same result |
| Unnormalised vectors | Ignores magnitude | Affected by magnitude |
| Best use case | Most text embeddings | When magnitude carries meaning |

> **Practical note:** Most modern embedding models output unit-normalised vectors, so dot product == cosine similarity. Vector databases like Pinecone default to dot product as it requires one less computation.

---

## 3. Vector Notation: What ‖A‖ Means

The double bar notation `‖A‖` means the **magnitude** (length) of vector A, also called the **norm**:

$$\|\mathbf{A}\| = \sqrt{A_1^2 + A_2^2 + A_3^2 + \ldots + A_n^2}$$

This is simply Pythagoras extended to n dimensions — the length of the hypotenuse given all sides. For example:

$$\mathbf{A} = [3, 4] \quad \Rightarrow \quad \|\mathbf{A}\| = \sqrt{3^2 + 4^2} = \sqrt{25} = 5$$

So when you see `‖A‖ = 1`, it means the vector has length exactly 1 — which is the definition of unit normalised.

---

## 4. Unit Normalisation (L2 Normalisation)

### In Plain Terms

Think of every embedding vector as an arrow pointing in some direction in space.

Without normalisation, arrows can be different lengths. A long document might produce a long arrow; a short sentence a short one.

**Unit normalised** means you take every arrow — no matter how long or short it was originally — and shrink or stretch it so it is exactly length 1. The direction stays exactly the same. You haven't changed what it means or what it's pointing at. You've just made all arrows the same length.

> **Real world analogy:** think of compass directions. It doesn't matter if you drew the arrow 1cm or 10cm on paper — north is still north. Unit normalising is like saying "all arrows are exactly 1cm; we only care about the direction they point."

### The Formula

To normalise any vector, divide each element by its magnitude:

$$\hat{\mathbf{A}} = \frac{\mathbf{A}}{\|\mathbf{A}\|}$$

Example: `A = [3, 4]`

```
‖A‖ = 5  →  Â = [3/5, 4/5] = [0.6, 0.8]

Verify: √(0.6² + 0.8²) = √(0.36 + 0.64) = √1.0 = 1  ✓
```

In Python:

```python
import numpy as np

a = np.array([3.0, 4.0])
a_normalized = a / np.linalg.norm(a)  # [0.6, 0.8]

print(np.linalg.norm(a_normalized))   # 1.0
```

### L2 Normalisation vs Unit Normalisation

**These are the same thing.** L2 is simply the technical name.

The "L2" refers to the L2 norm, which is the Euclidean length formula used above. It is called L2 because it squares the elements (power of 2) before summing. There are other norms — L1 (sum of absolute values), L∞ (maximum value) — but L2 is by far the most common in machine learning and embeddings. When someone says "unit normalised" in an ML context, they almost always mean L2 normalised.

| Term | Meaning |
|------|---------|
| Unit normalised | Vector has length exactly 1 |
| L2 normalised | Same thing — normalised using the L2 (Euclidean) norm |
| L2 norm | The √ΣAᵢ² formula for vector length |

### Why Embedding Models Use It

By normalising outputs, the model strips out any information about vector length and forces all similarity comparisons to be purely about direction — which is what you want when comparing semantic meaning.

The side benefit is that the maths gets simpler and faster: dot product and cosine similarity become identical, which matters at scale when doing millions of similarity lookups.

---

## 5. OpenAI Embeddings

OpenAI's embedding models (`text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`) all output unit-normalised vectors, confirmed in their official documentation:

> *"OpenAI embeddings are normalized to length 1, which means that cosine similarity can be computed slightly faster using just a dot product, and cosine similarity and Euclidean distance will result in identical rankings."* — OpenAI Docs

| Model | Dimensions | Unit Normalised |
|-------|-----------|-----------------|
| text-embedding-3-small | 1536 (configurable) | Yes |
| text-embedding-3-large | 3072 (configurable) | Yes |
| text-embedding-ada-002 | 1536 | Yes |

> **Gotcha:** if you manually truncate dimensions, the resulting shorter vector is no longer unit-normalised and must be re-normalised manually. If you use the API's built-in `dimensions` parameter, re-normalisation is handled automatically.
