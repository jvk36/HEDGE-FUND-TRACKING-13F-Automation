```mermaid
graph TD
    A[Block N\n(Previous Block)] -->|Mined by Miner 1| B[Block N+1\n(Coinbase Reward: 3.125 BTC + Fees)]
    A -->|Mined by Miner 2| C[Block N+1'\n(Competing Block)]
    B -->|Mined Next| D[Block N+2\n(Built on N+1)]
    C -->|Mined Next| E[Block N+2'\n(Built on N+1')]
    D --> F[Block N+3]
    F --> G[...]
    G --> H[Block N+101\n(Reward from Block N+1 Spendable)]

    subgraph Fork Scenario
        B -->|Temporary Chain| D
        C -->|Temporary Chain| E
        D -->|Longer Chain Wins| F
        E -->|Orphaned| X[Discarded]
    end

    subgraph Key
        I[Coinbase Maturity\n(100 Blocks)] --> H
        J[Block Reward Earned\n(Probabilistic)] --> B
        K[Confirmation\n(1-6 Blocks)] --> D
    end

    classDef block fill:#f9f,stroke:#333,stroke-width:2px
    classDef orphaned fill:#fdd,stroke:#f00,stroke-width:2px
    class A,B,C,D,E,F,G,H block
    class X orphaned
```
