# n/ Language Specification: The Ouroboros Code

> "In the n/ universe, there is no execution, only observation. Truth is the point of convergence."

**n/** (n-slash or n-lang) is a data-centric, lattice-based declarative programming language. This repository houses the single source of truth for the language—**The n/ Code of Law (The Spec)**.

[中文版 (Chinese Version)](README_zh.md)

---

## 🌌 The Trinity Isomorphism

`n/` erases the boundaries between Data, Type, and Logic. In the `n/` universe, all three are merely different observational aspects of the same geometric object: the **Combo**.

**Example: Type as Data, Merge as Validation**
```nlang
;; 1. Define a "Type" (Boundary)
@Adult: {{
    age: @int & >= 18
}}

;; 2. Get some "Data" (Existence)
~payload: { name: "Alice", age: 25 }

;; 3. Perform a "Merge" (Observation)
;; In n/, validation is not an action, but a convergence in lattice space.
user: ~payload & @Adult

;; If age doesn't match, 'user' collapses to _|_ (Bottom) with causal info.
```

---

## 📚 Specification Structure

The specification consists of core documents, order of evolution, and engineering realization.

### Core Specifications
| Volume | Focus | Core Documents (zh_TW) |
| :--- | :--- | :--- |
| **Vol I: The Axioms** | Math & Lexical | [Lattice](spec/zh_TW/SPEC_01_Foundation_and_Lattice.md), [Lexical](spec/zh_TW/SPEC_02_Lexical_Structure.md), [Combo](spec/zh_TW/SPEC_03_Combo_System.md) |
| **Vol II: The Dynamics** | Navigation & Logic | [Navigation](spec/zh_TW/SPEC_04_Navigation_and_Duality.md), [Trinity](spec/zh_TW/SPEC_05_The_Trinity_Isomorphism.md), [Unification](spec/zh_TW/SPEC_06_Unification_Logic.md), [Morphism](spec/zh_TW/SPEC_07_Logic_and_Pipe.md) |
| **Vol III: The Order** | Governance & Evolution | [Interim Constitution](spec/zh_TW/ORDER_00_Interim_Constitution.md), [Evolution (Draft)](spec/zh_TW/ORDER_01_Evolution_and_Governance.md) |
| **Vol IV: The System** | Runtime & Commit | [Runtime](spec/zh_TW/SPEC_08_Meta_and_Runtime.md), [StdLib](spec/zh_TW/SPEC_09_Standard_Library.md), [Commit](spec/zh_TW/SPEC_10_Evolution_and_Commit.md), [Reflection](spec/zh_TW/SPEC_11_Reflection_and_Synthesis.md) |
| **Vol V: The Architecture** | Logic & Network | [Recursion](spec/zh_TW/SPEC_12_Logic_Validation_and_Recursion.md), [Discovery](spec/zh_TW/SPEC_13_Discovery_and_Package.md), [Grammar](spec/zh_TW/SPEC_14_Formal_Grammar.md), [Anti-Patterns](spec/zh_TW/SPEC_15_Anti_Patterns.md) |
| **Vol VI: The Echo** | Proof & Self-Evolution | [Testing](spec/zh_TW/SPEC_16_Testing_and_Proof.md), [Self-Evolution](spec/zh_TW/SPEC_17_Self_Evolution.md), [Echo](spec/zh_TW/SPEC_18_The_Echo.md) |

### Realization & Practical Guides
- **Implementation**: [Engineering (REAL_01)](spec/zh_TW/REAL_01_Ouroboros_Engineering.md), [Protocols (REAL_02)](spec/zh_TW/REAL_02_Ouroboros_Protocols.md), [CAID (REAL_03)](spec/zh_TW/REAL_03_CAID_Protocol.md).
- **Diagnostics**: [ERROR_CODES](spec/zh_TW/ERROR_CODES.md), [Causal Chain (REAL_04)](spec/zh_TW/REAL_04_Causal_Chain_Protocol.md), [Compliance (REAL_05)](spec/zh_TW/REAL_05_Compliance_and_MVP.md).
- **Practical**: [Formatting (GUIDE_01)](spec/zh_TW/GUIDE_01_Style_and_Formatting.md), [Optimization (GUIDE_02)](spec/zh_TW/GUIDE_02_Engine_Optimization.md).
- **Research**: [Tropical Geometry (APP_01)](spec/zh_TW/APP_01_Tropical_Geometry.md), [Formal Verification (APP_02)](spec/zh_TW/APP_02_Formal_Verification.md), [Paradigms (APP_03)](spec/zh_TW/APP_03_Paradigm_Comparison.md).

> **Note**: Currently, **Traditional Chinese (`zh_TW`)** is the primary reference. English and Japanese translations are in progress.

---

## 🔍 Navigation

To understand `n/`, we recommend following this sequence:

1.  **[PREFACE](spec/zh_TW/PREFACE.md)**: The origin and philosophy.
2.  **[GLOSSARY](spec/zh_TW/GLOSSARY.md)**: Unified terminology.
3.  **[QUICK_REFERENCE](spec/zh_TW/QUICK_REFERENCE.md)**: Syntax at a glance.
4.  **[SPEC_00 Introduction](spec/zh_TW/SPEC_00_Introduction.md)**: Global architecture overview and versioning.
5.  **[SPEC_STATUS](spec/zh_TW/SPEC_STATUS.md)**: Current development progress.

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
