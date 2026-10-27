# Selection procedure

Use this every time you choose a tool, service or pattern: compute platform, database, IaC tool, CI system, scanner, monitoring stack, deployment strategy.

## 1. Collect the inputs that drive the choice

- Functional need: what the component must do.
- Scale and traffic pattern: steady, spiky, scheduled, or idle most of the time.
- Availability target, plus RPO and RTO where data is involved.
- Data sensitivity and compliance (PCI DSS, HIPAA, SOC 2, GDPR, data residency).
- Budget for the running cost and for the team's time.
- Team skills and size. A tool nobody on the team can operate is a risk.
- What already exists: tools in the repo, accounts, contracts, standards set by a platform team.
- Licensing and how much vendor lock-in the team accepts.

Ask only for inputs that are missing and would change the answer.

## 2. Shortlist two or three candidates

Include the option the existing setup already uses, if there is one. Drop options that fail a hard requirement and say why in one line.

## 3. Compare against this team's inputs

Use a short table. Rows are the candidates. Columns are the inputs that matter here, usually fit, running cost, operational load, security, lock-in and learning curve. Write each cell in words tied to this case. "Lower ops load: no nodes to patch for a team of three" is useful. "Easy" is not.

## 4. Recommend one and say when another would win

State the recommendation and the two or three reasons that decided it. Then name the condition that would change the answer, for example "EKS becomes the better choice once you have a platform team or need Kubernetes-only tooling."

## 5. Confirm and record

Ask the user to confirm. Once they confirm, write a decision record (see `templates.md`). Until then, the choice is a proposal and nothing gets built on it.

## Under time pressure

Keep every step, but compress them: one line of inputs you assumed, a table of two or three options, one recommendation, one question to confirm. That takes a minute to read and still leaves the decision with the user.

## Tie-breakers

Popularity and personal preference only break ties between options that fit equally well. A tool already used in the repo counts as a strong input but does not win automatically.
