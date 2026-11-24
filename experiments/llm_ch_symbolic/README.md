# LLM-Assisted CH Symbolic Experiment

Independent experiment directory. It does not modify SIGS main source, scripts,
tests, or historical results.

## Run

```bash
cd /Users/kang/SIGS
python3 experiments/llm_ch_symbolic/scripts/run_experiment.py
```

Modes:

```bash
python3 experiments/llm_ch_symbolic/scripts/run_experiment.py --skip-llm
python3 experiments/llm_ch_symbolic/scripts/run_experiment.py --validate-only
python3 experiments/llm_ch_symbolic/scripts/run_experiment.py --output-dir /tmp/llm_ch_output
```

## API configuration

The API key is never stored in source code, logs, reports, or result files.

Two supported locations, with environment variables taking precedence:

1. Environment:
   - `LLM_API_KEY` or `DEEPSEEK_API_KEY`
   - `LLM_BASE_URL` or `DEEPSEEK_BASE_URL`
   - `LLM_MODEL`

2. Local file:
   - `config/llm_config.json`

Copy the example first if needed:

```bash
cp config/llm_config.example.json config/llm_config.json
```

Then fill `api_key` and, if your account exposes a flash model, set `model` to
that exact model ID. The default is `deepseek-chat`; DeepSeek's fast
OpenAI-compatible endpoint is commonly available at `https://api.deepseek.com`.

Example:

```json
{
  "api_base": "https://api.deepseek.com",
  "api_key": "sk-...",
  "model": "deepseek-chat",
  "temperature": 0,
  "max_retries": 3,
  "timeout_seconds": 120
  "verify_tls": true
}
```

TLS verification is enabled by default and the client uses the `certifi` CA
bundle when available. If your environment requires disabling certificate
verification, set `verify_tls` to `false`, but keep it enabled unless you
know why the certificate is failing.

If only flash is needed, set `LLM_MODEL` or `model` to your flash model name
instead of the default.

## Layout

- `src/ch_equation.py`: CH trial, residual, symbols.
- `src/residual_builder.py`: original and formal residuals plus consistency check.
- `src/term_serializer.py`: expanded additive terms for LLM input.
- `src/llm_client.py`: OpenAI-compatible HTTP client and config loading.
- `src/llm_grouping.py`: fixed-prompt real LLM call.
- `src/grouping_validator.py`: deterministic grouping validation.
- `src/coefficient_extractor.py`: SymPy coefficient extraction.
- `src/algebraic_solver.py`: algebraic solving and branch classification.
- `src/original_pde_verifier.py`: raw-CH Maple-branch verification.

## Tests

```bash
cd /Users/kang/SIGS
python3 -m pytest experiments/llm_ch_symbolic/tests -q
```
