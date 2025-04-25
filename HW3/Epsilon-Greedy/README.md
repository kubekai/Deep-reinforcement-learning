# ε-貪婪演算法 (Epsilon-Greedy)

## 算式

以下使用 CodeCogs 生成的公式圖片：

### 動作選擇（ε-Greedy）

\<img src="[https://latex.codecogs.com/png.latex?A\_t%3D%5Cbegin%7Bcases%7D%5Carg%5Cmax\_i%20%5Chat%7B%5Cmu%7D\_i(t)%2C%20%26%20%5Ctext%7Bprob.%7D%201-%5Cvarepsilon%20%5C%5C%20%5Ctext%7Brandom%20arm%7D%2C%20%26%20%5Ctext%7Bprob.%7D%20%5Cvarepsilon%20%5Cend%7Bcases%7D\\](https://latex.codecogs.com/png.latex?A_t%3D%5Cbegin%7Bcases%7D%5Carg%5Cmax_i%20%5Chat%7B%5Cmu%7D_i\(t\)%2C%20%26%20%5Ctext%7Bprob.%7D%201-%5Cvarepsilon%20%5C%5C%20%5Ctext%7Brandom%20arm%7D%2C%20%26%20%5Ctext%7Bprob.%7D%20%5Cvarepsilon%20%5Cend%7Bcases%7D\\)" title="A\_t = { argmax\_i \hat{\mu}\_i(t), prob. 1-ε; random arm, prob. ε }" />

### 平均獎勵估計

\<img src="[https://latex.codecogs.com/png.latex?%5Chat%7B%5Cmu%7D\_i(t)%3D%5Cfrac%7B1%7D%7BN\_i(t)%7D%5Csum\_%7Bs%3D1%7D%5E%7Bt-1%7D%20R\_s%5Cmathbf%7B1%7D%7B%5C%7BA\_s%3Di%5C%7D%7D\\](https://latex.codecogs.com/png.latex?%5Chat%7B%5Cmu%7D_i\(t\)%3D%5Cfrac%7B1%7D%7BN_i\(t\)%7D%5Csum_%7Bs%3D1%7D%5E%7Bt-1%7D%20R_s%5Cmathbf%7B1%7D%7B%5C%7BA_s%3Di%5C%7D%7D\\)" title="\hat{\mu}*i(t)=1/N\_i(t) ∑*{s=1}^{t-1} R\_s 1{A\_s=i}" />

### 增量更新

\<img src="[https://latex.codecogs.com/png.latex?N\_i(t%2B1)%3DN\_i(t)%2B1\\](https://latex.codecogs.com/png.latex?N_i\(t%2B1\)%3DN_i\(t\)%2B1\\)" title="N\_i(t+1)=N\_i(t)+1" />
\<img src="[https://latex.codecogs.com/png.latex?Q\_i(t%2B1)%3DQ\_i(t)%2B%5Cfrac%7B1%7D%7BN\_i(t%2B1)%7D(R\_t-Q\_i(t))\\](https://latex.codecogs.com/png.latex?Q_i\(t%2B1\)%3DQ_i\(t\)%2B%5Cfrac%7B1%7D%7BN_i\(t%2B1\)%7D\(R_t-Q_i\(t\)\)\\)" title="Q\_i(t+1)=Q\_i(t)+1/N\_i(t+1)\*(R\_t - Q\_i(t))" />

### 累積獎勵與遺憾

\<img src="[https://latex.codecogs.com/png.latex?G\_T%3D%5Csum\_%7Bt%3D1%7D%5ET%20R\_t\\](https://latex.codecogs.com/png.latex?G_T%3D%5Csum_%7Bt%3D1%7D%5ET%20R_t\\)" title="G\_T = ∑\_{t=1}^T R\_t" />
\<img src="[https://latex.codecogs.com/png.latex?%5Cmu%5E%2A%3D%5Cmax\_i%20%5Cmu\_i\\](https://latex.codecogs.com/png.latex?%5Cmu%5E%2A%3D%5Cmax_i%20%5Cmu_i\\)" title="μ\* = max\_i μ\_i" />
\<img src="[https://latex.codecogs.com/png.latex?Regret(T)%3DT%5Cmu%5E%2A-%5Cmathbb%7BE%7D%5BG\_T%5D\\](https://latex.codecogs.com/png.latex?Regret\(T\)%3DT%5Cmu%5E%2A-%5Cmathbb%7BE%7D%5BG_T%5D\\)" title="Regret(T)=Tμ\* - E[G\_T]" />

## 解釋

- 參數 \$\varepsilon\$：控制「探索 (Exploration)」與「利用 (Exploitation)」之間的權衡。
- **利用 (Exploitation)**：以機率 \$1 - \varepsilon\$ 選擇當前 \$\hat{\mu}\_i(t)\$ 最大的臂，充分利用已知資訊。
- **探索 (Exploration)**：以機率 \$\varepsilon\$ 隨機選擇任何臂，探索其他臂的潛在價值。
- 若 \$\varepsilon\$ 過大，過度探索導致短期獎勵不足；若 \$\varepsilon\$ 過小，可能陷入次優解。

## 適合應用

- 線上廣告推薦：根據歷史點擊率 \$\hat{\mu}\_i\$ 動態調整展示頻次，並以機率 \$\varepsilon\$ 推薦新廣告。
- A/B 測試：根據方案轉換率 \$\hat{\mu}\_i\$ 決定主推方案，並偶爾以機率 \$\varepsilon\$ 測試新方案。
- 遊戲智能代理：在回合制遊戲中根據估計獎勵 \$\hat{\mu}\_i\$ 選擇動作，並探索未知動作。
- 推薦系統：動態推薦物品或內容，並以機率 \$\varepsilon\$ 嘗試新物品以更新使用者偏好。

## 額外圖形分析

### 圖 1：平均累積回報

![]\(Result/1.png)

在「Average Cumulative Reward Over Time」圖中：

- 不同 \$\varepsilon\$ 值的曲線斜率反映了長期累積回報效率。
- \$\varepsilon=0.1\$ 最快累積回報（線性最陡），因為及早探索找到最優臂後持續利用。
- \$\varepsilon=0.01\$ 次之，斜率介於二者之間。
- \$\varepsilon=0.0\$ （純利用）如果首選非最優臂，則累積回報最差。

### 圖 2：平均即時回報

![]\(Result/2.png)

在「Average Instantaneous Reward Over Time」圖中：

- \$\varepsilon=0.1\$ 初期波動後快速提升至高水準（約 0.9），穩定最大化即時收益。
- \$\varepsilon=0.01\$ 上升速度較慢，需較長時間收斂至最佳區間。
- \$\varepsilon=0.0\$ 平均獲得獎勵約 0.4 左右，因為鎖定了次優臂。

### 圖 3：探索比例

![]\(Result/3.png)

在「Exploration Fraction Over Time」圖中：

- 曲線約在理論值附近振盪：\$\varepsilon=0.1\$ 約 10%、\$\varepsilon=0.01\$ 約 1%、\$\varepsilon=0.0\$ 永遠為 0。
- 這反映了演算法中「隨機探索」機制的真實執行比例。

## ChatGPT 提示語

```
假設你是一位機器學習專家，請根據以下資訊協助分析 ε-貪婪演算法的核心表現：
1. 算法設定：臂數 K = 10，真實獎勵機率隨機生成，ε 分別為 0.0、0.01、0.1。
2. 圖表：
   - Average Cumulative Reward Over Time
   - Average Instantaneous Reward Over Time
   - Exploration Fraction Over Time
請綜合說明：
- 各 ε 下累積回報與即時回報的差異與原因。
- 探索比例如何影響回報曲線。
- 若要在新場景中選擇 ε，可參考哪些準則？
```

