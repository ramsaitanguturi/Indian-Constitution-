# Constitution RAG Agent - Development Instructions


## Project Vision

Build an AI-powered Constitutional Law assistant.

The system accepts a real-world legal problem and provides:

1. Relevant Constitutional Articles
2. Applicable clauses
3. Fundamental rights involved
4. Related Supreme Court judgments
5. Legal reasoning
6. Possible verdict/outcome


Example:

Input:

"Can government stop a peaceful protest?"

Output:

Article:
Article 19 - Freedom of Speech and Expression

Related Cases:
- Shreya Singhal v Union of India

Reasoning:
Restrictions must satisfy constitutional limitations.



Possible Verdict:
Government action may be unconstitutional if unreasonable.


---

# Core Architecture


The system must use:


## 1. Hierarchical Parent-Child RAG


Documents should not be stored as simple chunks.


Structure:


Parent Document:

Article 21

    |
    |
    Child Documents:

    - Clause explanation
    - Important cases
    - Examples
    - Interpretations



Retrieval Process:


User Query

↓

Find relevant Parent Article

↓

Retrieve child chunks

↓

Generate response



Benefits:

- Better context
- Higher retrieval accuracy
- Less hallucination



---


# 2. Agentic RAG


Implement multi-agent architecture.


Agents:


## Router Agent

Purpose:

Understand query and decide workflow.


Example:

User asks:

"Police searched my house without warrant"


Router identifies:

Category:
Personal liberty


Agents required:

- Constitution Agent
- Case Law Agent
- Reasoning Agent



---


## Constitution Agent


Responsibilities:

Retrieve:

- Articles
- Clauses
- Fundamental Rights



---


## Case Law Agent


Responsibilities:


Retrieve:

- Supreme Court cases
- Important judgments
- Legal principles



---


## Reasoning Agent


Responsibilities:

Connect:

User problem

+

Constitution articles

+

Case laws


Generate explanation.



---


## Verdict Agent


Responsibilities:

Generate:

- Possible judgement
- Supporting reasons
- Confidence score


Never provide fake certainty.


---

# Technology Requirements


Backend:

Python
FastAPI


AI Framework:

LangChain/LangGraph


Embedding:

Sentence Transformers


Vector Database:

ChromaDB initially


LLM:

OpenAI API

or

Open-source models


Frontend:

React

Tailwind CSS



Deployment:

Frontend:
Vercel


Backend:
Render


---

# Development Rules


Before coding:

1. Understand existing markdown documentation.
2. Improve architecture if required.
3. Update documentation after major decisions.
4. Keep code modular.
5. Write clean production-style code.


---

# Required Folder Structure


Final structure:


backend/

    app/

        agents/

        rag/

        database/

        api/

        models/


frontend/

    src/

        components/

        pages/

        services/


data/

    raw/

    processed/


tests/


---

# Implementation Priority


Do not build everything simultaneously.


Follow phases:

Phase 1:
Basic RAG prototype


Phase 2:
Parent-child retrieval


Phase 3:
Agentic workflow


Phase 4:
Frontend


Phase 5:
Deployment


---

# Quality Requirements


The system should:

- Explain answers
- Show retrieved sources
- Avoid hallucination
- Give confidence level
- Be deployable