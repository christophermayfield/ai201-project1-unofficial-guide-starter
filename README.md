# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
 Prediction market definitions and how they work. Some other documents on addiction and potential threats to democracy.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Prediction Market Accuracy In the Long Run | Describes how well the market performs compared to polls and other forecasting methods | `~/Desktop/Prediction Markets/1-s2.0-S0169207008000320-main.pdf` |
| 2 | Prediction Markets: Practical Experiments in Small Markets and Behaviours Observed | Discusses prediction markets run in 2006 to measure calibration and behaviour in small-scale markets | `~/Desktop/Prediction Markets/418-Article Text-1316-1-10-20121213.pdf` |
| 3 | Prediction Markets: An Extended Literature Review | Reviews the evolution of research on prediction markets | `~/Desktop/Prediction Markets/421-Article Text-1319-1-10-20121213.pdf` |
| 4 | Prediction Markets: An Emerging Form of Gambling? | Discusses prediction markets as a potential new form of gambling | `~/Desktop/Prediction Markets/Addiction - 2025 - Johnson - Prediction markets  An emerging form of gambling.pdf` |
| 5 | Distilling the Wisdom of Crowds | Compares prediction markets and prediction polls for forecasting accuracy | `~/Desktop/Prediction Markets/Atanasov2016PredictionMarketsPolls.pdf` |
| 6 | Using Prediction Markets to Estimate the Reproducibility of Scientific Research | Explores how prediction markets can estimate reproducibility in science | `~/Desktop/Prediction Markets/pnas.201516179.pdf` |
| 7 | Political Prediction Markets: Bad Law, But Good Policy? | Discusses the use of prediction markets in politics and related policy issues | `~/Desktop/Prediction Markets/political_prediction_markets.pdf` |
| 8 | Prediction Markets as a Public Health Threat | Discusses prediction markets as a potential public health and democratic threat | `~/Desktop/Prediction Markets/science.aee3932.pdf` |
| 9 | Who Wins and Who Loses in Prediction Markets? Evidence from Polymarket | Studies trading gains and losses on Polymarket | `~/Desktop/Prediction Markets/ssrn-6443103.pdf` |
| 10 | Statistical Tests of Real-Money vs Play-Money Prediction Markets | Tests statistical differences between real-money and play-money prediction markets | `~/Desktop/Prediction Markets/V16I1_Statistical_Tests_of_Real-Money_versus_Play-Money_Prediction_Markets.pdf` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
1000 tokens
**Overlap:**
100 tokens
**Why these choices fit your documents:**
These documents are relatively short, so this should be a good chunk size.
**Final chunk count:**
187
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->
 all-MiniLM-L6-v2
 This is a good model for this domain because it is a small model that is fast and accurate. I will retrieve 10 chunks per query. This is a good number because it is enough to get the context of the question, but not too many that it is slow. I just don't have a lot of money to spend on this project, so I'm going to stick with the smaller model and retrieve fewer chunks.

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | what are prediction markets? | Prediction markets are a type of market where people can bet on the outcome of an event. | Described prediction markets as markets used for forecasting and structuring uncertainty, but did not explicitly mention betting on event outcomes. | Relevant | Partially accurate |
| 2 | what are the benefits of prediction markets? | Prediction markets can be used to make predictions about the future, and they can be used to make decisions about the future. | Said prediction markets aggregate dispersed information, improve forecast accuracy, and can inform decision-makers and business decisions. | Relevant | Accurate |
| 3 | what are the prediction polls | a version of probability elicitation | Correctly defined prediction polls as a version of probability elicitation where participants submit and update probabilistic forecasts. | Relevant | Accurate |
| 4 | what is the wisdom of crowds? | The wisdom of crowds is the idea that a group of people can make better decisions than a single person because they have more information and more diverse perspectives. | Cited Surowiecki's book title from a bibliography chunk rather than explaining the core idea in plain language. | Partially relevant | Partially accurate |
| 5 | how are prediction markets a potential threat to democracy? | prediction markets are potentialy a threat to democracy because of insider trading risk. | Returned the insufficient-context fallback message instead of identifying insider trading or democratic manipulation risks. | Partially relevant | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

How are prediction markets a potential threat to democracy?

**What the system returned:**

"I could not find enough information in the loaded documents to answer that question."

**Root cause (tied to a specific pipeline stage):**

Retrieval returned chunks from `political_prediction_markets.pdf`, but the top results focused on election forecasting accuracy and legal history rather than democratic threats or insider trading. The relevant insider-trading and democratic-manipulation content exists in other papers (e.g. `science.aee3932.pdf`), but it was not ranked highly enough to pass into the generation context. The generator then correctly refused rather than hallucinating, but the user still did not get the expected answer.

**What you would change to fix it:**

Increase top-k or add query expansion for policy/risk questions, improve PDF text cleaning so semantic matches are stronger, and consider retrieving from papers tagged with political or public-health themes when questions mention democracy or threats.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
