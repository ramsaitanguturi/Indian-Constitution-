# System Architecture


## High Level Flow


User Question

↓

Legal Agent

↓

Query Understanding Agent

↓

Retriever Agent

↓

Parent Document Retrieval

↓

Child Chunk Retrieval

↓

Reasoning Agent

↓

Answer Generator


## Components


## 1. Query Agent

Purpose:

Understand user problem.


Example:

Input:

"Police arrested someone without warrant"


Extract:

Issue:
Illegal arrest


Keywords:

- Article 21
- Personal liberty
- Criminal procedure


---


## 2. Hierarchical RAG


Instead of storing only chunks:


Parent:

Article 21

    |
    |
Children:

    Clause explanation

    Important judgments

    Examples


Retrieval:

First find parent.

Then search children.


Advantages:

- Better context
- Less hallucination
- More accurate answers


---


## 3. Agentic Layer


Agents:


Research Agent

Find relevant articles.


Case Agent

Find court judgments.


Reasoning Agent

Analyze situation.


Judge Agent

Generate possible verdict.
