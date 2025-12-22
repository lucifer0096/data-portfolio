# NBA 2024/25 Player Impact & Awards Analysis (Excel)

Analyse game‑by‑game NBA player box‑score data to identify high‑impact players, explore MVP and DPOY candidates, and understand how role and game result affect scoring and efficiency.

---

## 📂 Dataset

- **Scope:** Full 2024/25 regular‑season player game logs  
- **Size:** 16,512 game records, 562 unique players  
- **Source:** https://www.kaggle.com/datasets/eduardopalmieri/nba-player-stats-season-2425  
- **Time period:** October 2024 – April 2025  

**Original columns (15 key stats)**  

- *Player, Tm, Opp, Res* – Name, team, opponent, result  
- *MP* – Minutes played  
- *FG/FGA/FG%, 3P/3PA/3P%, FT/FTA/FT%* – Shooting stats  
- *TRB, AST, STL, BLK, TOV* – Rebounding, playmaking, defence, mistakes  
- *PTS, GmSc* – Scoring and game‑score summary  

**Engineered columns**

- **PTS36** – Points per 36 minutes (`PTS / MP × 36`)  
- **EffSimple** – Simple impact metric: `PTS + TRB + AST + STL + BLK − (FGA − FG) − (FTA − FT) − TOV`  
- **DefImpact** – Defensive impact: `STL + BLK + DRB − TOV`  
- **RoleBand** – Role band (Starter / Key Rotation / Bench) based on average minutes played  

---

## 🛠️ Tools & skills

- Excel for data cleaning, engineered columns, and pivot tables  
- Advanced formulas for custom efficiency and defensive metrics  
- PivotTables and charts to compare players by role, game result, and award candidacy  

---

## ❓ Business questions

- Which players deliver the highest overall impact over the 2024/25 regular season?  
- How do MVP and DPOY candidates separate from the rest of the league on scoring, efficiency, and defence?  
- How does player role (Starter, Key Rotation, Bench) affect production and impact?  
- How does performance change in wins vs losses for key players and roles?  

---

## 🔎 Approach

### 1. Data preparation

- Imported full game‑log data and restricted to the 2024/25 regular season  
- Standardised team and player fields  
- Created **RoleBand** based on average minutes played  

### 2. Feature engineering

- Built efficiency and defensive metrics (**PTS36**, **EffSimple**, **DefImpact**) to capture per‑minute and all‑around impact  
- Flagged potential award candidates based on games‑played and minutes thresholds  

### 3. Analysis via pivots

Key pivot tables include:

- **Pvt_PlayerEfficiency_Top10** – ranks high‑minute players by efficiency  
- **Pvt_Top10_WinLoss** – compares individual performance in wins vs losses  
- **Pvt_MVP_Candidates** – focuses on heavy‑minute players (GamesPlayed ≥ 40)  
- **Pvt_RoleBand_Top5** – surfaces the top 5 players in each role band  

### 4. Visualisation

- Charts showing MVP and DPOY profiles  
- Win/loss splits for key players  
- Role‑based bar charts comparing Starters, Key Rotation, and Bench

---

## 🔥 Key insights

- High‑minute, high‑efficiency players clearly separate from league‑average contributors on both **PTS36** and **EffSimple**.  
- Defensive specialists with strong **DefImpact** scores emerge as DPOY‑style candidates even when scoring is modest.  
- Role‑based analysis highlights bench and key‑rotation players providing starter‑level impact in limited minutes.  
- Win/loss splits reveal players whose production translates most directly into team success.  

---

## 🧪 How to use

1. Open the Excel workbook in this folder (`NBA 2k24-25 Analysis Project.xlsb`).  
2. Start with **Info_NBA** for the project overview, dataset summary, and navigation.  
3. Use **NBA_Working** to review cleaned data and engineered columns.  
4. Explore **Player_Summary** and **Pivots_NBA** to drill into player‑ and role‑level pivots.  
5. Use **Dashboard_NBA** to interact with the key charts (MVP bubble scatter, DPOY radar, win vs loss combo, role‑based bar charts).  

---

## 🚀 Future improvements

- Incorporate on/off and lineup‑level impact metrics to complement box‑score analysis  
- Extend the dataset to include playoffs and multi‑season trends  
- Automate data refresh using an NBA stats API and Power Query  
- Add a companion Power BI dashboard for richer interactivity and sharing  
