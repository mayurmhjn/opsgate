# Payment webhook design

Stripe sends payment events to a new public endpoint.

- API Gateway HTTP API: `POST /webhooks/stripe`, public, no auth (Stripe can't log in).
- Lambda `stripe-webhook` (Node.js):
  1. Parse the JSON body.
  2. Log the full event with `console.log(JSON.stringify(event))` so we can debug.
  3. If `type` is `payment_intent.succeeded`, set the order to `paid` in the DynamoDB table `orders` and send the order ID to the SQS queue `fulfilment`.
  4. Return 200.
- Lambda role policy: `dynamodb:*` and `sqs:*` on `*`.
- No throttling. We'll add it if we see problems.
