import type { APIRoute } from "astro";
import { getLocationMasterById, getLocationMaster } from "../../db.js";

export const GET: APIRoute = async function get(context) {
  // Get the location ID from the URL
  const locationId = context.url.searchParams.get("locationId");
  if (!locationId) {
    // Get all locations from the database
    const locations = await getLocationMaster();
    return new Response(
      JSON.stringify({
        message: "No location ID provided",
      }),
    );
  } else {
    // Get the location from the database
    const location = await getLocationMasterById(locationId);
    return new Response(
      JSON.stringify({
        message: "Location ID was "+locationId,
      }),
    );
  }
};

export const POST: APIRoute = async function post(context) {
  return new Response(
    JSON.stringify({
      message: "This was a POST!",
    }),
  );
};

export const DELETE: APIRoute = async function delete_req(context) {
  return new Response(
    JSON.stringify({
      message: "This was a DELETE!",
    }),
  );
};
