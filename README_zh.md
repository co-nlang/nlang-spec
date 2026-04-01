# n/ 語言規格書：銜尾蛇法典 (The Ouroboros Code)

> 「在 n/ 的宇宙中，沒有執行，只有觀測。真理即是收斂之點。」

**n/** (n-slash 或 n-lang) 是一個以數據為中心、基於幾何格論（Lattice-based）的宣告式程式語言。本 Repo 存放 `n/` 語言的唯一真理來源——**n/ 法典**。

---

## 🌌 三位一體同構 (The Trinity Isomorphism)

`n/` 消除數據 (Data)、型別 (Type) 與態射 (Logic) 的界線。在 `n/` 的世界中，三者皆為同一個幾何物件 **Combo** 在不同觀測維度下的面相。

**範例：型別即數據，合併即驗證**
```nlang
;; 1. 定義一個「型別」(邊界)
@Adult: {{
    age: @int & >= 18
}}

;; 2. 獲取一份「數據」(存有)
~payload: { name: "Alice", age: 25 }

;; 3. 執行「合併」(觀測)
;; 在 n/ 中，驗證不是一個動作，而是幾何空間的交集收斂
user: ~payload & @Adult

;; 若 age 不符，user 將立即坍縮為 _|_ (Bottom) 並記錄因果
```

---

## 📚 規格書架構 (Specification Structure)

本法典由 18 份核心規格、演化秩序與具現標準組成。

### 核心規格 (The Core Specs)
| 卷別 | 主題 | 內容摘要 |
| :--- | :--- | :--- |
| **卷一：公設** | 數學基礎與詞法 | [格論 (SPEC_01)](spec/zh_TW/SPEC_01_Foundation_and_Lattice.md), [詞法 (SPEC_02)](spec/zh_TW/SPEC_02_Lexical_Structure.md), [結構 (SPEC_03)](spec/zh_TW/SPEC_03_Combo_System.md) |
| **卷二：流轉** | 導航與邏輯 | [導航 (SPEC_04)](spec/zh_TW/SPEC_04_Navigation_and_Duality.md), [三位一體 (SPEC_05)](spec/zh_TW/SPEC_05_The_Trinity_Isomorphism.md), [統一化 (SPEC_06)](spec/zh_TW/SPEC_06_Unification_Logic.md), [態射 (SPEC_07)](spec/zh_TW/SPEC_07_Logic_and_Pipe.md) |
| **卷三：秩序** | 治理與演化 | [臨時憲法 (ORDER_00)](spec/zh_TW/ORDER_00_Interim_Constitution.md), [正式治理 (ORDER_01)](spec/zh_TW/ORDER_01_Evolution_and_Governance.md) |
| **卷四：系統** | 運行時與提交 | [運行時 (SPEC_08)](spec/zh_TW/SPEC_08_Meta_and_Runtime.md), [標準庫 (SPEC_09)](spec/zh_TW/SPEC_09_Standard_Library.md), [提交 (SPEC_10)](spec/zh_TW/SPEC_10_Evolution_and_Commit.md), [反映 (SPEC_11)](spec/zh_TW/SPEC_11_Reflection_and_Synthesis.md) |
| **卷五：體系** | 驗證與網路 | [遞迴 (SPEC_12)](spec/zh_TW/SPEC_12_Logic_Validation_and_Recursion.md), [發現 (SPEC_13)](spec/zh_TW/SPEC_13_Discovery_and_Package.md), [語法 (SPEC_14)](spec/zh_TW/SPEC_14_Formal_Grammar.md), [反模式 (SPEC_15)](spec/zh_TW/SPEC_15_Anti_Patterns.md) |
| **卷六：餘韻** | 證明與演化 | [測試 (SPEC_16)](spec/zh_TW/SPEC_16_Testing_and_Proof.md), [自我演化 (SPEC_17)](spec/zh_TW/SPEC_17_Self_Evolution.md), [餘韻 (SPEC_18)](spec/zh_TW/SPEC_18_The_Echo.md) |

### 具現標準與實務指南
- **具現標準**：[工程實作 (REAL_01)](spec/zh_TW/REAL_01_Ouroboros_Engineering.md)、[通訊協議 (REAL_02)](spec/zh_TW/REAL_02_Ouroboros_Protocols.md)、[CAID 物理協議 (REAL_03)](spec/zh_TW/REAL_03_CAID_Protocol.md)。
- **診斷工具**：[錯誤代碼 (ERROR_CODES)](spec/zh_TW/ERROR_CODES.md)、[因果結構 (REAL_04)](spec/zh_TW/REAL_04_Causal_Chain_Protocol.md)、[合規性測試 (REAL_05)](spec/zh_TW/REAL_05_Compliance_and_MVP.md)。
- **實務指南**：[風格指南 (GUIDE_01)](spec/zh_TW/GUIDE_01_Style_and_Formatting.md)、[引擎優化 (GUIDE_02)](spec/zh_TW/GUIDE_02_Engine_Optimization.md)。
- **理論擴展**：[熱帶幾何 (APP_01)](spec/zh_TW/APP_01_Tropical_Geometry.md)、[形式證明 (APP_02)](spec/zh_TW/APP_02_Formal_Verification.md)、[範式比較 (APP_03)](spec/zh_TW/APP_03_Paradigm_Comparison.md)。

---

## 🔍 導讀與導航

若要深入了解 `n/`，建議按照以下順序閱讀：

1.  **[PREFACE (序言)](spec/zh_TW/PREFACE.md)**：了解語言誕生的起源與哲學。
2.  **[GLOSSARY (術語表)](spec/zh_TW/GLOSSARY.md)**：統一名詞定義。
3.  **[QUICK_REFERENCE (快速參考)](spec/zh_TW/QUICK_REFERENCE.md)**：語法速查。
4.  **[SPEC_00 (緒論)](spec/zh_TW/SPEC_00_Introduction.md)**：全域架構導覽。
5.  **[SPEC_STATUS (法典狀態)](spec/zh_TW/SPEC_STATUS.md)**：開發進度追蹤。

---

## 🏛️ 六層法典架構 (The 6-Layer Architecture)

`n/` 的演化受六層架構約束，詳見 [SPEC_00](spec/zh_TW/SPEC_00_Introduction.md)。

---

## 📄 授權 (License)

本規格書採用 **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** 授權。詳見 [LICENSE](LICENSE)。

---

## 🤝 聯絡與貢獻

- **GitHub 組織**: [co-nlang](https://github.com/co-nlang)
- **貢獻指南**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **討論區**: [GitHub Discussions](https://github.com/co-nlang/nlang-spec/discussions)

*"收斂是我們的目標，連貫是我們的紐帶。"*
