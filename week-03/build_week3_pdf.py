import os
import sys

# Add parent directory to sys.path so generate_pdfs can be imported
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from generate_pdfs import create_pdf

def build_pdf_week3():
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IDENTITY_KIT.pdf")
    title = "FlyRank AI Internship — Week 3 Deliverable"
    subtitle = "Assignment: Decide Once: Build Your Identity Kit"
    
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
            "text": "Executive Summary"
        },
        {
            "type": "paragraph",
            "text": "A consistent visual identity is what separates a portfolio that feels intentional from one that feels thrown together. Design consistency comes from making a small set of deliberate decisions once, allowing every page, project card, and ML case study to inherit them automatically."
        },
        {
            "type": "callout",
            "text": "<b>Core Purpose:</b> Establish a minimal, high-precision visual system engineered specifically to showcase production-ready ML models, empirical benchmark data, and clean interactive web interfaces without visual distraction."
        },
        {
            "type": "h1",
            "text": "1. Typography System"
        },
        {
            "type": "paragraph",
            "text": "The identity kit selects two core free fonts (from Google Fonts) plus a dedicated monospaced font strictly for code snippets and empirical benchmark metrics."
        },
        {
            "type": "table",
            "headers": ["Role", "Font Family", "Category", "Usage Rationale"],
            "rows": [
                ["Heading Font", "Plus Jakarta Sans", "Geometric Sans", "Crisp, bold geometric letterforms conveying modern technical authority."],
                ["Body Font", "Inter", "Humanist Sans", "Clean, neutral, high-legibility typeface designed for technical copy & UI."],
                ["Metrics / Code", "JetBrains Mono", "Monospaced", "Monospaced precision font reserved for tabular metrics, F1 scores, and code."]
            ],
            "widths": [90, 110, 100, 204]
        },
        {
            "type": "h1",
            "text": "2. Tight Color Palette (4 Tokens)"
        },
        {
            "type": "paragraph",
            "text": "The palette uses 4 tight, high-contrast colors designed to frame empirical technical work rather than compete with it."
        },
        {
            "type": "table",
            "headers": ["Token Role", "Color Name", "Hex Code", "Visual Purpose & Guardrails"],
            "rows": [
                ["Near-White Bg", "Slate Canvas", "#F8FAFC", "Crisp neutral background; avoids harsh white glare."],
                ["Near-Black Text", "Dark Slate", "#0F172A", "Primary text, headers, and borders for contrast."],
                ["Main Brand", "Tech Sapphire", "#1E40AF", "Anchor brand color for navigation, CTAs, and active states."],
                ["Metric Accent", "Empirical Emerald", "#059669", "Reserved strictly for metric callouts (F1, Accuracy) & live status."]
            ],
            "widths": [100, 100, 80, 224]
        },
        {
            "type": "h1",
            "text": "3. Logo & Favicon Monogram"
        },
        {
            "type": "paragraph",
            "text": "The logo is a clean geometric <b>AR</b> monogram (Abdul Raheem) enclosed in a precision 1.5px border badge with a live status dot indicator."
        },
        {
            "type": "callout",
            "text": "<b>Monogram Specs:</b> 40px × 40px Logo / 32px × 32px Favicon | Border: #0F172A (Dark Slate) | Accent: #059669 (Empirical Emerald status dot) | Typography: Plus Jakarta Sans ExtraBold (800)."
        },
        {
            "type": "h1",
            "text": "4. Two-Line Style Note"
        },
        {
            "type": "code",
            "text": "Fonts: Plus Jakarta Sans (Headings), Inter (Body), JetBrains Mono (Metrics). Palette: #F8FAFC (Bg), #0F172A (Text), #1E40AF (Main), #059669 (Metric Accent).\nMood: Minimal, high-precision technical lab aesthetic designed to let empirical benchmark data and clean interactive ML tools take center stage."
        },
        {
            "type": "h1",
            "text": "5. Pass / Revise Audit Checklist"
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>One or two fonts, not a pile:</b> Selected Plus Jakarta Sans for headings and Inter for body copy (JetBrains Mono for metrics)."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>A tight palette (3-4 colors) with actual hex codes:</b> Defined 4 exact tokens (#F8FAFC, #0F172A, #1E40AF, #059669)."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>A simple logo or favicon exists:</b> Created geometric AR monogram badge with SVG vector files and inline preview."
        },
        {
            "type": "checklist",
            "checked": True,
            "text": "<b>Style note describes a single coherent mood:</b> Two-line style note clearly frames the work with a minimal, high-precision technical lab aesthetic."
        },
        {
            "type": "h1",
            "text": "6. Portal Submission Copy"
        },
        {
            "type": "paragraph",
            "text": "FlyRank AI Internship — Week 3 Assignment: Decide Once: Build Your Identity Kit<br/><br/>Intern: Abdul Raheem | Track: General AI Fluency<br/><br/>Identity Kit Deliverable Summary:<br/>1. Type System: Plus Jakarta Sans (Headings) + Inter (Body) + JetBrains Mono (Metrics & Code).<br/>2. Tight Palette: #F8FAFC (Bg), #0F172A (Text), #1E40AF (Main), #059669 (Metric Accent).<br/>3. Monogram Logo / Favicon: Minimal geometric 'AR' badge with live Emerald status dot indicator.<br/>4. Two-Line Style Note added to AI Tutor prompt & AGENTS.md for full build consistency."
        }
    ]
    
    create_pdf(filename, title, subtitle, metadata, sections)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf_week3()
