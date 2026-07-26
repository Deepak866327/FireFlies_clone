from io import BytesIO
from typing import Any, Dict
from xml.sax.saxutils import escape as xml_escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from models import Meeting

DIVIDER = "-" * 32


def _format_timestamp(seconds) -> str:
    if seconds is None:
        return "--:--"
    total = int(seconds)
    minutes, secs = divmod(total, 60)
    return f"{minutes:02d}:{secs:02d}"


def _meeting_sections(meeting: Meeting) -> Dict[str, Any]:
    segments = sorted(meeting.segments, key=lambda segment: segment.order_index)
    return {
        "title": meeting.title,
        "date": meeting.created_at.strftime("%B %d, %Y %I:%M %p") if meeting.created_at else "",
        "participants": meeting.participants or "Not specified",
        "summary": meeting.summary or "No summary available.",
        "topics": [topic.label for topic in meeting.topics],
        "action_items": [
            {"text": item.text, "owner": item.owner, "is_done": item.is_done}
            for item in meeting.action_items
        ],
        "transcript": [
            {
                "timestamp": _format_timestamp(segment.start_time),
                "speaker": segment.speaker or "Unknown",
                "text": segment.text,
            }
            for segment in segments
        ],
    }


def export_txt(meeting: Meeting) -> str:
    data = _meeting_sections(meeting)
    lines = [
        data["title"],
        data["date"],
        f"Participants: {data['participants']}",
        "",
        DIVIDER,
        "SUMMARY",
        DIVIDER,
        data["summary"],
        "",
        DIVIDER,
        "TOPICS",
        DIVIDER,
    ]
    lines += [f"- {topic}" for topic in data["topics"]] or ["No topics extracted."]
    lines += ["", DIVIDER, "ACTION ITEMS", DIVIDER]

    if data["action_items"]:
        for item in data["action_items"]:
            box = "[x]" if item["is_done"] else "[ ]"
            owner = f" — {item['owner']}" if item["owner"] else ""
            lines.append(f"{box} {item['text']}{owner}")
    else:
        lines.append("No action items.")

    lines += ["", DIVIDER, "TRANSCRIPT", DIVIDER]
    for segment in data["transcript"]:
        lines += [f"[{segment['timestamp']}]", segment["speaker"], segment["text"], ""]

    return "\n".join(lines)


def export_markdown(meeting: Meeting) -> str:
    data = _meeting_sections(meeting)
    lines = [
        f"# {data['title']}",
        "",
        "## Date",
        data["date"],
        "",
        "## Participants",
        data["participants"],
        "",
        "## Summary",
        data["summary"],
        "",
        "## Topics",
    ]
    lines += [f"- {topic}" for topic in data["topics"]] or ["- No topics extracted."]
    lines += ["", "## Action Items"]

    if data["action_items"]:
        for item in data["action_items"]:
            checkbox = "[x]" if item["is_done"] else "[ ]"
            owner = f" — {item['owner']}" if item["owner"] else ""
            lines.append(f"- {checkbox} {item['text']}{owner}")
    else:
        lines.append("- No action items.")

    lines += ["", "## Transcript"]
    for segment in data["transcript"]:
        lines.append(f"**[{segment['timestamp']}] {segment['speaker']}:** {segment['text']}")

    return "\n".join(lines)


def export_pdf(meeting: Meeting) -> bytes:
    data = _meeting_sections(meeting)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(xml_escape(data["title"]), styles["Title"]), Spacer(1, 12)]

    story.append(Paragraph(f"Date: {xml_escape(data['date'])}", styles["Normal"]))
    story.append(Paragraph(f"Participants: {xml_escape(data['participants'])}", styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Summary", styles["Heading2"]))
    story.append(Paragraph(xml_escape(data["summary"]), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Topics", styles["Heading2"]))
    if data["topics"]:
        for topic in data["topics"]:
            story.append(Paragraph(f"• {xml_escape(topic)}", styles["Normal"]))
    else:
        story.append(Paragraph("No topics extracted.", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Action Items", styles["Heading2"]))
    if data["action_items"]:
        for item in data["action_items"]:
            box = "[x]" if item["is_done"] else "[ ]"
            owner = f" — {xml_escape(item['owner'])}" if item["owner"] else ""
            story.append(Paragraph(f"{box} {xml_escape(item['text'])}{owner}", styles["Normal"]))
    else:
        story.append(Paragraph("No action items.", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Transcript", styles["Heading2"]))
    for segment in data["transcript"]:
        story.append(
            Paragraph(
                f"<b>[{segment['timestamp']}] {xml_escape(segment['speaker'])}</b>: "
                f"{xml_escape(segment['text'])}",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
