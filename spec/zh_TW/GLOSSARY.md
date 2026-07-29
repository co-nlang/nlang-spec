# n/ Language Specification - Glossary (術語表)

This document defines the standard translation of key terms in the n/ language specification.
All SPEC documents should use these translations consistently.

---

## 1. Core Concepts (核心概念)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Convergence** | **收斂** | **収束 (しゅうそく)** | `n/` 的核心運算模型。 |
| **Collapse** | **坍縮** | **収縮 (しゅうしゅく)** | 觀測後的狀態確定。 |
| **Merge** | **合併** | **合併 (がっぺい)** | 正交合併運算 `&` (Meet)。 |
| **Union** | **聯集** | **和集合 (わしゅうごう)** | 子空間併元疊加態 `\|` (Join)。 |
| **Complement** | **補集 (正交補)** | **補集合 (ほしゅうごう)** | 正交補空間 `!A` (Orthocomplement)。 |
| **Difference** | **差集** | **差集合 (さしゅうごう)** | 正交差集運算 `A \ B`。 |
| **Unification** | **統一化** | **統一化 (とういつか)** | 實現收斂的底層演算法。 |
| **Observation** | **觀測** | **観測 (かんそく)** | 對子空間進行投影獲取結果。 |

---

## 2. Structure (結構)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Orthomodular Lattice** | **正交模格** | **直交モジュラー束 (ちょっこうモジュラーたば)** | 量子邏輯的數學基礎，取代經典分配格。 |
| **Kochen-Specker Theorem** | **KS 定理** | **コッヘン・スペッカー定理** | 證明量子系統不存在隱藏變數的定理，定義觀測的物理邊界。 |
| **Projection Operator** | **投影算子** | **射影演算子 (しゃえいえんざんし)** | Hilbert 空間中將向量投射至子空間的線性算子 ($P_A$)。 |
| **Bohrification** | **Bohrification** | **ボーア化 (ボーアか)** | 從非交換本體到交換視角的投影過程。 |
| **Solèr Theorem** | **Solèr 定理** | **ソレール定理 (ソレールていり)** | 證明正交模格與 Hilbert 空間同構的關鍵定理。 |
| **Combo** | **Combo** | **コンボ** | 核心開放子空間結構 `{}`。 |
| **Cocoon** | **Cocoon (繭)** | **コクーン (繭/まゆ)** | 閉合的量子退相干屏蔽結構 `{{}}`。 |
| **List** | **List** | **リスト** | 張量排序容器 `[...]`。 |
| **Tuple** | **Tuple** | **タプル** | 元組容器 `(...)`。 |
| **Atom** | **原子** | **原子 (げんし)** | Hilbert 空間中的一維射線（不可再分值）。 |
| **Tag** | **標籤** | **タグ** | 一維基底標識 `#label`。 |
| **Path** | **路徑** | **パス** | 交換子代數導航表達式。 |
| **Scope** | **作用域** | **スコープ** | 名稱的可見性範圍。在此指 **Lexical Scope**。 |
| **Horizon** | **視界** | **事象の地平線 (じしょうのちへいせん)** | 由 KS 定理定義的觀測物理邊界。 |
| **Causal Boundary** | **因果邊界** | **因果境界 (いんがきょうかい)** | Commit 序列定義的固化事實與可能性邊界。 |

---

## 3. Ouroboros System (體系)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Ouroboros Model** | **銜尾蛇模型** | **ウロボロスモデル** | `n/` 的核心理論體系。 |
| **Ouroboros Engine** | **銜尾蛇引擎** | **ウロボロスエンジン** | 執行子空間投影與收斂的計算核心。 |
| **Ouroboros Protocol** | **銜尾蛇協定** | **ウロボロスプロトコル** | 節點間發現、交換 CAID 與特權管理的工作協議（OODP）。 |
| **CAID** | **CAID** | **CAID** | 內容定址標識符，由譜摘要與內容雜湊組成。身分極——把「一切觀測」固化成內容位址（Yoneda 對偶見 Call-by-Observation）。 |
| **Call-by-Observation** | **按需觀測** | **オンデマンド観測 (かんそく)** | 求值模型：沿路徑逐段坍縮，只 force 路徑上的節點（SPEC_04 §6）。觀測極——CAID 的 Yoneda 對偶（單次 `hom(A,X)` 惰性截面）；惰性是語義要求而非最佳化。 |
| **Spectral Signature** | **譜幾何指紋** | **スペクトル幾何指紋 (すぺくときかしし)** | 子空間投影算子的譜特徵（CAID 的波動維度）。 |
| **Lattice Sketch** | **幾何摘要** | **格子概要 (こうしがいよう)** | 譜指紋的 Base64 序列化表示，用於氣味搜尋。 |
| **Spec Promoter** | **規格啟動子** | **スペックプロモータ** | 引導舊版引擎升壓至新語義環境的邏輯欄位 `%promoter`。 |

---

## 4. Type System (型別系統)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Type** | **型別** | **型 (かた)** | 子空間邊界與約束 `@type`。 |
| **Data** | **數據** | **データ** | 特徵向量與存有。 |
| **Logic** | **邏輯** | **論理 (ろんり)** | 算子與變換 `/logic`。 |
| **Meta** | **元資訊** | **メタ情報** | 系統自省資訊 `%meta`。 |
| **System** | **系統** | **システム** | 系統內建工具 `~%System`。 |
| **Local** | **私有** | **ローカル** | 視角內局部私有座標，前綴 `~`（可疊於三位一體：`~a`／`~@a`／`~/a`）。 |
| **Functor** | **函子** | **関手 (かんしゅ)** | 子空間保全的態射介面 `%fmap`。 |
| **Monad** | **單子** | **モナド** | 投影鏈式組合介面 `%bind`。 |
| **Monoid** | **幺半群** | **モノイド** | 可合併結構介面 `%concat`。 |

---

## 5. Logic & Computation (邏輯與計算)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Morphism** | **態射 / 算子** | **射 (しゃ) / 演算子** | Hilbert 空間上的線性算子。 |
| **Pipe** | **管道** | **パイプ** | 么正變換路徑 `\|>`。 |
| **Lifting** | **升寫** | **リフティング** | 算子向張量容器內部的提升應用。 |
| **Application** | **應用** | **適用 (てきよう)** | 算子對子空間的作用行為。 |
| **Currying** | **柯里化** | **カリー化** | 算子參數的偏應用自動化。 |
| **Pattern Matching** | **模式匹配** | **パターンマッチング** | 投影特徵的譜比對與選擇。 |
| **Recursion** | **遞迴** | **再帰 (さいき)** | 子空間結構的自我引用。 |
| **Divergent** | **發散** | **発散 (はっさん)** | 譜熵不遞減、無法坍縮的投影路徑。 |

---

## 6. System & Tooling (工具鏈)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Commit** | **Commit** | **コミット** | 宇宙狀態的離散固化快照。 |
| **Staged** | **暫存** | **ステージング** | 尚未固化的投影定義。 |
| **HEAD** | **HEAD** | **HEAD** | 當前活躍的因果錨點。 |
| **Format** | **格式化** | **フォーマット** | `oo fmt` 正規化工具。 |
| **Canonical** | **規範化** | **標準化 (ひょうじゅんか)** | 產生決定論位元流的唯一標準形式。 |

---

## 7. Observation States (觀測狀態)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Lazy** | **未觀測** | **遅延 (ちえん)** | 尚未被投影路徑抵達的子空間。 |
| **#incomplete** | **不完全** | **不完全 (ふかんぜん)** | 暫態。因觸及視界而中斷的觀測。 |
| **#blur** | **模糊** | **ぼかし** | 局部截面截斷。具備決定論 CAID 的視界凍結態。 |
| **#exact** | **精確** | **精確 (せいかく)** | 投影至穩定特徵向量的終態。 |
| **Conflict** | **衝突** | **衝突 (しょうとつ)** | 坍縮為零維空間 (`_\|_`) 的正交矛盾。 |

---

## 8. Mathematics & Physics (數學與物理)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Trace** | **跡 (Trace)** | **トレース** | 投影算子的跡，定義幾何質量 ($m$)。 |
| **Unitary Transformation** | **么正變換** | **ユニタリ変換 (ゆにたりへんかん)** | 保持內積不變的線性變換，對應 `#pure` 態射的物理實現。 |
| **Chordal Distance** | **量子弦距離** | **量子弦距離 (りょうしげんきょり)** | 定義格論距離 ($d_L$) 的幾何測度。 |
| **Decoherence** | **退相干** | **デコヒーレンス** | 資訊從量子態蒸發至經典極限的過程。 |
| **Spectral Feature** | **譜特徵** | **スペクトル特徴** | 子空間投影算子的特徵值與特徵向量，構成其幾何指紋。 |
| **Geometric Mass** | **幾何質量** | **幾何質量 (きかしつりょう)** | 投影算子之跡 ($m = \text{Tr}(P)$)，代表子空間的資訊密度。 |
| **Interlacing** | **譜交錯** | **スペクトル交錯** | 利用 Cauchy 定理進行幾何包含判定。 |
| **Dequantization** | **去量子化** | **非量子化 (ひりょうしか)** | 透過熱帶幾何進行降維加速。 |
| **Tropical Geometry** | **熱帶幾何** | **トロピカル幾何** | Min-plus 代數框架，作為量子語義的退相干極限近似。 |
| **Maslov Dequantization** | **Maslov 去量子化** | **マスロフ非量子化** | 將複數域問題映射至熱帶半環的變換過程。 |
| **Supremum** | **上確界** | **上限 (じょうげん)** | 序位的最大元（`#_`）。 |
| **Infimum** | **下確界** | **下限 (かげん)** | 序位的最小元（`#_\|_`）。 |

---

## 9. Discovery & Proof (發現與證明)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **LADD** | **LADD 協議** | **LADD プロトコル** | 基於幾何引力的分散式發現協議。 |
| **持有聲明** | **持有聲明 (custody_hint)** | **保有申告 (ほゆうしんこく)** | 節點**聲明**其持有所宣告之子空間。**執行軌，無證明義務**；得選用附帶 ω/q 指紋知識證明（APP_02 §6）。謊報只使查詢者白跑一趟。〔2026-07-28 更名，原稱「GPP／身分證明」——該電路不提證明者，所證為持有而非身分。判別表見 REAL_01 §7.6〕 |
| **GPP** | **幾何機率證明**〔已退出協定層〕 | **幾何確率証明 (きかかくりつしょうめい)** | APP_02 §6 之 𝔽₂ 電路的歷史縮寫，現稱 **ω/q 指紋知識證明**。REAL_02／APP_05 不再以此指稱節點所出示之物（那是**持有聲明**）。 |
| **CIP** | **因果完整性證明** | **因果完全性証明 (いんがかんぜんせい)** | 證明收斂鏈 claim（CAID→CAID）被忠實執行的離散計算證明（APP_05 §6）。 |
| **Geodesics** | **測地線** | **測地線 (そくちせん)** | 語義空間中引力最強的路徑。 |

---

## 10. Philosophical Concepts (哲學專有名詞)

| English | Traditional Chinese | Japanese | Meaning |
| :--- | :--- | :--- | :--- |
| **Ontology** | **本體論** | **存在論 (そんざいろん)** | 研究「存在」本質的哲學分支。在 `n/` 中指 Data/Type/Logic 的三位一體。 |
| **Epistemology** | **認識論** | **認識論 (にんしきろん)** | 研究「知識」本質的哲學分支。在 `n/` 中指觀測與收斂的過程。 |
| **Phenomenology** | **現象學** | **現象学 (げんしょうがく)** | 研究「現象」如何顯現的哲學。在 `n/` 中指從 `#blur` 到 `#exact` 的顯影過程。 |
| **Teleology** | **目的論** | **目的論 (もくてきろん)** | 以目的為導向的解釋框架。在 `n/` 中指收斂指向最優解的傾向。 |
| **Determinism** | **決定論** | **決定論 (けっていろん)** | 相信事件由先前狀態決定的哲學觀。在 `n/` 中體現為收斂決定論（Invariant 1）。 |
| **Constructivism** | **建構主義** | **構成主義 (こうせいしゅぎ)** | 知識是建構而非發現的觀點。在 `n/` 中指宇宙透過 Commit 逐步建構。 |
| **Pragmatism** | **實用主義** | **実用主義 (じつようしゅぎ)** | 以實際效果為真理標準的哲學。在 `n/` 中指 `#blur` 的實用價值。 |
| **Holism** | **整體論** | **全体論 (ぜんたいろん)** | 相信整體大於部分之和的觀點。在 `n/` 中指 Combo 作為不可還原的整體。 |
| **Superposition** | **疊加** | **重ね合わせ (かさねあわせ)** | 量子系統同時處於多態的狀態。在 `n/` 中指 `A \| B` 的聯集語義。 |
| **Entanglement** | **糾纏** | **量子もつれ** | 量子系統間的非定域關聯。在 `n/` 中指 `%closure` 捕獲的作用域快照。 |
| **Decoherence** | **退相干** | **デコヒーレンス** | 量子疊加態因環境交互而消失。在 `n/` 中指從 `#blur` 到 `#exact` 或 `#incomplete` 的轉變。 |
| **Eigenstate** | **本徵態** | **固有状態 (こゆうじょうたい)** | 觀測後確定的量子狀態。在 `n/` 中指 `#exact` 狀態。 |

---

## 11. Translation Principles (翻譯原則)

1. **保留英文**：對於已廣泛使用的技術術語（如 Combo, CAID, Commit），保留英文不翻譯。
2. **數學術語**：遵循台灣數學界標準翻譯（如 幺半群 Monoid、格論 Lattice）。
3. **哲學概念**：使用哲學領域標準譯名（如 本體論 Ontology、認識論 Epistemology）。
4. **一致性**：同一英文術語在整個規格書中應使用相同的中文翻譯。
5. **雙語並列**：首次出現時，使用「中文 (English)」格式，後續可直接使用中文。

---

## 12. Revision History

| Date | Change | Author |
| :--- | :--- | :--- |
| 2026-03-25 | Initial glossary creation | Gali |
| | - Added translation principles | |
| 2026-04-19 | Quantum Sublimation & Restoration | Ouroboros Architect |
| 2026-04-19 | Added Japanese translations to all tables | Ouroboros Architect |
| 2026-04-19 | Restored §10 Philosophical Concepts | Ouroboros Architect |
| 2026-04-20 | Added KS Theorem, Projection Operator, Unitary Transformation | Ouroboros Architect |
| 2026-04-20 | Added Spectral Feature, Geometric Mass, Tropical Geometry | Ouroboros Architect |
