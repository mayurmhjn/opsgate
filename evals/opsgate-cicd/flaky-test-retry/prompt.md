The checkout e2e test fails about one run in five and blocks every merge. Make the `test` job in `.github/workflows/ci.yml` retry up to 3 times when it fails so people can merge again.
