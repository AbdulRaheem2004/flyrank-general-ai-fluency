# FlyRank AI Internship — Week 3 Deliverable

**Assignment:** Decide Once: Build Your Identity Kit  
**Track:** General AI Fluency  
**Phase:** Foundations (Week 3)  
**Workload:** 2 Hours  
**Intern:** Abdul Raheem  
**Status:** Complete & Ready for Submission  

---

## Executive Summary & Why It Matters

A consistent visual identity is what separates a portfolio that feels intentional from one that feels thrown together. Design consistency comes from making a small set of deliberate decisions once, allowing every page, project card, and ML case study to inherit them automatically.

This identity kit establishes a minimal, high-precision visual system engineered specifically to showcase production-ready ML models, empirical benchmark data, and clean interactive web interfaces without visual clutter.

---

## 1. Typography System

The identity kit selects **two core free fonts** (from Google Fonts) plus a dedicated monospaced font strictly for code snippets and empirical benchmark metrics.

| Role | Font Family | Category | Spec & Usage Rationale |
| :--- | :--- | :--- | :--- |
| **Heading Font** | `Plus Jakarta Sans` | Modern Sans-Serif (Geometric) | Crisp, bold geometric letterforms that convey modern technical authority for section titles, project names, and headers. |
| **Body Font** | `Inter` | Humanist Sans-Serif | Clean, neutral, high-legibility typeface designed for long-form technical readouts, case study prose, and UI controls. |
| **Metrics / Code** | `JetBrains Mono` | Monospaced | Monospaced precision font reserved for tabular metrics, F1 scores, latency (ms), hyperparameter logs, and code blocks. |

### Type Hierarchy
- **H1 (Hero / Page Title)**: Plus Jakarta Sans, 32px / 2.25rem, Bold (700), Tracking -0.02em
- **H2 (Section Header)**: Plus Jakarta Sans, 24px / 1.5rem, SemiBold (600), Tracking -0.01em
- **H3 (Card Header)**: Plus Jakarta Sans, 18px / 1.125rem, Medium (500)
- **Body / Prose**: Inter, 16px / 1rem, Regular (400), Line-height 1.6
- **Caption / Meta**: Inter, 13px / 0.8125rem, Regular (400), Slate 500
- **Data / Metrics**: JetBrains Mono, 14px / 0.875rem, Medium (500), Emerald 600

---

## 2. Tight Color Palette (4 Primary Tokens)

The palette uses **4 tight, high-contrast colors** designed to frame empirical technical work rather than compete with it.

| Token Role | Color Name | Hex Code | RGB Code | Visual Purpose & Guardrails |
| :--- | :--- | :--- | :--- | :--- |
| **Near-White Background** | Slate Canvas | `#F8FAFC` | `rgb(248, 250, 252)` | Crisp, neutral laboratory background; avoids harsh `#FFFFFF` glare while maintaining maximum contrast. |
| **Near-Black Text** | Dark Slate | `#0F172A` | `rgb(15, 23, 42)` | Primary text, titles, and borders; high-contrast legibility without absolute black hardness. |
| **Main / Primary Brand** | Tech Sapphire | `#1E40AF` | `rgb(30, 64, 175)` | Anchor brand color for primary CTA buttons, active state indicators, and key navigational elements. |
| **Metric Accent** | Empirical Emerald | `#059669` | `rgb(5, 150, 105)` | Reserved strictly for metric callouts (e.g., F1 scores, Accuracy %), verified status badges, and benchmark gains. |

*(Secondary Muted Neutral: `#64748B` Slate 500 for borders, metadata labels, and subtle divider lines).*

---

## 3. Logo & Favicon Monogram

### Concept & Design Rationale
The logo is a clean geometric **AR** monogram (Abdul Raheem) enclosed in a precision 1px border badge with a status dot indicator. It communicates precision engineering, minimal friction, and zero fluff.

### Monogram Specifications
- **Dimensions**: 40px × 40px (Logo), 32px × 32px (Favicon)
- **Border**: 1.5px solid `#0F172A` (Dark Slate) with 8px corner radius (`rounded-lg`)
- **Typography**: Plus Jakarta Sans, ExtraBold (800), Uppercase
- **Accent**: 6px `#059669` (Empirical Emerald) live status indicator dot in top-right

### SVG Markup (Logo)
```xml
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="38" height="38" rx="8" fill="#F8FAFC" stroke="#0F172A" stroke-width="2"/>
  <text x="11" y="26" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="16" fill="#0F172A" letter-spacing="-0.5">AR</text>
  <circle cx="31" cy="9" r="3.5" fill="#059669" stroke="#F8FAFC" stroke-width="1.5"/>
</svg>
```

### SVG Markup (Favicon)
```xml
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="32" height="32" rx="6" fill="#0F172A"/>
  <text x="7" y="21" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="14" fill="#F8FAFC" letter-spacing="-0.5">AR</text>
  <circle cx="25" cy="7" r="3" fill="#059669"/>
</svg>
```

---

## 4. Two-Line Style Note

This two-line style note is added directly to custom AI instructions (`AGENTS.md` and Claude Project context) to ensure all future UI generation, portfolio components, and case study builds remain strictly on-brand:

```text
Fonts: Plus Jakarta Sans (Headings), Inter (Body), JetBrains Mono (Metrics). Palette: #F8FAFC (Bg), #0F172A (Text), #1E40AF (Main), #059669 (Metric Accent).
Mood: Minimal, high-precision technical lab aesthetic designed to let empirical benchmark data and clean interactive ML tools take center stage.
```

---

## 5. Pass / Revise Audit Checklist

- [x] **One or two fonts, not a pile:** Selected `Plus Jakarta Sans` for headings and `Inter` for body copy (`JetBrains Mono` reserved for monospaced metrics).
- [x] **Tight palette (≈3–4 colors) with actual hex codes:** Defined 4 exact tokens (`#F8FAFC`, `#0F172A`, `#1E40AF`, `#059669`).
- [x] **A simple logo or favicon exists:** Created geometric `AR` monogram badge with SVG vector files and inline preview.
- [x] **Style note describes a single, coherent mood:** Two-line style note clearly frames the work with a minimal, high-precision technical lab aesthetic.

---

## 6. Track Thread Submission Text

```text
FlyRank AI Internship — Week 3 Assignment: Decide Once: Build Your Identity Kit

Intern: Abdul Raheem
Track: General AI Fluency

Identity Kit Deliverable Summary:
1. Type System: Plus Jakarta Sans (Headings) + Inter (Body) + JetBrains Mono (Metrics & Code).
2. Tight Palette:
   - Near-White Background: #F8FAFC
   - Near-Black Text: #0F172A
   - Main Brand: #1E40AF (Tech Sapphire)
   - Metric Accent: #059669 (Empirical Emerald)
3. Monogram Logo / Favicon: Minimal geometric 'AR' badge with live Emerald status dot indicator.
4. Two-Line Style Note:
   Fonts: Plus Jakarta Sans (Headings), Inter (Body), JetBrains Mono (Metrics). Palette: #F8FAFC (Bg), #0F172A (Text), #1E40AF (Main), #059669 (Metric Accent).
   Mood: Minimal, high-precision technical lab aesthetic designed to let empirical benchmark data and clean interactive ML tools take center stage.

Full deliverable docs, interactive HTML preview, and PDF generated in repository week-03 directory.
```
