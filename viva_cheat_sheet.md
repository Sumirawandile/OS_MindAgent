# 🎓 OS-MindAgent: Complete Viva Preparation Cheat Sheet

This guide is specially prepared for your **CA3 Evaluation Viva (5 Marks)**. It covers the most expected questions from both your project evaluation panel and your faculty on **Agentic AI & Automation** and **Operating Systems (T7510)**.

---

## 🤖 Section 1: Agentic AI & Project Architecture Questions

### Q1: What makes your project an "Agentic AI" application rather than just a ChatGPT wrapper?
**Answer:** 
> "Standard ChatGPT prompt wrappers pass a prompt directly to an LLM without domain routing or state management. **OS-MindAgent** is an agentic workflow because:
> 1. **Autonomous Router Agent**: It analyzes incoming student queries and autonomously categorizes them into Symbiosis OS Syllabus Units 1–5 with a calculated confidence score.
> 2. **Specialist Tutor Agent**: It conditions responses on syllabus context, formatting explanations with definitions, mechanisms, examples, and exam tips.
> 3. **Smart Diagram & Quiz Tools**: It dynamically invokes tools to generate visual Mermaid.js flowcharts (Gantt charts, process states) and unit practice quizzes.
> 4. **State Persistence & Memory**: It logs queries to SQLite and exports formatted PDF notes."

### Q2: Why did you choose the Groq API over OpenAI or Ollama?
**Answer:**
> "We chose **Groq API** powered by **Llama-3.3-70B** because:
> - **Inference Speed**: Groq's LPU (Language Processing Unit) architecture delivers responses in sub-1.2 seconds, making interactive doubt resolution instant.
> - **Model Capability**: Llama-3.3-70B offers state-of-the-art technical reasoning and structured JSON output capability.
> - **Accessibility**: Groq provides a generous free tier ideal for student mini-projects without API credit constraints."

### Q3: How does your system handle topic categorization and confidence scoring?
**Answer:**
> "The Router Agent evaluates student input against syllabus keywords and conceptual definitions. It outputs a JSON response containing `unit_tag` (Unit 1 to 5), `unit_title`, `confidence` (e.g. 0.95), and `diagram_recommended`. If API connection drops, a robust keyword heuristic fallback ensures zero system downtime."

---

## 🖥 Section 2: Operating Systems (T7510) Core Viva Questions

### Q4: Explain the difference between FCFS and Round Robin CPU scheduling.
**Answer:**
> - **FCFS (First-Come, First-Served)**: Non-preemptive algorithm. Processes are executed in order of arrival. Suffers from the **Convoy Effect** where short processes wait behind long CPU-bound processes.
> - **Round Robin (RR)**: Preemptive algorithm. Each process gets a fixed time slice (**time quantum**). Reduces response time and prevents starvation.

### Q5: What are Coffman's 4 Necessary Conditions for Deadlock?
**Answer:**
> 1. **Mutual Exclusion**: At least one resource must be held in a non-shareable mode.
> 2. **Hold and Wait**: A process holds at least one resource while waiting for additional resources.
> 3. **No Preemption**: Resources cannot be forcibly taken from a process.
> 4. **Circular Wait**: A closed chain of processes exists where each process holds resources needed by the next.

### Q6: What is Peterson's Solution?
**Answer:**
> "Peterson's Solution is a classic software-based solution to the Critical Section problem for **2 processes**. It uses two shared variables: `flag[2]` (indicating desire to enter) and `turn` (indicating whose turn it is). It guarantees **Mutual Exclusion, Progress, and Bounded Waiting**."

### Q7: What is Belady's Anomaly and in which page replacement algorithm does it occur?
**Answer:**
> "Belady's Anomaly is the phenomenon where increasing the number of memory frames results in an **increase** in the number of page faults. It occurs in **FIFO (First-In, First-Out)** page replacement. Stack-based algorithms like **LRU** and **Optimal** do NOT suffer from Belady's Anomaly."

---

## 🛠 Section 3: Tech Stack & Implementation Viva Questions

### Q8: How is the database designed and how does PDF export work?
**Answer:**
> - **Database**: SQLite (`os_doubts.db`) with two tables: `doubts` (logs query, answer, unit tag, confidence score, timestamp) and `quizzes` (logs quiz scores).
> - **PDF Export**: ReportLab library formats logged rows into styled paragraphs, headers, and bulleted text saved to a downloadable PDF document (`OS_Doubt_Summary.pdf`).

### Q9: How is the dashboard created?
**Answer:**
> "The dashboard is created using **Gradio 4+** in Python. It features 4 interactive tabs: *Smart Doubt Resolver*, *Practice Quiz Generator*, *History & Notes Export*, and *Syllabus Explorer* with custom CSS styling."
