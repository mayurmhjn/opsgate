const express = require('express');
const app = express();
app.use(express.json());

app.post('/orders', async (req, res) => {
  const order = { id: `ord_${Date.now()}`, ...req.body };
  const payment = await fetch(`${process.env.PAYMENTS_URL}/payments`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ orderId: order.id, amountCents: req.body.amountCents }),
  }).then((r) => r.json());
  res.json({ ...order, payment });
});

app.listen(3001);
