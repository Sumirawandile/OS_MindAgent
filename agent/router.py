import json
import re
from groq import Groq
from config import GROQ_API_KEY, FAST_MODEL, OS_SYLLABUS

def extract_json(text: str) -> dict:
    """Extract the first JSON object found in a text string."""
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return {}

def classify_doubt(question: str):
    """
    Autonomous Router Agent: Classifies OS student doubts into Operating System topics,
    evaluates confidence score, and determines visual diagram tool recommendation.
    """
    q_lower = question.lower()
    
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            prompt = f"""
You are an Autonomous Router Agent for Operating Systems (OS) Curriculum T7510.
Analyze the following student doubt and classify it strictly into one of these 5 OS topics:
1. Introduction to Operating System (services, types, UNIX, layered structure)
2. Processes and Process Management (states, threads, CPU scheduling: FCFS, SJF, SRTF, RR, Priority)
3. IPC, Synchronization & Deadlocks (critical section, semaphores, Peterson's, Banker's algorithm, deadlocks)
4. Memory Management (paging, TLB, segmentation, virtual memory, page replacement: FIFO, LRU, Optimal)
5. File System (directory structures, file operations, access methods, mounting)

User Question: "{question}"

Respond strictly in valid JSON format (ONLY JSON, no extra text):
{{
  "unit_tag": "Exact Topic Title from the 5 listed above",
  "unit_title": "Exact Topic Title from the 5 listed above",
  "confidence": 0.95,
  "diagram_recommended": true,
  "diagram_type": "gantt"
}}
"""
            response = client.chat.completions.create(
                model=FAST_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            data = extract_json(response.choices[0].message.content)
            if data and "unit_title" in data:
                return data

        except Exception as e:
            print(f"Router API error (falling back to heuristic): {e}")

    # Keyword Heuristic Fallback Classifier
    if any(k in q_lower for k in ["fcfs", "sjf", "srtf", "round robin", "gantt", "priority", "scheduling", "process", "pcb", "thread", "context switch"]):
        return {
            "unit_tag": OS_SYLLABUS["Unit 2"]["title"],
            "unit_title": OS_SYLLABUS["Unit 2"]["title"],
            "confidence": 0.94,
            "diagram_recommended": True if any(k in q_lower for k in ["gantt", "scheduling", "state", "chart"]) else False,
            "diagram_type": "gantt" if "gantt" in q_lower or "scheduling" in q_lower else "process_state"
        }
    elif any(k in q_lower for k in ["deadlock", "banker", "semaphore", "peterson", "critical section", "mutex", "ipc", "monitor", "race condition"]):
        return {
            "unit_tag": OS_SYLLABUS["Unit 3"]["title"],
            "unit_title": OS_SYLLABUS["Unit 3"]["title"],
            "confidence": 0.95,
            "diagram_recommended": True if any(k in q_lower for k in ["banker", "deadlock", "rag", "resource", "semaphore"]) else False,
            "diagram_type": "deadlock_rag"
        }
    elif any(k in q_lower for k in ["page", "paging", "tlb", "lru", "fifo", "segmentation", "virtual memory", "page fault", "address"]):
        return {
            "unit_tag": OS_SYLLABUS["Unit 4"]["title"],
            "unit_title": OS_SYLLABUS["Unit 4"]["title"],
            "confidence": 0.93,
            "diagram_recommended": True if any(k in q_lower for k in ["paging", "tlb", "replacement", "memory"]) else False,
            "diagram_type": "paging"
        }
    elif any(k in q_lower for k in ["file", "directory", "mounting", "path", "inode", "access method"]):
        return {
            "unit_tag": OS_SYLLABUS["Unit 5"]["title"],
            "unit_title": OS_SYLLABUS["Unit 5"]["title"],
            "confidence": 0.91,
            "diagram_recommended": False,
            "diagram_type": "none"
        }
    else:
        return {
            "unit_tag": OS_SYLLABUS["Unit 1"]["title"],
            "unit_title": OS_SYLLABUS["Unit 1"]["title"],
            "confidence": 0.90,
            "diagram_recommended": False,
            "diagram_type": "none"
        }
