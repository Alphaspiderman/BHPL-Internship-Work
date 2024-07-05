import {Astro} from "astro";

export const GET = ({params, request }) => {
    Astro.cookies.delete("JWT_TOKEN");
    // Redirect to the homepage
    return new Response(JSON.stringify({
        path: new URL(request.url).pathname,
      })
    )
}