"""Shared Anthropic API client for Streamlit apps."""

import streamlit as st
from anthropic import Anthropic

DEFAULT_MODEL = "claude-sonnet-4-20250514"


@st.cache_resource
def get_client() -> Anthropic:
    """Get a cached Anthropic client instance."""
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("ANTHROPIC_API_KEY が設定されていません。Secrets を確認してください。")
        st.stop()
    return Anthropic(api_key=api_key)


def generate_text(
    system_prompt: str,
    user_message: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
) -> str:
    """Generate text using the Anthropic API.

    Args:
        system_prompt: System prompt to set context.
        user_message: User's input message.
        model: Model to use.
        max_tokens: Maximum tokens in response.

    Returns:
        Generated text string.
    """
    client = get_client()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def generate_streaming(
    system_prompt: str,
    user_message: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
):
    """Generate text with streaming using the Anthropic API.

    Args:
        system_prompt: System prompt to set context.
        user_message: User's input message.
        model: Model to use.
        max_tokens: Maximum tokens in response.

    Yields:
        Text chunks as they are generated.
    """
    client = get_client()
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def multi_agent_chain(
    agents: list[dict],
    initial_input: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
    on_agent_start=None,
    on_agent_complete=None,
) -> list[dict]:
    """Execute a chain of agents sequentially.

    Args:
        agents: List of dicts with 'name' and 'system_prompt' keys.
        initial_input: Input for the first agent.
        model: Model to use.
        max_tokens: Maximum tokens per agent response.
        on_agent_start: Callback(agent_name) when agent starts.
        on_agent_complete: Callback(agent_name, result) when agent completes.

    Returns:
        List of dicts with 'name' and 'output' keys.
    """
    results = []
    current_input = initial_input

    for agent in agents:
        name = agent["name"]
        system_prompt = agent["system_prompt"]

        if on_agent_start:
            on_agent_start(name)

        context = current_input
        if results:
            prev_outputs = "\n\n".join(
                f"## {r['name']} の分析結果\n{r['output']}" for r in results
            )
            context = f"{initial_input}\n\n---\n\n# これまでの分析結果\n\n{prev_outputs}"

        output = generate_text(
            system_prompt=system_prompt,
            user_message=context,
            model=model,
            max_tokens=max_tokens,
        )

        result = {"name": name, "output": output}
        results.append(result)

        if on_agent_complete:
            on_agent_complete(name, output)

        current_input = context

    return results
