# $\varepsilon$-貪婪演算法 (Epsilon-Greedy)

## 算式（詳細步驟）

1. **初始化**
   \[
     Q_i(1) = 0,
     \quad N_i(1) = 0,
     \quad \forall\,i = 1,2,\dots,K.
   \]

2. **動作選擇（ε-Greedy）**
   在第 $t$ 步，選擇臂 $A_t$：
   \[
     A_t =
     \begin{cases}
       \displaystyle \arg\max_{i} Q_i(t), & \text{以機率 }1 - \varepsilon, \\
       \text{從 }\{1,2,\dots,K\}\text{ 隨機選擇一臂}, & \text{以機率 }\varepsilon.
     \end{cases}
   \]

3. **獎勵抽樣**
   拉動臂 $A_t$ 後獲得即時獎勵 $R_t$：
   \[
     R_t \sim P_{A_t},
     \quad \mathbb{E}[R_t] = \mu_{A_t}.
   \]

4. **增量式估計更新**
   更新被選臂 $A_t$：
   \[
     N_{A_t}(t+1) = N_{A_t}(t) + 1,
   \]
   \[
     Q_{A_t}(t+1) = Q_{A_t}(t) + \frac{1}{N_{A_t}(t+1)}\bigl(R_t - Q_{A_t}(t)\bigr).
   \]
   其他臂 $i \neq A_t$ 保持：
   \[
     Q_i(t+1) = Q_i(t),
     \quad N_i(t+1) = N_i(t).
   \]

5. **累積獎勵與遺憾（Regret）**

   - 累積獎勵：
     \[
       G_T = \sum_{t=1}^T R_t.
     \]

   - 最優期望值：
     \[
       \mu^* = \max_{i}\,\mu_i.
     \]

   - 遺憾：
     \[
       \mathrm{Regret}(T)
       = T\,\mu^* - \mathbb{E}[G_T].
     \]

## 解釋

- **參數 $\varepsilon$**：控制「探索 (Exploration)」與「利用 (Exploitation)」之間的權衡。
- **利用 (Exploitation)**：以機率 $1 - \varepsilon$ 選擇當前 $Q_i(t)$ 最大的臂，充分利用已知資訊。
- **探索 (Exploration)**：以機率 $\varepsilon$ 隨機選擇臂，探索其他臂以更新估計。
- 若 $\varepsilon$ 過大，會過度探索導致短期獎勵不足；若 $\varepsilon$ 過小，可能陷入次優解。

## 適合應用

- 線上廣告推薦：動態推薦廣告並偶爾測試新廣告，以最大化點擊率。
- A/B 測試：根據歷史轉換率主推方案，並以少量機率測試候選方案。
- 遊戲智能代理：在回合制遊戲中權衡已知最佳動作與嘗試新動作。
- 推薦系統：動態推薦內容，同時探索新項目以捕捉使用者新興偏好。

## 圖形分析

### 圖 1：最優臂選擇機率隨時間變化
![](Result/1.png)
在「Probability of Selecting Optimal Arm Over Time」圖中：
- $\varepsilon = 0.0$（純利用）無探索，一旦初步估計失誤，後續不會選到最優臂。
- $\varepsilon = 0.01$ 以低探索率逐步發現最優臂，選中機率緩慢上升至約 0.5。
- $\varepsilon = 0.1$ 以高探索率快速辨識最優臂，選中機率在前 200 步已達 0.7–0.8。

### 圖 2：每臂平均被選次數
![](Result/2.png)
在「Average Selection Count per Arm」圖中：
- $\varepsilon = 0.0$ 完全鎖定初始認定最優的臂，總拉桿次數為 $T$。
- $\varepsilon = 0.01$ 主要集中於真實最優臂，其餘臂只做少量探索。
- $\varepsilon = 0.1$ 虽以最優臂為主，但同時保留較多資源給其他臂的探索。

## ChatGPT 提示語

```
假設你是一位資深機器學習工程師，請根據以下設定分析 ε-貪婪演算法性能：
1. 臂數 K = 10，真實獎勵機率隨機生成。
2. ε 分別為 0.0、0.01、0.1。
3. 圖表：
   - Probability of Selecting Optimal Arm Over Time
   - Average Selection Count per Arm
請解釋：
- 演算法在不同 ε 下的行為機制與結果。
- 圖中呈現的關鍵現象及其原因。
- 若要提升演算法，建議採取哪些改進策略？
```

