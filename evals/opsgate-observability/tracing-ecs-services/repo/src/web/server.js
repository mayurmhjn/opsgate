const express = require('express');
const app = express();
app.use(express.json());

app.post('/checkout', async (req, res) => {
  const order = await fetch(`${process.env.ORDERS_URL}/orders`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(req.body),
  }).then((r) => r.json());
  res.json(order);
});

app.listen(3000);
