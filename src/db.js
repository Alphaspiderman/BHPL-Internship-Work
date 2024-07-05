import { Connection } from "tedious";

async function runQuery(query, args) {
  const connection = new Connection({
    server: import.meta.env.DB_HOST,
    authentication: {
      type: "default",
      options: {
        userName: import.meta.env.DB_USERNAME,
        password: import.meta.env.DB_PASSWORD,
      },
    },
    options: {
      port: import.meta.env.DB_PORT, // Default Port
    },
  });
  const req = new Request(query, function (err, rowCount, rows) {
    return rows;
  })
  // Setup event handler when the connection is established.
  connection.on("connect", function (err) {
    if (err) {
      console.log("Error: ", err);
    }
    // If no error, then good to go...
    executeStatement(req, args);
  });

  // Initialize the connection.
  connection.connect();
}

async function executeStatement(query, args) {
    
}

async function getLocationMaster(isIT) {
  if (isIT) {
  }
  return runQuery("SELECT * FROM location_master");
}

async function getLocationMasterById(id) {
  return runQuery("SELECT * FROM location_master WHERE id = @id", { id });
}

export { getLocationMasterById, getLocationMaster };
