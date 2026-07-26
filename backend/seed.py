from datetime import datetime

from database import Base, engine, SessionLocal
from models import Meeting, TranscriptSegment, ActionItem, Topic

# Duration isn't a separate column on Meeting - it's implied by the last
# transcript segment's start_time, same as Fireflies derives it from audio length.
MEETINGS = [
    {
        "title": "Q3 Product Roadmap Planning",
        "created_at": datetime(2026, 7, 14, 10, 0),
        "participants": "Sarah Chen, Mike Rodriguez, Priya Patel, Tom Wilson",
        "summary": (
            "The product team reviewed progress on the Q3 roadmap, prioritized the "
            "notification revamp and mobile onboarding flow, and agreed to push the "
            "analytics dashboard to Q4. Mike raised concerns about engineering "
            "bandwidth given current sprint commitments, and the team agreed to "
            "revisit resourcing next week."
        ),
        "topics": [
            "Q3 Roadmap Prioritization",
            "Notification Revamp",
            "Mobile Onboarding Flow",
            "Engineering Bandwidth",
            "Analytics Dashboard Timeline",
        ],
        "action_items": [
            ("Finalize the Q3 roadmap doc and share with stakeholders by Friday", "Sarah Chen", False),
            ("Estimate engineering effort for the notification revamp", "Mike Rodriguez", False),
            ("Share updated onboarding wireframes by Wednesday", "Priya Patel", True),
            ("Investigate feasibility of moving analytics dashboard to Q4", "Tom Wilson", False),
            ("Schedule a follow-up on engineering resourcing next week", "Sarah Chen", False),
        ],
        "transcript": [
            ("Sarah Chen", 0, "Alright, let's get started. Thanks everyone for hopping on. Today we're going through the Q3 roadmap and trying to lock priorities before end of week."),
            ("Mike Rodriguez", 20, "Sounds good. I pulled up the engineering capacity numbers, so we can sanity check against that."),
            ("Sarah Chen", 45, "Perfect. Let's start with the notification revamp since that's been on the backlog for two quarters now."),
            ("Priya Patel", 70, "From a design side, I finished the first pass on the new notification center. I can share the Figma link after this."),
            ("Sarah Chen", 95, "Great, please do. Mike, what's your read on effort for that one?"),
            ("Mike Rodriguez", 120, "Honestly it's bigger than it looks. We'd need to touch the push service, the in-app center, and email digests. I'd guess three to four weeks with two engineers."),
            ("Sarah Chen", 150, "Okay, that's more than I expected but it's been requested a lot in customer feedback."),
            ("Tom Wilson", 170, "Agreed, it's come up in almost every churn interview I've read this month."),
            ("Sarah Chen", 195, "Let's prioritize it then. Next up, mobile onboarding flow."),
            ("Priya Patel", 220, "This one's smaller. I have wireframes mostly done, just need to validate the empty states."),
            ("Sarah Chen", 245, "When can you have those ready?"),
            ("Priya Patel", 270, "I can share by Wednesday."),
            ("Sarah Chen", 290, "Perfect, I'll add that as an action item."),
            ("Mike Rodriguez", 310, "For onboarding, engineering side is pretty light. Maybe a week, mostly frontend."),
            ("Tom Wilson", 330, "I can take that one if Mike's tied up on notifications."),
            ("Mike Rodriguez", 350, "That works for me."),
            ("Sarah Chen", 370, "Great, let's move to analytics dashboard. I know this has been requested but I'm wondering if it should slip to Q4."),
            ("Tom Wilson", 395, "Given the notification work just got bigger, I think that's the right call."),
            ("Mike Rodriguez", 415, "Yeah, we don't have bandwidth to do both well in Q3."),
            ("Sarah Chen", 435, "Okay, let's tentatively push it. Tom, can you double check there's no hard commitment to a customer on that timeline?"),
            ("Tom Wilson", 460, "Will do, I'll check with sales this week."),
            ("Sarah Chen", 480, "Thanks. Let's also talk bandwidth more broadly, Mike you mentioned some concerns before the call."),
            ("Mike Rodriguez", 505, "Yeah, between the notification work and the ongoing bug backlog, the team's pretty stretched. I don't think we can take on anything new without dropping something."),
            ("Sarah Chen", 530, "Noted. Let's set up a separate resourcing conversation next week so we can look at this properly."),
            ("Mike Rodriguez", 555, "Works for me."),
            ("Priya Patel", 575, "One more thing, should we loop in support on the notification center design? They'll have opinions on what alerts matter most."),
            ("Sarah Chen", 600, "Good call, I'll add them to the next design review."),
            ("Tom Wilson", 620, "Also worth checking with the data team on tracking events for the new onboarding flow."),
            ("Priya Patel", 645, "I'll reach out to them this week."),
            ("Sarah Chen", 665, "Great. I think that covers the main items. Let's recap action items before we wrap."),
            ("Sarah Chen", 690, "I'll finalize the roadmap doc and send it out by Friday. Mike, effort estimate for notifications. Priya, wireframes by Wednesday. Tom, feasibility check on pushing analytics to Q4."),
            ("Mike Rodriguez", 715, "Sounds right."),
            ("Tom Wilson", 735, "All good on my end."),
            ("Priya Patel", 755, "Same here, sounds good."),
            ("Sarah Chen", 775, "Awesome, thanks everyone. Talk next week."),
        ],
    },
    {
        "title": "Weekly Engineering Standup",
        "created_at": datetime(2026, 7, 16, 9, 30),
        "participants": "Mike Rodriguez, Tom Wilson, Aisha Khan, Daniel Kim",
        "summary": (
            "The engineering team synced on sprint progress. The auth service "
            "migration is on track for Thursday, but the reporting API is blocked "
            "on a third-party rate limit issue. Daniel will investigate a caching "
            "workaround, and the team agreed to deprioritize flaky test cleanup "
            "until next sprint."
        ),
        "topics": [
            "Sprint Progress",
            "Auth Service Migration",
            "Reporting API Rate Limits",
            "Flaky Tests",
            "On-call Handoff",
        ],
        "action_items": [
            ("Investigate caching workaround for the reporting API rate limit", "Daniel Kim", False),
            ("Finish auth service migration by Thursday", "Mike Rodriguez", False),
            ("Update the on-call runbook with the new deploy steps", "Aisha Khan", True),
            ("Triage the top 5 flaky tests next sprint", "Tom Wilson", False),
        ],
        "transcript": [
            ("Mike Rodriguez", 0, "Morning everyone, let's keep this quick. Tom, want to kick us off?"),
            ("Tom Wilson", 15, "Sure. Yesterday I finished the onboarding frontend work from last week's roadmap call, today I'm picking up code review for the API gateway PR."),
            ("Mike Rodriguez", 40, "Nice, I'll take a look at that PR after this."),
            ("Aisha Khan", 55, "I wrapped up the deploy pipeline fix yesterday, deploys are back to under five minutes. Today I'm updating the on-call runbook."),
            ("Mike Rodriguez", 80, "Awesome, that pipeline fix was overdue."),
            ("Daniel Kim", 95, "I'm still stuck on the reporting API. We're hitting rate limits from the third-party vendor way earlier than expected."),
            ("Mike Rodriguez", 120, "How much room do we actually have left?"),
            ("Daniel Kim", 140, "Basically none during peak hours. It's throttling around 60% of requests."),
            ("Tom Wilson", 160, "Have we talked to the vendor about a higher tier?"),
            ("Daniel Kim", 180, "I emailed them yesterday, no response yet."),
            ("Mike Rodriguez", 200, "Okay, let's not block on that. Can we cache responses in the meantime?"),
            ("Daniel Kim", 220, "Yeah, that's probably the right call. I'll look into a short-lived cache today."),
            ("Mike Rodriguez", 240, "Great, let's make that today's priority. On my end, auth service migration is going well, should be done by Thursday."),
            ("Tom Wilson", 270, "Any blockers on that?"),
            ("Mike Rodriguez", 285, "Not really, just a lot of test coverage to write."),
            ("Aisha Khan", 300, "Let me know if you want a second pair of eyes on the migration PR."),
            ("Mike Rodriguez", 320, "Appreciate it, I'll ping you when it's up."),
            ("Tom Wilson", 335, "Quick note, the flaky test suite is getting worse, I counted twelve failures yesterday that weren't real bugs."),
            ("Mike Rodriguez", 360, "Yeah I've noticed. Let's not tackle it this sprint though, we're pretty full."),
            ("Tom Wilson", 380, "Fair, I'll just triage the worst five next sprint so they stop blocking CI."),
            ("Daniel Kim", 400, "That would help a lot honestly."),
            ("Aisha Khan", 415, "One more thing, I'm on-call starting tomorrow. Runbook update should be in by end of day."),
            ("Mike Rodriguez", 435, "Perfect timing. Anything else before we wrap?"),
            ("Tom Wilson", 450, "Nothing from me."),
            ("Daniel Kim", 460, "Same."),
            ("Aisha Khan", 470, "All good."),
            ("Mike Rodriguez", 480, "Great, thanks everyone, have a good one."),
            ("Tom Wilson", 495, "One last thing actually, should I file a ticket for the vendor rate limit so we have a paper trail?"),
            ("Mike Rodriguez", 515, "Good idea, go ahead and file it under the reporting API epic."),
            ("Tom Wilson", 535, "Will do."),
            ("Daniel Kim", 550, "I'll link the ticket once I have caching numbers to share."),
            ("Mike Rodriguez", 570, "Perfect, thanks Daniel."),
        ],
    },
    {
        "title": "Marketing Campaign Kickoff - Fall Launch",
        "created_at": datetime(2026, 7, 20, 13, 0),
        "participants": "Elena Martinez, Jordan Lee, Sam Okafor, Nina Petrova",
        "summary": (
            "The marketing team kicked off planning for the fall product launch "
            "campaign. They aligned on a mid-September launch date, agreed to lead "
            "with the notification revamp as the headline feature, and split "
            "ownership of creative, paid media, and PR. Budget approval is still "
            "pending from finance."
        ),
        "topics": [
            "Fall Launch Timeline",
            "Creative Direction",
            "Paid Media Budget",
            "PR Strategy",
            "Notification Revamp Messaging",
        ],
        "action_items": [
            ("Submit the campaign budget request to finance by Monday", "Elena Martinez", False),
            ("Draft creative brief for the launch video", "Jordan Lee", False),
            ("Build the paid media plan across channels", "Sam Okafor", False),
            ("Draft press release for the notification revamp", "Nina Petrova", True),
            ("Confirm launch date with the product team", "Elena Martinez", False),
            ("Source a freelance video editor", "Jordan Lee", False),
        ],
        "transcript": [
            ("Elena Martinez", 0, "Thanks for joining, let's kick off fall launch planning. High level, we're targeting mid-September."),
            ("Jordan Lee", 20, "Is that locked with product, or still tentative?"),
            ("Elena Martinez", 40, "Still tentative, I need to confirm with Sarah's team, but let's plan around it for now."),
            ("Sam Okafor", 60, "Works for me, gives us about eight weeks."),
            ("Elena Martinez", 80, "Right. The headline feature is going to be the notification revamp, it's been the most requested thing in customer feedback."),
            ("Nina Petrova", 105, "That's a good angle for press too, I can position it as solving a real pain point rather than just a feature drop."),
            ("Elena Martinez", 130, "Perfect, can you start on a press release draft?"),
            ("Nina Petrova", 150, "Yep, I'll have a first draft by end of week."),
            ("Jordan Lee", 170, "For creative, I'm thinking a short launch video plus a landing page refresh. Should I start on the brief?"),
            ("Elena Martinez", 195, "Yes please, and loop in Priya from product design so it's consistent with the actual UI."),
            ("Jordan Lee", 220, "Will do."),
            ("Sam Okafor", 235, "On paid media, what's our rough budget looking like?"),
            ("Elena Martinez", 255, "I don't have final numbers yet, I'm submitting the request to finance Monday."),
            ("Sam Okafor", 275, "Okay, I'll draft a plan assuming last quarter's budget and adjust once we know."),
            ("Elena Martinez", 295, "Sounds good. Which channels are you thinking?"),
            ("Sam Okafor", 315, "Probably paid social as the bulk, some search, and maybe a small retargeting push in the last two weeks."),
            ("Nina Petrova", 340, "Are we doing any influencer or partner outreach this time?"),
            ("Elena Martinez", 360, "Good question, let's revisit that once we know budget. Keep it in your back pocket though."),
            ("Nina Petrova", 380, "Will do."),
            ("Jordan Lee", 395, "For the video, I want to bring in a freelance editor, our internal bandwidth is tight this month."),
            ("Elena Martinez", 415, "Fine by me, go ahead and source someone."),
            ("Jordan Lee", 435, "I have a couple people in mind, I'll reach out this week."),
            ("Sam Okafor", 455, "Should we also plan a launch day social calendar, or is that part of the creative brief?"),
            ("Jordan Lee", 480, "I'll fold it into the brief so it's all in one place."),
            ("Elena Martinez", 500, "Perfect. Let's also nail down a tagline before we go too far on creative."),
            ("Nina Petrova", 520, "I can pull a few options together from the press release work."),
            ("Elena Martinez", 540, "Great, send those over by Wednesday and we'll pick one as a team."),
            ("Sam Okafor", 565, "Should we loop in sales so they're not caught off guard by the launch?"),
            ("Elena Martinez", 585, "Yes, I'll send a heads up to sales leadership this week."),
            ("Jordan Lee", 605, "Sounds like a solid plan. Anything blocking before next steps?"),
            ("Elena Martinez", 625, "Just the budget approval, everything else can move in parallel."),
            ("Sam Okafor", 645, "Makes sense."),
            ("Nina Petrova", 660, "All good from my side."),
            ("Elena Martinez", 675, "Great, thanks everyone, let's regroup next week with budget confirmed."),
        ],
    },
    {
        "title": "Customer Success - Enterprise Client Renewal Call",
        "created_at": datetime(2026, 7, 22, 15, 0),
        "participants": "Rachel Adams, Ben Turner, Laura Kim (Northwind Logistics)",
        "summary": (
            "Rachel and Ben met with Northwind Logistics to discuss their upcoming "
            "contract renewal. Laura raised concerns about reporting limitations "
            "and seat pricing, but confirmed strong overall satisfaction with the "
            "platform. The team agreed to a custom reporting proposal and a "
            "discounted seat tier in exchange for a two-year commitment."
        ),
        "topics": [
            "Contract Renewal Terms",
            "Reporting Limitations",
            "Seat Pricing",
            "Two-Year Commitment Discount",
            "Feature Requests",
        ],
        "action_items": [
            ("Send a custom reporting proposal to Laura by Friday", "Rachel Adams", False),
            ("Draft updated pricing for the two-year commitment", "Ben Turner", False),
            ("Schedule a product demo of the new dashboard for Northwind's team", "Rachel Adams", False),
            ("Check with legal on custom contract terms", "Ben Turner", True),
            ("Follow up with Laura early next week", "Rachel Adams", False),
        ],
        "transcript": [
            ("Rachel Adams", 0, "Hi Laura, thanks for making time today. We wanted to talk through the renewal ahead of your contract ending next month."),
            ("Laura Kim", 25, "Of course, happy to be here. Overall we've been really happy with the platform, just have a few things to flag before we sign."),
            ("Rachel Adams", 50, "That's great to hear, and please, let's go through them."),
            ("Laura Kim", 65, "Biggest one is reporting. Our ops team needs custom exports that match our internal dashboards, and right now we're doing a lot of manual work."),
            ("Ben Turner", 95, "Can you give an example of what's missing specifically?"),
            ("Laura Kim", 115, "Mainly we need meeting summaries broken down by team and exportable to CSV on a schedule, not just one-off downloads."),
            ("Rachel Adams", 145, "That's doable. We've actually had a few enterprise clients ask for similar things."),
            ("Ben Turner", 165, "I can put together a custom reporting proposal, scoped to scheduled exports by team."),
            ("Laura Kim", 185, "That would help a lot."),
            ("Rachel Adams", 195, "I'll make sure that's sent over by Friday."),
            ("Laura Kim", 215, "Second thing, and I want to be upfront about this, our finance team flagged the per-seat pricing as expensive compared to what we budgeted."),
            ("Ben Turner", 250, "Understood. How many seats are we talking about for the renewal?"),
            ("Laura Kim", 275, "We're looking to actually grow from 40 to 60 seats next year."),
            ("Rachel Adams", 295, "Okay, that's helpful context. If you're open to a two-year commitment, we can likely offer a better per-seat rate given the volume increase."),
            ("Laura Kim", 325, "That's worth discussing, what kind of discount are we talking about?"),
            ("Ben Turner", 345, "I'd need to run the numbers, but historically we've done fifteen to twenty percent off list price for two-year enterprise deals at this seat count."),
            ("Laura Kim", 375, "That would make the finance conversation a lot easier."),
            ("Rachel Adams", 395, "Great, Ben will draft updated pricing this week and I'll get it to you."),
            ("Laura Kim", 415, "Appreciated. One more small thing, is there any timeline on the new analytics dashboard? A few of our managers have been asking."),
            ("Rachel Adams", 445, "It's actually in progress, not committed to a hard date yet, but I'd love to set up a demo of what exists so far."),
            ("Laura Kim", 470, "That would be great, our team would appreciate seeing where it's headed."),
            ("Rachel Adams", 490, "I'll get something on the calendar."),
            ("Ben Turner", 505, "I'll also confirm with our legal team that the custom reporting terms can go into the contract addendum."),
            ("Laura Kim", 530, "Sounds good. Overall this has been a productive call."),
            ("Rachel Adams", 550, "Agreed. So to recap, custom reporting proposal by Friday, updated two-year pricing this week, and a dashboard demo on the calendar."),
            ("Laura Kim", 580, "Perfect, I'll loop in our finance lead once I have the pricing."),
            ("Rachel Adams", 600, "Sounds good, I'll follow up early next week to check in."),
            ("Laura Kim", 615, "Great, talk soon, thanks both."),
            ("Ben Turner", 630, "Thanks Laura, have a good one."),
        ],
    },
    {
        "title": "All-Hands: Hiring Plan & Budget Review",
        "created_at": datetime(2026, 7, 24, 11, 0),
        "participants": "David Osei, Sarah Chen, Mike Rodriguez, Elena Martinez, Rachel Adams",
        "summary": (
            "Leadership reviewed the H2 hiring plan against current budget. The "
            "team agreed to prioritize two senior engineering hires and one "
            "customer success hire before year end, while pausing additional "
            "marketing headcount until Q1. David asked each lead to finalize "
            "updated headcount requests by end of month."
        ),
        "topics": [
            "H2 Hiring Plan",
            "Engineering Headcount",
            "Customer Success Headcount",
            "Marketing Headcount Freeze",
            "Budget Review",
        ],
        "action_items": [
            ("Finalize job descriptions for two senior engineering roles", "Mike Rodriguez", False),
            ("Submit headcount request for the customer success hire", "Rachel Adams", False),
            ("Hold marketing headcount until the Q1 review", "Elena Martinez", True),
            ("Compile updated headcount requests from all leads by end of month", "Sarah Chen", False),
            ("Review final budget numbers with finance", "David Osei", False),
        ],
        "transcript": [
            ("David Osei", 0, "Thanks everyone for joining. Today's mainly about hiring plans for the second half, and making sure it lines up with budget."),
            ("Sarah Chen", 25, "I put together a rough summary beforehand, should I start there?"),
            ("David Osei", 45, "Yeah, go ahead."),
            ("Sarah Chen", 55, "So across the org we have requests for six new hires this half, two engineering, one customer success, two marketing, and one design."),
            ("David Osei", 90, "And where does that put us against budget?"),
            ("Sarah Chen", 110, "Roughly ten percent over what finance modeled for H2, mainly driven by the marketing requests."),
            ("David Osei", 135, "Okay. Mike, walk us through the engineering asks."),
            ("Mike Rodriguez", 155, "We're stretched thin on the platform team, specifically around the notification and reporting work. Two senior engineers would get us back to a sustainable pace."),
            ("David Osei", 185, "Are these backfills or net new?"),
            ("Mike Rodriguez", 200, "Net new, we haven't backfilled anyone this year."),
            ("David Osei", 220, "That's a strong case. Let's prioritize those two."),
            ("Rachel Adams", 240, "On customer success, we're seeing renewal conversations get more complex, especially with enterprise accounts. One additional CSM would help a lot there."),
            ("David Osei", 275, "How urgent is that one relative to engineering?"),
            ("Rachel Adams", 295, "I'd say close behind, we're already stretched during renewal season."),
            ("David Osei", 315, "Let's approve that one too then."),
            ("Elena Martinez", 330, "For marketing, I had two requests in, but I understand if budget's tight."),
            ("David Osei", 355, "Given where we are, I think we need to hold marketing headcount until Q1. Sorry Elena, I know that's not ideal."),
            ("Elena Martinez", 385, "Understood, we can manage with contractors in the meantime for the fall campaign."),
            ("David Osei", 410, "Appreciate that. What about design?"),
            ("Sarah Chen", 425, "That one's lower priority right now, I'd say revisit alongside marketing in Q1."),
            ("David Osei", 450, "Agreed. So to summarize, two engineering hires and one customer success hire approved now, marketing and design pushed to Q1."),
            ("Mike Rodriguez", 485, "I'll get job descriptions finalized this week so we can start posting."),
            ("Rachel Adams", 505, "I'll submit the formal headcount request for the CS role."),
            ("Elena Martinez", 525, "I'll hold off on the marketing reqs and revisit in the Q1 planning cycle."),
            ("David Osei", 550, "Sarah, can you compile the final updated headcount requests from everyone by end of month?"),
            ("Sarah Chen", 575, "Yep, I'll pull that together."),
            ("David Osei", 590, "I'll take the final numbers back to finance to confirm we're within budget."),
            ("Mike Rodriguez", 610, "Sounds good."),
            ("Rachel Adams", 620, "Thanks everyone."),
            ("Elena Martinez", 630, "Sounds good, thanks."),
            ("David Osei", 640, "Great, appreciate everyone's time. Talk soon."),
        ],
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Meeting).count() > 0:
        print("Database already seeded, skipping.")
        db.close()
        return

    for data in MEETINGS:
        meeting = Meeting(
            title=data["title"],
            participants=data["participants"],
            created_at=data["created_at"],
            summary=data["summary"],
        )
        db.add(meeting)
        db.flush()

        for label in data["topics"]:
            db.add(Topic(meeting_id=meeting.id, label=label))

        for index, (speaker, start_time, text) in enumerate(data["transcript"]):
            db.add(
                TranscriptSegment(
                    meeting_id=meeting.id,
                    order_index=index,
                    speaker=speaker,
                    start_time=start_time,
                    text=text,
                )
            )

        for text, owner, is_done in data["action_items"]:
            db.add(
                ActionItem(
                    meeting_id=meeting.id,
                    text=text,
                    owner=owner,
                    is_done=is_done,
                )
            )

    db.commit()
    db.close()
    print(f"Seeded {len(MEETINGS)} meetings.")


if __name__ == "__main__":
    seed()
