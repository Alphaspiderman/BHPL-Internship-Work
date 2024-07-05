import { sequence } from "astro:middleware";
import { Astro } from "astro";
import * as jose from "jose";

const unprotectedPaths = [
  "/login",
  "/auth/entra",
  "/auth/callback",
  "/public.pem",
];

async function checkProtected(context, next) {
  context.require_authentication = true;
  const path = context.url.pathname;
  if (unprotectedPaths.includes(path)) {
    context.require_authentication = false;
  }
  if (path.startsWith("/static/")) {
    context.require_authentication = false;
  }
  return await next();
}

async function checkJWTCookie(context, next) {
  if (context.require_authentication) {
    if (context.cookies.has("JWT_TOKEN")) {
      return await next();
    } else {
      return context.redirect("/login");
    }
  }
  return await next();
}

async function decodeJWT(context, next) {
  if (context.require_authentication) {
    // Load our RSA public key
    const publicKey = await fetch("/public.pem").then((res) => res.text());
    jwt = Astro.cookies.get("JWT_TOKEN");
    payload = jose.JWT.decode(jwt);
    console.log(payload);
    return await next();
  }
  return await next();
}

export const onRequest = sequence(checkProtected, checkJWTCookie, decodeJWT);
