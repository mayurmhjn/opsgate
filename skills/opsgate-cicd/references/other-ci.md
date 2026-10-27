# Other CI systems

The same principles apply everywhere: untrusted code never runs with deploy credentials, production waits for an approval, deploys never overlap, and credentials are short-lived. These are the usual names for each control. Check the current documentation, since features and plan tiers change.

| Control | GitLab CI | Jenkins | AWS CodePipeline |
|---------|-----------|---------|------------------|
| Approval before production | Protected environments with deployment approvals (GitLab Premium or Ultimate; on Free, say what is missing) | `input` step whose `submitter` lists the approvers | Manual approval action |
| Only trusted branches can deploy | Protected branches, and protected variables that only protected branches receive | Branch conditions, and folder or job permissions | Source and trigger filters on the pipeline |
| No overlapping deploys | `resource_group` on the deploy job | `disableConcurrentBuilds()`, or `lock` from the Lockable Resources plugin | Superseded (the default) and queued modes run one execution per stage, and only parallel mode overlaps. Keep the current mode unless every release must deploy in order. |
| Short-lived cloud credentials | `id_tokens` with an audience, trusted by the cloud role on the project path, ref type and ref | Credentials plugin with role assumption, or the cloud provider's OIDC plugin | A service role per action |
| Untrusted contributions | Merge request pipelines from forks run in the fork without any of the parent project's CI/CD variables. Running them in the parent project needs a deliberate trigger. | Multibranch "trust" settings decide whether a fork's Jenkinsfile runs. Don't trust forks by default. | Source connections scoped to the repositories and branches you mean |
| Pinned shared config | `include` with a fixed `ref` (a commit SHA) | Shared libraries loaded at a fixed version | Not applicable |
| Job token scope | CI job token allowlist | Credentials bound only in the stages that need them | Role trust and permissions per action |
