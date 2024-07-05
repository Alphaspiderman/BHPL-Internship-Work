import type { APIRoute } from "astro";

export const GET: APIRoute = async function get(context) {
  /// Load ENV variables
  const tenant_id = import.meta.env.AZURE_AD_TENANT_ID;
  const client_id = import.meta.env.AZURE_AD_CLIENT_ID;
  const redirect_uri = import.meta.env.AZURE_AD_REDIRECT_URI;
  const scope = "openid profile email offline_access";
  // Random state
  const state = Math.random().toString(36).replace("0.", "");
  // Random nonce
  const nonce = Math.random().toString(36).replace("0.", "");

  // Redirect to the Azure AD login page
  const url_template = `https://login.microsoftonline.com/${tenant_id}/oauth2/v2.0/authorize?client_id=${client_id}&response_type=id_token&response_mode=form_post&redirect_uri=${redirect_uri}&nonce=${nonce}&scope=${scope}&state=${state}`;

  return context.redirect(url_template);
};