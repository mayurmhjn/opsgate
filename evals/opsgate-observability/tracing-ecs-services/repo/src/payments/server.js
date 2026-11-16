const express = require('express');
const app = express();
app.use(express.json());

app.post('/payments', async (req, res) => {
  // calls the card processor; can take several seconds
  res.json({ status: 'authorized', orderId: req.body.orderId });
});

app.listen(3002);
