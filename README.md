# n/ Language Specification: The Ouroboros Code

> "In the n/ universe, there is no execution, only observation. Truth is the point of convergence."

**n/** (n-slash or n-lang) is an **observation-centric semantic operating system**, built on a declarative, lattice-geometric core. This repository houses the single source of truth for the language—**The n/ Code of Law (The Spec)**.

[中文版 (Chinese Version)](README_zh.md)

**Current version: v0.2.0** — the stability watershed. The spec is stable; changes are tracked in the [CHANGELOG](spec/CHANGELOG.md) under the [versioning policy](meta/VERSIONING.md).

---

## 🌌 The Trinity Isomorphism

`n/` eliminates the boundaries between Data, Type, and Logic. In the world of `n/`, all three are merely different faces of the same geometric object, the **Combo**, seen through different observational dimensions.

**Example: Type as Data, Merge as Verification**
```nlang
;; 1. Define a "Type" (Boundary)
@Adult: {
    age: @int & 18..
}

;; 2. Acquire "Data" (Existence)
~payload: { name: "Alice", age: 25 }

;; 3. Execute "Merge" (Observation)
;; In n/, verification is not an action, but a convergence in geometric space.
user: ~payload & @Adult

;; If age doesn't match, 'user' immediately collapses to _|_ (Bottom) with causal tags.
```

---

## 📚 Specification Structure

The code consists of 18 core specs, orders of evolution, realization standards, and the digital cosmology appendices.

### Core Specifications
| Volume | Theme | Summary |
| :--- | :--- | :--- |
| **Vol I: Axioms** | Foundations | [Lattice (01)](spec/zh_TW/SPEC_01_Foundation_and_Lattice.md), [Lexical (02)](spec/zh_TW/SPEC_02_Lexical_Structure.md), [Structure (03)](spec/zh_TW/SPEC_03_Combo_System.md) |
| **Vol II: Flow** | Navigation & Logic | [Navigation (04)](spec/zh_TW/SPEC_04_Navigation_and_Duality.md), [Trinity (05)](spec/zh_TW/SPEC_05_The_Trinity_Isomorphism.md), [Unification (06)](spec/zh_TW/SPEC_06_Unification_Logic.md), [Morphism (07)](spec/zh_TW/SPEC_07_Logic_and_Pipe.md) |
| **Vol III: Order** | Governance | [Interim Constitution](spec/zh_TW/ORDER_00_Interim_Constitution.md), [Governance](spec/zh_TW/ORDER_01_Evolution_and_Governance.md) |
| **Vol IV: System** | Runtime & Commit | [Runtime (08)](spec/zh_TW/SPEC_08_Meta_and_Runtime.md), [StdLib (09)](spec/zh_TW/SPEC_09_Standard_Library.md), [Commit (10)](spec/zh_TW/SPEC_10_Evolution_and_Commit.md), [Reflection (11)](spec/zh_TW/SPEC_11_Reflection_and_Synthesis.md) |
| **Vol V: Network** | Discovery & Validation | [Recursion (12)](spec/zh_TW/SPEC_12_Logic_Validation_and_Recursion.md), [Discovery Protocol (13)](spec/zh_TW/SPEC_13_Ouroboros_Discovery_Protocol.md), [Grammar (14)](spec/zh_TW/SPEC_14_Formal_Grammar.md), [Anti-Patterns (15)](spec/zh_TW/SPEC_15_Anti_Patterns.md) |
| **Vol VI: Echo** | Proof & Evolution | [Testing (16)](spec/zh_TW/SPEC_16_Testing_and_Proof.md), [Self-Evolution (17)](spec/zh_TW/SPEC_17_Self_Evolution.md), [The Echo (18)](spec/zh_TW/SPEC_18_The_Echo.md) |

### Syntax Series (Normative Orthography)
Per-construct syntax rulings, finalized as the authoritative surface grammar (backed by the formal grammar in SPEC_14).
*   **[Conventions & Index (SYNTAX_00)](spec/zh_TW/SYNTAX_00_Conventions.md)**: 13 chapters — lexical structure, literals & atoms, paths, containers, prefixes, comparison & subtyping, observation duality, metadata, morphism application & definition, enum/poset, pipe & ternary.

### Digital Cosmology (Appendix Series)
The physics-intuition layer for `n/`'s design (non-normative; the rigorous mathematics lives in the theory paper series).
*   **[Overview & Index](spec/zh_TW/COSMOLOGY/00_COSMOLOGY_Overview.md)**: 7 chapters — mass-energy equivalence ($E=\text{Tr}(P)c^2$), semantic gravity, the Kochen–Specker computational horizon (horizon depth $= H^3$), the holographic deficit, and observer self-representation ($n=4$).

### Standards & Guides
- **Realization**: [Engineering (REAL_01)](spec/zh_TW/REAL_01_Ouroboros_Engineering.md), [Protocols (REAL_02)](spec/zh_TW/REAL_02_Ouroboros_Protocols.md), [CAID (REAL_03)](spec/zh_TW/REAL_03_CAID_Protocol.md), [Causal Chain (REAL_04)](spec/zh_TW/REAL_04_Causal_Chain_Protocol.md).
- **Diagnostics**: [Tag Registry (TAG_REGISTRY)](spec/zh_TW/TAG_REGISTRY.md), [Compliance (REAL_05)](spec/zh_TW/REAL_05_Compliance_and_MVP.md).
- **Guides**: [Style (GUIDE_01)](spec/zh_TW/GUIDE_01_Style_and_Formatting.md), [Optimization (GUIDE_02)](spec/zh_TW/GUIDE_02_Engine_Optimization.md), [Incremental (GUIDE_03)](spec/zh_TW/GUIDE_03_Incremental_Convergence.md), [EML Execution (GUIDE_04)](spec/zh_TW/GUIDE_04_EML_Execution_Strategy.md).
- **Theory**: [Tropical (APP_01)](spec/zh_TW/APP_01_Tropical_Geometry.md), [Formal Proof (APP_02)](spec/zh_TW/APP_02_Formal_Verification.md), [Paradigms (APP_03)](spec/zh_TW/APP_03_Paradigm_Comparison.md), [Math (APP_04)](spec/zh_TW/APP_04_Mathematical_Foundations.md), [LADD (APP_05)](spec/zh_TW/APP_05_LADD_Global_Logic_Lattice.md), [Unified Field Theory (APP_06)](spec/zh_TW/APP_06_Unified_Field_Theory.md), [Obstruction Ladder Guide (APP_07)](spec/zh_TW/APP_07_The_Obstruction_Ladder.md).

> **Note**: Currently, **Traditional Chinese (`zh_TW`)** is the primary reference. English and Japanese translations are in progress.

---

## 🔍 Navigation

To understand `n/`, we recommend following this sequence:

1.  **[PREFACE](spec/zh_TW/PREFACE.md)**: The origin and philosophy.
2.  **[GLOSSARY](spec/zh_TW/GLOSSARY.md)**: Unified terminology.
3.  **[QUICK_REFERENCE](spec/zh_TW/QUICK_REFERENCE.md)**: Syntax at a glance.
4.  **[SPEC_00 Introduction](spec/zh_TW/SPEC_00_Introduction.md)**: Global architecture overview and versioning.
5.  **[COSMOLOGY](spec/zh_TW/COSMOLOGY/00_COSMOLOGY_Overview.md)**: Gain a deeper understanding of the isomorphism between lattice theory and physics.

---

## 🏛️ The 6-Layer Architecture

The evolution of `n/` is governed by a 6-layer structure, ensuring core stability and peripheral flexibility. See [SPEC_00](spec/zh_TW/SPEC_00_Introduction.md).

---

## 📄 License

This specification is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**. See [LICENSE](LICENSE) for details.

---

## 🤝 Community & Contact

- **GitHub Organization**: [co-nlang](https://github.com/co-nlang)
- **Official Website**: [co-nlang.org](http://co-nlang.org) (TBD)
- **Discussions**: [GitHub Discussions](https://github.com/co-nlang/nlang-spec/discussions)

*"Convergence is our goal; Coherence is our bond."*
