# Checkout errors, today

All times UTC.

- 14:02 Deploy v1.42.0 to production finished (pipeline run 8812). Contains: checkout v2 code behind the `checkout_v2` flag (off), fix for duplicate order emails, fix for the coupon rounding bug, dependency updates.
- 14:05 Smoke tests passed. Checkout error rate 0.2% (normal).
- 14:28 Product turned on `checkout_v2` for 10% of users in AWS AppConfig.
- 14:30 `checkout_v2` raised to 100%.
- 14:31 Checkout 5xx alarm fired. Error rate 7.8%.
- 14:40 Error rate 8.1%. Most errors: `TypeError: cannot read properties of undefined (reading 'taxCode')` in `checkoutV2/submit.js`.
