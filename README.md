# TradeBot
Partially public code of my private repository.

Uses public libraries: pytorch, numpy, csv, json, requests, time, datetime

Tasks (Automated):
1. obtain data
- Find all companies that fulfill the private filter
  - utilizes Web Scraping
2. prepare data
3. Run private algorithm on cooked data
- return Confirmation
4. Buy & Sell
- if confirmation > threshold: 
  - purchaseOrder() @ specified buyTime
  - if price > pThreshold: 
    - sellOrder() @ specified sellTime
    else:
      - send notification to user's phone to manually handle sell
