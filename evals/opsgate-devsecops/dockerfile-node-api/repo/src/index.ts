import Fastify from 'fastify';
import { Pool } from 'pg';

const app = Fastify({ logger: true });
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.get('/health', async () => ({ ok: true }));

app.get('/orders/:id', async (req) => {
  const { id } = req.params as { id: string };
  const { rows } = await pool.query('select * from orders where id = $1', [id]);
  return rows[0] ?? null;
});

app.listen({ host: '0.0.0.0', port: Number(process.env.PORT ?? 3000) });
