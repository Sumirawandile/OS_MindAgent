import json
from groq import Groq
from config import GROQ_API_KEY, PRIMARY_MODEL, OS_SYLLABUS
from agent.router import classify_doubt
from agent.diagram import generate_mermaid_diagram
from database.db import save_doubt

def resolve_os_doubt(question: str, history: list = None, force_diagram: bool = False):
    """
    Main agent function to resolve OS doubts using Groq Llama-3.3-70B.
    Classifies OS topic, generates step-by-step explanation, appends visual diagrams, and logs to SQLite.
    """
    if history is None:
        history = []
        
    # 1. Classify the question into OS Topics & evaluate confidence
    meta = classify_doubt(question)
    unit_title = meta.get("unit_title", meta.get("unit_tag", "Introduction to Operating System"))
    unit_tag = unit_title
    confidence = meta.get("confidence", 0.95)
    diagram_recommended = meta.get("diagram_recommended", False) or force_diagram
    diagram_type = meta.get("diagram_type", "gantt")
    
    # 2. Build OS Tutor Prompt
    system_prompt = f"""
You are **OS-MindAgent**, an expert, friendly Operating Systems professor tutoring a 3rd-Year CSE student under Symbiosis Course T7510.
The current syllabus topic is **{unit_title}**.

Structure your answer clearly using Markdown:
1. **Core Concept / Definition**: Clear 2-3 sentence definition.
2. **Step-by-Step Explanation**: Bullet points or numbered steps explaining the mechanism.
3. **Real-World / Code Example**: A simple Linux/C code snippet or real-world OS analogy.
4. **Key Exam Takeaway / Viva Formula**: Quick bullet summary for lab exams and viva.

Keep the tone encouraging, structured, technical, and easy to follow.
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    for user_msg, assistant_msg in history[-3:]:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
        
    messages.append({"role": "user", "content": question})

    answer_text = ""
    
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            answer_text = completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API call error: {e}")
            answer_text = get_fallback_answer(unit_title, question)
    else:
        answer_text = get_fallback_answer(unit_title, question)

    diagram_md = ""
    if diagram_recommended:
        diagram_md = generate_mermaid_diagram(diagram_type, question)
        
    save_doubt(
        unit_tag=unit_title,
        question=question,
        answer=answer_text,
        confidence=confidence,
        has_diagram=bool(diagram_md)
    )

    return {
        "answer": answer_text,
        "unit_tag": unit_title,
        "unit_title": unit_title,
        "confidence": confidence,
        "diagram_md": diagram_md
    }

def get_fallback_answer(topic_title: str, question: str) -> str:
    """Fallback offline answer generator for OS topics."""
    return f"""### 📌 Core Concept: {question}

**Topic:** {topic_title}

1. **Definition**: In Operating Systems, this concept handles how system resources (CPU, Memory, Disk) are assigned and managed efficiently.
2. **Key Steps**:
   - The OS tracks resource states in kernel data structures (e.g., Process Control Block or Page Tables).
   - Decisions are made based on preemptive or non-preemptive policies.
   - Interrupts or system calls signal transitions between User mode and Kernel mode.
3. **Example**:
   - In C/Linux programming: `fork()` creates a child process, `exec()` loads a program, and `wait()` synchronizes parent and child.
4. **Exam Tip**: Always mention state transitions, PCB attributes, and execution context when writing answers for {topic_title}.

*(Note: Add your `GROQ_API_KEY` in `.env` or `config.py` for live AI explanations via Groq Llama-3.3-70B).*
"""
