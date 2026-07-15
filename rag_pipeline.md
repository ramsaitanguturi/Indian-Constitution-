# RAG Pipeline


## Data Loading


Sources:

- Indian Constitution PDF
- Supreme Court Judgments
- Legal explanations


Process:


PDF

↓

Text extraction

↓

Cleaning

↓

Parent creation

↓

Child chunk creation

↓

Embedding

↓

Vector Database



## Parent Child Example


Parent:

Article 19


Children:


19(1)(a)

Freedom of speech


19(2)

Reasonable restrictions


Cases:

Shreya Singhal Case



## Retrieval


Step 1:

Search parents


Step 2:

Retrieve children


Step 3:

Send context to LLM


Step 4:

Generate answer
