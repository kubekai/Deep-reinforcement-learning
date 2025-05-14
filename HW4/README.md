# 🎰 DQN 演算法優缺點比較  
> ⬇️ 點開／收合每個演算法，查看精簡的優缺點列表，詳細資訊在 HackMD 中 

---

<details>
<summary>🟢 Naive DQN for Static Mode  │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/r1Uvc531el" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- **實作簡單**：只需一個 Q-network 作為基線  
- **計算量低**：無需額外機制，適用於狀態轉移固定、靜態環境  
- **易於調試**：結構單純，快速定位問題  

### ❌ 缺點
- **高估偏差**：使用單一網路同時選擇與評估動作  
- **收斂緩慢**：缺乏穩定化手段，對環境變化難以適應  
- **震盪大**：在複雜或隨機場景下表現不穩定  

</details>

---

<details>
<summary>🔵 Enhanced DQN Variants for Player Mode │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/SJP4BfJgee" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- **Double DQN** 減少 overestimation bias  
- **Dueling DQN** 將狀態價值與動作優勢分離，提升策略表現  
- **Prioritized Experience Replay** 加速對高誤差樣本的學習  
- **NoisyNet / Rainbow** 等一體化方案可進一步增強探索  

### ❌ 缺點
- **結構複雜**：多網路分支或機制，超參數增多  
- **運算量大**：需維護 target network、優先回放等額外計算  
- **調參成本高**：需要在不同變體間選擇與調整  

</details>

---

<details>
<summary>🛠 Enhance DQN for Random Mode (WITH Training Tips) │ <sub><a href="https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/SyJdxaelxg" target="_blank">HackMD 筆記</a></sub></summary>

### ✅ 優點
- **泛化能力佳**：能適應隨機起點的場景  
- **穩定性提升**：結合多種增強技術，學到更穩定的策略  

### ❌ 缺點
- **訓練不穩定**：隨機性高，reward variance 大  
- **收斂難度增加**：需更多訓練技巧與調參  

### 📝 Training Tips
- **Train Model** : 使用 `PyTorch Lightning ` 架構進行訓練
- **Gradient Clipping**：使用 `gradient_clip_val`（例如 1.0）防止梯度爆炸  
- **Learning Rate Scheduling**：StepLR 或 CosineAnnealing 衰減學習率  
- **Target Network Update**：適度加快 `target_net` 同步頻率  
- **ε-Greedy Decay**：線性或指數衰減 ε，平衡探索與利用  
- **Prioritized Replay**：重點學習高 TD-error 的樣本  
- **Reward Shaping**：加入中間獎勵，降低 sparse reward 的困難度  

</details>
