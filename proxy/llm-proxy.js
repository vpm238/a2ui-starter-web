/**
 * Minimal Anthropic LLM proxy for Cloudflare Workers.
 *
 * Purpose: keep ANTHROPIC_API_KEY in a Worker secret instead of on the
 * device. The web starter POSTs to `<worker-url>/v1/messages` with the same
 * body shape Anthropic expects; the worker forwards it, streaming the
 * response back unchanged.
 *
 * Deploy:
 *   1. npm install -g wrangler
 *   2. cd proxy/ && wrangler secret put ANTHROPIC_API_KEY   (paste your key)
 *   3. wrangler deploy
 *   4. Note the resulting https://a2ui-llm-proxy.<you>.workers.dev URL
 *   5. In web/index.html (or whoever serves it): set window.A2UI_PROXY_URL
 *      to that URL before the module script runs.
 */

// Lock this to your own deploy origins. '*' means anyone can hit the proxy
// and burn your Anthropic quota — fine for local dev, bad for public demos.
// The origin is scheme+host+port; paths don't matter for CORS.
const ALLOWED_ORIGINS = [
  'https://vpm238.github.io',       // GitHub Pages deploy
  'http://localhost:5173',          // `python3 -m http.server 5173`
  'http://127.0.0.1:5173',
];

function cors(origin) {
  const allowed = ALLOWED_ORIGINS.includes('*') ? '*' :
    (ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0] || '*');
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, anthropic-version',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const corsHeaders = cors(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
    }

    const url = new URL(request.url);
    if (url.pathname !== '/v1/messages') {
      return new Response('Not Found', { status: 404, headers: corsHeaders });
    }

    if (!env.ANTHROPIC_API_KEY) {
      return new Response(JSON.stringify({ error: 'Worker missing ANTHROPIC_API_KEY secret' }), {
        status: 500, headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }

    // Forward to Anthropic. Stream the body-stream through so SSE works.
    const forwarded = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: request.body,
    });

    // Return streamed response with CORS headers added.
    const outHeaders = new Headers(forwarded.headers);
    for (const [k, v] of Object.entries(corsHeaders)) outHeaders.set(k, v);
    return new Response(forwarded.body, {
      status: forwarded.status,
      headers: outHeaders,
    });
  }
};
