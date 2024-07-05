import type { APIRoute } from "astro";
import * as jose from "jose";

export const GET: APIRoute = async function get(context) {
  return context.redirect("/login");
};

export const POST: APIRoute = async function post(context) {
  // Load ENV variables
  const tenant_id = import.meta.env.AZURE_AD_TENANT_ID;
  const client_id = import.meta.env.AZURE_AD_CLIENT_ID;

  const form_data = await context.request.formData();
  const jwt = form_data.get("id_token");

  // Make a JWKS keystore
  const res = await fetch(
    "https://login.microsoftonline.com/common/.well-known/openid-configuration",
  );
  const page = await res.json();
  const jwks = await fetch(page["jwks_uri"]);
  const resp = await jwks.json();
  const JWKS = jose.createLocalJWKSet(resp);
  const verified = await jose.jwtVerify(jwt, JWKS, {
    audience: client_id,
    issuer: `https://login.microsoftonline.com/${tenant_id}/v2.0`,
  });
  var email = verified.payload.email;
  console.log(email);
};
