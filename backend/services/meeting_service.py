import re
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models import ActionItem, Meeting, Topic, TranscriptSegment
from schemas import MeetingUpdate

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "this", "that", "it", "we", "i", "you",
    "he", "she", "they", "let's", "let", "going", "just", "really", "think",
    "know", "yeah", "okay", "so", "can", "will", "would", "should", "have",
    "has", "had", "do", "does", "did", "not", "if", "at", "by", "from", "as",
    "up", "about", "into", "over", "after", "before", "then", "there", "here",
    "also", "one", "two", "get", "got", "like", "want", "need",
}

ACTION_PHRASES = (
    "i'll", "will ", "need to", "going to", "should ", "let's", "to finalize",
    "to send", "to schedule", "to draft", "to submit", "to check", "to update",
    "to follow up", "to confirm", "to share", "to investigate",
)


def parse_transcript_text(transcript_text: str) -> List[dict]:
    """Turns raw 'Speaker: text' lines into ordered segment dicts."""
    segments = []
    lines = [line.strip() for line in transcript_text.strip().splitlines() if line.strip()]

    for index, line in enumerate(lines):
        speaker, separator, text = line.partition(":")
        if separator:
            speaker = speaker.strip()
            text = text.strip()
        else:
            speaker = None
            text = line

        segments.append(
            {
                "order_index": index,
                "speaker": speaker or None,
                "start_time": float(index * 15),
                "text": text,
            }
        )

    return segments


def transcript_text_from_json(payload) -> str:
    """Flattens an uploaded .json transcript into plain 'Speaker: text' lines."""
    if isinstance(payload, dict) and "transcript" in payload:
        payload = payload["transcript"]

    if isinstance(payload, list):
        lines = []
        for item in payload:
            if isinstance(item, dict):
                speaker = item.get("speaker", "")
                text = item.get("text", "")
                lines.append(f"{speaker}: {text}" if speaker else text)
            else:
                lines.append(str(item))
        return "\n".join(lines)

    if isinstance(payload, dict) and "text" in payload:
        return payload["text"]

    return str(payload)


def generate_summary(segments: List[dict]) -> str:
    """Deterministic placeholder summary - no external AI call."""
    if not segments:
        return "No transcript content available to summarize."

    speakers = sorted({seg["speaker"] for seg in segments if seg["speaker"]})
    speaker_part = f" among {len(speakers)} participants" if speakers else ""

    preview = " ".join(seg["text"] for seg in segments[:3])
    if len(preview) > 280:
        preview = preview[:280] + "..."

    return (
        f"This meeting covered {len(segments)} discussion points{speaker_part}. "
        f'It opened with: "{preview}"'
    )


def extract_topics(segments: List[dict], limit: int = 5) -> List[str]:
    """Deterministic keyword-frequency mock for topic extraction."""
    counts: Dict[str, int] = {}

    for seg in segments:
        words = re.findall(r"[a-zA-Z']+", seg["text"].lower())
        for word in words:
            if len(word) < 4 or word in STOPWORDS:
                continue
            counts[word] = counts.get(word, 0) + 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [word.capitalize() for word, _ in ranked[:limit]]


def extract_action_items(segments: List[dict], limit: int = 6) -> List[dict]:
    """Rule-based mock: flags segments containing common commitment phrasing."""
    items = []

    for seg in segments:
        lowered = seg["text"].lower()
        if any(phrase in lowered for phrase in ACTION_PHRASES):
            items.append({"text": seg["text"], "owner": seg["speaker"]})
        if len(items) >= limit:
            break

    return items


def create_meeting(
    db: Session, title: str, participants: Optional[str], transcript_text: str
) -> Meeting:
    segments = parse_transcript_text(transcript_text)
    summary = generate_summary(segments)
    topics = extract_topics(segments)
    action_items = extract_action_items(segments)

    meeting = Meeting(title=title, participants=participants, summary=summary)
    db.add(meeting)
    db.flush()

    for segment in segments:
        db.add(TranscriptSegment(meeting_id=meeting.id, **segment))

    for label in topics:
        db.add(Topic(meeting_id=meeting.id, label=label))

    for item in action_items:
        db.add(ActionItem(meeting_id=meeting.id, text=item["text"], owner=item["owner"]))

    db.commit()
    db.refresh(meeting)
    return meeting


def update_meeting(db: Session, meeting: Meeting, payload: MeetingUpdate) -> Meeting:
    if payload.title is not None:
        meeting.title = payload.title
    if payload.participants is not None:
        meeting.participants = payload.participants

    db.commit()
    db.refresh(meeting)
    return meeting


def delete_meeting(db: Session, meeting: Meeting) -> None:
    db.delete(meeting)
    db.commit()
