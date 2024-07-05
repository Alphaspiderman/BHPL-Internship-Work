// pool-manager.js
import * as mssql from "mssql";
const pools = new Map();

function get(name) {
  if (!pools.has(name)) {
    throw new Error("Pool does not exist");
  }
  return pools.get(name);
}

function closeAll() {
  Promise.all(
    Array.from(pools.values()).map((connect) => {
      return connect.then((pool) => pool.close());
    }),
  );
}

function create(name, config) {
  if (pools.has(name)) {
    throw new Error("Pool already exists");
  }
  const pool = new mssql.ConnectionPool(config);
  // automatically remove the pool from the cache if `pool.close()` is called
  const close = pool.close.bind(pool);
  pool.close = (...args) => {
    pools.delete(name);
    return close(...args);
  };
  pools.set(name, pool.connect());
  return pools.get(name);
}

export { get, create, closeAll };
