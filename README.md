## Feature Evaluator

A small utility to crawl an article page and extract feature-quality signals using Crawl4AI’s dynamic crawling and LLM-powered content extraction. We use Crawl4AI for:
- dynamic crawling with a headless browser (robust to JS-heavy sites),
- built-in content cleaning/normalization (HTML → clean text/markdown),
- LLM-based extraction against a schema (consistent structured outputs).

### Prerequisites
- Python 3.10+
- macOS/Linux (Windows WSL2 recommended)
- uv (fast Python package/deps manager)

Install uv:
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
# then restart your shell or follow the printed PATH instructions
```

### Install dependencies with uv and run diagnostics
1) Install project dependencies from `pyproject.toml`/`uv.lock`:
```bash
uv sync
```
2) One-time Crawl4AI setup (downloads browser/runtime assets):
```bash
uv run crawl4ai-setup
```
3) Sanity check / diagnostics:
```bash
uv run crawl4ai-doctor
```
If anything fails, see the Crawl4AI docs: [Crawl4AI Documentation](https://github.com/unclecode/crawl4ai) and search issues/FAQs.

### Clone and run this repo
```bash
git clone <your-repo-url>.git
cd feature-evaluator

# Install deps
uv sync

# If you plan to use a remote LLM, export your API key(s)
# export OPENAI_API_KEY=...
# export ANTHROPIC_API_KEY=...
# export GROQ_API_KEY=...

# Run the script via uv (no need to activate a venv)
uv run python main.py
```
By default, `main.py` uses the provider `ollama/gemma3` (local). You can switch to another provider (e.g., `openai/gpt-4o-mini`) and pass an API token. See the provider notes below.

### What it returns (features/stats)
The LLM extracts the following features from the crawled text, each as a proportion in [0, 1]:
- statistics_addition: sentences with numerical data, percentages, or cited figures
- quotation_addition: sentences with direct quotations
- cite_sources: sentences that cite sources
- high_fluency: sentences written in a high-fluency style
- accurate_terminology: sentences using accurate terminology
- non_manipulative_tone: sentences with non-manipulative tone

Additionally, we aim to report basic counts:
- total_number_of_sentences
- total_sentences_with_statistics

Note: Counts may be used internally or printed depending on how you run/extend `main.py`.


### Switching providers
- Ollama (local): install Ollama and pull a model, e.g. `ollama pull gemma3`.
- OpenAI/Groq/Anthropic: set the corresponding `provider` and export your API key env var; pass it to `LLMConfig` via `api_token` in `main.py`.

### Troubleshooting
- Run `uv run crawl4ai-doctor` to verify all dependencies (browser, playwright, ffmpeg, etc.).
- If crawling stalls on heavy JS sites, increase `page_timeout` in `CrawlerRunConfig`.
- For inconsistent extraction, lower `temperature`, refine `instructions`, or ensure `schema` aligns with desired fields.
- Consult the Crawl4AI docs and issues: [Crawl4AI on GitHub](https://github.com/unclecode/crawl4ai).

 