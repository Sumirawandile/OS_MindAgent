import gradio as gr
import os
from config import OS_SYLLABUS, GROQ_API_KEY, TOPIC_CHOICES, UNIT_TO_TOPIC, AGENTIC_AI_FRAMEWORK_INFO
from database.db import init_db, fetch_all_doubts, fetch_quiz_stats, clear_all_history
from database.pdf_exporter import generate_pdf_report
from agent.solver import resolve_os_doubt
from agent.quiz import generate_unit_quiz, evaluate_unit_quiz

# Initialize SQLite database tables on launch
init_db()

# Global state for quiz
active_quiz_state = {"questions": [], "unit_tag": "Processes and Process Management"}

def handle_doubt_submit(question, history, force_diagram):
    if not question.strip():
        return "", history, "Select a sample doubt or enter your question to launch AI analysis...", 0.0, ""
        
    res = resolve_os_doubt(question, history, force_diagram)
    
    answer_text = res["answer"]
    confidence = res["confidence"]
    diagram_md = res["diagram_md"]
    
    if diagram_md:
        answer_text += f"\n\n{diagram_md}"
    
    history = history or []
    history.append((question, answer_text))
    
    return "", history, answer_text, confidence, diagram_md

def handle_sample_click(sample_question):
    return sample_question

def handle_generate_quiz(topic_tag):
    global active_quiz_state
    questions = generate_unit_quiz(topic_tag)
    active_quiz_state = {"questions": questions, "unit_tag": topic_tag}
    
    q1 = questions[0] if len(questions) > 0 else {}
    q2 = questions[1] if len(questions) > 1 else {}
    q3 = questions[2] if len(questions) > 2 else {}
    
    q1_label = f"Q1: {q1.get('question', '')}"
    q1_opts = gr.Radio(choices=q1.get('options', []), label=q1_label, visible=True, value=None)
    
    q2_label = f"Q2: {q2.get('question', '')}"
    q2_opts = gr.Radio(choices=q2.get('options', []), label=q2_label, visible=True, value=None)
    
    q3_label = f"Q3: {q3.get('question', '')}"
    q3_opts = gr.Radio(choices=q3.get('options', []), label=q3_label, visible=True, value=None)
    
    return q1_opts, q2_opts, q3_opts, "💡 **Quiz Session Loaded!** Select choices below and click **Submit Answers**.", gr.Button(visible=True)

def handle_submit_quiz(choice1, choice2, choice3):
    global active_quiz_state
    questions = active_quiz_state.get("questions", [])
    topic_tag = active_quiz_state.get("unit_tag", "Processes and Process Management")
    
    if not questions:
        return "⚠️ Please generate a quiz first!"
        
    choices = [choice1, choice2, choice3]
    report_md, score, total = evaluate_unit_quiz(topic_tag, questions, choices)
    return report_md

def handle_refresh_history(topic_filter):
    records = fetch_all_doubts(topic_filter)
    if not records:
        return "<div class='empty-log'>ℹ️ No resolved doubts logged in database. Submit a question to populate history!</div>"
        
    formatted = []
    for r in records:
        topic_name = UNIT_TO_TOPIC.get(r['unit_tag'], r['unit_tag'])
        formatted.append(
            f"### 📑 Log #{r['id']} | `{topic_name}`\n"
            f"⏱️ **Timestamp:** _{r['timestamp']}_\n\n"
            f"❓ **Question:** {r['question']}\n\n"
            f"💡 **Solution:**\n{r['answer']}\n\n"
            f"---"
        )
    return "\n\n".join(formatted)

def handle_export_pdf(topic_filter):
    pdf_filename = generate_pdf_report(topic_filter)
    return pdf_filename

def handle_clear_history():
    clear_all_history()
    return "✅ History logs cleared successfully.", None

# Custom CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root, .light {
    --body-text-color: #0F172A !important;
    --background-fill-primary: #F8FAFC !important;
    --background-fill-secondary: #FFFFFF !important;
    --block-background-fill: #FFFFFF !important;
    --block-border-color: #E2E8F0 !important;
    --button-primary-background-fill: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    --button-primary-text-color: #FFFFFF !important;
}

* {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
    box-sizing: border-box !important;
}

body, .gradio-container {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

.gradio-container *, 
.gradio-container p, 
.gradio-container span, 
.gradio-container li, 
.gradio-container label, 
.gradio-container div,
.prose, .prose *, .md, .md * {
    color: #0F172A !important;
}

.gradio-container label, .gr-form label, fieldset label {
    color: #1E3A8A !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

.dashboard-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #2563EB;
    padding: 16px 24px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.06);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-logo {
    font-size: 1.8rem;
}

.nav-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #1E3A8A !important;
    letter-spacing: -0.01em;
}

.tab-nav button, button[role="tab"] {
    border-radius: 8px !important;
    color: #1E40AF !important;
    background: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 11px 22px !important;
    border: 1px solid #DBEAFE !important;
    margin-right: 6px !important;
    transition: all 0.2s ease !important;
}

.tab-nav button.selected, button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #1D4ED8 !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
}

.dashboard-card, .gr-form, .gr-box, fieldset {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 22px !important;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.05) !important;
}

textarea, input[type="text"], .gr-input, select, .gr-dropdown {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #0F172A !important;
    border-radius: 8px !important;
    font-size: 0.98rem !important;
    padding: 12px !important;
}

.primary-btn button, button.primary-btn, .primary-btn {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.0rem !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35) !important;
}

.sample-chip button, button.sample-chip {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 8px !important;
    text-align: left !important;
    padding: 12px 16px !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    display: block !important;
    width: 100% !important;
    margin-bottom: 8px !important;
}

.dashboard-output-box {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 26px !important;
    color: #0F172A !important;
    line-height: 1.85 !important;
    font-size: 1.0rem !important;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.05) !important;
}

.empty-log {
    background: #EFF6FF;
    border: 1.5px dashed #BFDBFE;
    padding: 26px;
    border-radius: 10px;
    text-align: center;
    color: #1E40AF;
}
"""

with gr.Blocks(title="OS-MindAgent: Doubt Resolution Workspace") as demo:
    
    # Header Navbar
    gr.HTML("""
    <div class="dashboard-navbar">
        <div class="nav-brand">
            <span class="nav-logo"></span>
            <span class="nav-title">OS-MindAgent: Operating Systems Doubt Resolution System</span>
        </div>
    </div>
    """)
    
    with gr.Tabs():
        
        # TAB 1: SMART DOUBT RESOLVER
        with gr.Tab("Smart Doubt Resolver"):
            with gr.Row():
                # LEFT CONTROL PANEL
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["dashboard-card"]):
                        gr.Markdown("### ⚙️ Doubt Resolution Control Panel")
                        question_input = gr.Textbox(
                            label="Enter Operating Systems Question:",
                            placeholder="e.g. How does Round Robin scheduling work with a 2ms time quantum?",
                            lines=3
                        )
                        
                        force_diagram_chk = gr.Checkbox(
                            label="📊 Generate Visual Diagram / Gantt Chart",
                            value=False,
                            info="Appends process transition diagrams or Gantt timelines."
                        )
                        
                        submit_btn = gr.Button("🚀 Resolve Doubt Now", variant="primary", size="lg", elem_classes=["primary-btn"])
                    
                    gr.Markdown("#### 💡 Preset Sample Queries")
                    s1 = gr.Button("1️⃣ Round Robin vs FCFS with Gantt Chart", size="sm", elem_classes=["sample-chip"])
                    s2 = gr.Button("2️⃣ Peterson's Solution for Critical Section", size="sm", elem_classes=["sample-chip"])
                    s3 = gr.Button("3️⃣ Banker's Algorithm for Deadlock Avoidance", size="sm", elem_classes=["sample-chip"])
                    s4 = gr.Button("4️⃣ Difference between Paging and Segmentation", size="sm", elem_classes=["sample-chip"])
                    s5 = gr.Button("5️⃣ Belady's Anomaly in Page Replacement", size="sm", elem_classes=["sample-chip"])
                    
                # RIGHT MAIN WORKBENCH PANEL
                with gr.Column(scale=2):
                    answer_output = gr.Markdown(
                        "### 🎓 AI Solution Workbench\n*Submit an OS question from the control panel or select a sample query to view the structured answer explanation...*",
                        elem_classes=["dashboard-output-box"]
                    )
                    
                    diagram_output = gr.Markdown("")
                    
            chatbot_state = gr.State([])
            
            # Event Bindings
            submit_btn.click(
                fn=handle_doubt_submit,
                inputs=[question_input, chatbot_state, force_diagram_chk],
                outputs=[question_input, chatbot_state, answer_output, gr.Number(visible=False), diagram_output]
            )
            
            s1.click(handle_sample_click, inputs=[gr.State("Explain Round Robin vs FCFS with Gantt Chart")], outputs=[question_input])
            s2.click(handle_sample_click, inputs=[gr.State("What is Peterson's Solution for Critical Section?")], outputs=[question_input])
            s3.click(handle_sample_click, inputs=[gr.State("Explain Banker's Algorithm for Deadlock Avoidance")], outputs=[question_input])
            s4.click(handle_sample_click, inputs=[gr.State("Difference between Paging and Segmentation")], outputs=[question_input])
            s5.click(handle_sample_click, inputs=[gr.State("What is Belady's Anomaly in Page Replacement?")], outputs=[question_input])

        # TAB 2: PRACTICE QUIZ GENERATOR
        with gr.Tab("📝 Practice Quiz Generator"):
            with gr.Group(elem_classes=["dashboard-card"]):
                gr.Markdown("### 🎯 Practice Quiz Generator")
                gr.Markdown("Select an OS topic below to generate a 3-question evaluation quiz.")
                
                with gr.Row():
                    quiz_topic_select = gr.Dropdown(
                        choices=TOPIC_CHOICES,
                        value="Processes and Process Management",
                        label="Select OS Topic:"
                    )
                    gen_quiz_btn = gr.Button("🎲 Generate Quiz Session", variant="primary", elem_classes=["primary-btn"])
                    
            quiz_status = gr.Markdown("Click **Generate Quiz Session** to load questions.")
            
            with gr.Group(elem_classes=["dashboard-card"]):
                q1_radio = gr.Radio(choices=[], label="Q1", visible=False)
                q2_radio = gr.Radio(choices=[], label="Q2", visible=False)
                q3_radio = gr.Radio(choices=[], label="Q3", visible=False)
                
                submit_quiz_btn = gr.Button("✅ Submit Answers for Evaluation", variant="primary", visible=False, elem_classes=["primary-btn"])
            
            quiz_result_output = gr.Markdown("", elem_classes=["dashboard-output-box"])
            
            gen_quiz_btn.click(
                fn=handle_generate_quiz,
                inputs=[quiz_topic_select],
                outputs=[q1_radio, q2_radio, q3_radio, quiz_status, submit_quiz_btn]
            )
            
            submit_quiz_btn.click(
                fn=handle_submit_quiz,
                inputs=[q1_radio, q2_radio, q3_radio],
                outputs=[quiz_result_output]
            )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False, css=custom_css, theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate"))

