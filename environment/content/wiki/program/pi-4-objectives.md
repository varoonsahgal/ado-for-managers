# PI 4 Objectives

[[_TOC_]]

| | |
|---|---|
| PI | **PI 4** (Sprint 13, Sprint 14, Sprint 15, Sprint 16) |
| Agreed at | PI 4 Planning, start of Sprint 13 |
| Scored at | PI 4 System Demo, end of Sprint 16 |
| Owner | Ruth Ellison, Program Manager |

> This page records what teams **committed to at PI 4 Planning**. Target sprints shown here are the targets agreed at planning. The live schedule is the Delivery Plan **HarborPoint Program Plan**. If a target has moved since planning, the Feature's History and Discussion show who moved it and why.

## How to read this page

- **Committed** objectives are what the team is confident it will deliver this PI. Committed Features carry the tag `PI4-Committed`.
- **Stretch** objectives are planned but not promised. They are not counted when we judge whether a team met its commitments.
- **Mandatory** work (regulatory exam readiness) is not scored with business value. It is non-negotiable.
- **Business value (BV)** is a 1 to 10 score assigned by the initiative owners at PI planning (10 = highest). It is separate from the Business Value field on the Feature. **Actual BV** is scored at the PI 4 System Demo.

## Program-level objective (shared)

| Objective | Feature | Teams | Planned target | BV | Type |
|---|---|---|---|---|---|
| Members receive real-time alerts for suspicious transactions and can confirm or deny them in the app | F9 Real-Time Fraud Alerts | **Mobile Banking** (owner), **Security**, **Core Platform** | Sprint 16 | 10 | Committed |

F9 serves portfolio priority #1 (*Protect every member*). Each contributing team lists its part of F9 below.

## Mobile Banking

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| Deliver Mobile Check Deposit 2.0 to all members | F2 Mobile Check Deposit 2.0 | Sprint 14 | 9 | Committed |
| Deliver the member-facing app experience for Real-Time Fraud Alerts (alert, confirm or deny, auto-lock) | F9 Real-Time Fraud Alerts | Sprint 16 | 10 | Committed (shared) |
| Members can log in with Face ID or fingerprint | F3 Biometric Login (with Security) | Sprint 16 | 7 | Committed |
| Member-to-Member Transfers decomposed into stories and ready for PI 5 Planning | F4 Member-to-Member Transfers | Sprint 16 | 4 | Stretch |

## Digital Accounts

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| New members can open an account fully online | F6 Online Account Opening | Sprint 16 | 8 | Committed |
| Members see monthly spending summaries and budget alerts | F7 Spending Insights | Sprint 15 | 4 | Committed |
| Instant Card Controls scoped and estimated, ready to start delivery | F5 Instant Card Controls | Sprint 16 | 6 | Stretch |

Paperless Statements & Documents (F8) was finished in Sprint 13 as carry-in work from PI 3. It is not a PI 4 objective.

## Security

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| Fraud scoring engine v2 in production. Real-Time Fraud Alerts builds on it | F10 Fraud Scoring Engine v2 | Sprint 15 | 9 | Committed |
| Real-time risk-score API and alert decision feedback for Fraud Alerts | F9 Real-Time Fraud Alerts | Sprint 16 | 10 | Committed (shared) |
| Adaptive multi-factor authentication for high-risk actions | F11 Adaptive Multi-Factor Authentication | Sprint 16 | 7 | Committed |
| Device binding risk signal for Biometric Login | F3 Biometric Login (Mobile owns) | Sprint 16 | 7 | Committed (contributing) |
| Account Takeover Protection discovery complete for PI 5 | F12 Account Takeover Protection | Sprint 16 | 5 | Stretch |
| Exam readiness: audit evidence automation | F21 Audit Evidence Automation | Sprint 18 | n/a | Mandatory |
| Exam readiness: access review automation (with Core Platform) | F22 Access Review Automation | Sprint 18 | n/a | Mandatory |

## Core Platform

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| One notification service for push, SMS and email across all channels | F23 Unified Notification Service | Sprint 15 | 8 | Committed |
| Member API Gateway live for internal and partner APIs | F24 Member API Gateway | Sprint 16 | 7 | Committed |
| High-priority push channel and delivery receipts for Fraud Alerts | F9 Real-Time Fraud Alerts | Sprint 16 | 10 | Committed (shared) |
| Service account inventory for exam readiness | F22 Access Review Automation (Security owns) | Sprint 18 | n/a | Mandatory (contributing) |
| API readiness for Member-to-Member Transfers | F4 Member-to-Member Transfers (Mobile owns) | Sprint 16 | 3 | Stretch |

## Branch Experience

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| Lobby check-in and queue management in all branches | F19 Lobby Check-In & Queue Management | Sprint 15 | 6 | Committed |
| In-branch digital onboarding: tablet kiosk, digital signatures and pre-filled applications | F18 In-Branch Digital Onboarding | Sprint 17 | 7 | Committed |
| Teller Workstation Refresh discovery for PI 5 | F20 Teller Workstation Refresh | Sprint 16 | 3 | Stretch |

## Member Support

| Objective | Feature | Planned target | BV | Type |
|---|---|---|---|---|
| Members can raise and track service requests from any channel | F13 Omnichannel Service Requests | Sprint 15 | 8 | Committed |
| Secure messaging and chat between members and agents | F14 Secure Messaging & Chat | Sprint 17 | 6 | Committed |
| Callback Scheduling ready for PI 5 Planning | F16 Callback Scheduling | Sprint 16 | 3 | Stretch |

## Cross-team dependencies agreed at PI 4 Planning

| Predecessor | Successor | Status at planning |
|---|---|---|
| F10 Fraud Scoring Engine v2 (Security, target Sprint 15) | F9 Real-Time Fraud Alerts (Mobile Banking, target Sprint 16) | OK |
| F23 Unified Notification Service (Core Platform, target Sprint 15) | F9 Real-Time Fraud Alerts (Mobile Banking, target Sprint 16) | OK |
| F24 Member API Gateway (Core Platform, target Sprint 16) | F4 Member-to-Member Transfers (Mobile Banking, start Sprint 17) | OK |

Dependencies are maintained as Predecessor/Successor links on the Features and are visible in the Delivery Plan.

## Scoring at the PI 4 System Demo

| Team | Planned BV (committed) | Actual BV |
|---|---|---|
| Mobile Banking | | *Scored at PI 4 System Demo* |
| Digital Accounts | | *Scored at PI 4 System Demo* |
| Security | | *Scored at PI 4 System Demo* |
| Core Platform | | *Scored at PI 4 System Demo* |
| Branch Experience | | *Scored at PI 4 System Demo* |
| Member Support | | *Scored at PI 4 System Demo* |

Actual BV is scored by the initiative owners for each objective that was delivered. Partial delivery earns partial value at the owner's discretion.
