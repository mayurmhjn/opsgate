# Requirements

Status: approved by Ravi (engineering manager), 2026-10-22

## Workload
Appointment booking for a chain of 60 physiotherapy clinics. Patients book on a web app; clinic staff manage calendars. A nightly job sends SMS reminders.

## Non-functional requirements
- Availability target: 99.9% during clinic hours (07:00 to 21:00 local).
- Scale: about 5,000 bookings a day, peaks Monday mornings at about 40 requests per second.
- Latency: booking page under 1 second at p95.
- Data classification: patient names, phone numbers, appointment notes (health-related personal data).
- Compliance: GDPR. Data must stay in the EU.
- Regions: eu-central-1 preferred.
- Budget: up to 1,500 EUR per month for production.

## Team and existing setup
- Five developers (TypeScript, Node.js), one part-time ops person. Some Docker experience, no Kubernetes.
- GitHub for code and CI. No AWS accounts yet.

## Open questions
None.
