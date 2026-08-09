# FlyRank AI Internship — Week 2 Deliverable: The Prompt Ladder

**Track**: General AI Fluency  
**Phase**: Foundations (Week 2)  
**Workload**: 2 Hours  
**Intern**: Abdul Raheem  
**Status**: Ready for Submission  
**PDF Deliverable**: [PROMPT_LADDER.pdf](file:///e:/Projects/General%20AI%20Fluency/week-02/PROMPT_LADDER.pdf)  

---

## Executive Summary & Voice Card Banner

### Objective
This deliverable demonstrates disciplined prompt engineering through a systematic 5-step ladder process (plus 1 weak baseline prompt). Every iteration adds **exactly one named layer** to solve a specific defect in the output. The evaluation tracks empirical improvements in output quality, identifies honest failure modes (including a prompt change that degraded output quality), and concludes with a production-ready, stranger-reusable prompt template.

### Standing Instruction: Voice Card (6 Words)
> 🎙️ **Voice Card**: `"direct, technical, precise, metrics-driven, zero fluff"`  
> **Rule**: All project framing, copy generation, and case study beats must eliminate corporate buzzwords (*"results-driven"*, *"cutting-edge"*, *"innovative"*, *"seamless"*) and prioritize verifiable empirical data (F1 score, latency ms, benchmark links).

---

## The Prompt Ladder: 6 Iteration Runs

---

### Run 0: Weak Baseline Prompt

#### Baseline Prompt
```text
Help me write portfolio copy for my machine learning project.
```

#### Baseline Output (Full Excerpt)
> *"I am a passionate and results-driven AI developer who created an innovative machine learning project. This cutting-edge application leverages state-of-the-art algorithms to analyze data seamlessly and deliver high-impact results for users. By integrating modern framework best practices, the system optimizes data processing and creates incredible value. Contact me to learn more about my background and skills!"*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: N/A (Original baseline prompt).
2. **What Actually Improved in the Output**: N/A (Establishes baseline). The output is vague, full of corporate marketing fluff, and contains zero technical data.
3. **What Still Failed**: The output is embarrassingly generic. It lacks domain specifics, engineering decisions, performance metrics, target audience context, or any structural formatting.
4. **What I Would Try Next**: Introduce a clear structural goal by mandating a technical 3-beat case study format (Problem, Key Decisions, Outcomes).

---

### Run 1: Version 1 (V1)
**Layer Added**: `1. Clearer Goal`

#### Prompt (V1)
```text
Help me write portfolio copy for my machine learning project. 

Structure it specifically as a technical 3-beat case study consisting of:
1. Beat 1: The Problem
2. Beat 2: What I Did & Key Decisions
3. Beat 3: What Came Of It (Verifiable Outcomes)
```

#### Output Excerpt (V1)
> ***Beat 1: The Problem***  
> *Machine learning projects are often difficult for users to evaluate because they take too long to run and lack clear user interfaces.*  
> 
> ***Beat 2: What I Did & Key Decisions***  
> *I trained a custom vision model and developed a web front-end to showcase the predictions. I optimized the model performance and streamlined the data pipeline.*  
> 
> ***Beat 3: What Came Of It (Verifiable Outcomes)***  
> *The model ran faster, had higher accuracy, and provided an interactive demonstration for anyone visiting the website.*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: Added explicit structural requirements (3-beat case study framework: Problem, Key Decisions, Outcomes).
2. **What Actually Improved in the Output**: The output transformed from a single rambling marketing paragraph into three distinct, structured engineering sections.
3. **What Still Failed**: The text relies entirely on generic placeholders (*"custom vision model"*, *"ran faster"*, *"higher accuracy"*) with zero concrete metrics, frameworks, or empirical data points.
4. **What I Would Try Next**: Supply real context containing specific frameworks, baseline latency, precision metrics, and dataset sizes.

---

### Run 2: Version 2 (V2)
**Layer Added**: `2. Real Context`

#### Prompt (V2)
```text
Help me write portfolio copy for my machine learning project. 

Structure it specifically as a technical 3-beat case study consisting of:
1. Beat 1: The Problem
2. Beat 2: What I Did & Key Decisions
3. Beat 3: What Came Of It (Verifiable Outcomes)

Context:
- Project: PyTorch computer vision model run on FP16 mixed precision.
- Baseline: 5-second boot time Jupyter notebook with high RAM overhead.
- Solution Metrics: Reduced CPU inference latency to 12ms per frame; achieved 0.94 F1 score on 10,000 validation frames.
- Web UI: Built using Vanilla JS/HTML with zero framework dependencies under 100KB payload.
```

#### Output Excerpt (V2)
> ***Beat 1: The Problem***  
> *Standard machine learning projects often stop at Jupyter notebooks that take over 5 seconds to load and consume huge amounts of RAM. This happens because Jupyter notebooks execute Python cells sequentially and load heavy graphical libraries into memory, which causes significant friction for non-technical users who just want to test an ML model.*  
> 
> ***Beat 2: What I Did & Key Decisions***  
> *I trained a computer vision model in PyTorch. I converted the floating point precision from standard FP32 (32-bit floating point) to FP16 mixed precision (16-bit floating point). FP16 is a quantization technique that reduces memory bandwidth requirements by half while maintaining numerical stability. Then I built a web page using basic HTML and Vanilla JavaScript without any external libraries like React or Vue, keeping the code footprint under 100KB.*  
> 
> ***Beat 3: What Came Of It (Verifiable Outcomes)***  
> *The FP16 optimization reduced average inference latency down to 12 milliseconds per frame on CPU. The model achieved a 0.94 F1 score across 10,000 validation image frames.*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: Appended empirical technical context (PyTorch FP16, 5s baseline vs 12ms CPU latency, 0.94 F1, 10k frames, Vanilla JS <100KB UI).
2. **What Actually Improved in the Output**: The output now incorporates concrete technical facts and verifiable metrics (12ms, 0.94 F1, 100KB payload) rather than vague claims ("faster", "accurate").
3. **What Still Failed (⚠️ Honest "This Made It Worse" Moment)**: The LLM assumed an uneducated target reader! It spent half the output defining elementary concepts (*"FP16 is 16-bit floating point...", "React or Vue are external libraries..."*), inflating word count and degrading an engineering case study into an introductory tutorial.
4. **What I Would Try Next**: Define a specific technical audience so the model assumes high technical literacy and stops defining basic computer science terms.

---

### Run 3: Version 3 (V3)
**Layer Added**: `3. Defined Audience`

#### Prompt (V3)
```text
Help me write portfolio copy for my machine learning project. 

Structure it specifically as a technical 3-beat case study consisting of:
1. Beat 1: The Problem
2. Beat 2: What I Did & Key Decisions
3. Beat 3: What Came Of It (Verifiable Outcomes)

Context:
- Project: PyTorch computer vision model run on FP16 mixed precision.
- Baseline: 5-second boot time Jupyter notebook with high RAM overhead.
- Solution Metrics: Reduced CPU inference latency to 12ms per frame; achieved 0.94 F1 score on 10,000 validation frames.
- Web UI: Built using Vanilla JS/HTML with zero framework dependencies under 100KB payload.

Target Audience: Senior Machine Learning Hiring Manager or Staff AI Engineer evaluating technical candidate capabilities.
```

#### Output Excerpt (V3)
> ***Beat 1: The Problem***  
> *Standard ML portfolio projects often stop at Jupyter notebooks or rely on bloated web dashboards with 5+ second boot times and high resource overhead. This creates friction for senior engineers attempting to verify real-time performance and model robustness.*  
> 
> ***Beat 2: What I Did & Key Decisions***  
> *To eliminate overhead, I trained an end-to-end PyTorch vision model utilizing FP16 mixed precision, balancing memory footprint with precision. I replaced heavy web frameworks with a lightweight Vanilla JS/HTML interface styled with raw CSS variables, maintaining client-side payload under 100KB.*  
> 
> ***Beat 3: What Came Of It (Verifiable Outcomes)***  
> *Achieved an F1 score of 0.94 on 10,000 validation frames, reduced average CPU inference latency to 12ms per frame, and delivered a seamless interactive user experience paired with benchmark results.*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: Defined the target persona as a Senior ML Hiring Manager / Staff AI Engineer.
2. **What Actually Improved in the Output**: The model completely stopped explaining elementary concepts (FP16, CPU, JS libraries), shifting tone to peer-level engineering communication.
3. **What Still Failed**: It reintroduced corporate fluff (*"end-to-end vision model"*, *"seamless interactive user experience"*) and presented decisions in long, dense paragraphs rather than scannable bullet points.
4. **What I Would Try Next**: Enforce negative constraints banning buzzwords and mandating bullet points for Beat 2.

---

### Run 4: Version 4 (V4)
**Layer Added**: `4. Constraints`

#### Prompt (V4)
```text
Help me write portfolio copy for my machine learning project. 

Structure it specifically as a technical 3-beat case study consisting of:
1. Beat 1: The Problem
2. Beat 2: What I Did & Key Decisions
3. Beat 3: What Came Of It (Verifiable Outcomes)

Context:
- Project: PyTorch computer vision model run on FP16 mixed precision.
- Baseline: 5-second boot time Jupyter notebook with high RAM overhead.
- Solution Metrics: Reduced CPU inference latency to 12ms per frame; achieved 0.94 F1 score on 10,000 validation frames.
- Web UI: Built using Vanilla JS/HTML with zero framework dependencies under 100KB payload.

Target Audience: Senior Machine Learning Hiring Manager or Staff AI Engineer evaluating technical candidate capabilities.

Constraints:
- Strictly enforce a 6-word Voice Card: "direct, technical, precise, metrics-driven, zero fluff".
- Banned Buzzwords: "seamless", "innovative", "cutting-edge", "end-to-end", "impactful", "leveraging".
- Format: Beat 2 must be formatted as 3 bullet points. Keep Beat 1 under 40 words.
```

#### Output Excerpt (V4)
> ***Beat 1: The Problem***  
> *Standard ML portfolios stop at Jupyter notebooks or heavy dashboards with 5+ second boot times. Technical reviewers require fast verification of inference accuracy without cloning bloated repositories.*  
> 
> ***Beat 2: What I Did & Key Decisions***  
> *- Trained PyTorch vision model using FP16 mixed precision to cut memory bandwidth while maintaining numerical precision.*  
> *- Replaced web frameworks with Vanilla JS/HTML interface styled with raw CSS, keeping client bundle under 100KB.*  
> *- Published explicit error distribution analyses and precision/recall trade-off curves in benchmark notebooks.*  
> 
> ***Beat 3: What Came Of It (Verifiable Outcomes)***  
> *- Achieved F1 score of 0.94 on 10,000 validation frames.*  
> *- Reduced average CPU inference latency to 12ms per frame.*  
> *- Delivered interactive visual demo paired with benchmark notebook.*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: Enforced 6-word Voice Card, explicitly banned generic corporate buzzwords, limited word count, and mandated bulleted formatting.
2. **What Actually Improved in the Output**: Corporate fluff was completely purged. Sentences became active, technical, and immediately scannable for a busy recruiter or engineering lead.
3. **What Still Failed**: Beat 3 claims empirical metrics (0.94 F1, 12ms latency), but does not reference specific repository files or reproducible benchmark notebook paths.
4. **What I Would Try Next**: Add verification requirements mandating that all outcome claims link directly to verifiable repository artifacts.

---

### Run 5: Version 5 (V5)
**Layer Added**: `5. Verification Requirements`

#### Prompt (V5)
```text
Help me write portfolio copy for my machine learning project. 

Structure it specifically as a technical 3-beat case study consisting of:
1. Beat 1: The Problem
2. Beat 2: What I Did & Key Decisions
3. Beat 3: What Came Of It (Verifiable Outcomes)

Context:
- Project: PyTorch computer vision model run on FP16 mixed precision.
- Baseline: 5-second boot time Jupyter notebook with high RAM overhead.
- Solution Metrics: Reduced CPU inference latency to 12ms per frame; achieved 0.94 F1 score on 10,000 validation frames.
- Web UI: Built using Vanilla JS/HTML with zero framework dependencies under 100KB payload.

Target Audience: Senior Machine Learning Hiring Manager or Staff AI Engineer evaluating technical candidate capabilities.

Constraints:
- Strictly enforce a 6-word Voice Card: "direct, technical, precise, metrics-driven, zero fluff".
- Banned Buzzwords: "seamless", "innovative", "cutting-edge", "end-to-end", "impactful", "leveraging".
- Format: Beat 2 must be formatted as 3 bullet points. Keep Beat 1 under 40 words.

Verification Requirements:
- Every outcome metric in Beat 3 MUST be explicitly paired with a verifiable repository artifact link (e.g., [Model Notebook w05_model.ipynb], [Baseline Notebook w04_baseline_score.ipynb], [Live Demo UI index.html]).
```

#### Output Excerpt (V5)
> ***Beat 1: The Problem***  
> *Standard ML portfolios stop at Jupyter notebooks or heavy dashboards with 5+ second boot times. Technical reviewers require fast verification of inference accuracy without cloning bloated repositories.*  
> 
> ***Beat 2: What I Did & Key Decisions***  
> *- Trained PyTorch vision model using FP16 mixed precision to cut memory bandwidth while maintaining numerical precision.*  
> *- Replaced web frameworks with Vanilla JS/HTML interface styled with raw CSS, keeping client bundle under 100KB.*  
> *- Published explicit error distribution analyses and precision/recall trade-off curves in benchmark notebooks.*  
> 
> ***Beat 3: What Came Of It (Verifiable Outcomes)***  
> *- Achieved **F1 score of 0.94** on 10,000 validation frames [[Model Notebook w05_model.ipynb](file:///e:/Projects/General%20AI%20Fluency/capstone-ai-os/work/notebooks/w05_model.ipynb)].*  
> *- Reduced average CPU inference latency to **12ms per frame** [[Baseline Notebook w04_baseline_score.ipynb](file:///e:/Projects/General%20AI%20Fluency/capstone-ai-os/work/notebooks/w04_baseline_score.ipynb)].*  
> *- Delivered interactive visual demo under 100KB payload paired with benchmark code [[Live Demo UI index.html](file:///e:/Projects/General%20AI%20Fluency/capstone-ai-os/work/index.html)].*

#### Four Evaluation Notes
1. **What Changed in the Prompt**: Added verification requirements mandating direct artifact links for all outcome claims.
2. **What Actually Improved in the Output**: Every performance metric is now anchored to an explicit, verifiable repository artifact, converting standard resume assertions into proof-backed evidence.
3. **What Still Failed**: None. The output meets all quality criteria, adheres to the Voice Card, targets the exact persona, and delivers zero-fluff proof.
4. **What I Would Try Next**: Clean up and parameterize into a reusable prompt template for any intern on the FlyRank AI track.

---

## Comparative Output Analysis Matrix

| Version | Layer Added | Output Quality Score | Primary Output Defect | Key Output Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | None (Original) | 1 / 10 | 100% corporate fluff; zero technical metrics. | Established weak starting point. |
| **V1** | 1. Clearer Goal | 3 / 10 | Generic placeholders ("ran faster", "high accuracy"). | Organized text into 3 logical engineering beats. |
| **V2** | 2. Real Context | 4 / 10 | ⚠️ **Degraded**: LLM patronized reader by defining basic CS terms. | Cites real numbers (12ms latency, 0.94 F1 score). |
| **V3** | 3. Defined Audience | 6 / 10 | Contained soft corporate adjectives & dense text blocks. | Eliminated elementary definitions; targeted peer engineer. |
| **V4** | 4. Constraints | 8 / 10 | Outcome metrics lacked verifiable repository links. | Purged all fluff; formatted into scannable bullet points. |
| **V5** | 5. Verification | 10 / 10 | None. Production-ready deliverable. | Paired all outcome claims with verifiable artifact links. |

---

## Final Reusable Prompt Template

*Cleaned up and parameterized so any AI intern or peer engineer can execute it without assistance:*

```markdown
# Role & Goal
You are an expert AI/ML Technical Portfolio Editor. Draft a 3-beat technical case study for an engineering project based on the input data provided below.

# Input Project Parameters
- Project Name: [Insert Project Name]
- Core Tech Stack: [e.g., PyTorch FP16, Vanilla JS, FastAPI, Docker]
- Baseline Problem & Friction: [e.g., 5-second boot time Jupyter notebook with high RAM overhead]
- Key Technical Decisions: [Insert 2-3 key architecture or optimization decisions made]
- Verifiable Metrics: [e.g., 12ms CPU latency per frame, 0.94 F1 score on 10k validation frames]
- Proof Artifact Links: [e.g., w05_model.ipynb, w04_baseline_score.ipynb]

# Target Audience
Senior Machine Learning Hiring Manager or Staff AI Engineer evaluating technical candidate capabilities.

# Structure & Format
- Beat 1: The Problem (Max 40 words. Focus on engineering friction for technical reviewers).
- Beat 2: What I Did & Key Decisions (Exactly 3 bullet points focusing on trade-offs and execution).
- Beat 3: What Came Of It (Verifiable Outcomes) (Bulleted list of empirical outcomes paired with artifact links).

# Constraints (Voice Card)
- Enforce Voice Card: "direct, technical, precise, metrics-driven, zero fluff".
- Banned Words: "seamless", "innovative", "cutting-edge", "end-to-end", "impactful", "leveraging", "results-driven", "synergy".
- Do NOT define basic technical concepts (e.g., FP16, CPU, API, RAM). Assume senior engineering literacy.

# Verification Rule
- Every metric cited in Beat 3 MUST be explicitly paired with a bracketed proof artifact link from the Input Project Parameters.
```

---

## Pass / Revise Criteria Checklist

- [x] **Six Runs Total**: Baseline plus 5 versions (V1 through V5).
- [x] **Single Named Layer Per Version**:
  - V1: `Clearer Goal`
  - V2: `Real Context`
  - V3: `Defined Audience`
  - V4: `Constraints`
  - V5: `Verification Requirements`
- [x] **Notes Describe Output Changes**: All evaluation notes focus on empirical output results rather than restating prompt edits.
- [x] **Honest "This Made It Worse" Moment**: Documented in V2 where adding technical context caused the LLM to patronize the reader with basic definitions.
- [x] **Stranger-Reusable Final Prompt**: Cleaned up into a parameterized Markdown template ready for independent execution.
