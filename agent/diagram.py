def generate_mermaid_diagram(diagram_type: str, context_text: str = "") -> str:
    """
    Generates text-based visual diagrams for OS concepts (Gantt charts, Process States, Deadlock RAG, Paging TLB).
    Returns clean markdown-formatted strings for Gradio display.
    """
    dt = diagram_type.lower()

    if "gantt" in dt or "scheduling" in dt:
        return """
---
### 📊 CPU Scheduling: Gantt Chart (Example: 4 Processes)

```
FCFS Gantt Chart
─────────────────────────────────────────
Time:   0      4      9      12     14
        |------|------|------|------|
CPU:     P1(4)  P2(5)  P3(3)  P4(2)
─────────────────────────────────────────
```

```
Round Robin Gantt Chart (Quantum Q = 2ms)
─────────────────────────────────────────
Time:   0  2  4  6  8  10 12 14
        |--|--|--|--|--|--|--|--|
CPU:    P1 P2 P3 P4 P1 P2 P3 ...
─────────────────────────────────────────
```

**Key Insight:** FCFS = long single blocks; Round Robin = short alternating blocks.
"""

    elif "process_state" in dt or "state" in dt:
        return """
---
### 📊 Process State Transition Diagram

```
     ┌───────────────────────────────────────────────────────────┐
     │                   Process State Machine                     │
     └───────────────────────────────────────────────────────────┘

   [New] ──admitted──► [Ready] ◄──────── I/O Complete ──────── [Waiting]
                          │                                          ▲
                   scheduler dispatch                           I/O or
                          │                                    event wait
                          ▼                                          │
                      [Running] ─────────────────────────────────────┘
                          │
                      exit/finish
                          │
                          ▼
                      [Terminated]
```

**Key:** Every process goes New → Ready → Running. From Running it can go:
- → Waiting (I/O request), → Ready (interrupt/preemption), → Terminated (exit)
"""

    elif "deadlock" in dt or "rag" in dt or "banker" in dt:
        return """
---
### 📊 Deadlock: Resource Allocation Graph (RAG)

```
     Processes           Resources
     ─────────           ─────────
     [P1] ──────requests──────► [R1]
      ▲                           │
      │                        allocated
   allocated                      │
      │                           ▼
     [R2] ◄──────requests────── [P2]
```

**Circular Wait = DEADLOCK!** All 4 Coffman conditions are present:
1. Mutual Exclusion   2. Hold & Wait   3. No Preemption   4. Circular Wait

**Banker's Algorithm Safe State Check:**
```
Allocation  Max  Need  Available
P1: [1,0]  [2,0] [1,0]   [1,1]
P2: [0,1]  [1,2] [1,1]
Safe Sequence: P1 → P2 ✅
```
"""

    elif "paging" in dt or "memory" in dt or "tlb" in dt:
        return """
---
### 📊 Memory Management: Paging & TLB

```
  Logical Address: | Page# (p) | Offset (d) |
                          │
                    ┌─────▼──────┐
                    │  TLB Check │
                    └─────┬──────┘
              Hit ◄────── │ ──────► Miss
               │           │           │
        Frame# (f)   Page Table     Page Table
               │    (slower RAM)      Lookup
               └─────────► Physical Address = f + d
```

**TLB Hit** → Fast (1 memory access)
**TLB Miss** → Slow (2 memory accesses: page table + data)

**Page Replacement Algorithms:**
```
Reference string: 1 2 3 4 1 2 5 1 2 3
Frames = 3

FIFO:    Faults = 7    ← simple but Belady's Anomaly
LRU:     Faults = 6    ← no anomaly, more overhead
Optimal: Faults = 5    ← best but not implementable
```
"""

    elif "file" in dt or "directory" in dt:
        return r"""
---
### 📊 File System: Directory Structure


```
      Single-Level          Two-Level            Tree (Hierarchical)
      ────────────          ─────────            ──────────────────
        [Root]              [Root]                    [Root /]
      /  |  |  \           /     \                  /         \
    f1  f2  f3  f4      [User1] [User2]        [/home]       [/etc]
                          |  |     |  |            |
                         f1  f2   f3  f4       [/student]
                                                   |
                                               [notes.txt]
```

**Acyclic Graph** allows sharing (hard links) without cycles.
**General Graph** requires garbage collection to detect cycles.
"""

    else:
        return """
---
### 📊 Agentic AI Multi-Agent Architecture Blueprint

```
  Student OS Query
       │
       ▼
 ┌─────────────────┐
 │  Router Agent   │ ──► Autonomous OS Topic Tag + Confidence %
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │  Tutor Agent    │ ──► Groq Compound AI → Step-by-Step Solution
 └────────┬────────┘
          │
          ▼
 ┌─────────────────┐
 │  SQLite Memory  │ ──► Multi-turn Session State + PDF Exporter
 └─────────────────┘
```
"""
