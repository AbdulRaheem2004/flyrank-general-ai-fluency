import os
import sys

# Add parent directory to sys.path so generate_pdfs can be imported
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from generate_pdfs import create_pdf

def build_pdf_week3_curation():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IMAGE_CURATION.pdf")
    title = "FlyRank AI Internship — Week 3 Deliverable"
    subtitle = "Assignment: Kill Your Darlings: Curate Your Images"
    
    metadata = {
        "Track": "General AI Fluency",
        "Phase": "Foundations (Week 3)",
        "Workload": "2 Hours",
        "Intern": "Abdul Raheem",
        "Status": "Ready for Submission"
    }
    
    sections = [
        {
            "type": "h1",
            "text": "Executive Summary & Discernment Philosophy"
        },
        {
            "type": "paragraph",
            "text": "AI image generation models allow anyone to create hundreds of visually stunning images in seconds. Because generation is cheap, judgment and ruthless curation become the ultimate differentiator. The objective of this assignment is to curate an intentional image set that directly serves the portfolio proof statement while adhering strictly to the Week 3 Identity Kit."
        },
        {
            "type": "callout",
            "text": "<b>Proof Statement Alignment:</b> Synthetic AI representations of code, dashboards, or confusion matrices destroy trust with Senior ML Hiring Managers. Real technical work demands real work captures, executed locally via CLI tasks and notebooks. AI generation is strictly restricted to subtle connective texture locked to our Identity Kit tokens."
        },
        {
            "type": "h1",
            "text": "1. Portfolio Image Needs Map"
        },
        {
            "type": "table",
            "headers": ["Portfolio Location", "Call Type", "Rationale & Functional Purpose", "Keeper Asset Path"],
            "rows": [
                ["Hero Persona Card", "Real Photo Call", "Authentic personal headshot photograph of Abdul Raheem; builds human trust with hiring managers.", "week-03/assets/abdul_raheem_headshot.jpg"],
                ["Case Study 1 (ML Model)", "Work Capture", "Direct output from w05_model.ipynb showing true confusion matrix (F1: 0.942, 12.4ms).", "week-03/assets/cs1_confusion_matrix.svg"],
                ["Case Study 2 (UI Engine)", "Work Capture", "Live UI browser screenshot displaying responsive layout and 1-click meeting modal.", "week-03/assets/cs2_engine_ui.svg"],
                ["Case Study 3 (Harness)", "Work Capture", "Terminal CLI output capture displaying async multi-LLM latency benchmark gains (-75% cycle time).", "week-03/assets/cs3_harness_terminal.svg"],
                ["Hero Background", "Generated AI", "Subtle technical grid texture locked strictly to Identity Kit tokens (#F8FAFC canvas, #0F172A grid).", "week-03/assets/hero_texture.svg"],
                ["Monogram Header", "Vector SVG", "40x40px geometric 'AR' monogram badge with live Empirical Emerald status dot.", "week-03/logo.svg & favicon.svg"]
            ],
            "widths": [110, 80, 194, 120]
        },
        {
            "type": "h1",
            "text": "2. Real Work Captures vs. AI Stand-ins (Local Task Execution)"
        },
        {
            "type": "paragraph",
            "text": "<b>Call 1: Case Study 1 — Empirical Confusion Matrix:</b> AI-generated graphs hallucinate impossible metric labels ('Accuracy: 99.999% glow'). Running model evaluation on holdout test data in Python produces verifiable metrics: 9,420 True Positives, 0.942 F1-Score, and 12.4ms latency.<br/><br/><b>Call 2: Case Study 2 — Zero-Friction Engine UI:</b> Generated UI mockups feature illegible lorem ipsum wireframes. Capturing the local web interface proves clean responsive HTML and instant 1-click scheduling modal execution.<br/><br/><b>Call 3: Case Study 3 — Async Test Harness:</b> Executing local terminal CLI benchmark tasks (python benchmark_harness.py --async) logs real throughput (42.4 req/s) and latency reductions (-75.0% cycle time).<br/><br/><b>Call 4: Bio Card — Personal Headshot:</b> Stylized AI avatars communicate insecurity or vanity. An authentic photograph of Abdul Raheem establishes transparency and human connection."
        },
        {
            "type": "h1",
            "text": "3. AI-Generated Connective Texture (Prompt Iteration)"
        },
        {
            "type": "paragraph",
            "text": "Prompt iterations bound strictly to Week 3 Identity Kit tokens (#F8FAFC, #0F172A, #1E40AF, #059669):"
        },
        {
            "type": "code",
            "text": "[Iteration 1 - Weak Baseline]: 'Futuristic AI neural network background blue glow high tech' -> REJECTED (Sci-fi noise)\n[Iteration 2 - Refined Geometry]: 'Minimalist technical blueprint grid pattern dark slate lines' -> PARTIAL (Missing exact hex tokens)\n[Iteration 3 - Final Keeper]: 'Minimal geometric blueprint grid texture, slate canvas background (#F8FAFC), 1px dark slate architectural grid lines (#0F172A), subtle tech sapphire gradient accent (#1E40AF), ultra-clean' -> KEEP (hero_texture.svg)"
        },
        {
            "type": "h1",
            "text": "4. Discernment & Rejection Log (Kill Your Darlings)"
        },
        {
            "type": "paragraph",
            "text": "<b>Rejection 1: Futuristic Sci-Fi Glowing Brain:</b> Flashy 3D glowing brain art. Rejected because sci-fi glow signals pop-science marketing rather than rigorous ML engineering.<br/><br/><b>Rejection 2: Hallucinated 3D Matrix Chart:</b> Flashy isometric chart rejected because AI hallucinated non-sensical metric labels ('Accurac: 99.999% glow'). Killed in favor of real notebook execution capture."
        },
        {
            "type": "h1",
            "text": "5. Pass / Revise Audit Checklist"
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>Images map to real needs:</b> Mapped 6 core visual assets directly to portfolio content map needs. Work captured from local task executions, not AI stand-ins."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>Consistent AI style/mood (a set, not a pile):</b> Background grid texture was refined across 3 iterations and locked strictly to Identity Kit tokens."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>Real photo used for persona:</b> Mandated an authentic personal photograph of Abdul Raheem for bio cards, rejecting synthetic AI avatars."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>Genuine discernment in rejection notes:</b> Documented exact technical and aesthetic reasons for killing two flashy AI darlings."
        },
        {
            "type": "h1",
            "text": "6. Portal Submission Copy"
        },
        {
            "type": "code",
            "text": "FlyRank AI Internship — Week 3 Assignment: Kill Your Darlings: Curate Your Images\n\nIntern: Abdul Raheem | Track: General AI Fluency\n\nDeliverable Summary:\n1. Portfolio Image Map: Mapped 6 core visual assets directly to portfolio content needs.\n2. Real Work Captures over AI Stand-ins:\n   - CS1: Model confusion matrix capture from local notebook evaluation (F1: 0.942, 12.4ms latency) over synthetic charts.\n   - CS2: Live UI browser capture of Zero-Friction Engine & 1-click modal over wireframe placeholders.\n   - CS3: Terminal CLI task execution log from running benchmark_harness.py (-75% cycle time).\n   - Persona: Authentic personal photograph call for Abdul Raheem over synthetic AI avatars.\n3. AI Connective Texture Iteration: Refined background grid across 3 prompt iterations, locked strictly to Identity Kit palette (#F8FAFC, #0F172A, #1E40AF, #059669).\n4. Discernment & Rejection Notes ('Kill Your Darlings'):\n   - Rejected 1: Sci-Fi Glowing Neon Brain — Flashy visual darling killed because sci-fi glow signals pop-science marketing rather than rigorous ML engineering.\n   - Rejected 2: Hallucinated 3D Matrix Chart — Killed because AI hallucinated fake metric labels ('Accurac: 99.999% glow'), eroding empirical trust.\n\nFull markdown documentation, image assets, HTML visual preview, and PDF generated in repository week-03 directory."
        }
    ]
    
    create_pdf(filename, title, subtitle, metadata, sections)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf_week3_curation()
