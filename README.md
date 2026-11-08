# ResearchRAG

A Python learning project for searching scientific papers and building answers with verifiable citations. The goal is to compare dense retrieval, hybrid retrieval, and reranking on the same paper corpus.

## Current progress

The dense retrieval baseline runs in a Jupyter notebook and uses:

- **PyMuPDF** to extract text with PDF page numbers.
- **150-word chunks** with no overlap, kept within page boundaries.
- **Sentence Transformers** (`BAAI/bge-small-en-v1.5`) to embed passages and queries.
- **Chroma** to store embeddings locally and search by cosine similarity.

Results include passage text, paper ID, page number, chunk ID, and similarity score. A small development benchmark compares Chroma with exhaustive cosine search over two papers.

This is an early prototype. The CLI, automated test suite, and answer generation are still planned.

## Setup

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

From the repository root:

```bash
uv sync
uv pip install -e .
mkdir -p data/papers
```

Add your own copies of the PDFs used by the baseline notebook:

```text
data/papers/nemotron3super.pdf
data/papers/attention_is_all_you_need.pdf
```

PDFs and generated indexes are local and are not included in this repository. Use papers you are permitted to access and process. The embedding model downloads on first use.

## Run the baseline

Launch JupyterLab from the experiment directory so the notebook's relative paths resolve correctly:

```bash
cd experiment
uv run --with jupyterlab --with ipykernel jupyter lab
```

Open `01_dense-baseline experiment.ipynb` and run the cells in order. The notebook extracts and chunks both papers, stores embeddings in `data/`, and runs search examples. Its final benchmark section compares the top-three results from Chroma and exhaustive cosine search.

The benchmark uses seven answerable development questions and checks whether a retrieved passage matches the labeled paper and PDF page. This is a preliminary check; it does not establish whether the passage contains all supporting evidence or measure answer quality.

## Project layout

```text
src/researchrag/retrieval.py              # Shared search and collection validation
experiment/01_dense-baseline experiment.ipynb
experiment/02_overlap experiment.ipynb   # Placeholder for the next experiment
data/                                   # Local PDFs and Chroma index (ignored)
```

## Next steps

- Compare chunking with and without overlap.
- Add a runnable CLI, offline tests, and a reproducible benchmark.
- Compare dense retrieval with BM25 and hybrid retrieval using reciprocal rank fusion.
- Add cross-encoder reranking and report retrieval quality and latency.
- Add optional grounded answers with citation validation, followed by optional Hermes integration.
