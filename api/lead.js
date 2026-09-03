// api/lead.js — receives the contact-form JSON and files it in the in-house Lead To Close CRM.
// It calls the capture_probate_lead RPC, which inserts the lead tagged `probate`, assigned to
// Vennessa Mele, and the CRM's trg_notify_new_lead trigger emails/texts her (48-hour partner
// notification per the referral agreement). No third-party marketing platform is involved.
//
// The publishable ("anon") key below is public by design and only grants EXECUTE on this one
// SECURITY DEFINER RPC; override via the SUPABASE_ANON_KEY env var in Vercel if you prefer.
const SUPA = process.env.SUPABASE_URL || "https://jqbtbftwmlkikvpwyqgv.supabase.co";
const KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_JD2RtlMt2pg13lZzmP4Cug_xxLGXfSd";

export default async function handler(req, res) {
  if (req.method !== "POST") { res.status(405).json({ ok: false, error: "method_not_allowed" }); return; }

  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b && typeof b === "object" ? b : {};

  // Only forward the fields the CRM expects (ignore anything extra a bot might inject).
  const p = {
    name: b.name, email: b.email, phone: b.phone, city: b.city,
    stage: b.stage, question: b.question, call_ok: b.call_ok,
    page: b.page, hp: b.hp,
  };

  if (!p.name || !p.email) { res.status(400).json({ ok: false, error: "missing_name_or_email" }); return; }

  try {
    const r = await fetch(`${SUPA}/rest/v1/rpc/capture_probate_lead`, {
      method: "POST",
      headers: { apikey: KEY, Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ p }),
    });
    const d = await r.json().catch(() => ({}));
    if (r.ok && d && d.ok) { res.status(200).json({ ok: true }); return; }
    res.status(502).json({ ok: false, error: (d && d.error) || "capture_failed" });
  } catch {
    res.status(502).json({ ok: false, error: "network_error" });
  }
}
