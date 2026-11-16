const { writer, reader } = require("./db");

async function createOrder(customerId, items) {
  const { rows } = await writer.query(
    "INSERT INTO orders (customer_id, items) VALUES ($1, $2) RETURNING id",
    [customerId, JSON.stringify(items)]
  );
  return rows[0].id;
}

// Used by the confirmation page right after checkout, and by order history.
async function getOrder(id) {
  const { rows } = await reader.query("SELECT * FROM orders WHERE id = $1", [id]);
  return rows[0];
}

module.exports = { createOrder, getOrder };
