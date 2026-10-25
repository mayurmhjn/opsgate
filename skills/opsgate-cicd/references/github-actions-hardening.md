# GitHub Actions hardening

Most of this applies to other CI systems too, under different names.

## Triggers

- `pull_request_target` and `workflow_run` run with the base repository's secrets and a write-capable token. Never check out and run pull request code in them. Run untrusted code in `pull_request`, and pass results to a privileged follow-up workflow as artifacts that are treated as data.
- Artifacts produced by untrusted runs are untrusted. In the privileged workflow, never execute them or run package managers or `npx` with the working directory inside them (they can carry `node_modules/.bin`, `.npmrc` or scripts). Extract them to a separate directory, check the contents, and run only tools installed outside the artifact.
- Caches written by a privileged run can be poisoned by pull request code. Don't share cache keys between untrusted and privileged workflows.
- Restrict manual triggers (`workflow_dispatch`) that deploy with environment branch rules.

## Untrusted input

- Never put `${{ github.event.* }}` fields such as titles, bodies, branch names or commit messages, or `inputs.*`, directly inside a `run` script. Pass them through `env:` and quote them as shell variables.

## Permissions and credentials

- Set the top-level `permissions` to the minimum (often `contents: read`), and grant more per job only where needed. The repository or organization setting only sets the default. A `permissions` key in the workflow can still raise it, except for pull requests from forks.
- Prefer the built-in token or a GitHub App token over personal access tokens.
- Use OIDC to the cloud provider, with the trust policy's subject limited to the repository and the branch or environment. No stored cloud access keys.
- Production deploy jobs use a protected environment: required reviewers, and deployment branches limited to the release branch.
- Secrets live in environments where possible, so only the gated job can read them.

## Supply chain

- Pin every third-party action to a full commit SHA, with the version in a comment, for example `uses: owner/action@<full sha> # v4.2.1`. Look up the SHA, don't guess it.
- Keep pins current with automated update PRs (Dependabot or Renovate).
- Pin container images by digest where reproducibility matters.
- Turn on tag immutability in the registry, and deploy by the immutable tag or digest that was built.

## Reliability

- Concurrency groups per environment. Production deploys use `cancel-in-progress: false`, so a running deploy is never cancelled. Only one run waits in the queue: a newer pending run replaces an older pending one. Pull request checks may cancel superseded runs.
- Timeouts on jobs, so a hung step doesn't block the queue.
- Cache dependencies with the setup action's built-in cache, keyed on the lock file.
