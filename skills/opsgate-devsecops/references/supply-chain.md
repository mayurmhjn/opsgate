# Supply chain: SBOM, signing and provenance

## Order in the release job

1. Build and push the image. Record its **digest** from the push output. Everything after this uses the digest, never a tag.
2. Generate the SBOM for that image digest, not for the source tree, so it lists what actually shipped.
3. Sign the image by digest.
4. Attach the SBOM to the image as a signed attestation, so it travels with the digest.
5. Produce build provenance (for example SLSA provenance) where the build platform supports it.
6. Verify, in the same job: check the signature and the attestation against the expected signer before the release is marked done.

## Signing

- Prefer keyless signing with the CI's OIDC identity, which leaves no long-lived key to protect. Keyless signatures are recorded in a public transparency log, so the repository and workflow names become public. If that is a problem, use a key held in a cloud KMS and grant the release role only the sign permission.
- Never store a private signing key in the repository or as a plain CI secret.

## Verification

Verification only means something if it checks **who** signed:

- Pin the expected identity (for example the release workflow path and tag ref) and the OIDC issuer exactly. If you must use a regular expression, escape the dots and anchor both ends.
- Verify inside the release pipeline after signing, again in the deploy step or with an admission policy in the cluster, and document the command for customers.

## Registry caveats

- Some signing tools store signatures and attestations as extra tags derived from the image digest. In a registry with tag immutability, a second signature or attestation for the same digest can then fail. Check the current support of the tool and registry for OCI referrers, which avoid this.
- Lifecycle rules that delete old images can also delete their signatures and attestations. Keep them for as long as the release is supported.

## Pinning the tools

Pin the SBOM, signing and verification tools and actions to a full SHA or digest, and look up the current release. A compromised signing tool undermines everything it signs.
