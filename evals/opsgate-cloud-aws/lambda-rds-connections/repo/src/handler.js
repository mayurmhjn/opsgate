const { Pool } = require('pg');

exports.handler = async (event) => {
  const pool = new Pool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD, // injected from Secrets Manager at deploy
    database: 'orders',
    max: 10,
  });
  const { rows } = await pool.query(
    'select id, status, total_cents from orders where customer_id = $1 order by created_at desc limit 20',
    [event.pathParameters.customerId],
  );
  return { statusCode: 200, body: JSON.stringify(rows) };
};
