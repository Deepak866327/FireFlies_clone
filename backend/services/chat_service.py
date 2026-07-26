from typing import List

from models import Meeting
from services.llm import get_provider
from services.llm.base import ChatTurn

SYSTEM_PROMPT_TEMPLATE = """You are an AI assistant helping users understand a meeting.

Answer ONLY using the supplied meeting information.

If the answer is not present in the meeting, reply exactly:
"I couldn't find that information in this meeting."

Do not invent facts.
Do not hallucinate.

If the user asks for a summary, use the meeting summary.
Otherwise answer using transcript evidence.

--- MEETING INFORMATION ---
Title: {title}

Summary:
{summary}

Topics:
{topics}

Action Items:
{action_items}

Transcript:
{transcript}
"""

MAX_HISTORY_MESSAGES = 5


def _build_system_prompt(meeting: Meeting) -> str:
    topics = "\n".join(f"- {topic.label}" for topic in meeting.topics) or "None"
    action_items = (
        "\n".join(f"- [{'x' if item.is_done else ' '}] {item.text}" for item in meeting.action_items)
        or "None"
    )
    segments = sorted(meeting.segments, key=lambda segment: segment.order_index)
    transcript = (
        "\n".join(f"{segment.speaker or 'Unknown'}: {segment.text}" for segment in segments)
        or "No transcript available."
    )

    return SYSTEM_PROMPT_TEMPLATE.format(
        title=meeting.title,
        summary=meeting.summary or "No summary available.",
        topics=topics,
        action_items=action_items,
        transcript=transcript,
    )


def ask_about_meeting(
    meeting: Meeting, provider_name: str, question: str, history: List[ChatTurn]
) -> str:
    provider = get_provider(provider_name)
    system_prompt = _build_system_prompt(meeting)

    trimmed_history = history[-MAX_HISTORY_MESSAGES:]
    messages: List[ChatTurn] = [*trimmed_history, {"role": "user", "content": question}]

    return provider.ask(system_prompt, messages)
