# Contributing to n/ Language Specification

> Guidelines for contributing to the n/ language specification.

---

## 📐 Types of Contributions / 貢獻類型

We welcome various types of contributions:

### 1. **Clarifications / 澄清**
- Fixing ambiguous wording
- Adding examples to unclear sections
- Correcting typos or grammatical errors

### 2. **Corrections / 修正**
- Fixing technical inaccuracies
- Correcting broken cross-references
- Updating outdated information

### 3. **Translations / 翻譯**
- Translating SPEC documents to new languages
- Improving existing translations
- Maintaining terminology consistency

### 4. **Extensions / 擴展**
- Proposing new features (via RFC process)
- Adding new sections to existing SPECs
- Creating supplementary guides

---

## 🏛️ Guiding Principles / 核心守護原則

Every contribution must strictly adhere to the following core tenets of `n/`:

### 1. Semantic Invariants Preservation
Any change to the specification must not violate the **5 Invariants** defined in `SPEC_00`:
- **Invariant 1: Convergence Determinism**
- **Invariant 2: Information Monotonicity**
- **Invariant 3: Observation Purity**
- **Invariant 4: Composite Closure**
- **Invariant 5: Semantic Immutability**

### 2. Bootstrapping Integrity (Layered Freezing)
- **Layer 0 & 1**: Core axioms and fundamental structures. These are subject to strict freezing periods.
- **N-1 Toolchain Principle**: Official CAIDs for SPEC_v(N) must be calculated using SPEC_v(N-1) tools.

### 3. Terminology Sovereignty
- All translations must strictly follow the `GLOSSARY.md` found in their respective language directories. Do not introduce new terms without an RFC.

---

## 📝 Contribution Process / 貢獻流程

In the `n/` ecosystem, we maintain a strict separation between **Discussion (Drafts)** and **Law (Finalized Spec)**. 

### Step 1: Where to Start?
- **Small Fixes**: Typos, broken links, or minor clarifications can be submitted directly as PRs to this repository (`nlang-spec`).
- **Substantial Changes**: Proposing new features, modifying SPEC logic, or introducing new REAL standards **MUST** start in the **[@co-nlang/rfcs](https://github.com/co-nlang/rfcs)** repository.

### Step 2: The RFC Lifecycle (The "Drill" Phase)
1.  **Submit RFC**: Create a Pull Request in the `rfcs` repository using the provided template.
2.  **Discussion**: The community and the **Council of Four** will review the proposal.
3.  **Simulation Drill**: Significant RFCs must undergo a **Simulation Drill** (see **[ORDER_00](./spec/zh_TW/ORDER_00_Interim_Constitution.md)**). You may be asked to provide an engine-compatible test case.
4.  **Approval**: Once 3/5 of the Council (including 2/2 Logic Guardians for SPEC changes) approve, the RFC is marked as `Accepted`.

### Step 3: Formal Implementation
Once an RFC is accepted:
1.  A formal PR will be created in `nlang-spec` to update the Code of Law.
2.  The PR must reference the original RFC and include the digital signatures of the approving Council members.
3.  Upon merge, the change is officially part of the current Epoch.

---

## ✍️ Style Guidelines / 風格指南

### Markdown Format

```markdown
## Section Title

- **Bold term**: Definition
- Code: `` `inline` ``
- Blocks: ```nlang ... ```

[Internal Link](./SPEC_01_Foundation_and_Lattice.md)
[External Link](https://example.com)
```

### Terminology

**Always use `GLOSSARY.md` for translations:**

| English | 繁體中文 | 日本語 |
| :--- | :--- | :--- |
| Convergence | 收斂 | 収束 |
| Morphism | 態射 | 射 |
| Functor | 函子 | 関手 |

**Do NOT invent new translations** — if a term is missing, add it to GLOSSARY.md first.

### Cross-References

**Correct:**
```markdown
See **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** for details.
```

**Incorrect:**
```markdown
See SPEC_01 for details.  ;; Missing link
See **[SPEC_01](SPEC_01_Foundation_and_Lattice.md)**  ;; Missing ./
```

### Code Examples

Use `nlang` for code blocks:

````markdown
```nlang
;; Example code
x: 100 @int
result: x |> /double
```
````

---

## 🌐 Translation Guidelines / 翻譯指南

### For New Languages

1. **Create Directory**:
   ```bash
   mkdir -p spec/fr_FR
   mkdir -p assets/fr_FR
   ```

2. **Copy Structure**:
   ```bash
   cp -r spec/zh_TW/*.md spec/fr_FR
   ```

3. **Translate Content**:
   - Keep filenames unchanged
   - Translate markdown content only
   - Preserve all links and formatting

4. **Update README**:
   - Add language to the table
   - Update status

### Translation Principles

1. **Accuracy over Literalness**: Convey meaning, not just words
2. **Consistency**: Use GLOSSARY.md terms
3. **Clarity**: Prefer clear, simple sentences
4. **Cultural Adaptation**: Adapt examples when helpful

---

## 🔍 Review Process / 審查流程

### Reviewer Checklist

- [ ] Terminology consistency (check GLOSSARY.md)
- [ ] Semantic Invariant check (Logical Guardians review)
- [ ] Physical Determinism check (REAL Engineers review)
- [ ] Digital Assistant (AI) Geometric Assertion check
- [ ] All links work
- [ ] Code examples are valid nlang

### Maintainer Responsibilities (The Council of Four)

During the Interim Phase (**ORDER_00**), the **Council of Four** (SPEC Guardians and REAL Engineers) is responsible for:
- Reviewing PRs within their respective domains.
- Verifying Digital Assistant assertions. Overriding an AI assertion requires an explicit justification in the commit metadata.
- Merging when consensus is reached (3/5 for general, 2/2 for core SPEC).
- Updating the `SPEC_STATUS.md` tracker.

---

## 📋 RFC Process / RFC 流程

For major changes or new features:

1. **Create RFC Issue**: Describe the proposal
2. **Community Discussion**: 2-week discussion period
3. **Revision**: Incorporate feedback
4. **Decision**: Maintainers approve/reject
5. **Implementation**: Update SPEC documents

### RFC Template

```markdown
## Summary
Brief description of the proposal

## Motivation
Why is this change needed?

## Proposed Change
Detailed description of the change

## Examples
Code examples showing the change

## Impact
- Backward compatibility: Yes/No
- Implementation effort: Low/Medium/High
- Migration path: How to migrate existing code

## Alternatives Considered
What other approaches were considered?
```

---

## 🏆 Recognition / 表彰

Contributors are recognized in:

1. **CONTRIBUTORS.md**: List of all contributors.
2. **Commit History**: Git commits preserve authorship.
3. **Special Acknowledgement**: 
   - This Preface and the core vision of this Code were co-authored, aligned, and refined by the **n/ Architects** and their **Digital Collaborative Partners (led by Gemini)**.
   - We recognize the collaborative value of human creativity and AI-driven logical derivation in defining next-generation semantic systems.
4. **Release Notes**: Major contributors mentioned.

---

## ❓ Questions / 問題

- **General Questions**: Use [GitHub Discussions](https://github.com/co-nlang/nlang-spec/discussions)
- **Bug Reports**: Use [GitHub Issues](https://github.com/co-nlang/nlang-spec/issues)
- **Translation Questions**: Check [GLOSSARY.md](./spec/zh_TW/GLOSSARY.md) first

---

## 📜 License / 授權

By contributing, you agree that your contributions will be licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

---

**Thank you for contributing to the n/ language specification!** 🎉
