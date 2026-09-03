# ocprobate.solutions

Static site. No build step. Deploys to Vercel as-is.

## Deploy
1. Push this folder to a GitHub repo (or run `vercel` in it).
2. Import in Vercel; framework preset "Other"; output directory `.`
3. Add the domain ocprobate.solutions in Vercel and point the registrar's DNS to Vercel (A record 76.76.21.21, or the CNAME Vercel shows).

## Connect the contact form
Edit `config.js` and set `formEndpoint` to the inbound webhook URL from the campaign platform. The form POSTs JSON with: name, email, phone, city, stage, question, call_ok, page, submitted. Until it is set, the form shows a direct-email fallback.

## Before launch
- Replace the headshot placeholder on the homepage (`.who .ph`) with an `<img>`.
- Replace the three review placeholders with verbatim reviews (with permission).
- Replace the four video placeholders with embedded players.
- Verify current thresholds and fees with an attorney; update `content.py` and rebuild.

## Rebuild after editing content
`python3 gen/build.py` writes the site to `out/`. Deploy `out/`.

## After launch (SEO / GEO)
- Submit sitemap.xml in Google Search Console and Bing Webmaster Tools.
- Create a Google Business Profile for Vennessa Mele with Orange County service area, linking here.
- Match the bio and DRE number exactly on Zillow, Realtor.com, LinkedIn, and the Cosine Realty site, all linking here.
- Add one new FAQ or guide a month; update the "Last reviewed" date when you do.
