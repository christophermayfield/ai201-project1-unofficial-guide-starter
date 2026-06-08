# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I picked the domain of prediction markets, which are a type of market where people can bet on the outcome of an event.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Predction Market Accuracy In the Long Run | Describes how well the market does as opposed to other things | Current WD |
| 2 |PREDICTION MARKETS: PRACTICAL
EXPERIMENTS IN SMALL MARKETS AND
BEHAVIOURS OBSERVED | This paper discusses a series of prediction markets created and operated in the summer of 2006 to
measure calibration and behaviour of small-scale prediction markets| Current WD |
| 3 | PREDICTION MARKETS: AN EXTENDED
LITERATURE REVIEW| This paper presents an attempt to study and monitor the evolution of research on prediction markets
(PM).| Current WD |
| 4 |Prediction markets: An emerging form of gambling? |We write to direct the readership to a potential new form of
gambling: prediction markets. | Current WD |
| 5 | Distilling the Wisdom of Crowds | This paper discusses the wisdom of crowds and how it can be used to make predictions | Current WD |
| 6 | Using prediction markets to estimate the
reproducibility of scientific research| Discuses the lack of reproducibility of scientific research and how prediction markets can be used to estimate it | Current WD |
| 7 |POLITICAL PREDICTION MARKETS:
BAD LAW, BUT GOOD POLICY? | This paper discusses the use of prediction markets in politics | Current WD |
| 8 | Prediction markets as a public health threat| This paper discusses the use of prediction markets in public health | Current WD |
| 9 | Who Wins and Who Loses In Prediction Markets?
Evidence from Polymarket∗|study trading gains and losses on Polymarket, the world’s largest prediction market
platform. | Current WD |
| 10 | Statistical Tests of real-money vs play-money prediction markets | | |

---

## Chunking Strategy


 I will chunk the documents into 1000 token chunks with 100 token overlap. These documents are relatively short, so this should be a good chunk size.

**Chunk size:** 1000 tokens

**Overlap:** 100 tokens

**Reasoning:** This should be a good chunk size for the documents.

**Final chunk count:** 187

---

## Retrieval Approach


 I will use the all-MiniLM-L6-v2 embedding model. This is a good model for this domain because it is a small model that is fast and accurate. I will retrieve 10 chunks per query. This is a good number because it is enough to get the context of the question, but not too many that it is slow.

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:**
10
**Production tradeoff reflection:**
If I were deploying this for real users and cost wasn't a constraint, I would use a larger model and retrieve more chunks. This would be more accurate, but it would also be slower and more expensive. I just don't have a lot of money to spend on this project, so I'm going to stick with the smaller model and retrieve fewer chunks.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | what are prediction markets?| Prediction markets are a type of market where people can bet on the outcome of an event. |
| 2 | what are the benefits of prediction markets? | Prediction markets can be used to make predictions about the future, and they can be used to make decisions about the future. |
| 3 | what are the prediction polls| a version of probability elicitation|
| 4 | what is the wisdom of crowds? | The wisdom of crowds is the idea that a group of people can make better decisions than a single person because they have more information and more diverse perspectives. |
| 5 | how are prediction markets a potential threat to democracy?| prediction markets are potentialy a threat to democracy because of insider trading risk. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. noisy or inconsistent documents

2. potential chunks that split key information across boundaries

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->


---

┌─────────────────────────────────────────────────────────────┐
│                    RAG SYSTEM ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────┘


INDEXING PHASE
==============

    ┌─────────────────────┐
    │ Document Sources    │
    │ - PDFs              │
    │ - Text Files        │
    │ - Web Documents     │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Document Ingestion  │
    │ Load documents      │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │ Chunking                            │
    │ Function: chunk_text()              │
    │ Chunk Size: 1000 tokens             │
    │ Overlap: 100 tokens                 │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Text Chunks         │
    │ [chunk_1]           │
    │ [chunk_2]           │
    │ [chunk_n]           │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │ Embedding Model                     │
    │ all-MiniLM-L6-v2                    │
    │ Convert text → vectors              │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Vector Store        │
    │ Store embeddings    │
    │ + source chunks     │
    └─────────────────────┘



QUERY PHASE
===========

                         ┌─────────────────────┐
                         │ User Question       │
                         └──────────┬──────────┘
                                    │
                                    ▼
    ┌─────────────────────┐  similarity search
    │ Vector Store        │────────────────────┐
    └──────────┬──────────┘                    │
               │                               │
               ▼                               ▼
    ┌─────────────────────────────────────┐
    │ Retrieval                           │
    │ Find most relevant chunks           │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Retrieved Chunks    │
    │ Context Documents   │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │ Generation                          │
    │ LLM receives:                       │
    │ 1. User Question                    │
    │ 2. Retrieved Chunks                 │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Final Response      │
    │ Grounded Answer     │
    └─────────────────────┘



END-TO-END FLOW
===============

Documents
    │
    ▼
Document Ingestion
    │
    ▼
Chunking
(1000 tokens, 100 overlap)
    │
    ▼
Embedding
(all-MiniLM-L6-v2)
    │
    ▼
Vector Store
    ▲
    │
User Question
    │
    ▼
Retrieval
    │
    ▼
Relevant Chunks
    │
    ▼
Generation (LLM)
    │
    ▼
Response



## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

     I will use Claude and Cursor to help me code. I will give Claude the planning.md file and ask it to implement the code. I will then give Cursor the code and ask it to help me debug the code. I expect it to make some mistakes, but I will be able to fix them. I'll review the spec to make sure I'm not missing anything and that the model is doing what I want it to do. i'll start with the ingestion and chunking stage and then move on to the embedding and retrieval stage and then the generation stage. Further, I'll use the requirements.txt file to install the dependencies and the .env file to store the API keys. I'll start with chunk_text() and go from there. 


**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
