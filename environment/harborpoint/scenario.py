"""Structured transcription of the HarborPoint World Bible (facilitator/world-bible.md).

This module holds *scenario data only*: people, teams, areas, calendar rules, the portfolio
(Epics E1-E6, Features F1-F24), per-team sprint history tables (section 6), the exact Sprint 14
item tables, explicit future items, F5's 20 ordered stories, Member Support's planted problems
(sections 6.6 and 9), dependencies (section 7), bug flows and the sandbox mini sets (section 9).

`generate.py` turns these tables into a dataset with revision histories. `facts.py` recomputes
every checkable number from the generated revisions and compares it with its *own* EXPECTED
table (transcribed independently from the World Bible), so a transcription error here is caught.

Conventions
- Sprints are referred to by number (9..20). Days of a sprint are 1..10 (Mon wk1 .. Fri wk2).
- Feature keys are "F1".."F24", Epic keys "E1".."E6". `None` as a group/parent means "orphan".
- Team area paths are relative to the project root, with backslash separators.
"""
from __future__ import annotations

PROJECT_NAME = "HarborPoint"
PROJECT_DESCRIPTION = (
    "HarborPoint Financial - Member Experience Transformation Program (METP, \"Project Lighthouse\"). "
    "Training environment for the course \"Azure DevOps for Managers\"."
)
PROCESS = "Agile"

SEED = "harborpoint-world-bible-v1"

# ----------------------------------------------------------------------------- calendar (section 3.2)
HISTORY_SPRINTS = (9, 10, 11, 12, 13)
ALL_SPRINTS = tuple(range(9, 21))
PIS = {3: (9, 10, 11, 12), 4: (13, 14, 15, 16), 5: (17, 18, 19, 20)}
CURRENT_SPRINT = 14


def pi_of(sprint: int) -> int:
    for pi, sprints in PIS.items():
        if sprint in sprints:
            return pi
    raise ValueError(f"sprint {sprint} is outside PI 3-5")


def iteration_rel(sprint: int) -> str:
    """Iteration path relative to the project root, e.g. 'PI 4\\Sprint 14'."""
    return f"PI {pi_of(sprint)}\\Sprint {sprint}"


# Team days off (section 3.2): Sprint 16 two days (company holiday), Sprint 17 one day. All teams.
# The World Bible does not fix which days; we use S16 days 4-5 (Thu/Fri of week 1) and S17 day 5.
TEAM_DAYS_OFF = {16: (4, 5), 17: (5,)}
WORKING_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# ----------------------------------------------------------------------------- areas and teams (3.1, 3.3)
DELIVERY_TEAMS = (
    "Mobile Banking", "Digital Accounts", "Security", "Core Platform", "Branch Experience", "Member Support",
)
TEAM_AREA = {
    "Mobile Banking": "Digital\\Mobile Banking",
    "Digital Accounts": "Digital\\Digital Accounts",
    "Security": "Security",
    "Core Platform": "Core Platform",
    "Branch Experience": "Branch Experience",
    "Member Support": "Member Support",
}
TOP_AREAS = ["Digital", "Digital\\Mobile Banking", "Digital\\Digital Accounts", "Security", "Core Platform",
             "Branch Experience", "Member Support", "Training"]
MAX_PARTICIPANTS = 30

TEAM_DESCRIPTIONS = {
    "HarborPoint Team": "Program-level view of everything in METP (Ruth Ellison, Program Manager). Excludes training sandboxes.",
    "Digital Portfolio": "Priya Raman's portfolio view across Mobile Banking and Digital Accounts (Epics and Features).",
    "Mobile Banking": "Delivery team: HarborPoint mobile app (iOS and Android).",
    "Digital Accounts": "Delivery team: online account opening, statements, insights and card controls.",
    "Security": "Delivery team: fraud detection, authentication and exam readiness.",
    "Core Platform": "Delivery team: APIs, notifications and platform enablers.",
    "Branch Experience": "Delivery team: in-branch digital experiences.",
    "Member Support": "Delivery team: service requests, chat and agent tools.",
}

# Default team: per the course lead's update to section 3.3, the default team must NOT include
# Training. Team field values: root (no children) + the five top-level delivery areas (with children).
DEFAULT_TEAM_AREAS = [("", False), ("Digital", True), ("Security", True), ("Core Platform", True),
                      ("Branch Experience", True), ("Member Support", True)]

# ----------------------------------------------------------------------------- people (section 2)
TEAM_PEOPLE = {
    "Mobile Banking": [("Diego Ramirez", "Engineering Manager"), ("Hannah Cole", "Product Owner"),
                       ("Ethan Brooks", "Sr. iOS Engineer"), ("Mei Tanaka", "Android Engineer"),
                       ("Jamal Washington", "Mobile Engineer"), ("Sofia Rossi", "Mobile Engineer"),
                       ("Ava Patel", "QA Engineer")],
    "Digital Accounts": [("Grace Liu", "Engineering Manager"), ("Ben Adeyemi", "Product Owner"),
                         ("Olivia Grant", "Engineer"), ("Noah Kim", "Engineer"), ("Fatima Hassan", "Engineer"),
                         ("Lucas Meyer", "Engineer"), ("Chloe Martin", "QA Engineer")],
    "Security": [("Aisha Karimi", "Security Engineering Lead and Product Owner"), ("Viktor Novak", "Engineer"),
                 ("Rachel Stein", "Engineer"), ("Omar Haddad", "Engineer"), ("Ingrid Larsen", "Engineer"),
                 ("Kwame Mensah", "Engineer")],
    "Core Platform": [("Nadia Petrova", "Platform Lead and Product Owner"), ("Sam Okoro", "Engineer"),
                      ("Julia Weber", "Engineer"), ("Arjun Mehta", "Engineer"), ("Elena Popescu", "Engineer")],
    "Branch Experience": [("Maya Johnson", "Product Owner"), ("Daniel Park", "Engineering Manager"),
                          ("Zoe Clarke", "Engineer"), ("Ravi Shankar", "Engineer"), ("Tomas Herrera", "Engineer")],
    "Member Support": [("Isaac Thompson", "Product Owner"), ("Leila Ahmadi", "Engineer"),
                       ("Marco Bianchi", "Engineer"), ("Nora Fitzgerald", "Engineer"),
                       ("Kyle Morgan", "Engineer (left HarborPoint in Sprint 12)")],
}
LEADERSHIP = [("Dana Whitfield", "EVP, Member Experience"), ("Marcus Reed", "Chief Information Officer"),
              ("Simone Laurent", "Chief Risk Officer"), ("Priya Raman", "Director, Digital Banking"),
              ("Hector Alvarez", "VP, Branch Network"), ("Carmen Diaz", "Director, Member Support"),
              ("Ruth Ellison", "Program Manager, METP"), ("Leo Fischer", "PMO Reporting Analyst"),
              ("Nadia Petrova", "Platform Lead")]
PRODUCT_OWNER = {"Mobile Banking": "Hannah Cole", "Digital Accounts": "Ben Adeyemi", "Security": "Aisha Karimi",
                 "Core Platform": "Nadia Petrova", "Branch Experience": "Maya Johnson",
                 "Member Support": "Isaac Thompson"}
# Who picks up generated history work. Kyle Morgan is deliberately excluded: the World Bible's
# "4 items assigned to Kyle Morgan" fact must hold for a project-wide Assigned To query.
ENGINEERS = {
    "Mobile Banking": ["Ethan Brooks", "Mei Tanaka", "Jamal Washington", "Sofia Rossi"],
    "Digital Accounts": ["Olivia Grant", "Noah Kim", "Fatima Hassan", "Lucas Meyer"],
    "Security": ["Viktor Novak", "Rachel Stein", "Omar Haddad", "Ingrid Larsen", "Kwame Mensah"],
    "Core Platform": ["Sam Okoro", "Julia Weber", "Arjun Mehta", "Elena Popescu"],
    "Branch Experience": ["Zoe Clarke", "Ravi Shankar", "Tomas Herrera"],
    "Member Support": ["Leila Ahmadi", "Marco Bianchi", "Nora Fitzgerald"],
}
QA_ENGINEER = {"Mobile Banking": "Ava Patel", "Digital Accounts": "Chloe Martin"}

# ----------------------------------------------------------------------------- Epics (section 4), in rank order
EPICS = [
    dict(key="E1", title="Fraud Detection & Security", area="Security", owner="Simone Laurent", priority=1,
         start=9, target=20, tags=[], value_area="Business",
         description="Strategic priority #1, Protect every member: detect and stop fraud in real time and harden authentication."),
    dict(key="E2", title="Digital Banking Modernization", area="Digital", owner="Priya Raman", priority=1,
         start=9, target=20, tags=[], value_area="Business",
         description="Strategic priority #2, Digital that feels human: a modern mobile and online banking experience."),
    dict(key="E3", title="Customer Support Modernization", area="Member Support", owner="Carmen Diaz", priority=2,
         start=9, target=19, tags=[], value_area="Business",
         description="Strategic priority #3, Effortless support: omnichannel service requests, chat and agent knowledge."),
    dict(key="E4", title="Branch Experience Transformation", area="Branch Experience", owner="Hector Alvarez",
         priority=2, start=9, target=20, tags=[], value_area="Business",
         description="Strategic priority #4, Branches as relationship hubs: appointments, lobby flow and in-branch onboarding."),
    dict(key="E5", title="Platform Foundations", area="Core Platform", owner="Nadia Petrova", priority=2,
         start=9, target=16, tags=["enabler"], value_area="Architectural",
         description="Enabler, Platform that scales: member API gateway and a unified notification service."),
    dict(key="E6", title="Compliance: Examination Readiness", area="Security", owner="Simone Laurent", priority=1,
         start=12, target=18, tags=["mandatory"], value_area="Business",
         description="Mandatory: be ready for the regulatory examination. Exam fieldwork begins in Sprint 18."),
]
E6_CREATED = (12, 3)  # sprint, day: "Created in Sprint 12 (day 3). Never re-ranked, so it sits last."

# ----------------------------------------------------------------------------- Features (section 5, 5.0)
# closed_sprint: the sprint at whose end the Feature was closed. Features not listed as Closed stay
# New/Active per `state`. F14 (New) and F15 (Active) are planted exceptions to the lifecycle rule.
_F = dict
FEATURES = [
    _F(key="F1", title="Mobile App Redesign", epic="E2", team="Mobile Banking", contributing=[], state="Closed",
       closed_sprint=11, start=9, target=11, bv=13, tc=8, effort=55, risk=3, tags=[],
       description="Redesign the HarborPoint mobile app around the new design system: navigation, home, accounts and transfers."),
    _F(key="F2", title="Mobile Check Deposit 2.0", epic="E2", team="Mobile Banking", contributing=[], state="Active",
       start=10, target=14, bv=13, tc=13, effort=93, risk=1, tags=["PI4-Committed", "at-risk"],
       description="Next-generation mobile check deposit: guided capture, instant feedback, clear limits and faster availability."),
    _F(key="F3", title="Biometric Login", epic="E2", team="Mobile Banking", contributing=["Security"], state="Active",
       start=12, target=16, bv=8, tc=5, effort=51, risk=2, tags=["PI4-Committed", "cross-team"],
       description="Face ID and fingerprint login with step-up for high-risk actions, built with Security."),
    _F(key="F4", title="Member-to-Member Transfers", epic="E2", team="Mobile Banking", contributing=["Core Platform"],
       state="New", start=17, target=20, bv=20, tc=8, effort=None, risk=2, tags=["PI5-Candidate"],
       description="Send money to another HarborPoint member by phone number or email. Planned for PI 5, not yet decomposed."),
    _F(key="F5", title="Instant Card Controls", epic="E2", team="Digital Accounts", contributing=[], state="New",
       start=15, target=17, bv=20, tc=20, effort=105, risk=2, tags=["leadership-ask"],
       description="Members lock and unlock cards, set travel notices and control how their cards can be used, instantly."),
    _F(key="F6", title="Online Account Opening", epic="E2", team="Digital Accounts", contributing=[], state="Active",
       start=11, target=16, bv=13, tc=8, effort=56, risk=2, tags=["PI4-Committed"],
       description="Open a membership and first account online in minutes, with identity verification and instant funding."),
    _F(key="F7", title="Spending Insights", epic="E2", team="Digital Accounts", contributing=[], state="Active",
       start=10, target=15, bv=5, tc=3, effort=43, risk=3, tags=["PI4-Committed"],
       description="Categorized spending, trends and budget alerts in online banking and the app."),
    _F(key="F8", title="Paperless Statements & Documents", epic="E2", team="Digital Accounts", contributing=[],
       state="Closed", closed_sprint=13, start=9, target=13, bv=5, tc=5, effort=52, risk=3, tags=[],
       description="eStatements, tax documents and notices in a secure document center; suppress paper for enrolled members."),
    _F(key="F9", title="Real-Time Fraud Alerts", epic="E1", team="Mobile Banking",
       contributing=["Security", "Core Platform"], state="Active", start=13, target=16, bv=20, tc=20, effort=51,
       risk=1, tags=["PI4-Committed", "cross-team"],
       description="Alert members in real time about suspicious transactions and let them confirm or deny in the app."),
    _F(key="F10", title="Fraud Scoring Engine v2", epic="E1", team="Security", contributing=[], state="Active",
       start=9, target=17, original_target=15, bv=13, tc=13, effort=65, risk=2, tags=["PI4-Committed"],
       description="Machine-learning fraud scoring with real-time risk scores, explainable reason codes and model governance."),
    _F(key="F11", title="Adaptive Multi-Factor Authentication", epic="E1", team="Security", contributing=[],
       state="Active", start=10, target=16, bv=13, tc=8, effort=43, risk=2, tags=["PI4-Committed"],
       description="Risk-based MFA: challenge members only when the risk justifies it; passkeys and recovery."),
    _F(key="F12", title="Account Takeover Protection", epic="E1", team="Security", contributing=[], state="New",
       start=17, target=20, bv=13, tc=5, effort=34, risk=2, tags=["PI5-Candidate"],
       description="Detect and stop account takeover: credential stuffing, session hijack and suspicious profile changes."),
    _F(key="F13", title="Omnichannel Service Requests", epic="E3", team="Member Support", contributing=[],
       state="Active", start=11, target=15, bv=8, tc=8, effort=48, risk=2, tags=["PI4-Committed"],
       description="One service-request experience across app, web, phone and branch, with routing and status tracking."),
    _F(key="F14", title="Secure Messaging & Chat", epic="E3", team="Member Support", contributing=[], state="New",
       start=13, target=17, bv=8, tc=5, effort=34, risk=2, tags=["PI4-Committed"],
       description="Secure chat between members and agents, with file upload, transcripts and bot handoff."),
    _F(key="F15", title="Agent Knowledge Base", epic="E3", team="Member Support", contributing=[], state="Active",
       start=9, target=12, bv=5, tc=3, effort=40, risk=3, tags=[],
       description="A searchable knowledge base for support agents, with approval workflow and suggested articles."),
    _F(key="F16", title="Callback Scheduling", epic="E3", team="Member Support", contributing=[], state="New",
       start=17, target=19, bv=5, tc=5, effort=21, risk=3, tags=["PI5-Candidate"],
       description="Members book a callback slot instead of waiting on hold."),
    _F(key="F17", title="Online Appointment Scheduling", epic="E4", team="Branch Experience", contributing=[],
       state="Closed", closed_sprint=12, start=9, target=12, bv=8, tc=8, effort=46, risk=3, tags=[],
       description="Book, reschedule and cancel branch appointments online, with reminders and banker calendars."),
    _F(key="F18", title="In-Branch Digital Onboarding", epic="E4", team="Branch Experience", contributing=[],
       state="Active", start=13, target=17, bv=13, tc=8, effort=33, risk=2, tags=["PI4-Committed"],
       description="Paperless onboarding at the branch on a tablet, reusing data members entered online."),
    _F(key="F19", title="Lobby Check-In & Queue Management", epic="E4", team="Branch Experience", contributing=[],
       state="Active", start=11, target=15, bv=5, tc=3, effort=33, risk=3, tags=["PI4-Committed"],
       description="Check in on arrival, see the wait time and get a text when a banker is ready."),
    _F(key="F20", title="Teller Workstation Refresh", epic="E4", team="Branch Experience", contributing=[],
       state="New", start=18, target=20, bv=5, tc=2, effort=21, risk=3, tags=["PI5-Candidate"],
       description="Modernize teller workstations: hardware, transaction screens and cash drawer integration."),
    _F(key="F21", title="Audit Evidence Automation", epic="E6", team="Security", contributing=[], state="Active",
       start=12, target=18, bv=8, tc=20, effort=43, risk=1, tags=["mandatory"],
       description="Automate collection and indexing of control evidence for the regulatory examination."),
    _F(key="F22", title="Access Review Automation", epic="E6", team="Security", contributing=["Core Platform"],
       state="Active", start=13, target=18, bv=5, tc=20, effort=23, risk=2, tags=["mandatory", "cross-team"],
       description="Automated quarterly access reviews and certification campaigns with exam-ready reporting."),
    _F(key="F23", title="Unified Notification Service", epic="E5", team="Core Platform", contributing=[],
       state="Active", start=11, target=15, bv=8, tc=13, effort=38, risk=2, tags=["PI4-Committed", "enabler"],
       value_area="Architectural",
       description="One service for email, SMS and push notifications with templates, preferences and delivery tracking."),
    _F(key="F24", title="Member API Gateway", epic="E5", team="Core Platform", contributing=[], state="Active",
       start=9, target=16, bv=8, tc=8, effort=68, risk=3, tags=["PI4-Committed", "enabler"],
       value_area="Architectural",
       description="Secure, versioned APIs for members' accounts, transactions and cards, for apps and partners."),
]
FEATURE_PRIORITY = {1: ["F2", "F5", "F9", "F10", "F21"],
                    2: ["F1", "F3", "F6", "F8", "F11", "F13", "F17", "F18", "F22", "F23", "F24"],
                    3: ["F4", "F7", "F12", "F14", "F15", "F19"],
                    4: ["F16", "F20"]}
RISK_LABEL = {1: "1 - High", 2: "2 - Medium", 3: "3 - Low"}
SEVERITY_LABEL = {1: "1 - Critical", 2: "2 - High", 3: "3 - Medium", 4: "4 - Low"}

# Tags that are added by a later revision rather than at creation: (tag, sprint, day).
TAG_EVENTS = {"PI4-Committed": (12, 9), "PI5-Candidate": (13, 8), "at-risk": (13, 6)}
AT_RISK_COMMENT = "Flagging F2 at risk: carry-over keeps growing and stories are queuing for QA."
PI4_COMMENT = "Committed in PI 4 planning."
PI5_COMMENT = "Proposed as a PI 5 candidate."

F10_CHANGE = dict(sprint=14, day=2, old_target=15, new_target=17, by="Aisha Karimi",
                  comment=("Re-planned: exam-readiness work (F21/F22) takes priority until exam fieldwork in Sprint 18. "
                           "The risk-score API for Fraud Alerts moves to Sprint 16. — AK"))

# ----------------------------------------------------------------------------- section 6: sprint history
# Each team: "table" (Planned/Done/n/Carry per sprint, Bible's own columns), "mix" (closed-story mix by
# Feature: (n, pts)), "carries" (stories carried from sprint s to s+1 AND closed there:
# (from_sprint, feature|None, n, pts)), "cycle" (target average Activated->Closed days).
# Carry-overs into Sprint 14 are the explicit Sprint 14 items marked carried (below).
HISTORY = {
    "Mobile Banking": dict(
        table={9: (38, 33, 12, (2, 5)), 10: (44, 37, 12, (3, 7)), 11: (50, 41, 13, (4, 9)),
               12: (56, 45, 12, (5, 11)), 13: (62, 44, 12, (6, 18))},
        mix={9: {"F1": (9, 24), None: (3, 9)},
             10: {"F1": (6, 18), "F2": (3, 8), None: (3, 11)},
             11: {"F1": (4, 13), "F2": (5, 16), None: (4, 12)},
             12: {"F2": (4, 15), "F3": (4, 14), None: (4, 16)},
             13: {"F2": (3, 11), "F3": (3, 10), None: (6, 23)}},
        # S12->S13 also carries F2 1/5 = Sprint 14 item #1, which is NOT closed in S13 (explicit item).
        carries=[(9, "F1", 1, 3), (9, None, 1, 2), (10, "F1", 1, 2), (10, "F2", 1, 3), (10, None, 1, 2),
                 (11, "F2", 2, 5), (11, None, 2, 4), (12, "F3", 1, 3), (12, None, 3, 3)],
        cycle={9: 3.5, 10: 4.5, 11: 6.0, 12: 7.5, 13: 9.0},
        resolved_dwell={9: 1.0, 10: 1.5, 11: 2.5, 12: 3.5, 13: 4.5},
        always_resolved=True, carried_started=True,
    ),
    "Digital Accounts": dict(
        table={9: (26, 24, 9, (1, 2)), 10: (26, 26, 10, (0, 0)), 11: (25, 25, 10, (0, 0)),
               12: (27, 24, 9, (1, 3)), 13: (26, 26, 10, (0, 0))},
        mix={9: {"F8": (7, 19), None: (2, 5)},
             10: {"F8": (5, 13), "F7": (4, 10), None: (1, 3)},
             11: {"F8": (4, 10), "F7": (3, 8), "F6": (2, 5), None: (1, 2)},
             12: {"F8": (2, 5), "F7": (3, 8), "F6": (4, 11)},
             13: {"F8": (2, 5), "F7": (2, 5), "F6": (5, 14), None: (1, 2)}},
        carries=[(9, "F8", 1, 2), (12, "F6", 1, 3)],
        cycle={9: 4.5, 10: 4.5, 11: 4.5, 12: 4.5, 13: 4.5},
    ),
    "Security": dict(
        table={9: (24, 22, 8, (1, 2)), 10: (25, 21, 8, (1, 4)), 11: (26, 22, 8, (1, 4)),
               12: (30, 21, 7, (3, 9)), 13: (32, 20, 7, (4, 12))},
        mix={9: {"F10": (5, 14), None: (3, 8)},
             10: {"F10": (4, 11), "F11": (3, 8), None: (1, 2)},
             11: {"F10": (3, 9), "F11": (3, 8), None: (2, 5)},
             12: {"F10": (2, 6), "F11": (2, 5), "F21": (3, 10)},
             13: {"F10": (1, 3), "F11": (1, 3), "F21": (3, 9), "F22": (2, 5)}},
        carries=[(9, "F10", 1, 2), (10, "F11", 1, 4), (11, "F10", 1, 4), (12, "F10", 1, 3), (12, "F21", 2, 6)],
        cycle={9: 4.0, 10: 4.5, 11: 5.0, 12: 4.5, 13: 5.0},
    ),
    "Core Platform": dict(
        table={9: (21, 20, 7, (1, 1)), 10: (22, 20, 7, (1, 2)), 11: (21, 21, 7, (0, 0)),
               12: (21, 19, 7, (1, 2)), 13: (22, 20, 7, (1, 2))},
        mix={9: {"F24": (5, 15), None: (2, 5)},
             10: {"F24": (5, 14), None: (2, 6)},
             11: {"F24": (3, 9), "F23": (3, 9), None: (1, 3)},
             12: {"F24": (3, 8), "F23": (3, 9), None: (1, 2)},
             13: {"F24": (2, 6), "F23": (4, 11), None: (1, 3)}},
        carries=[(9, "F24", 1, 1), (10, "F24", 1, 2), (12, "F24", 1, 2)],
        cycle={9: 4.0, 10: 4.5, 11: 4.0, 12: 4.5, 13: 4.0},
    ),
    "Branch Experience": dict(
        table={9: (19, 18, 7, (1, 1)), 10: (20, 17, 6, (1, 3)), 11: (18, 18, 7, (0, 0)),
               12: (19, 16, 6, (1, 3)), 13: (20, 18, 7, (1, 2))},
        mix={9: {"F17": (6, 16), None: (1, 2)},
             10: {"F17": (5, 14), None: (1, 3)},
             11: {"F17": (4, 11), "F19": (3, 7)},
             12: {"F17": (2, 5), "F19": (3, 8), None: (1, 3)},
             13: {"F19": (3, 8), "F18": (2, 5), None: (2, 5)}},
        carries=[(9, "F17", 1, 1), (10, "F17", 1, 3), (12, "F19", 1, 3)],
        cycle={9: 4.5, 10: 4.0, 11: 4.5, 12: 5.0, 13: 4.5},
    ),
    "Member Support": dict(
        # "True delivery" table (section 6.6). What Azure DevOps records differs (planted problems).
        table={9: (20, 18, 7, (1, 2)), 10: (19, 17, 6, (1, 2)), 11: (21, 19, 7, (1, 2)),
               12: (20, 18, 7, (1, 2)), 13: (21, 19, 7, (1, 2))},
        mix={9: {"F15": (5, 13), None: (2, 5)},
             10: {"F15": (5, 14), None: (1, 3)},
             11: {"F15": (3, 8), "F13": (4, 11)},
             12: {"F15": (2, 5), "F13": (4, 11), None: (1, 2)},
             13: {"F13": (4, 11), "F14": (2, 5), None: (1, 3)}},
        carries=[(9, "F15", 1, 2), (10, "F15", 1, 2), (11, "F13", 1, 2), (12, "F13", 1, 2)],
        cycle={9: 4.5, 10: 4.0, 11: 4.5, 12: 4.5, 13: 5.0},
        recorded_velocity=[18, 17, 19, 13, 8],
    ),
}

# Explicit specs for *new* (non-carried) items of some (team, sprint, feature) groups, plus the final
# outcome of carried-in items. Used for Member Support's "done but left in Resolved" and missing points.
HISTORY_OVERRIDES = {
    ("Member Support", 12, "F13"): dict(
        carry_in_outcome="Resolved",
        new=[dict(pts=3, outcome="Resolved"), dict(pts=3, outcome="Closed", tags=["omnichannel"]),
             dict(pts=3, outcome="Closed")]),
    ("Member Support", 13, "F13"): dict(
        carry_in_outcome="Resolved",
        new=[dict(pts=3, outcome="Resolved", tags=["omni-channel"]),
             dict(title="Request category taxonomy cleanup", pts=None, true_pts=3, outcome="Closed"),
             dict(pts=3, outcome="Closed", tags=["omnichannel"])]),
    ("Member Support", 13, "F14"): dict(
        new=[dict(pts=3, outcome="Resolved"), dict(pts=2, outcome="Closed")]),
}

# ----------------------------------------------------------------------------- history titles
# One title per generated history story, consumed in creation order within each (team, group).
HISTORY_TITLES = {
    ("Mobile Banking", "F1"): [
        "Redesigned home screen layout", "New navigation tab bar", "Account summary cards",
        "Design system color tokens in the app", "Typography and spacing update", "Redesigned login screen",
        "Transaction list with infinite scroll", "Transaction detail view redesign", "Quick actions on home screen",
        "Redesigned transfer flow screens", "Empty states and loading skeletons",
        "Profile and settings screen redesign", "Redesigned bill pay entry screen",
        "Accessibility labels for redesigned screens", "In-app tour of the redesigned app",
        "Redesigned alerts and messages inbox", "Haptic feedback on key actions",
        "Tablet layout for redesigned home screen", "What's new screen for the redesigned app"],
    ("Mobile Banking", "F2"): [
        "New check capture camera screen", "Front and back capture guidance overlay",
        "Deposit amount entry with validation", "Choose the deposit account", "Upload check images to deposit service",
        "Deposit review and submit screen", "Deposit status in the activity feed", "Automatic cropping of check images",
        "Blur and glare detection on capture", "Deposit limit check before submission",
        "Deposit receipt with confirmation number", "Explain rejected deposits with reason codes",
        "Push notification when a deposit clears", "Mobile deposit terms acceptance", "Deposit funnel analytics events"],
    ("Mobile Banking", "F3"): [
        "Face ID login on iOS", "Fingerprint login on Android", "Biometric opt-in prompt after password login",
        "Secure key storage for biometric tokens", "Biometric login toggle in settings",
        "Disable biometrics after a password change", "Biometric login error messages"],
    ("Mobile Banking", None): [
        "Fix layout glitches on small screens", "Seasonal app icon for marketing campaign", "Upgrade crash reporting SDK",
        "Remove deprecated payee API calls", "Rate-the-app prompt", "iOS 18 compatibility fixes",
        "Android 15 target SDK update", "Branch locator map performance", "Marketing banner carousel on home screen",
        "Refactor the networking layer", "Rotate certificate pins", "In-app feedback form",
        "Contact us screen refresh", "Replace legacy charting library", "Login rate limit messaging",
        "App startup time optimization", "Offline mode banner", "Promotional rates widget for marketing",
        "Migrate push tokens to the new provider", "Spanish translations for app strings"],
    ("Digital Accounts", "F8"): [
        "eStatement enrollment toggle", "Monthly statement PDF viewer", "Seven-year statement archive",
        "Paperless consent capture and audit", "Email when a new statement is ready", "Tax document (1099-INT) download",
        "Download statements as PDF", "Paperless enrollment banner at login", "Document center navigation",
        "Notices and disclosures inbox", "Statement rendering service integration",
        "Paperless enrollment for joint accounts", "Suppress paper statements in the print vendor feed",
        "Accessible PDF statements", "Statement search by account", "Document retention rules",
        "Paperless reminders for members not enrolled", "Year-end summary document",
        "Handle statement delivery failures", "Paperless adoption reporting"],
    ("Digital Accounts", "F7"): [
        "Transaction categorization engine", "Spending by category chart", "Monthly spending trend view",
        "Recategorize a transaction", "Merchant name cleanup rules", "Income vs spending summary",
        "Insights card on the home dashboard", "Recurring charges detection", "Category drill-down list",
        "Spending insights opt-out setting", "Weekly spending digest notification", "Insights performance caching"],
    ("Digital Accounts", "F6"): [
        "Product selection step for new members", "Applicant identity details form",
        "Eligibility and membership questions", "Real-time identity verification integration",
        "Disclosures and e-sign consent", "Application review summary page", "Account number provisioning",
        "Duplicate applicant detection", "Application abandonment analytics", "Application status emails",
        "Mobile-friendly application layout"],
    ("Digital Accounts", None): [
        "Session timeout warning dialog", "Update online banking footer links", "Upgrade frontend build tooling",
        "Fix date picker on Safari", "Retire legacy password reset page"],
    ("Security", "F10"): [
        "Feature store for transaction signals", "Model training pipeline for fraud scoring",
        "Real-time scoring service skeleton", "Device fingerprint signal ingestion", "Geo-velocity risk signal",
        "Reason codes for fraud scores", "Score threshold configuration", "Champion-challenger model routing",
        "Historical backtest harness", "Analyst case queue integration", "Score audit logging",
        "Model retraining schedule", "False positive review workflow", "Scoring API authentication",
        "Fraud label feedback ingestion"],
    ("Security", "F11"): [
        "Risk-based authentication decision service", "SMS one-time passcode fallback", "Authenticator app enrollment",
        "Login risk signals from device and location", "MFA challenge screen in online banking",
        "Remember this device option", "MFA event logging for audit", "Step-up authentication for payee changes",
        "MFA policy admin console"],
    ("Security", "F21"): [
        "Evidence repository structure for the exam", "Automated change-management evidence export",
        "Control owner evidence reminders", "Evidence index for examiners", "Firewall rule review evidence capture",
        "Backup and recovery test evidence"],
    ("Security", "F22"): ["Access review data model", "Entitlement extract from the HR system"],
    ("Security", None): [
        "Patch vulnerable TLS library", "Rotate service account secrets", "Phishing simulation reporting",
        "Penetration test remediation items", "SIEM alert tuning", "Security awareness training tracker"],
    ("Core Platform", "F24"): [
        "API gateway infrastructure provisioning", "OAuth 2.0 token service for member APIs", "Accounts API v1",
        "Transactions API v1", "API versioning strategy", "Gateway request logging and tracing", "Member profile API",
        "API throttling policies", "Payments API v1", "Standard API error contract",
        "Gateway health checks and alerts", "Blue-green deployment for the gateway", "API key management for partners",
        "Cards API v1", "Publish OpenAPI documentation", "Gateway caching for read endpoints",
        "Contract tests for core APIs", "Gateway autoscaling rules"],
    ("Core Platform", "F23"): [
        "Notification service architecture spike", "Email channel adapter", "SMS channel adapter",
        "Push notification channel adapter", "Notification event schema", "Delivery retry queue",
        "Member contact preference lookup", "Notification audit trail", "Quiet hours enforcement",
        "Notification service monitoring dashboard"],
    ("Core Platform", None): [
        "Upgrade Kubernetes cluster version", "Database connection pool tuning", "Migrate build agents to new images",
        "Reduce log retention costs", "Decommission old file transfer server", "Terraform module cleanup",
        "Disaster recovery failover test"],
    ("Branch Experience", "F17"): [
        "Appointment booking page", "Branch and service selection", "Available time slot lookup",
        "Appointment confirmation email", "Reschedule an appointment", "Cancel an appointment",
        "Appointment reminders by text", "Banker calendar sync", "Appointment types configuration",
        "Banker availability management", "Book appointments from the mobile app", "Add an appointment to my calendar",
        "Walk-in vs appointment reporting", "Accessibility review for the booking flow", "Appointment notes for bankers",
        "No-show tracking", "Appointment scheduling analytics"],
    ("Branch Experience", "F19"): [
        "Lobby check-in tablet app", "Check in by phone number", "Visit reason selection", "Banker queue dashboard",
        "Estimated wait time calculation", "Check in with an existing appointment", "Banker can reorder the queue",
        "Lobby screen display layout", "Check-in privacy notice"],
    ("Branch Experience", "F18"): ["Branch onboarding workflow design", "Member identity lookup at the branch"],
    ("Branch Experience", None): [
        "Branch printer driver update", "Fix teller login timeout", "Branch guest Wi-Fi portal refresh",
        "Update branch hours on the website", "Replace signature pads at pilot branches"],
    ("Member Support", "F15"): [
        "Knowledge base article editor", "Article search for agents", "Article categories and tags",
        "Article approval workflow", "Suggested articles in the agent console", "Article feedback ratings",
        "Import legacy help documents", "Article version history", "Knowledge base access permissions",
        "Article usage reporting", "Related articles panel", "Article expiry reminders",
        "Search synonyms for banking terms", "Knowledge base performance tuning", "Knowledge base guide for agents"],
    ("Member Support", "F13"): [
        "Service request data model", "Request intake API", "Agent request queue", "Assign requests to agents",
        "Request status change audit log", "Request priority levels", "Request search for agents",
        "Request history timeline", "Request categories configuration", "Internal notes on requests",
        "Reopen a request"],
    ("Member Support", "F14"): ["Secure chat session service", "Chat entry point in online banking"],
    ("Member Support", None): [
        "Update support phone tree messages", "Agent console login performance", "Fix ticket export encoding",
        "Retire legacy email-to-ticket gateway", "Agent console browser compatibility fixes"],
}

# ----------------------------------------------------------------------------- Sprint 14 items (exact)
# carried: sprints the item lived in before Sprint 14 (e.g. (12, 13) = carried twice).
# added_day: created mid-sprint on that Sprint 14 day (not in Planned). created_day: created on that
# Sprint 14 day directly in the sprint. stale_days / resolved_days_ago: now-relative planted facts.
def _s(title, parent, pts, state, assigned=None, **kw):
    return dict(title=title, parent=parent, pts=pts, state=state, assigned=assigned, **kw)


S14_ITEMS = {
    "Mobile Banking": [
        _s("Auto-capture check edges with on-device ML", "F2", 5, "Active", "Ethan Brooks", n=1, carried=(12, 13), stale_days=9),
        _s("Deposit limit messaging by member tier", "F2", 3, "Resolved", "Mei Tanaka", n=2, carried=(13,), resolved_days_ago=6),
        _s("Retry flow for failed check uploads", "F2", 3, "Active", "Ethan Brooks", n=3, carried=(13,), stale_days=10),
        _s("Face ID and fingerprint enrollment", "F3", 3, "Resolved", "Jamal Washington", n=4, carried=(13,), resolved_days_ago=5),
        _s("Dark mode polish for redesigned screens", None, 2, "Active", "Sofia Rossi", n=5, carried=(13,)),
        _s("Upgrade analytics SDK", None, 2, "New", None, n=6, carried=(13,), tags=["tech-debt"]),
        _s("Real-time image quality feedback", "F2", 5, "Closed", "Mei Tanaka", n=7),
        _s("Endorsement detection on check back", "F2", 5, "Active", "Ethan Brooks", n=8),
        _s("Duplicate check detection", "F2", 3, "New", None, n=9),
        _s("Deposit history with check images", "F2", 3, "New", "Jamal Washington", n=10),
        _s("Accessibility fixes for deposit flow", "F2", 2, "Closed", "Sofia Rossi", n=11),
        _s("Biometric step-up for high-risk actions", "F3", 5, "Resolved", "Jamal Washington", n=12, resolved_days_ago=2),
        _s("Passcode fallback when biometrics fail", "F3", 3, "Closed", "Sofia Rossi", n=13),
        _s("Fraud alert preferences in app settings", "F9", 3, "Active", "Sofia Rossi", n=14),
        _s("Member confirms or denies a flagged transaction", "F9", 8, "Active", "Mei Tanaka", n=15, key="MB-15",
           comment=(3, "UI done; can't integrate until Security's risk-score API exists.", ["blocked"])),
        _s("Fraud alert UX design spike", "F9", 2, "Closed", "Jamal Washington", n=16),
        _s("Holiday promo banner (marketing request)", None, 3, "Active", "Ethan Brooks", n=17, added_day=3, tags=["unplanned"]),
        _s("App Store listing refresh", None, 2, "New", "Sofia Rossi", n=18, added_day=4, tags=["unplanned"]),
        _s("Upgrade push notification SDK", None, 3, "New", None, n=19, tags=["tech-debt"]),
    ],
    "Digital Accounts": [
        _s("ID document capture with auto-crop", "F6", 5, "Active", "Olivia Grant"),
        _s("Instant account funding by debit card", "F6", 3, "Closed", "Noah Kim"),
        _s("Application save and resume", "F6", 3, "Active", "Fatima Hassan"),
        _s("Joint applicant invitation", "F6", 3, "New", None),
        _s("Address verification for applicants", "F6", 3, "New", "Lucas Meyer"),
        _s("Monthly spending summary email", "F7", 3, "Closed", "Lucas Meyer"),
        _s("Category budget alerts", "F7", 2, "Closed", "Lucas Meyer"),
        _s("Merchant logo enrichment", "F7", 2, "Closed", "Chloe Martin"),
        _s("Statement search by date range", None, 2, "Active", "Noah Kim"),
    ],
    "Security": [
        _s("Automate evidence export for access logs", "F21", 5, "Active", "Viktor Novak", carried=(13,), tags=["compliance"]),
        _s("Quarterly control attestation workflow", "F21", 3, "Active", "Rachel Stein", carried=(13,), tags=["compliance"]),
        _s("Orphaned account detection", "F22", 2, "New", "Kwame Mensah", carried=(13,), tags=["compliance"]),
        _s("Model monitoring for fraud scores", "F10", 2, "Active", "Omar Haddad", carried=(13,)),
        _s("Evidence retention policy enforcement", "F21", 3, "Closed", "Omar Haddad", tags=["compliance"]),
        _s("Remediate mock-exam findings", "F21", 3, "Active", "Omar Haddad", tags=["compliance"]),
        _s("Privileged access review automation", "F22", 5, "Active", "Ingrid Larsen", tags=["compliance"]),
        _s("Velocity rules for card-not-present fraud", "F10", 5, "Active", "Kwame Mensah"),
        _s("Trusted device list management", "F11", 3, "Closed", "Ingrid Larsen"),
        _s("Risk-based MFA policy engine", "F11", 5, "New", None),
    ],
    "Core Platform": [
        _s("Notification templates service", "F23", 2, "Active", "Julia Weber", carried=(13,)),
        _s("High-priority push channel for fraud alerts", "F9", 5, "Active", "Sam Okoro", key="CP-1"),
        _s("Rate limiting for partner APIs", "F24", 3, "Closed", "Arjun Mehta"),
        _s("API gateway developer portal", "F24", 5, "Active", "Elena Popescu"),
        _s("SMS delivery status webhooks", "F23", 2, "Closed", "Julia Weber"),
        _s("Load test notification service", "F23", 2, "New", None),
        _s("Deprecate legacy SOAP endpoints", None, 3, "New", None, tags=["tech-debt"]),
    ],
    "Branch Experience": [
        _s("Branch tablet kiosk mode", "F18", 2, "Active", "Daniel Park", carried=(13,)),
        _s("Digital signature capture for account forms", "F18", 5, "Active", "Zoe Clarke"),
        _s("Pre-fill member data from online application", "F18", 3, "New", None),
        _s("Queue wait-time display for lobby screens", "F19", 3, "Closed", "Ravi Shankar"),
        _s("Text members when it is their turn", "F19", 2, "Closed", "Tomas Herrera"),
        _s("Lobby check-in analytics", "F19", 2, "Active", "Ravi Shankar"),
        _s("Branch staff training mode", None, 2, "New", None),
    ],
    "Member Support": [
        _s("Service request status tracker", "F13", 2, "Active", "Leila Ahmadi", carried=(13,), tags=["omnichannel"]),
        _s("Service request status tracker", "F13", 2, "New", None, created_day=1, tags=["omni-channel"], duplicate=True),
        _s("Unified request intake form", "F13", 3, "Resolved", "Marco Bianchi", tags=["omnichannel"]),
        _s("Request routing rules", "F13", 3, "Active", "Nora Fitzgerald", tags=["omni-channel"]),
        _s("Request SLA timers", "F13", 3, "New", None, tags=["omnichanel"]),
        _s("Chat transcript export", "F14", 3, "Closed", "Marco Bianchi"),
        _s("Secure file upload in chat", "F14", 5, "Active", "Nora Fitzgerald"),
        _s("Typing indicators and read receipts", "F14", 2, "Active", "Leila Ahmadi"),
    ],
}

# ----------------------------------------------------------------------------- explicit future items
# (team, parent, title, pts, sprint or None = backlog/unscheduled, key or None)
FUTURE_ITEMS = [
    # 5.0b F2 (all New, Sprint 15)
    ("Mobile Banking", "F2", "Endorsement guidance animation", 3, 15, None),
    ("Mobile Banking", "F2", "Deposit hold explanations", 3, 15, None),
    ("Mobile Banking", "F2", "Multiple checks in one deposit session", 8, 15, None),
    # 5.0b F3
    ("Mobile Banking", "F3", "Biometric consent and privacy notice", 3, 15, None),
    ("Mobile Banking", "F3", "Biometric login analytics", 2, 15, None),
    ("Mobile Banking", "F3", "Re-enroll biometrics after device change", 5, 16, None),
    ("Mobile Banking", "F3", "Biometric login on tablets", 3, 16, None),
    ("Security", "F3", "Device binding risk signal", 3, 15, None),
    # section 7: F9 story-level
    ("Mobile Banking", "F9", "Show real-time fraud alert in the app", 5, 15, "MB-2"),
    ("Mobile Banking", "F9", "Push notification for high-risk transactions", 5, 15, "MB-4"),
    ("Mobile Banking", "F9", "Auto-lock card after a member denies a transaction", 5, 16, "MB-5"),
    ("Mobile Banking", "F9", "Fraud alert copy and accessibility review", 2, 16, "MB-6"),
    ("Security", "F9", "Real-time fraud risk score API", 8, 16, "SEC-1"),
    ("Security", "F9", "Alert decision feedback to fraud engine", 5, 16, "SEC-2"),
    ("Core Platform", "F9", "Alert delivery receipts and retry", 3, 15, "CP-2"),
    # 6.2 Digital Accounts
    ("Digital Accounts", "F6", "Fraud screening at account opening", 5, 15, None),
    ("Digital Accounts", "F6", "Welcome journey emails", 2, 16, None),
    ("Digital Accounts", "F6", "Accessibility audit for account opening", 2, 16, None),
    ("Digital Accounts", "F7", "Spending trends year over year", 3, 15, None),
    ("Digital Accounts", "F7", "Export insights to CSV", 2, 15, None),
    # 6.3 Security
    ("Security", "F10", "Merchant risk signals in scoring", 5, 15, None),
    ("Security", "F10", "Shadow-mode scoring comparison", 3, 16, None),
    ("Security", "F10", "Scoring latency under 150 ms", 5, 17, None),
    ("Security", "F10", "Model governance documentation", 2, 17, None),
    ("Security", "F11", "Passkey enrollment", 5, 15, None),
    ("Security", "F11", "MFA recovery flow", 3, 16, None),
    ("Security", "F11", "Step-up challenges for wire transfers", 3, 16, None),
    ("Security", "F21", "Exam request portal for auditors", 5, 15, None),
    ("Security", "F21", "Control testing evidence pack", 3, 16, None),
    ("Security", "F21", "Mock exam #2 readiness", 2, 17, None),
    ("Security", "F22", "Quarterly access certification campaign", 5, 15, None),
    ("Security", "F22", "Access review reporting for exam", 3, 16, None),
    ("Core Platform", "F22", "Service account inventory", 3, 15, None),
    # F12: 8 New stories (34 pts) S17-S20 (titles/points/sprints chosen here; totals per Bible)
    ("Security", "F12", "Account takeover risk signals", 5, 17, None),
    ("Security", "F12", "New device login alerts", 3, 17, None),
    ("Security", "F12", "Credential stuffing detection", 8, 18, None),
    ("Security", "F12", "Session hijack detection", 5, 18, None),
    ("Security", "F12", "Account recovery hardening", 5, 19, None),
    ("Security", "F12", "Hold suspicious profile changes", 3, 19, None),
    ("Security", "F12", "Takeover case management workflow", 3, 20, None),
    ("Security", "F12", "Member education on account takeover", 2, 20, None),
    # 6.4 Core Platform
    ("Core Platform", "F23", "Notification preferences API", 3, 15, None),
    ("Core Platform", "F24", "API usage analytics", 3, 15, None),
    ("Core Platform", "F24", "Partner onboarding automation", 5, 16, None),
    # 6.5 Branch Experience
    ("Branch Experience", "F19", "Appointment-to-lobby handoff", 3, 15, None),
    ("Branch Experience", "F18", "ID scan at branch onboarding", 5, 15, None),
    ("Branch Experience", "F18", "Same-day debit card printing integration", 5, 16, None),
    ("Branch Experience", "F18", "Onboarding checklist for branch staff", 3, 16, None),
    ("Branch Experience", "F18", "Digital welcome packet", 2, 17, None),
    ("Branch Experience", "F18", "Large-text and accessibility mode", 3, 17, None),
    ("Branch Experience", "F20", "Teller workstation rollout plan", 3, 18, None),
    ("Branch Experience", "F20", "New teller transaction screen", 5, 18, None),
    ("Branch Experience", "F20", "Cash drawer integration", 5, 19, None),
    ("Branch Experience", "F20", "Quick member lookup for tellers", 5, 19, None),
    ("Branch Experience", "F20", "Teller workstation training", 3, 20, None),
    # 6.6 Member Support
    ("Member Support", "F13", "Member notifications on request updates", None, None, None),
    ("Member Support", "F13", "Agent workload balancing", None, None, None),
    ("Member Support", "F14", "Co-browse for complex requests", None, None, None),
    ("Member Support", "F14", "Chatbot handoff to agent", 5, 16, None),
    ("Member Support", "F16", "Callback request from the app", 5, 17, None),
    ("Member Support", "F16", "Callback queue for agents", 3, 18, None),
    ("Member Support", "F16", "Callback outcome tracking", 3, 18, None),
    ("Member Support", "F16", "Callback analytics", 2, 19, None),
]

# F5 Instant Card Controls: 20 child stories, all New, unscheduled, in this order. (title, pts, mvp)
F5_STORIES = [
    ("Card lock and unlock service and API", 8, True),
    ("Lock and unlock a card in online banking and the app", 5, True),
    ("Real-time card status sync with card processor", 8, True),
    ("Travel notice self-service", 5, True),
    ("Travel notice auto-expiry and reminders", 3, False),  # the "should" item
    ("Card control change notifications", 5, True),
    ("Card controls audit trail", 5, True),
    ("Accessibility review for card controls", 3, True),
    ("Fraud team view of member-locked cards", 5, True),
    ("Spending limits by category", 8, False),
    ("Merchant category blocking", 13, False),
    ("International transaction toggle", 5, False),
    ("Report a lost or stolen card and order a replacement", 8, False),
    ("Digital wallet token controls", 13, False),
    ("Support agent console for card controls", 8, False),
    ("Card controls analytics events", 3, False),
    ("Recurring payment exceptions when a card is locked", None, False),
    ("Joint owner permissions for card controls", None, False),
    ("Business debit card controls", None, False),
    ("Spending alerts by threshold", None, False),
]
F5_SHOULD_INDEX = 5  # 1-based order of the "should" item

# Digital Accounts backlog order rule (section 6.2): in-progress Sprint 14 items, then the remaining
# committed F6/F7 work (all New, 20 pts) in this order, then F5 in order, then everything else.
DA_COMMITTED_ORDER = ["Joint applicant invitation", "Address verification for applicants",
                      "Fraud screening at account opening", "Welcome journey emails",
                      "Accessibility audit for account opening", "Spending trends year over year",
                      "Export insights to CSV"]

# ----------------------------------------------------------------------------- Member Support planted (6.6, 9)
MS_ZOMBIES = [  # Active, Iteration = Sprint 12, added mid-S12, never moved
    dict(title="Escalation rules for priority members", parent="F13", pts=3, assigned="Kyle Morgan", day=3,
         tags=["omnichannel"]),
    dict(title="Agent presence indicator", parent="F13", pts=5, assigned="Kyle Morgan", day=3, tags=["omnichannel"]),
    dict(title="Request attachment virus scanning", parent="F13", pts=2, assigned="Nora Fitzgerald", day=4,
         tags=["omnichanel"]),
]
MS_KYLE_BACKLOG = [  # New, backlog, under F16, assigned to Kyle Morgan (created before he left)
    dict(title="Callback time-slot picker", parent="F16", pts=5),
    dict(title="Callback reminders by text", parent="F16", pts=3),
]
KYLE_LEFT_SPRINT = 12
# 4 Removed stories (descoped F13/F15 ideas). Generated as unparented so F13/F15 child counts stay exact.
MS_REMOVED = [
    dict(title="Public FAQ portal for the knowledge base", pts=5, created=(10, 3), removed=(12, 2)),
    dict(title="Voice transcription for service requests", pts=8, created=(11, 2), removed=(12, 6)),
    dict(title="Agent leaderboard and badges", pts=3, created=(10, 7), removed=(13, 2)),
    dict(title="Service requests by SMS", pts=None, created=(11, 8), removed=(13, 7)),
]

# ----------------------------------------------------------------------------- dependencies (section 7)
# (predecessor key, successor key). Stored on the successor as a "Predecessor" link.
DEPENDENCIES = [("F10", "F9"), ("F23", "F9"), ("F24", "F4"),
                ("SEC-1", "MB-15"), ("SEC-1", "MB-2"), ("SEC-2", "MB-5"), ("CP-1", "MB-4"),
                ("F5-01", "MB-5")]
RELATED_LINKS = [  # context only: (key, key, comment)
    ("BUG-MOB-P5", "MB14-14", "Same settings screen"),
    ("BUG-MOB-P3", "F23", "Confirmation emails go through the notification service"),
]

# ----------------------------------------------------------------------------- bugs (sections 6.1, 6.2, 6.6)
# start = open bugs before Sprint 9; flow = {sprint: (opened, closed)}.
# Security, Core Platform and Branch Experience flows are NOT in the World Bible: small, steady,
# generated values (reported as a gap in facts.md).
BUG_FLOW = {
    "Mobile Banking": dict(start=8, flow={9: (4, 3), 10: (6, 3), 11: (8, 2), 12: (11, 3), 13: (13, 2), 14: (6, 1)}),
    "Digital Accounts": dict(start=7, flow={9: (3, 3), 10: (2, 3), 11: (3, 3), 12: (2, 3), 13: (2, 3), 14: (1, 1)}),
    "Member Support": dict(start=5, flow={9: (2, 2), 10: (2, 1), 11: (2, 2), 12: (3, 1), 13: (3, 1), 14: (2, 0)}),
    "Security": dict(start=3, flow={9: (1, 1), 10: (2, 1), 11: (1, 2), 12: (2, 1), 13: (1, 1), 14: (1, 0)}),
    "Core Platform": dict(start=2, flow={9: (1, 1), 10: (1, 1), 11: (2, 1), 12: (1, 2), 13: (1, 1), 14: (1, 0)}),
    "Branch Experience": dict(start=2, flow={9: (1, 1), 10: (1, 0), 11: (1, 2), 12: (1, 1), 13: (2, 1), 14: (0, 0)}),
}
BUG_FLOW_FROM_BIBLE = ("Mobile Banking", "Digital Accounts", "Member Support")

# Mobile open bugs now (42): exact distributions (section 6.1).
MOBILE_OPEN_SEVERITY = {1: 3, 2: 11, 3: 18, 4: 10}
MOBILE_OPEN_PRIORITY = {1: 4, 2: 14, 3: 18, 4: 6}
MOBILE_OPEN_STATE = {"New": 30, "Active": 9, "Resolved": 3}
MOBILE_ESCAPED_SINCE_S11 = 17  # of 38 bugs created since S11 (~45%)

PLANTED_BUGS = [
    dict(key="BUG-MOB-P1", team="Mobile Banking", title="Check deposit fails for images larger than 5 MB", parent="F2",
         priority=1, severity=2, state="New", assigned=None, created=(14, 2), tags=["escaped-defect"]),
    dict(key="BUG-MOB-P2", team="Mobile Banking", title="App crashes when switching accounts during deposit", parent="F2",
         priority=1, severity=1, state="Active", assigned="Ethan Brooks", created=(13, 3), tags=[]),
    dict(key="BUG-MOB-P3", team="Mobile Banking", title="Deposit confirmation email shows wrong amount", parent=None,
         priority=2, severity=2, state="Active", assigned="Ethan Brooks", created=(13, 6), tags=["escaped-defect"]),
    dict(key="BUG-MOB-P4", team="Mobile Banking", title="Biometric prompt loops on some Android devices", parent="F3",
         priority=2, severity=2, state="Active", assigned="Jamal Washington", created=(13, 8), tags=[]),
    dict(key="BUG-MOB-P5", team="Mobile Banking", title="Fraud alert toggle does not persist after logout", parent="F9",
         priority=2, severity=3, state="New", assigned=None, created=(14, 4), tags=[]),
]
# Section 9 #5: two P1 bugs filed at the ROOT area (not counted in Member Support's area flow).
# State and severity are not given in the Bible; they mirror the sandbox copy (New/Sev 2, Active/Sev 3).
ROOT_BUGS = [
    dict(key="BUG-ROOT-1", title="Chat disconnects after 60 seconds", parent=None, priority=1, severity=2,
         state="New", assigned=None, created=(14, 2), tags=[]),
    dict(key="BUG-ROOT-2", title="Service request emails sent twice", parent=None, priority=1, severity=3,
         state="Active", assigned="Marco Bianchi", created=(14, 3), tags=[]),
]

BUG_TITLES = {
    "Mobile Banking": [
        "Balance not refreshing after pull-to-refresh", "Transfer screen keyboard covers amount field",
        "Push notification opens the wrong account", "Login button unresponsive on slow networks",
        "Transaction search ignores accented characters", "Dark mode text unreadable on statements tab",
        "App freezes when rotating during login", "Duplicate transactions shown after reconnect",
        "Bill pay date picker allows weekends", "Account nickname truncated on home card",
        "Session expires during check capture", "VoiceOver reads wrong label on transfer button",
        "Pending transactions show the wrong sign", "Quick balance widget shows stale data",
        "Payee list sorts incorrectly", "App crashes on launch after OS update",
        "Check image upload hangs at 99%", "Deposit amount field accepts letters",
        "Wrong deposit limit shown for joint accounts", "Camera permission prompt shown twice",
        "Front image cropped incorrectly on small phones", "Deposit history missing after app restart",
        "Spinner never stops on deposit review", "Large font setting breaks deposit screen layout",
        "Rejected deposit reason not displayed", "Deposit receipt shows the wrong date",
        "Biometric login fails after app update", "Face ID prompt appears behind a modal",
        "Fingerprint enrollment error message unclear", "Biometric toggle resets after logout",
        "Transfer confirmation shows previous amount", "Account switcher shows closed accounts",
        "Statement PDF fails to open on Android 15", "Push notifications not received on some Android devices",
        "Home screen cards overlap on tablets", "Back button exits app from deposit flow",
        "Promo banner covers navigation bar", "Wrong currency symbol for travel accounts",
        "Analytics SDK sends duplicate events", "Pull-to-refresh triggers twice",
        "Transaction categories missing icons", "Error toast shown after a successful transfer",
        "Login screen logo blurry on high-resolution screens", "Contact support link opens a blank page",
        "Settings screen crashes when toggling alerts", "Card image not loading on slow networks",
        "Logout does not clear cached balances", "Build shows outdated version number in About screen",
        "Deposit flow loses state when app is backgrounded", "Wrong error shown when camera is unavailable",
        "Accessibility focus lost after deposit submit"],
    "Digital Accounts": [
        "Statement PDF missing last page", "eStatement email link expires too early",
        "Application form loses data on browser back", "Spending chart colors fail contrast check",
        "Category totals off by one cent", "Paperless toggle shows wrong state for joint owners",
        "ID verification timeout message unclear", "Tax document download fails in Firefox",
        "Merchant names show raw processor codes", "Insights card blank for new members",
        "Application email sent with broken link", "Document center sort order wrong",
        "Address autocomplete suggests wrong state", "Statement viewer zoom resets on page change",
        "Duplicate applicant check flags spouses", "Funding amount field accepts negative values",
        "Budget alert sent for the wrong category", "Statement search returns nothing for December",
        "Save and resume link opens an empty application", "Monthly summary email shows the wrong month"],
    "Member Support": [
        "Agent console freezes when opening long requests", "Knowledge base search misses plural terms",
        "Request queue count does not refresh", "Article editor drops formatting on paste",
        "Request status email shows an internal note", "Chat window overlaps cookie banner",
        "Request assignment notification sent twice", "Agent cannot attach PDFs over 2 MB",
        "Request timeline shows wrong time zone", "Suggested articles panel empty for new requests",
        "Request search ignores closed requests filter", "Chat transcript missing agent name",
        "Request category list shows retired categories", "Agent console logout loses unsaved notes",
        "Request priority not saved on edit", "Knowledge base links broken after import",
        "Member cannot reopen a resolved request", "Chat session ends without warning",
        "Request intake form rejects apostrophes in names"],
    "Security": [
        "Fraud score API returns 500 on missing device ID", "MFA code accepted after expiry",
        "Audit log timestamps recorded in local time", "Risk score threshold not applied to wires",
        "Evidence export missing March records", "Authenticator enrollment QR code too small",
        "Session not revoked after password reset", "Model monitoring alert fires only on weekends",
        "Trusted device list shows duplicates", "Access review export truncates long names",
        "Velocity rule ignores declined transactions"],
    "Core Platform": [
        "Gateway returns 502 under burst load", "Token refresh fails at midnight UTC",
        "Notification retries exceed the limit", "Accounts API pagination skips records",
        "SMS adapter drops messages with emoji", "Rate limit headers missing on 429 responses",
        "Email adapter bounces not recorded", "OpenAPI docs show wrong base URL",
        "No alert before push certificate expiry"],
    "Branch Experience": [
        "Appointment reminder sent for a cancelled visit", "Check-in tablet loses Wi-Fi connection",
        "Time slots offered on branch closed days", "Queue dashboard shows wrong banker name",
        "Lobby screen text too small", "Kiosk mode exits on tablet reboot",
        "Appointment confirmation missing branch address", "Signature capture lags on older tablets"],
}

# ----------------------------------------------------------------------------- sandboxes (section 9)
SANDBOX_L11_FEATURE = "Omnichannel Service Requests (sandbox)"
SANDBOX_L9_FEATURE = "Instant Card Controls (planning copy)"


def _b(n, title, pts, state, sprint, wit="User Story", **kw):
    return dict(n=n, title=title, pts=pts, state=state, sprint=sprint, type=wit, **kw)


# Lab 11 sandbox mini set (exact list). area: None = Training\P##, "Training" = parent area (planted).
SANDBOX_L11_ITEMS = [
    _b(1, "Request intake form", 3, "Resolved", 13, tags=["omnichannel"]),
    _b(2, "Request status page", 2, "Resolved", 13, tags=["omni-channel"]),
    _b(3, "Agent queue view", 5, "Closed", 13),
    _b(4, "Category taxonomy cleanup", None, "Closed", 13),
    _b(5, "Routing rules engine", 3, "Active", 14, tags=["omnichannel"]),
    _b(6, "Routing rules engine", 3, "New", 14, tags=["omni-channel"], duplicate=True),
    _b(7, "Escalation rules", 3, "Active", 12, assigned="Kyle Morgan", stale_days=25),
    _b(8, "Presence indicator", 5, "Active", 12, assigned="Kyle Morgan", stale_days=25),
    _b(9, "Attachment scanning", 2, "Active", 12, assigned="Nora Fitzgerald", stale_days=20),
    _b(10, "Member notifications", None, "New", 15),
    _b(11, "Chat transcript export", 3, "Closed", 14),
    _b(12, "Secure file upload", 5, "Active", 14, tags=["omnichanel"]),
    _b(13, "Typing indicators", 2, "Active", 14, tags=["omnichannel"]),
    _b(14, "Chat disconnects after 60 seconds", None, "New", None, wit="Bug", priority=1, severity=2, area="Training"),
    _b(15, "Request emails sent twice", None, "Active", None, wit="Bug", priority=1, severity=3, area="Training"),
    _b(16, "Search returns stale results", None, "Active", None, wit="Bug", priority=2, severity=3),
    _b(17, "Old intake prototype", None, "Removed", None),
    _b(18, "Legacy form migration", None, "Removed", None),
]

PROGRESS_COMMENTS = [
    "Progress update: implementation underway, no blockers.",
    "Paired on this today; remaining work is error handling.",
    "Unit tests passing locally; pull request opened.",
    "Rebased on main and addressed review comments.",
    "About halfway through; demoed progress at stand-up.",
    "Integration tests added; finishing edge cases.",
    "Picked this back up after stand-up; on track.",
    "Updated the approach after a quick design review.",
]
STALE_COMMENTS = {
    "Auto-capture check edges with on-device ML":
        "Edge detection still misfires on dark countertops; need a better training set.",
    "Retry flow for failed check uploads": "Retry works on Wi-Fi; still flaky on cellular handoff.",
}
