from core.prompt_compiler import compiler

MASTER_PROMPT = compiler.compile_daily()

print(f"Master Prompt Loaded ({len(MASTER_PROMPT):,} chars)")


def load_prompt():

    return MASTER_PROMPT