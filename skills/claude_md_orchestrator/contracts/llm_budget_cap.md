# CONTRACT C-008: llm-budget-cap

The LLM access layer must enforce a daily cost budget and a per call
token cap. The current access layer has no budget. ``recommend_next``,
``swan_ensemble``, ``groq_agent``, ``hive_spawn``, ``lazyllmchat``,
``vulnbot``, and ``vuln_agent`` can spend Groq tokens without an
operator visible cap. The orchestrator will wrap the
:func:`llm_factory.get_llm_backend` factory with a proxy that
counts input and output tokens through ``tiktoken``, computes the
dollar cost from a per model price table, and refuses the call when
the daily budget or the per call token cap is exhausted.

The trigger is any LLM call that flows through
:func:`llm_factory.get_llm_backend` or
:func:`llm_factory.try_get_llm_backend`. The inputs are the prompt
passed to the LLM, the model identifier, the daily budget in United
States dollars, the per call token cap, and the per model price
table. The happy path is the proxy counts the tokens, charges the
cost, and forwards the call when the call fits the budget. The sad
paths cover the daily budget exhausted, the per call token cap
exceeded, the token estimator offline, a malformed price table, a
concurrent writer on the ledger, and a clock skew between the
host and the ledger. The data flow is the proxy reads the budget
configuration from ``payload.json``, loads the ledger from
``sessions/llm_budget.json``, counts the tokens, charges the cost,
writes the ledger, and forwards the call. The observability is the
``llm_budget`` command and the ``lazyown_get_llm_budget`` MCP tool.
The out of scope is anything beyond the budget: the actual LLM
output, the response caching, and the model selection.

- daily budget in United States dollars
- per call token cap
- per model price table
- token counter through tiktoken
- ledger on sessions/llm_budget.json
- proxy that wraps llm_factory.get_llm_backend
- CLI command llm_budget
- MCP tool lazyown_get_llm_budget
