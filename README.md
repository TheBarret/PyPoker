# PyPoker
This Poker hand solver was designed and improved by Claude Opus.

The evaluator maps a set of 5 poker cards to a total order (so you can compare any two 5‑card hands) using a small,  
deterministic, combinatorially structured function. Here’s a clean mathematical decomposition of what it’s doing.  
The architecture is lexicographic, bit‑packed total order over 5‑card poker hands derived from rank‑frequency patterns and suit/straight constraints.  

## Inputs and basic encoding

- **Input**: a list of 5 cards, each with:
  - rank `r ∈ {2,3,…,14}` (via `Rank`), and
  - suit `s ∈ {1,2,3,4}` (via `Suit`).
- Extract:
  - rank vector: `R = (r₁, r₂, r₃, r₄, r₅)`
  - suit set: `S = {s₁, s₂, s₃, s₄, s₅}`

- **Hand type** `t` is drawn from:
  - `HandType ∈ {HIGH_CARD, ONE_PAIR, …, ROYAL_FLUSH}` (enum values `0…9`).

The function returns:
- `t`: hand type (primary strength),
- `v`: a 64‑bit integer key for tie‑breaking.

---

## Frequency‑based pattern classification

Define the **rank‑frequency map**:

- For each rank `r`, set:
  - `f(r) = number of cards with rank r`.

- Sort the pairs `(r, f(r))` by `(f(r), r)` in descending lexicographic order:
  - `(f₁, r₁), (f₂, r₂), …`
  - where `f₁ ≥ f₂ ≥ …` and ties broken by `r₁ ≥ r₂ ≥ …`.

- The sorted structure yields:
  - **Pattern (count vector)**: `Π = (f₁, f₂, …)`
  - **Rank groups**: `R_G = (r₁, r₂, …)`

These patterns map to poker types:

| Pattern `Π`        | HandType              |
|--------------------|-----------------------|
| `(4, 1)`           | FOUR_OF_KIND         |
| `(3, 2)`           | FULL_HOUSE           |
| `(3, 1, 1)`        | THREE_OF_KIND        |
| `(2, 2, 1)`        | TWO_PAIR             |
| `(2, 1, 1, 1)`     | ONE_PAIR             |
| `(1,1,1,1,1)` + flush | FLUSH              |
| `(1,1,1,1,1)` + straight | STRAIGHT        |
| `(1,1,1,1,1)` + both | STRAIGHT_FLUSH / ROYAL_FLUSH |

Separate straight/flush checks:

- **Flush**: `len(S) == 1` (all suits equal).
- **Straight**: ranks are distinct (`len(Π) == 5`) and:
  - either `max(R) - min(R) == 4`, or
  - `R = {14, 5, 4, 3, 2}` (the wheel, 5‑high straight).

---

## Hand‑type hierarchy and value space

The result is a pair `(t, v)` where:

- `t ∈ {0, …, 9}` is the hand type,
- `v ∈ ℕ` is a **packed 64‑bit integer** used for comparison.

The class constants are:

- `β = 4` bits per rank (since `2⁴ = 16 > 14`),
- `γ = 5 × β = 20` bits for up to 5 kickers.

The packing is:

```python
v = t << γ        # hand type in high bits
for r in ranks:
    v = (v << β) | r
```

In math terms:

- `v = t × 2^γ + Σ r_k × 2^{β(m−k)}`  
  where `r₁, r₂, …, r_m` are the tie‑breaking ranks in descending importance.

This is a **lexicographic encoding**:
- First order by `t`.
- Then, within the same type, order by the rank tuple (trips, pairs, kickers, etc.).

So:
- `(t₁, v₁) > (t₂, v₂)` ⟺ hand 1 beats hand 2 in standard 5‑card poker.

---

## Concrete examples of `_pack`

### Straight flush vs royal flush

- Royal flush: `t = 9`, high card `= 14`
  - `v = 9 × 2²⁰ + 14`
- 5‑high straight flush: `t = 8`, high card `= 5`
  - `v = 8 × 2²⁰ + 5`

### Four of a kind `(r₄, r₁)`

- `v = 7 × 2²⁰ + 2⁴ × r₄ + r₁`

### Full house `(r₃, r₂)`

- `v = 6 × 2²⁰ + 2⁴ × r₃ + r₂`

### Two pair `(r₂⁽¹⁾, r₂⁽²⁾, r₁)`

- `v = 2 × 2²⁰ + 2⁸ × r₂⁽¹⁾ + 2⁴ × r₂⁽²⁾ + r₁`

### High card `(r₁ ≥ r₂ ≥ ⋯ ≥ r₅)`

- `v = 0 × 2²⁰ + 2¹⁶r₁ + 2¹²r₂ + 2⁸r₃ + 2⁴r₄ + r₅`


## The evaluator defines a function

`E: Hands^(5) → HandType × ℕ`

where:
- `Hands^(5)` is the space of 5‑card poker hands,
- `HandType` labels strength tier,
- `ℕ` is the set of packed 64‑bit keys.

The mapping:

1. **Extract structure**:
   - Compute frequencies `f(r)` → pattern `Π`.
   - Detect flush / straight conditions.

2. **Assign type**:
   - Use `Π` and flush/straight flags to pick `t ∈ HandType`.

3. **Order‑preserving encoding**:
   - Pack `t` and a **rank tuple** `(r₁, r₂, …)` into:
     - `v = t × 2^γ + Σ r_k × 2^{β(m−k)}`
   - Comparison:
     - `E(h₁) > E(h₂)` ⟺ `h₁` beats `h₂` in 5‑card poker.

