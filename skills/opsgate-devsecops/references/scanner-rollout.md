# Scanner rollout

## Categories and common choices

Choose from what the repo contains and what the team already runs. These are common, widely used options, not the only ones. Check each tool's current documentation for features and supported languages.

| Category | What it finds | Common options |
|----------|---------------|----------------|
| Secrets | Keys and tokens in code and history | gitleaks, trufflehog, platform secret scanning with push protection |
| Code (SAST) | Injection, unsafe APIs, bad patterns | Semgrep, CodeQL |
| Dependencies (SCA) | Known vulnerable packages | osv-scanner, Trivy, Grype, Dependabot alerts |
| Container images | Vulnerable OS and language packages in the image | Trivy, Grype |
| IaC | Insecure cloud and Kubernetes configuration | Checkov, Trivy config mode (successor to tfsec), KICS |
| Running application (DAST) | Issues only visible at runtime: headers, auth flaws, exposed endpoints | OWASP ZAP baseline or API scans against a preview or staging deployment. Never against production without approval |

One tool that covers several categories (for example Trivy for images, dependencies and IaC) means fewer things to pin, update and tune. Add a second tool only where it finds what the first misses.

## Living with a backlog

The goal is that the backlog doesn't grow while it is being worked down.

- **Diff or baseline mode** where the tool has one: scan only what changed against the base branch (for example Semgrep's baseline commit, scanning a commit range for secrets, or a dependency scanner's pull request diff).
- **Ignore file of current findings** where it doesn't: list today's findings in the tool's ignore file, each with a reason and an expiry date (use the tool's expiry field where it has one, such as `exp:` in `.trivyignore`), and fail on anything not in the file at high or critical severity.
- Track the backlog itself in code scanning or an issue tracker, with owners.

Every category gates on new high and critical findings from the first day. Lower severities can start as warnings. For container images, gate on findings with a fix available (for example an ignore-unfixed option), since nobody can act on the rest in a pull request. That option does not stop a newly published, fixable base image vulnerability from failing an unrelated pull request. Run a scheduled image scan that opens issues so base image updates happen on their own, and keep the pull request gate for findings the change could have fixed.

## Making results visible

- Upload SARIF to code scanning on pushes to the default branch and on `pull_request` runs, so reviewers see alerts on the diff. The upload job needs `security-events: write`, plus `actions: read` in private repositories. Code scanning on private repositories needs a code security license. Without one, use annotations or the job summary.
- Code scanning accepts uploads from `pull_request` runs even with a read-only token, fork pull requests included. Other triggers need `security-events: write`.
- Make the scan jobs required status checks.

## Safety of the scan jobs

- Run scans in `pull_request` workflows, never by checking out fork code in a privileged trigger.
- Grant `security-events: write` only to a job that uploads results and doesn't build or run pull request code. Put the upload in its own job that downloads the results, or don't grant the permission on pull request runs. Analyzers that build and upload in one step (such as CodeQL for compiled languages) can turn their own upload off so a separate job uploads, or use the platform's default setup.
- Pin every scanner action and image to a full SHA or digest. Popular actions have been compromised through mutable tags. To resolve a tag to a SHA, query exactly that tag: `git ls-remote https://github.com/OWNER/ACTION 'refs/tags/vX.Y.Z' 'refs/tags/vX.Y.Z^{}'`. For an annotated tag, use the commit SHA on the line ending in `^{}`. For a lightweight tag, only the plain line comes back, and that SHA is the commit.
