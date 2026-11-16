const { Pool } = require("pg");

const writer = new Pool({ host: process.env.DB_WRITER_HOST, database: "orders" });
const reader = new Pool({ host: process.env.DB_READER_HOST, database: "orders" });

module.exports = { writer, reader };
