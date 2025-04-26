# Epsilon-Greedy
## https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/S1GR7xY1xe
# UCB (Upper Confidence Bound)
## https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/BkhzV19kel
# Softmax
## https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/HJon3k51xl
# Thompson Sampling
## https://hackmd.io/@1wquA7--QryPpt4pYcCWsQ/BkJRQl5kel

# MAB 演算法優缺點比較

## Epsilon Greedy  
**優點：**  
演算法概念直觀，實作容易；透過設定 epsilon 即可直接控制探索比例；計算需求低，適合大量拉霸或即時系統。  

**缺點：**  
epsilon 需人工調整且常要隨時間遞減；固定探索率在收斂後期可能犧牲收益；未考慮估計不確定度，對非平穩環境適應性較差。  

---

## UCB（Upper Confidence Bound）  
**優點：**  
利用信賴區間同時衡量價值估計與不確定度，能自動調節探索；理論後悔值上限明確；通常不需外部超參數。  

**缺點：**  
計算信賴區間時需依賴時間與臂次數統計，對初期估計及問題平穩性較敏感；若獎勵分布複雜或變動，信賴界設計不易；有時會過度探索罕見臂。  

---

## Softmax（Boltzmann Exploration）  
**優點：**  
透過溫度參數將價值轉換為機率，探索與利用過程平滑且可微；溫度遞減可自然收斂；適合策略梯度等可導方法。  

**缺點：**  
需要小心設計溫度退火曲線，過熱易隨機、過冷易貪婪；仍未直接利用不確定度資訊；計算需指數運算，對大臂數時較耗資源。  

---

## Thompson Sampling  
**優點：**  
基於貝葉斯後驗抽樣，自然平衡探索與利用；通常取得接近最優的理論後悔值；對非平穩或上下文情境可延伸性佳，超參數需求少。  

**缺點：**  
需選擇合適先驗分布，先驗不當恐影響收斂；複雜分布或大規模參數時抽樣成本高；實務中若無共軛性，推斷與更新可能需近似或數值方法。  
