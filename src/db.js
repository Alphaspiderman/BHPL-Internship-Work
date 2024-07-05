import * as db from './pool-manager.js';

function runQuery(query, args) {
  try {
    const pool = db.get("intranet");
  } catch (error) {
    const pool = db.create("intranet", {
        user: import.meta.env.DB_USERNAME,
        password: import.meta.env.DB_PASSWORD,
        server: import.meta.env.DB_HOST,
        database: import.meta.env.DB_NAME,
        pool: {
            max: 10,
            min: 0,
            idleTimeoutMillis: 30000
        }
    });
  }
    return pool.request().input(args).query(query);
}