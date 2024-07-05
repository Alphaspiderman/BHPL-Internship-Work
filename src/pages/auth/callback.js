import * as jose from "jose";
import { Astro } from "astro";

export async function POST({ request }) {
  // Load ENV variables
  const tenant_id = import.meta.env.AZURE_AD_TENANT_ID;
  const client_id = import.meta.env.AZURE_AD_CLIENT_ID;

  // Get JWT from form
  const data = await request.formData();
  console.log(data);
  const jwt = data.get("id_token");

  // Make keystore if needed
  var res = await fetch(
    "https://login.microsoftonline.com/common/.well-known/openid-configuration",
  );
  var page = await res.json();
  const jwks = await fetch(page["jwks_uri"]);

  var resp = await jwks.json();
  const JWKS = jose.createLocalJWKSet(resp);


  // Verify the JWT
  const verified = await jose.jwtVerify(jwt, JWKS, {
    audience: client_id,
    issuer: `https://login.microsoftonline.com/${tenant_id}/v2.0`,
  });
  var email = verified.payload.email;
  console.log(email);
}
