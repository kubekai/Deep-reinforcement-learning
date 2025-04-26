# 🎰 MAB 演算法優缺點比較
> ⬇️ 點開／收合每個演算法，查看精簡的優缺點列表  

---

<details>
<summary>🎯 **Epsilon-Greedy** │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/S1GR7xY1xe" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- 🔹 **概念簡單、實作容易**  
- 🔹 只需一個 `epsilon` 調整探索比例  
- 🔹 **計算量低**，適合即時或大量臂場景  

### ❌ 缺點
- 🔸 `epsilon` 需人工設計，常須隨時間遞減  
- 🔸 固定探索率在收斂後期 **犧牲收益**  
- 🔸 未考慮 **估計不確定度**，對非平穩環境適應性差  

</details>

---

<details>
<summary>📈 **UCB (Upper Confidence Bound)** │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/BkhzV19kel" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- 🔹 同時衡量 **價值估計 + 不確定度**，自動調節探索  
- 🔹 有 **明確理論後悔值上限**  
- 🔹 一般 **不需額外超參數**  

### ❌ 缺點
- 🔸 初期樣本少時，信賴區估計不穩  
- 🔸 **信賴界設計** 依賴假設，面對複雜／非平穩分布較難  
- 🔸 有時會 **過度探索** 罕見臂  

</details>

---

<details>
<summary>🌡️ **Softmax /Boltzmann Exploration** │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/HJon3k51xl" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- 🔹 溫度參數將價值平滑轉為機率，**探索-利用過程漸進**  
- 🔹 溫度退火可 **自然收斂**  
- 🔹 易與 **可導方法**（策略梯度）整合  

### ❌ 缺點
- 🔸 必須 **精心設計退火曲線**；過熱隨機、過冷貪婪  
- 🔸 仍未直接利用 **不確定度**  
- 🔸 需 **指數運算**，臂數大時較耗資源  

</details>

---

<details>
<summary>🎲 **Thompson Sampling** │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/BkJRQl5kel" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- 🔹 基於 **貝葉斯後驗抽樣**，自然平衡探索與利用  
- 🔹 理論後悔值接近最優，**實務表現穩定**  
- 🔹 易延伸至 **上下文、多參數或非平穩** 場景  

### ❌ 缺點
- 🔸 需選擇 **合適先驗分布**；不當先驗影響收斂  
- 🔸 複雜分布或大規模參數時，**抽樣 / 更新成本高**  
- 🔸 無共軛先驗時，需 **近似推斷** 或數值方法  

</details>

---

