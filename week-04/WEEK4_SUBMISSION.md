# Assignment: Three Roads: Choose Your Stack with AI

> **Student Name**: Abdul Raheem  
> **Program**: FlyRank AI Internship (Week 4)  
> **Proof Statement**: *"I build production-ready ML/AI systems with verifiable performance metrics, benchmark notebooks, and clean visual web interfaces."*  
> **Live URL**: [https://abdulraheem-ai.netlify.app/](https://abdulraheem-ai.netlify.app/)  
> **Voice Card**: `direct, technical, precise, metrics-driven, zero fluff`  

---

## 1. The Four Input Constraints

1. **Free Only**: $0 hosting budget. Must run on zero-cost public hosting tiers (Netlify free tier).
2. **Honest Skill Level**: Intermediate proficiency in HTML5, CSS3, and JavaScript logic. Prefer to focus technical bandwidth on ML model benchmarks, inference pipelines, and empirical data rather than debugging web build tools or package managers.
3. **Portfolio Purpose & Sitemap**:
   - Single target action: Senior ML Hiring Manager books a 15-minute Technical Intro Chat.
   - Sitemap: 1-Page architecture featuring Hero Proof Claim, ML Case Study 1 (F1: 0.942 / 12ms latency), UI Case Study 2 (Zero-Friction Engine), Async Multi-LLM Harness Case Study 3, and Footer CTA.
4. **Work Display Requirements**:
   - Benchmark performance cards (JetBrains Mono metrics).
   - Embedded interactive ML demos (via Hugging Face Spaces / Modal / iframe).
   - Verifiable GitHub code repository links & Jupyter notebook evaluation runs.
   - Clean, technical long-form reading layout (`Inter` + `Plus Jakarta Sans`).
5. **Backend Status**: **Not yet.** Interactive ML models run on dedicated external inference servers (Hugging Face / Modal). The portfolio site itself requires zero dynamic backend logic, database connections, or server-side state.

---

## 2. Three Stack Options (Simplest to Most Powerful)

| Parameter | Option A: Simplest (Chosen) | Option B: Balanced | Option C: Most Powerful |
| :--- | :--- | :--- | :--- |
| **Stack** | **Vanilla HTML5 + Vanilla CSS + JS** | **Vite + React / Astro** | **Next.js (App Router)** |
| **How to Build** | Write raw semantic HTML & CSS; organize into clean modular files. | Build component tree (`.jsx` / `.astro`); run `npm run build` static output bundle. | Full-stack React app with App Router, server components, and route handlers. |
| **Where to Host (Free)** | Netlify Free Tier (Direct Drag-and-Drop or basic Git push). | Netlify Free Tier (Automated Git build pipeline). | Netlify / Vercel Free Tier (Serverless Node runtime). |
| **Needs Backend?** | **No.** 100% static asset serving. | **No.** Static site generation (SSG) output. | **Optional.** Offers API routes, but unnecessary for this site. |
| **Real Trade-off** | Repeating common layout structures (headers/footers) across HTML files manually. | Must manage Node.js versions, `package.json`, and Vite build configuration. | High complexity tax: hydration errors, SSR configuration, node package vulnerabilities. |
| **Deploy Build Time** | **0 seconds** (Instant static serve). | **15–45 seconds** per deployment. | **45–120 seconds** per deployment. |

---

## 3. Pressure-Testing the Front-Runner (Option A)

* **What breaks if I pick the simplest (Option A)?**
  Nothing breaks technically. The only friction is maintaining duplicated navigation header/footer markup across multiple HTML files if expanded beyond a single page. For a focused 1-page portfolio, this trade-off costs zero runtime overhead and has zero failure points.

* **What do I maintain if I pick the most powerful (Option C)?**
  I would maintain a heavy `node_modules` dependency tree, framework updates (React 19 / Next 15 breaking changes), serverless function quotas, and hydration mismatches. Every minute spent fixing a broken Node package is a minute lost training ML models or polishing benchmark metrics.

* **Can I finish in two weeks?**
  **Yes.** With Option A, there is zero setup time, zero configuration overhead, and zero build debugging. I can spend 100% of the remaining 2 weeks writing clean semantic markup, embedding interactive model benchmarks, and refining case study copy.

* **Does it show my work the way it needs to be shown?**
  **Yes, perfectly.** High-precision ML metrics, SVG confusion matrices, interactive Hugging Face demo embeds, and GitHub repo links render faster and cleaner in raw semantic HTML5 than inside heavy client-side JavaScript frameworks.

---

## 4. Written Rationale

> **Chosen Stack**: Option A — Vanilla HTML5, Vanilla CSS3, Vanilla JS.  
> **Discarded Alternatives**: 
> 1. *Option B (Vite + React/Astro)*: Rejected because adding an `npm build` pipeline for a 1-page metric portfolio adds unnecessary build complexity without improving user experience.
> 2. *Option C (Next.js App Router)*: Rejected because server-side rendering, hydration, and API routes are completely irrelevant for a static ML portfolio.  
> 
> **Can I maintain this?**  
> Yes. Option A has **zero maintenance debt**. There are no framework dependencies to update, no lockfile conflicts, and no build pipeline failures. Updating the site requires editing HTML/CSS directly with zero risk of breaking third-party packages.
> 
> **Does it show my work well?**  
> Yes. It lets empirical benchmark data take center stage without client-side render lag. By embedding Hugging Face models via lightweight iframes and displaying metrics in high-contrast monospace typographic badges (`JetBrains Mono`), the hiring manager sees verifiable performance instantly.
> 
> **Backend Answer**: Currently, **not yet**. The site serves zero server-side logic; model inference is delegated to external specialized hosts.

---

## 5. Live Milestone Proof

* **Live URL**: [https://abdulraheem-ai.netlify.app/](https://abdulraheem-ai.netlify.app/)
* **Second-Device Test**: Verified on mobile device (HTTP 200 OK).
* **Workspace Status**: Identity Kit, Case Studies, and Content Map are fully loaded for Week 5 build.
