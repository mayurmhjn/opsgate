// Client for the card processor. On failure it throws an Error with
// err.code (processor decline or error code) and err.status (HTTP status).
async function charge(request) {
  const res = await fetch(`${process.env.PROCESSOR_URL}/v1/charges`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${process.env.PROCESSOR_KEY}` },
    body: JSON.stringify(request),
  });
  const data = await res.json();
  if (!res.ok) {
    const err = new Error(data.message || 'charge failed');
    err.code = data.code;
    err.status = res.status;
    throw err;
  }
  return data;
}

module.exports = { charge };
