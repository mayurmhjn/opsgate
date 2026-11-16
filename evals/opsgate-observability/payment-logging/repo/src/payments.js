const { charge } = require('./provider');

// API Gateway -> Lambda. Body: { orderId, amountCents, cardNumber, cvc, expiry, email }
exports.handler = async (event) => {
  const body = JSON.parse(event.body);
  try {
    const result = await charge({
      orderId: body.orderId,
      amountCents: body.amountCents,
      card: { number: body.cardNumber, cvc: body.cvc, expiry: body.expiry },
      receiptEmail: body.email,
    });
    return { statusCode: 200, body: JSON.stringify({ chargeId: result.id }) };
  } catch (err) {
    console.log('payment failed');
    return { statusCode: 502, body: JSON.stringify({ error: 'payment failed' }) };
  }
};
