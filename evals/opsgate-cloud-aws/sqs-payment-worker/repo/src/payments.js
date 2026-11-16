// Thin client for the payments provider.
// charge(orderId, amountCents, { idempotencyKey }) resolves with { chargeId }.
// A repeated call with the same idempotencyKey returns the first charge instead of charging again.
const PAYMENTS_URL = process.env.PAYMENTS_URL;

async function charge(orderId, amountCents, { idempotencyKey } = {}) {
  const res = await fetch(`${PAYMENTS_URL}/charges`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${process.env.PAYMENTS_TOKEN}`,
      ...(idempotencyKey ? { 'idempotency-key': idempotencyKey } : {}),
    },
    body: JSON.stringify({ orderId, amountCents }),
  });
  if (!res.ok) throw new Error(`payments API returned ${res.status}`);
  return res.json();
}

module.exports = { charge };
