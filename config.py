import os
from dotenv import load_dotenv

load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



PRIMARY_MODEL = "openai/gpt-oss-120b"
FAST_MODEL = "openai/gpt-oss-20b"

# Operating Systems (OS) Subject Syllabus Structure
OS_SYLLABUS = {
    "Unit 1": {
        "title": "Introduction to Operating System",
        "topics": [
            "Introduction and need of OS",
            "Evolution of OS",
            "Layered Architecture / Logical structure of OS",
            "OS services",
            "Types of OS (Batch, Multi-programmed, Time-sharing, Distributed, Real-time)",
            "Introduction to UNIX OS"
        ]
    },
    "Unit 2": {
        "title": "Processes and Process Management",
        "topics": [
            "Process concept & Process states (New, Ready, Running, Waiting, Terminated)",
            "CPU bound vs I/O bound processes",
            "Process & Thread management services",
            "CPU Schedulers (Short-term, Medium-term, Long-term, Dispatcher)",
            "Preemptive vs Non-preemptive scheduling",
            "Scheduling algorithms: FCFS, SJF, SRTF, Round Robin (RR), Priority, Multilevel Feedback Queue"
        ]
    },
    "Unit 3": {
        "title": "IPC, Synchronization & Deadlocks",
        "topics": [
            "Interprocess Communication (Message passing, Shared memory)",
            "Race condition & Critical Section Problem",
            "Mutual Exclusion with busy waiting (Disabling interrupts, Lock variables, Peterson's solution, TSL instruction)",
            "Sleep and Wakeup calls, Semaphores, Monitors",
            "Classical IPC Problems (Dining Philosophers, Producer-Consumer, Readers-Writers)",
            "Deadlock characterization (4 Necessary conditions)",
            "Deadlock handling: Prevention, Avoidance (Banker's Algorithm), Detection & Recovery"
        ]
    },
    "Unit 4": {
        "title": "Memory Management",
        "topics": [
            "Logical vs Physical address space & Address binding",
            "Contiguous vs Non-contiguous memory allocation",
            "Paging concept, Translation Lookaside Buffer (TLB), Inverted Page Table",
            "Segmentation",
            "Virtual Memory & Demand Paging",
            "Page replacement policies: FIFO, LRU (Least Recently Used), Optimal"
        ]
    },
    "Unit 5": {
        "title": "File System",
        "topics": [
            "File concepts, attributes, operations, types, and file organization",
            "Access methods (Sequential, Direct)",
            "Memory mapped files",
            "Directory structures (Single-level, Two-level, Hierarchical/Tree, Acyclic graph, General graph)",
            "File system mounting & File sharing",
            "Path names & Directory operations"
        ]
    }
}

# OS Topics for UI Display (Clean Topic Names, No "Unit" labels)
TOPIC_CHOICES = [
    "Introduction to Operating System",
    "Processes and Process Management",
    "IPC, Synchronization & Deadlocks",
    "Memory Management",
    "File System"
]

TOPIC_TO_UNIT = {
    "Introduction to Operating System": "Unit 1",
    "Processes and Process Management": "Unit 2",
    "IPC, Synchronization & Deadlocks": "Unit 3",
    "Memory Management": "Unit 4",
    "File System": "Unit 5"
}

UNIT_TO_TOPIC = {
    "Unit 1": "Introduction to Operating System",
    "Unit 2": "Processes and Process Management",
    "Unit 3": "IPC, Synchronization & Deadlocks",
    "Unit 4": "Memory Management",
    "Unit 5": "File System"
}

# Agentic AI & Automation Architecture Metadata (For viva / professor presentation)
AGENTIC_AI_FRAMEWORK_INFO = {
    "course_name": "Agentic AI & Automation",
    "system_architecture": "Multi-Agent System with Autonomous Routing, Custom Tool Dispatch, and Persistent Session Memory",
    "components": [
        "Router Agent: Autonomous query triage into OS topics with confidence scoring",
        "Specialist Tutor Agent: LLM reasoning with structured explanation synthesis",
        "Custom Tool Dispatch: Mermaid.js visual Gantt charts, RAG state diagrams, and ReportLab PDF Exporter",
        "Persistent Memory: SQLite database logging multi-turn doubts and quiz records",
        "MCP / Gradio Integration: Standalone web app interface designed with Gradio controls"
    ]
}
