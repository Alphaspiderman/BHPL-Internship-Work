import { sequence } from "astro:middleware";
import { Astro } from "astro";
import * as jose from "jose";
import fs from "fs";
import crypto from "crypto";

const unprotectedPaths = [
  "/login",
  "/auth/entra",
  "/auth/callback",
  "/public.pem",
];

const routeDepartments = {
  "/api/location": ["IT"],
};

async function checkProtected(context, next) {
  context.require_authentication = true;
  const path = context.url.pathname;
  if (unprotectedPaths.includes(path)) {
    context.require_authentication = false;
  }
  if (path.startsWith("/static/")) {
    context.require_authentication = false;
  }
  if (path.startsWith("/api/")) {
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
    const jwt = context.cookies.get("JWT_TOKEN")["value"];
    const key = fs.readFileSync("./public-key.pem");
    // Convert to string
    const keyString = key.toString();
    const publicKey = await jose.importSPKI(keyString, "RS256");
    const { payload, header } = await jose.jwtVerify(jwt, publicKey);
    context.jwt_payload = payload;
    context.jwt_header = header;
    return await next();
  }
  return await next();
}

async function routeRequiresDepartment(context, next) {
  if (context.require_authentication) {
    if (routeDepartments[context.url.pathname]) {
      const department = context.jwt_payload["department"];
      if (routeDepartments[context.url.pathname].includes(department)) {
        return await next();
      } else {
        console.log(context);
        return context.send("Unauthorized", 401);
      }
    }
  }
  return await next();
}

export const onRequest = sequence(checkProtected, checkJWTCookie, decodeJWT, routeRequiresDepartment);
