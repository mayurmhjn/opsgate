# GitHub Actions hardening

For GitLab CI, Jenkins and AWS CodePipeline, see `other-ci.md`.

## Triggers

- `pull_request_target`, `workflow_run` and `issue_comment` run in the default-branch context, with access to secrets and a token that can write. Never check out and run pull request code in them. Run untrusted code in `pull_request`, and pass results to a privileged follow-up workflow as artifacts.
- Artifacts produced by untrusted runs are untrusted data. In the privileged workflow:
  - never execute them, or run package managers or `npx` with the working directory inside them (they can carry `node_modules/.bin`, `.npmrc` or scripts)
  - never write their contents to `GITHUB_ENV`, `GITHUB_OUTPUT` or into `${{ }}` expressions without validating them
  - extract them to a separate directory, check the contents, and run only tools installed outside the artifact, from a working directory outside it (never `working-directory` set to the artifact folder)
- Cache poisoning: untrusted code that runs in a default-branch-context workflow, even one without secrets, can write caches that every later privileged run restores. Cache writes don't depend on the token's permissions, and restore keys match by prefix. Keep untrusted code out of those workflows, and consider skipping caches in release and deploy builds.

## Untrusted input

- Never put `${{ github.event.* }}` fields such as titles, bodies, branch names or commit messages, or `inputs.*`, directly inside a `run` script. Pass them through `env:` and quote them as shell variables.

## Permissions and credentials

- Set the top-level `permissions` to the minimum (often `contents: read`), and grant more per job only where needed. The repository or organization setting only sets the default. A `permissions` key in the workflow can still raise it, except where fork pull requests get a read-only token.
- Use `persist-credentials: false` on checkout unless a later step needs to push, so the token isn't left in `.git/config` where artifacts or caches can pick it up.
- Prefer the built-in token or a GitHub App token over personal access tokens.
- Use OIDC to the cloud provider. Roles that deploy or apply to production trust only the protected environment's subject (`environment:NAME`), not a branch subject, because default-branch triggers such as `workflow_run` share the branch ref. Customize the subject claim where a branch subject must stay.
- Production deploy jobs use a protected environment with required reviewers. The reviewers are the control. A branch rule alone doesn't stop default-branch triggers.
- Secrets live in environments where possible, so only the gated job can read them.

## Supply chain

- Pin every third-party action to a full commit SHA, with its version in a comment (`uses: owner/action@<full sha> # vX.Y.Z`). Look up the current release and its SHA. Never write a remembered version or SHA.
- Keep pins current with automated update PRs (Dependabot or Renovate).
- Deploy by image digest, or by an immutable tag in a registry that enforces tag immutability. Not every registry supports it.

## Reliability

- Concurrency groups per environment. Production deploys use `cancel-in-progress: false`, so a running deploy is never cancelled. Only one run waits in the queue: a newer pending run replaces an older pending one.
- Timeouts on jobs, so a hung step doesn't block the queue.
- Cache dependencies with the setup action's built-in cache, keyed on the lock file, in workflows that only run trusted code.
