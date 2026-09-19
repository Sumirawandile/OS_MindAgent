import json
from groq import Groq
from config import GROQ_API_KEY, FAST_MODEL, OS_SYLLABUS, TOPIC_TO_UNIT, UNIT_TO_TOPIC, TOPIC_CHOICES
from database.db import save_quiz_result

# Curated Fallback Quiz Questions for Operating Systems Topics
FALLBACK_QUIZZES = {
    "Unit 1": [
        {
            "question": "Which of the following OS architecture layers directly interacts with hardware?",
            "options": ["Kernel", "Shell", "User Application", "GUI Interface"],
            "answer": "Kernel",
            "explanation": "The Kernel is the core component of an OS that manages hardware resources directly."
        },
        {
            "question": "Which service transitions a process from User Mode to Kernel Mode?",
            "options": ["System Call", "Context Switch", "Thread Pool", "Spooling"],
            "answer": "System Call",
            "explanation": "System calls provide the interface between a process and the operating system kernel."
        },
        {
            "question": "Which OS type is designed to respond to events within strict time constraints?",
            "options": ["Real-Time OS", "Batch OS", "Time-Sharing OS", "Distributed OS"],
            "answer": "Real-Time OS",
            "explanation": "Real-Time Operating Systems (RTOS) guarantee processing within rigid time bounds."
        }
    ],
    "Unit 2": [
        {
            "question": "In a typical operating system, which of the following is NOT a valid transition between process states?",
            "options": ["Ready -> Running", "Running -> Waiting", "Waiting -> Ready", "Terminated -> Running"],
            "answer": "Terminated -> Running",
            "explanation": "Once a process is in Terminated state, its execution has finished and PCB is freed. It cannot transition back to Running."
        },
        {
            "question": "Which field is NOT typically stored in a Process Control Block (PCB)?",
            "options": ["Process ID (PID)", "Program Counter (PC)", "Page Table Base Register (PTBR)", "CPU Cache Contents"],
            "answer": "CPU Cache Contents",
            "explanation": "CPU cache memory contents are handled dynamically by CPU hardware cache controllers, not stored in the software PCB."
        },
        {
            "question": "Which CPU scheduling algorithm can lead to the 'Convoy Effect'?",
            "options": ["First-Come, First-Served (FCFS)", "Round Robin (RR)", "Shortest Remaining Time First (SRTF)", "Priority Scheduling"],
            "answer": "First-Come, First-Served (FCFS)",
            "explanation": "In FCFS, a long CPU-bound process holds the CPU while shorter I/O-bound processes wait behind it (Convoy Effect)."
        }
    ],
    "Unit 3": [
        {
            "question": "Which of the following is NOT one of Coffman's 4 necessary conditions for Deadlock?",
            "options": ["Preemption allowed", "Mutual Exclusion", "Hold and Wait", "Circular Wait"],
            "answer": "Preemption allowed",
            "explanation": "No Preemption (resources cannot be forcibly taken) is the necessary condition. Preemption prevents deadlock."
        },
        {
            "question": "What algorithm is used for Deadlock Avoidance in Operating Systems?",
            "options": ["Banker's Algorithm", "Peterson's Algorithm", "Dekker's Algorithm", "Bakery Algorithm"],
            "answer": "Banker's Algorithm",
            "explanation": "Dijkstra's Banker's Algorithm checks resource allocations for safe state transitions to avoid deadlock."
        },
        {
            "question": "What type of variable is a Semaphore?",
            "options": ["Integer variable with wait() and signal() operations", "Boolean flag only", "String array", "Pointer to PCB"],
            "answer": "Integer variable with wait() and signal() operations",
            "explanation": "A Semaphore is an integer variable accessed through atomic operations wait (P) and signal (V)."
        }
    ],
    "Unit 4": [
        {
            "question": "What component speeds up virtual-to-physical address translation in paging?",
            "options": ["Translation Lookaside Buffer (TLB)", "Dispatcher", "Inverted Heap", "Swapper"],
            "answer": "Translation Lookaside Buffer (TLB)",
            "explanation": "The TLB is a high-speed associative hardware cache for page table lookups."
        },
        {
            "question": "Which page replacement algorithm suffers from Belady's Anomaly?",
            "options": ["FIFO (First In First Out)", "LRU (Least Recently Used)", "Optimal Page Replacement", "LFU"],
            "answer": "FIFO (First In First Out)",
            "explanation": "Belady's Anomaly (more frames -> more page faults) occurs in FIFO page replacement."
        },
        {
            "question": "What happens during a Page Fault?",
            "options": ["The required page is not in RAM and must be fetched from secondary storage", "CPU crashes", "TLB overflows", "Process is terminated"],
            "answer": "The required page is not in RAM and must be fetched from secondary storage",
            "explanation": "A Page Fault trap occurs when a process accesses a page marked invalid/absent in main memory."
        }
    ],
    "Unit 5": [
        {
            "question": "Which directory structure prevents circular references and allows file sharing?",
            "options": ["Acyclic Graph Directory", "Single-Level Directory", "Two-Level Directory", "Linear Directory"],
            "answer": "Acyclic Graph Directory",
            "explanation": "An Acyclic Graph structure allows directories/files to have shared subdirectories without loops."
        },
        {
            "question": "Which file access method reads records sequentially from beginning to end?",
            "options": ["Sequential Access", "Direct / Random Access", "Indexed Access", "Hashed Access"],
            "answer": "Sequential Access",
            "explanation": "Sequential Access reads data one record after another, which is common for tape and text streams."
        },
        {
            "question": "What system operation connects a file system to a specific location in the directory tree?",
            "options": ["Mounting", "Binding", "Linking", "Formatting"],
            "answer": "Mounting",
            "explanation": "Mounting attaches a filesystem structure to a designated mount point directory."
        }
    ]
}

# Alias fallback quizzes for topic titles
for u_key, t_title in UNIT_TO_TOPIC.items():
    if u_key in FALLBACK_QUIZZES:
        FALLBACK_QUIZZES[t_title] = FALLBACK_QUIZZES[u_key]

def generate_unit_quiz(topic_tag: str):
    """
    Generates 3 MCQs for the specified OS topic using Groq API or curated fallback questions.
    """
    topic_title = UNIT_TO_TOPIC.get(topic_tag, topic_tag)
    unit_key = TOPIC_TO_UNIT.get(topic_title, "Unit 1")
    
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            prompt = f"""
Generate 3 distinct multiple-choice questions (MCQs) for 3rd year CSE Operating Systems exam on topic: {topic_title}.
Respond strictly in JSON format matching this schema:
{{
  "questions": [
    {{
      "question": "Question text...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Exact text of correct option",
      "explanation": "Brief explanation of why it is correct"
    }}
  ]
}}
"""
            completion = client.chat.completions.create(
                model=FAST_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            data = json.loads(completion.choices[0].message.content)
            if isinstance(data, dict):
                for key in ["questions", "quiz", "mcqs"]:
                    if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                        return data[key]
            elif isinstance(data, list) and len(data) > 0:
                return data
        except Exception as e:
            print(f"Quiz generation error: {e}")
            
    return FALLBACK_QUIZZES.get(topic_title, FALLBACK_QUIZZES.get(unit_key, FALLBACK_QUIZZES["Unit 1"]))

def evaluate_unit_quiz(topic_tag: str, quiz_questions: list, user_choices: list):
    """
    Evaluates user choices safely against correct answers, calculates score, logs to DB, and returns report.
    """
    score = 0
    total = len(quiz_questions) if quiz_questions else 0
    feedback_items = []
    
    if not quiz_questions:
        return "⚠️ No questions available to evaluate.", 0, 0
    
    for idx, (q, choice) in enumerate(zip(quiz_questions, user_choices), start=1):
        if not isinstance(q, dict):
            continue
            
        correct = q.get("answer", q.get("correct_answer", ""))
        explanation = q.get("explanation", q.get("reason", f"The correct answer is {correct}."))
        
        # Robust string matching for option choices
        choice_str = str(choice or "").strip()
        correct_str = str(correct or "").strip()
        
        is_correct = False
        if choice_str and correct_str:
            c_clean = choice_str.lower()
            ans_clean = correct_str.lower()
            
            if c_clean == ans_clean or ans_clean in c_clean or c_clean in ans_clean:
                is_correct = True
                
        if is_correct:
            score += 1
            feedback_items.append(f"✅ **Q{idx}: Correct!** (`{choice_str}`)\n_{explanation}_")
        else:
            feedback_items.append(f"❌ **Q{idx}: Incorrect.**\n- Your choice: `{choice_str if choice_str else 'Not Answered'}`\n- Correct answer: `{correct_str}`\n- _Explanation: {explanation}_")
            
    pct = round((score / total) * 100) if total > 0 else 0
    
    try:
        save_quiz_result(topic_tag, score, total)
    except Exception as e:
        print(f"Error saving quiz result: {e}")
    
    summary = f"### 📊 Quiz Results: {score}/{total} ({pct}%)\n\n" + "\n\n".join(feedback_items)
    return summary, score, total

generate_topic_quiz = generate_unit_quiz
evaluate_topic_quiz = evaluate_unit_quiz
