# Market and Stratefgic Interaction in Network

## Description
This project implements a market-clearing algorthim using a bipartitie graph described in the market.gml file. 
The graph consists of: 

- **Sellers (Set A):** Nodes with 'bipartite = 0', each having an initial price
- **Buyers (Set B):** Nodes with 'bipartite = 1', with preferences defined by 'valuation' attributes on edges. 

## Requirements
- Python 3.7+
- `networkx`
- `matplotlib`

Install:
```bash
pip install networkx matplotlib
```
## How to Run: 
From the terminal, run: 
```bash
python market_strategy.py market.gml --plot --interactive
```
