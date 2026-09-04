import os, json, html, shutil
from content import *

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "out"))
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

def write(path, s):
    p = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s)

# ------------------------------------------------------------------ CSS
CSS = """:root{
  --paper:#F7F5EF;--panel:#FCFBF7;--card:#FFFFFF;
  --ink:#232E29;--soft:#455049;--muted:#6C766F;
  --pine:#1E4034;--pine-2:#2C5A48;--sage:#8FA99A;--sage-soft:#D8E2DB;
  --sand:#EDE6D6;--sand-2:#F2ECDF;--gold:#A9803F;
  --rule:#DCE3DD;--hair:#E9E4D8;--link:#1E5A48;
  --shadow:0 1px 2px rgba(31,61,51,.05),0 10px 30px rgba(31,61,51,.06);
  --shadow-sm:0 1px 2px rgba(31,61,51,.06);
  --serif:"Source Serif 4","Iowan Old Style",Georgia,serif;}
*{box-sizing:border-box}
html{font-size:18px;-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);line-height:1.62;font-weight:400;
  background-image:radial-gradient(60rem 30rem at 92% -8%,rgba(143,169,154,.10),transparent 60%);background-repeat:no-repeat}
a{color:var(--link);text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{color:var(--pine)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid var(--pine);outline-offset:2px;border-radius:2px}
.wrap{max-width:44rem;margin:0 auto;padding:0 1.25rem}

/* header */
header.top{border-bottom:1px solid var(--hair);background:color-mix(in srgb,var(--panel) 88%,transparent);backdrop-filter:saturate(1.05) blur(6px);position:sticky;top:0;z-index:20}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-top:.85rem;padding-bottom:.85rem;flex-wrap:wrap}
.brand{font-weight:600;color:var(--pine);text-decoration:none;font-size:1.08rem;letter-spacing:.005em;line-height:1.15;display:flex;flex-direction:column}
.brand::before{content:"";display:inline-block;width:1.6rem;height:1.6rem;margin-bottom:.28rem;border-radius:50%;
  background:radial-gradient(circle at 32% 30%,var(--sage),var(--pine) 78%);box-shadow:inset 0 0 0 3px rgba(255,255,255,.65)}
.brand small{display:block;font-weight:400;font-size:.78rem;color:var(--muted);letter-spacing:0}
nav.main a{margin-left:1.15rem;text-decoration:none;color:var(--soft);font-size:.94rem;padding-bottom:.15rem}
nav.main a:hover{color:var(--pine)}
nav.main a[aria-current]{color:var(--pine);border-bottom:2px solid var(--gold)}
main{padding:2.6rem 0 3.2rem}

/* type */
h1{font-size:2.2rem;line-height:1.12;font-weight:600;color:var(--pine);margin:0 0 1rem;letter-spacing:-.015em;text-wrap:balance}
h2{font-size:1.42rem;line-height:1.22;font-weight:600;color:var(--pine);margin:2.4rem 0 .7rem;letter-spacing:-.01em}
h2::before{content:"";display:block;width:2.2rem;height:2px;background:var(--gold);opacity:.7;margin-bottom:.7rem;border-radius:2px}
h3{font-size:1.12rem;font-weight:600;margin:1.7rem 0 .4rem;color:var(--pine-2)}
p{margin:0 0 1.1rem}
.lede{font-size:1.22rem;line-height:1.5;color:var(--soft);margin-bottom:1.6rem;text-wrap:pretty}
.eyebrow{display:inline-block;font-size:.74rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:.5rem}
.meta{font-size:.9rem;color:var(--muted);margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid var(--rule)}
ul,ol{padding-left:1.3rem}li{margin-bottom:.45rem}
dl.steps dt{font-weight:600;color:var(--pine);margin-top:1.1rem}
dl.steps dd{margin:.25rem 0 0 0;padding-left:1rem;border-left:3px solid var(--sage)}
ol.numbered li{margin-bottom:.8rem}

/* home letter — hero */
.letter{font-size:1.3rem;line-height:1.55;max-width:39rem;margin:.5rem 0 2.4rem;position:relative;padding:1.9rem 0 0}
.letter::before{content:"";position:absolute;top:0;left:0;width:3rem;height:3px;background:var(--gold);border-radius:3px}
.letter p:first-of-type{font-size:1.42rem;line-height:1.4;color:var(--pine)}
.letter p{margin-bottom:1.15rem}
.letter .sig{font-size:1rem;color:var(--muted);margin-top:1.4rem;padding-top:1.1rem;border-top:1px solid var(--hair)}
.letter .sig strong{display:block;color:var(--ink);font-size:1.1rem}

/* who / bio */
.who{display:grid;grid-template-columns:130px 1fr;gap:1.5rem;align-items:start;margin:2.5rem 0;background:var(--panel);border:1px solid var(--hair);border-radius:16px;padding:1.5rem;box-shadow:var(--shadow-sm)}
.who img,.who .ph{width:130px;height:162px;object-fit:cover;background:var(--sand);border:1px solid var(--rule);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:.75rem;color:var(--muted);text-align:center;padding:.5rem}
.who p{margin-bottom:.6rem}
.facts{font-size:.92rem;color:var(--soft);line-height:1.55}

/* quiet callout */
.quiet{background:linear-gradient(180deg,var(--sand-2),var(--sand));border:1px solid var(--hair);border-radius:16px;padding:1.4rem 1.5rem;margin:2.2rem 0;box-shadow:var(--shadow-sm)}
.quiet p:last-child{margin-bottom:0}
.quiet strong{color:var(--pine)}

/* contact form */
.contactbox{border:1px solid var(--hair);background:var(--panel);border-radius:18px;padding:1.7rem;margin:2.8rem 0 0;box-shadow:var(--shadow)}
.contactbox h2{margin-top:0}.contactbox h2::before{display:none}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem 1.3rem}
label{display:block;font-size:.9rem;font-weight:600;margin-bottom:.32rem;color:var(--soft)}
input,select,textarea{width:100%;font:inherit;font-size:1rem;padding:.68rem .8rem;border:1px solid #B9C4BC;background:#fff;color:var(--ink);border-radius:10px;transition:border-color .15s,box-shadow .15s}
input:focus,select:focus,textarea:focus{border-color:var(--pine);box-shadow:0 0 0 3px var(--sage-soft)}
textarea{min-height:6rem;resize:vertical}
.full{grid-column:1/-1}
button.primary{font:inherit;font-size:1.02rem;font-weight:600;background:var(--pine);color:#fff;border:0;padding:.8rem 1.5rem;cursor:pointer;border-radius:11px;box-shadow:var(--shadow-sm);transition:background .15s,transform .05s}
button.primary:hover{background:var(--pine-2)}
button.primary:active{transform:translateY(1px)}
.note{font-size:.9rem;color:var(--muted);margin-top:.8rem}
.status{margin-top:1rem;font-weight:600;color:var(--pine)}

/* reviews */
.reviews blockquote{margin:0 0 1.4rem;padding:1rem 1.2rem;border-left:3px solid var(--sage);background:var(--panel);border-radius:0 12px 12px 0;font-size:1.05rem}
.reviews blockquote p{margin:0}
.reviews cite{display:block;font-style:normal;font-size:.9rem;color:var(--muted);margin-top:.5rem}

/* videos */
.videos{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.videos .v{background:linear-gradient(160deg,#DEE7E0,#C7D5CD);aspect-ratio:16/9;display:flex;align-items:flex-end;padding:.85rem;font-size:.9rem;color:var(--pine);border:1px solid var(--hair);border-radius:12px;position:relative;overflow:hidden}
.videos .play{position:absolute;left:50%;top:44%;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:var(--pine);opacity:.92;box-shadow:0 4px 14px rgba(31,61,51,.3)}
.videos .play::after{content:"";position:absolute;left:18px;top:13px;border-left:14px solid #fff;border-top:10px solid transparent;border-bottom:10px solid transparent}
.videos .vt{line-height:1.3;font-weight:600}.videos .vt small{display:block;color:var(--muted);font-size:.8rem;margin-top:.15rem;font-weight:400}

/* guide index — cards */
.index{list-style:none;padding:0;display:grid;gap:.9rem}
.index li{margin:0}
.index li a{display:block;background:var(--card);border:1px solid var(--hair);border-radius:14px;padding:1rem 1.15rem;text-decoration:none;box-shadow:var(--shadow-sm);transition:transform .12s,box-shadow .12s,border-color .12s}
.index li a:hover{transform:translateY(-2px);box-shadow:var(--shadow);border-color:var(--sage)}
.index a strong,.index a b{color:var(--pine)}
.index li a{font-weight:600;color:var(--pine)}
.index span{display:block;color:var(--soft);font-size:.95rem;font-weight:400;margin-top:.25rem}

/* faq */
.faq details{border-top:1px solid var(--hair);padding:.7rem 0}
.faq details:last-child{border-bottom:1px solid var(--hair)}
.faq summary{cursor:pointer;font-weight:600;color:var(--pine);list-style:none;padding:.35rem 1.8rem .35rem 0;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:.2rem;top:.25rem;font-weight:400;color:var(--gold);font-size:1.2rem;line-height:1}
.faq details[open] summary::after{content:"2"}
.faq details p{margin:.55rem 0 .6rem}

/* toc */
.toc{font-size:.95rem;margin-bottom:2rem;padding:1.1rem 1.3rem;background:var(--panel);border:1px solid var(--hair);border-radius:14px}
.toc a{margin-right:1rem;white-space:nowrap}

/* aside */
.aside{margin-top:3rem;padding:1.6rem;border:1px solid var(--hair);background:var(--sand-2);border-radius:16px}
.aside p{margin-bottom:.6rem}.aside p:last-child{margin-bottom:0}

/* cities */
.cities{columns:2;column-gap:2rem}
.cities li{break-inside:avoid;margin-bottom:.5rem}

/* checklist */
.check h2{margin-top:2rem}
.check ul{list-style:none;padding:0}
.check li{padding-left:1.9rem;position:relative;margin-bottom:.75rem}
.check li::before{content:"";position:absolute;left:0;top:.35rem;width:.9rem;height:.9rem;border:1.5px solid var(--pine);border-radius:4px}

/* timeline */
.timeline{list-style:none;padding:0;margin:0}
.timeline li{display:grid;grid-template-columns:7.5rem 1fr;gap:1rem;padding:1rem 0;border-top:1px solid var(--hair)}
.timeline li:last-child{border-bottom:1px solid var(--hair)}
.timeline .when{font-weight:600;color:var(--pine)}

/* footer */
footer.bottom{border-top:1px solid var(--hair);background:var(--panel);font-size:.85rem;color:var(--muted);padding:2rem 0 2.8rem;line-height:1.55;margin-top:3.5rem}
footer.bottom p{margin-bottom:.5rem}
footer.bottom a{color:var(--soft)}

.print{display:none}
@media (max-width:640px){html{font-size:17px}.grid,.videos{grid-template-columns:1fr}.who{grid-template-columns:100px 1fr;gap:1rem;padding:1.1rem}.who img,.who .ph{width:100px;height:125px}.cities{columns:1}.timeline li{grid-template-columns:1fr;gap:.2rem}nav.main a{margin-left:0;margin-right:1.1rem}h1{font-size:1.8rem}.letter{font-size:1.18rem}.letter p:first-of-type{font-size:1.28rem}}
@media print{header.top,footer.bottom,.contactbox,.aside,.toc,nav{display:none}.print{display:block}body{background:#fff;font-size:11pt}main{padding:0}.who,.quiet{box-shadow:none}}
/* tools */
.tool{border:1px solid var(--hair);background:var(--panel);border-radius:16px;padding:1.4rem;margin:0 0 1.2rem;box-shadow:var(--shadow-sm)}
.tool h3{margin-top:0}.tool h3::before{display:none}
.trow{display:flex;gap:.6rem}.trow input{flex:1}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem 1.3rem}
.result{font-family:var(--serif);font-weight:600;font-size:2.1rem;color:var(--pine);margin:1rem 0 .2rem;letter-spacing:-.01em}
.netline{display:flex;justify-content:space-between;gap:1rem;padding:.55rem 0;border-bottom:1px solid var(--hair);font-size:.98rem}
.netline span:last-child{font-weight:600;font-variant-numeric:tabular-nums}
.accentbox{border-color:var(--sage)!important;background:linear-gradient(180deg,var(--sand-2),var(--panel))}
.toolgrid li a b{font-size:1.06rem}
.comps{width:100%;border-collapse:collapse;font-size:.92rem}
.comps th{text-align:left;color:var(--muted);font-weight:600;padding:.5rem;border-bottom:1px solid var(--hair);white-space:nowrap}
.comps td{padding:.5rem;border-bottom:1px solid var(--hair);white-space:nowrap}
.glossary dt{font-weight:600;color:var(--pine);margin-top:1.15rem;font-size:1.02rem}
.glossary dd{margin:.3rem 0 0;padding:0;color:var(--soft)}
@media(max-width:640px){.trow{flex-direction:column}.g3{grid-template-columns:1fr 1fr}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

# ------------------------------------------------------------------ SCHEMA
PERSON = {
 "@type":"RealEstateAgent","@id":SITE+"/#vennessa","name":NAME,
 "url":SITE,"telephone":PHONE_TEL,"email":EMAIL,
 "identifier":{"@type":"PropertyValue","propertyID":"California DRE License","value":DRE},
 "areaServed":{"@type":"AdministrativeArea","name":"Orange County, California"},
 "knowsAbout":["Probate real estate","Inherited property sales","Court confirmation sales","Estate sales"],
 "worksFor":{"@type":"RealEstateAgent","name":BROKER,"identifier":{"@type":"PropertyValue","propertyID":"California DRE License","value":BROKER_LIC}},
}

def schema(obj):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org",**obj},ensure_ascii=False)+'</script>'

# ------------------------------------------------------------------ LAYOUT
NAV = [("/guide/","Guides"),("/tools/","Tools"),("/faq/","Questions"),("/glossary/","Glossary"),("/orange-county/","Cities"),("/resources/","Resources"),("/contact/","Contact")]

def page(path, title, desc, body, extra_head="", canonical=None, current=None):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a>' for h,t in NAV)
    canon = canonical or (SITE+path)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="OC Probate Solutions">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{extra_head}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="/">OC Probate Solutions<small>{NAME}, Realtor · Orange County</small></a>
<nav class="main" aria-label="Main">{nav}</nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="bottom"><div class="wrap">
<p>{NAME}, California real estate salesperson, DRE #{DRE}, licensed under {BROKER}, DRE #{BROKER_LIC}. {PHONE} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>This site explains how probate real estate works in Orange County so that executors and heirs can make informed decisions. It is not legal, tax, or financial advice. Figures such as thresholds, fees, and deadlines change; verify current numbers with your attorney or the court. Content last reviewed {UPDATED}.</p>
<p><a href="/guide/">Guides</a> · <a href="/faq/">Questions</a> · <a href="/orange-county/">Cities</a> · <a href="/resources/">Resources</a> · <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a></p>
</div></footer>
</body></html>"""
    write(path+("index.html" if path.endswith("/") else ""), doc)

CONTACT_FORM = """
<div class="contactbox" id="ask">
<h2>Ask a question, or tell me where you are</h2>
<p>I reply by email within one business day. No calls unless you ask for one.</p>
<form id="askform" novalidate>
<div class="grid">
<div><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
<div><label for="f-city">City of the property</label><input id="f-city" name="city"></div>
<div class="full"><label for="f-stage">Where are you in the process?</label>
<select id="f-stage" name="stage">
<option value="">Choose one</option>
<option>Just lost someone, haven't done anything yet</option>
<option>Talking to an attorney / about to file</option>
<option>Appointed, have my Letters</option>
<option>Not sure yet</option>
<option>Ready to talk about selling</option>
<option>Just want a value on the house</option>
</select></div>
<div class="full"><label for="f-q">Your question (optional)</label><textarea id="f-q" name="question"></textarea></div>
<div class="full"><label style="font-weight:400"><input type="checkbox" name="call_ok" value="yes" style="width:auto;margin-right:.5rem">It's okay to call me instead of emailing</label></div>
<div class="full"><button class="primary" type="submit">Send to Vennessa</button><div class="status" id="askstatus" aria-live="polite"></div></div>
</div>
</form>
<p class="note">Your information goes to Vennessa and nowhere else. It is never sold or shared with investors.</p>
</div>
<script src="/config.js"></script>
<script>
(function(){var f=document.getElementById('askform'),s=document.getElementById('askstatus');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();
var d=Object.fromEntries(new FormData(f).entries());d.page=location.pathname;d.submitted=new Date().toISOString();
if(!d.name||!d.email){s.textContent='Please add your name and an email address so I can reply.';return;}
s.textContent='Sending…';
var url=(window.SITE_CONFIG||{}).formEndpoint;
if(!url){s.textContent='The form is not connected yet. Email me directly at '+'"""+EMAIL+"""'+'.';return;}
fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
.then(function(r){if(!r.ok)throw 0;s.textContent='Sent. I will reply to '+d.email+' within one business day.';f.reset();})
.catch(function(){s.textContent='That did not go through. Email me directly at '+'"""+EMAIL+"""'+' and I will reply the same way.';});
});})();
</script>
"""

ASIDE = f"""
<div class="aside">
<p><strong>Have a question about your own situation?</strong> Email me a photo of your Letters and the property address, and I will tell you what your authority means and what the house is likely worth. It costs nothing and there is no obligation.</p>
<p><a href="/contact/">Ask a question</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
</div>"""

# ------------------------------------------------------------------ HOME
guide_links = "".join(f'<li><a href="/guide/{g["slug"]}/">{g["title"]}</a><span>{g["summary"]}</span></li>' for g in GUIDES[:5])
home = f"""
<span class="eyebrow">Orange County probate</span>
<h1>Selling a house in probate in Orange County</h1>
<div class="letter">
<p>If you are reading this, you have probably just been handed responsibility for a house that belonged to someone you loved, along with a stack of paperwork and a mailbox filling up with offers from people you have never met.</p>
<p>I sell probate homes in Orange County. Most of what I do is explain how the process works, tell families what their house is actually worth, and then wait until they are ready. Some of them sell. Some keep the house. Either is fine.</p>
<p>Everything on this site is free to read and use. If you want to talk, I am easy to reach. If you do not, I hope the guides help.</p>
<p class="sig"><strong>{NAME}</strong>Realtor, DRE #{DRE} · {BROKER}<br>Orange County, California</p>
</div>

<div class="who">
<img src="/img/headshot-placeholder.svg" alt="Vennessa Mele, placeholder portrait" width="120" height="150">
<div>
<p>I have worked with executors, administrators, and trustees across Orange County, from Fullerton to Mission Viejo and the coast in between. I know what Letters mean, how a Notice of Proposed Action works, and what to expect at a confirmation hearing at the Costa Mesa Justice Center. I coordinate directly with your attorney so nothing falls between us.</p>
<p class="facts">California DRE #{DRE} · {BROKER}, DRE #{BROKER_LIC} · <a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
</div>

<h2>Start here</h2>
<ul class="index">{guide_links}</ul>
<p><a href="/guide/">All guides</a> · <a href="/faq/">Answers to common questions</a> · <a href="/resources/executor-checklist/">The executor's checklist</a></p>

<h2>Short videos</h2>
<p>One question each, about a minute long.</p>
<div class="videos">
<div class="v"><span class="play" aria-hidden="true"></span><span class="vt">Who I am and why I work with probate families<small>1:04 · coming soon</small></span></div>
<div class="v"><span class="play" aria-hidden="true"></span><span class="vt">The three things every executor needs to do first<small>0:58 · coming soon</small></span></div>
<div class="v"><span class="play" aria-hidden="true"></span><span class="vt">Full authority vs. limited authority<small>1:12 · coming soon</small></span></div>
<div class="v"><span class="play" aria-hidden="true"></span><span class="vt">The investor letters, and what the house is really worth<small>1:07 · coming soon</small></span></div>
</div>

<h2>What families have said</h2>
<p class="note">Sample reviews shown for layout; verified client reviews will replace them.</p>
<div class="reviews">
<!-- SAMPLE REVIEWS for layout only. Replace with verbatim client reviews (with permission) before launch. -->
<blockquote>My dad's house in Fullerton had fifty years of everything in it and I live in Phoenix. Vennessa explained what my Letters meant, found the estate sale people, and sent me photos every week. I never once felt pushed. When we were ready, it sold in nine days.<cite>Karen, Fullerton (sample)</cite></blockquote>
<blockquote>There were four of us and we did not agree on anything. She got us all on one call, walked through the comps, and somehow we left that call with a plan. My brother still says she is the reason we are speaking.<cite>Michael, Huntington Beach (sample)</cite></blockquote>
<blockquote>We had limited authority and a court hearing, which terrified me. She told me exactly what would happen, sat with me in the courtroom in Costa Mesa, and the sale was confirmed with no overbid. Our attorney said she was the most prepared agent he had worked with.<cite>Diane, Orange (sample)</cite></blockquote>
</div>

<div class="quiet">
<p><strong>Do you even need an agent?</strong> Not always. If one heir is buying the others out, or the estate is small enough for a simplified procedure and the family already has a buyer, you may not. I will tell you that if it is true. What I will not do is send you a cash offer, put you on a call list, or tell you there is a deadline when there is not.</p>
</div>

{CONTACT_FORM}
"""
home_schema = schema({"@graph":[
 {"@type":"WebSite","@id":SITE+"/#site","url":SITE,"name":"OC Probate Solutions","description":"Plain-language guides for Orange County executors and heirs on selling a house during probate, by Realtor Vennessa Mele.","publisher":{"@id":SITE+"/#vennessa"}},
 PERSON,
 {"@type":"WebPage","@id":SITE+"/#page","url":SITE,"name":"Selling a house in probate in Orange County","isPartOf":{"@id":SITE+"/#site"},"about":{"@id":SITE+"/#vennessa"}},
]})
page("/","Selling a house in probate in Orange County | Vennessa Mele, Realtor",
     "Plain-language help for Orange County executors and heirs: how probate works, what your Letters mean, what the house is worth, and when to sell. Free guides from Realtor Vennessa Mele.",
     home, home_schema)

# ------------------------------------------------------------------ GUIDES
gl = "".join(f'<li><a href="/guide/{g["slug"]}/">{g["title"]}</a><span>{g["summary"]}</span></li>' for g in GUIDES)
page("/guide/","Probate real estate guides for Orange County executors",
     "Long-form guides on probate timelines, full vs. limited authority, court confirmation, step-up in basis, selling as-is, investor offers, heirs, and clean-outs.",
     f"<h1>Guides</h1><p class='lede'>Everything an Orange County executor needs to know about the house, written to be read on a phone at 11pm. Each guide starts with the short answer.</p><ul class='index'>{gl}</ul>"+ASIDE,
     current="/guide/")

for i,g in enumerate(GUIDES):
    url=f"/guide/{g['slug']}/"
    prev_=GUIDES[i-1] if i>0 else None; next_=GUIDES[i+1] if i<len(GUIDES)-1 else None
    nxt = f"<p class='note'>Next guide: <a href='/guide/{next_['slug']}/'>{next_['title']}</a></p>" if next_ else ""
    body=f"<h1>{g['title']}</h1><p class='lede'>{g['summary']}</p><p class='meta'>By {NAME}, DRE #{DRE} · Orange County, California · Last reviewed {UPDATED}</p>{g['body']}{nxt}{ASIDE}"
    sch=schema({"@type":"Article","headline":g['title'],"description":g['summary'],"url":SITE+url,"dateModified":"2026-09-01","author":{"@id":SITE+"/#vennessa"},"publisher":{"@id":SITE+"/#vennessa"},"about":"Probate real estate in Orange County, California","keywords":g['keywords'],"mainEntityOfPage":SITE+url})
    page(url,f"{g['title']} | OC Probate Solutions",g['summary'],body,sch+schema(PERSON),current="/guide/")

# ------------------------------------------------------------------ FAQ
def slug(s):
    import re
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:60]
toc="".join(f'<a href="#{slug(c)}">{c}</a> ' for c,_ in FAQ)
faq_html=f"<div class='toc'>{toc}</div>"
entities=[]
for cat,qs in FAQ:
    faq_html+=f"<h2 id='{slug(cat)}'>{cat}</h2><div class='faq'>"
    for q,a in qs:
        anchor="prop-19" if "Proposition 19" in q else slug(q)
        faq_html+=f"<details id='{anchor}'><summary>{q}</summary><p>{a}</p></details>"
        entities.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    faq_html+="</div>"
n=sum(len(q) for _,q in FAQ)
page("/faq/",f"{n} questions Orange County executors ask about selling a house in probate",
     "Direct answers on probate timelines, Letters, full vs. limited authority, court confirmation, mortgages, insurance, taxes, Prop 19, investor offers, and working with an agent.",
     f"<h1>Questions executors ask</h1><p class='lede'>{n} questions, each answered in a few sentences. Answers are specific to California and, where it matters, to Orange County.</p>{faq_html}{ASIDE}",
     schema({"@type":"FAQPage","mainEntity":entities})+schema(PERSON), current="/faq/")

# ------------------------------------------------------------------ CITIES
cl="".join(f'<li><a href="/orange-county/{s}/">{n}</a></li>' for s,n,_ in CITIES)
page("/orange-county/","Probate home sales by city in Orange County",
     "What is different about selling a probate home in Anaheim, Irvine, Santa Ana, Huntington Beach, Fullerton, Costa Mesa, Newport Beach, and other Orange County cities.",
     f"<h1>Orange County, city by city</h1><p class='lede'>Probate works the same everywhere in the county; the houses, the buyers, and the questions do not. All hearings are at the Costa Mesa Justice Center regardless of where the property is.</p><ul class='cities'>{cl}</ul><p>Not listed? I work throughout the county. <a href='/contact/'>Ask about your city.</a></p>{ASIDE}",
     current="/orange-county/")
for s,n,d in CITIES:
    url=f"/orange-county/{s}/"
    body=f"""<h1>Selling a probate home in {n}</h1>
<p class='lede'>{d}</p>
<p class='meta'>By {NAME}, DRE #{DRE} · Last reviewed {UPDATED}</p>
<h2>What is the same everywhere in Orange County</h2>
<ul>
<li>The probate petition is filed with the Orange County Superior Court and heard at the Costa Mesa Justice Center, 3390 Harbor Boulevard, Costa Mesa.</li>
<li>Your authority to sell comes from your Letters. <a href="/guide/full-authority-vs-limited-authority/">Full authority</a> means a normal sale with a 15-day notice to heirs; limited authority means a <a href="/guide/court-confirmation-sale-explained/">court confirmation hearing</a>.</li>
<li>The house's tax basis <a href="/guide/step-up-in-basis-inherited-house/">steps up</a> to its value at the date of death.</li>
<li>A Change in Ownership Statement (BOE-502-D) is due to the Orange County Assessor within 150 days.</li>
</ul>
<h2>What I check first for a {n} property</h2>
<ul>
<li>Title: how it was held, and whether it is actually in probate or passes another way.</li>
<li>Permits: the Assessor's square footage against what is actually there.</li>
<li>Any HOA, Mello-Roos, or special assessments, and the transfer paperwork they require.</li>
<li>Recent sales of comparable homes within a half mile, adjusted for condition, as of the date of death and today.</li>
</ul>
<h2>What it is worth</h2>
<p>I will pull the comparable sales for a {n} property at no cost and tell you what it would bring on the open market and whether any offer you have received is reasonable. Send me the address and, if you have them, a photo of your Letters.</p>
<p><a href="/guide/">All guides</a> · <a href="/faq/">Questions</a> · <a href="/orange-county/">Other cities</a></p>{ASIDE}"""
    sch=schema({"@type":"WebPage","url":SITE+url,"name":f"Selling a probate home in {n}","description":d,"about":{"@type":"Place","name":f"{n}, California"},"author":{"@id":SITE+"/#vennessa"}})
    page(url,f"Selling a probate home in {n}, CA | Vennessa Mele",f"What executors should know about selling an inherited house in {n}, Orange County: authority, hearings, disclosures, buyers, and value.",body,sch+schema(PERSON),current="/orange-county/")

# ------------------------------------------------------------------ RESOURCES
page("/resources/","Executor resources: checklist, probate timeline, and who to call",
     "A printable executor's checklist, a California probate timeline, and the kinds of professionals an Orange County estate usually needs.",
     f"""<h1>Resources</h1>
<p class='lede'>Two printable guides and a short list of who else you may need. No email required.</p>
<ul class='index'>
<li><a href="/resources/executor-checklist/">The executor's checklist</a><span>Every task from the first two weeks through closing the estate, in order. Print it and check things off.</span></li>
<li><a href="/resources/probate-timeline/">The California probate timeline</a><span>What happens when, from filing the petition to final distribution, with where the house fits.</span></li>
</ul>
<h2>Who else an estate usually needs</h2>
<dl class='steps'>
<dt>A probate attorney</dt><dd>Files the petition, handles notices and the accounting, and answers to the court. Fees are statutory and paid from the estate at the end. I can introduce you to attorneys in Orange County who do this every day and return calls.</dd>
<dt>A CPA who handles estates</dt><dd>For the decedent's final return, the estate's fiduciary return, and basis questions. Worth a one-hour consultation even for simple estates.</dd>
<dt>An estate sale company</dt><dd>Sells the contents on site for a share of proceeds. Most will do a free walkthrough and tell you if there is enough to hold a sale.</dd>
<dt>A clean-out and hauling service</dt><dd>For whatever an estate sale and donations do not take. Ask for a flat quote after a walkthrough.</dd>
<dt>A locksmith and a handyman</dt><dd>Re-key the house early. Fix safety items before anyone walks through.</dd>
<dt>Orange County offices</dt><dd>Superior Court probate: Costa Mesa Justice Center, 3390 Harbor Blvd. Clerk-Recorder for death certificates and recorded deeds. Assessor for the Change in Ownership Statement. Links change; search the office name and "Orange County" for the current page.</dd>
</dl>
<p>I keep a current list of the professionals I actually work with. <a href="/contact/">Ask and I will send it.</a></p>{ASIDE}""",current="/resources/")

ck=""
for h,items in CHECKLIST:
    ck+=f"<h2>{h}</h2><ul>"+"".join(f"<li>{i}</li>" for i in items)+"</ul>"
page("/resources/executor-checklist/","The executor's checklist for a California probate with a house",
     "A printable, in-order checklist for personal representatives: securing the house, filing, Letters, creditors, selling, and closing the estate.",
     f"<div class='check'><h1>The executor's checklist</h1><p class='lede'>In order, from the first two weeks through closing the estate. Print it. Not every item applies to every estate; your attorney will tell you which to skip.</p><p class='meta'>Prepared by {NAME}, DRE #{DRE} · {UPDATED} · Not legal advice</p>{ck}<p class='print'>ocprobate.solutions · {NAME} · {PHONE} · {EMAIL}</p></div>{ASIDE}",
     schema({"@type":"HowTo","name":"Executor's checklist for a California probate with real property","author":{"@id":SITE+"/#vennessa"},"step":[{"@type":"HowToSection","name":h,"itemListElement":[{"@type":"HowToStep","text":i} for i in items]} for h,items in CHECKLIST]})+schema(PERSON),
     current="/resources/")

TL=[("Week 0","Death. Secure the house, keep insurance and utilities current, locate the will."),
("Weeks 1–6","Meet an attorney. Petition for Probate filed with Orange County Superior Court. Notice published and mailed to heirs."),
("Weeks 6–12","Hearing at the Costa Mesa Justice Center. Personal representative appointed. Letters issued, with full or limited authority."),
("Month 3","Estate bank account opened. Notice to creditors mailed; four-month claim period begins. BOE-502-D filed with the Assessor (150-day deadline from death)."),
("Months 3–4","Probate referee appraises the house as of the date of death. Inventory and Appraisal filed."),
("Months 3–6","House cleaned out and listed. Offer accepted."),
("Months 4–7","Full authority: Notice of Proposed Action mailed, 15 days pass, escrow closes. Limited authority: petition for confirmation filed, hearing 6–10 weeks out, sale confirmed or overbid, escrow closes."),
("Month 7","Creditor claim period ends. Claims paid or rejected."),
("Months 7–12","Tax returns filed. Attorney prepares the accounting."),
("Months 9–18","Petition for final distribution heard. Court approves. Heirs receive their shares. Estate closes."),]
tl="".join(f"<li><span class='when'>{w}</span><span>{t}</span></li>" for w,t in TL)
page("/resources/probate-timeline/","The California probate timeline, with where the house fits",
     "A month-by-month timeline of a typical Orange County probate, from petition to final distribution, showing when the house can be listed and sold.",
     f"<h1>The California probate timeline</h1><p class='lede'>A typical uncontested Orange County probate. Yours will differ; the order rarely does.</p><p class='meta'>Prepared by {NAME}, DRE #{DRE} · {UPDATED} · Not legal advice</p><ul class='timeline'>{tl}</ul><p class='note' style='margin-top:1.5rem'>Court calendars, contested petitions, and creditor disputes extend this. Read <a href='/guide/how-long-probate-takes-california/'>how long probate really takes</a> for what slows it down.</p><p class='print'>ocprobate.solutions · {NAME} · {PHONE} · {EMAIL}</p>{ASIDE}",
     schema(PERSON),current="/resources/")

# ------------------------------------------------------------------ CONTACT / PRIVACY
page("/contact/","Contact Vennessa Mele about a probate home in Orange County",
     "Ask a question about your Letters, your authority, or what the house is worth. Free, no obligation, reply by email within one business day.",
     f"<h1>Contact</h1><p class='lede'>Email is fastest. If you send a photo of your Letters and the property address, I can usually answer your first questions in one reply.</p><p><a href='mailto:{EMAIL}'>{EMAIL}</a><br><a href='tel:{PHONE_TEL}'>{PHONE}</a> (text is fine)</p><p class='facts'>{NAME} · California DRE #{DRE} · {BROKER}, DRE #{BROKER_LIC} · Orange County</p>{CONTACT_FORM}",
     schema(PERSON),current="/contact/")
page("/privacy/","Privacy","How information submitted on this site is used.",
     f"<h1>Privacy</h1><p>Anything you send through this site goes to {NAME} and to the campaign platform that delivers it to her. It is used to reply to you and, if you ask, to keep in touch about your property. It is not sold, shared with investors, or added to any list you did not ask to be on. Ask to be removed at any time by emailing <a href='mailto:{EMAIL}'>{EMAIL}</a> and it will be done the same day. This site uses no advertising cookies.</p>")

# ------------------------------------------------------------------ STATIC FILES
write("/styles.css",CSS)
write("/img/headshot-placeholder.svg","""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 150" role="img" aria-label="Headshot placeholder"><rect width="120" height="150" fill="#E3E9E4"/><circle cx="60" cy="58" r="24" fill="#B7C9BE"/><path d="M18 150c4-32 22-46 42-46s38 14 42 46z" fill="#B7C9BE"/><text x="60" y="140" font-family="Georgia,serif" font-size="9" fill="#1F3D33" text-anchor="middle">Photo coming</text></svg>""")
write("/config.js","""// Contact-form endpoint. Posts JSON to the in-house /api/lead serverless function,
// which files the lead in the Lead To Close CRM (tagged `probate`, assigned to Vennessa).
window.SITE_CONFIG = { formEndpoint: "/api/lead/" };
""")
from tools import emit_tools
emit_tools(page, schema, PERSON, ASIDE)

urls=["/","/guide/","/tools/","/tools/home-value/","/tools/market-analysis/","/tools/mortgage-calculator/","/tools/dscr-calculator/","/tools/find-a-home/","/glossary/","/faq/","/orange-county/","/resources/","/resources/executor-checklist/","/resources/probate-timeline/","/contact/"]+[f"/guide/{g['slug']}/" for g in GUIDES]+[f"/orange-county/{s}/" for s,_,_ in CITIES]
write("/sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{SITE}{u}</loc><lastmod>2026-09-01</lastmod></url>\n" for u in urls)+"</urlset>\n")
write("/robots.txt",f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
write("/llms.txt",f"""# OC Probate Solutions

> Plain-language guides for executors, administrators, and heirs selling a house during probate in Orange County, California. Written by {NAME}, a California-licensed real estate salesperson (DRE #{DRE}) with {BROKER} (DRE #{BROKER_LIC}) who specializes in probate and inherited-property sales throughout Orange County.

Contact: {EMAIL}, {PHONE}. Free consultations; no obligation.

## Guides
"""+"".join(f"- [{g['title']}]({SITE}/guide/{g['slug']}/): {g['summary']}\n" for g in GUIDES)+f"""
## Questions
- [{n} questions executors ask]({SITE}/faq/): direct answers on Letters, authority, court confirmation, mortgages, insurance, taxes, Prop 19, investor offers.

## Resources
- [Executor's checklist]({SITE}/resources/executor-checklist/)
- [California probate timeline]({SITE}/resources/probate-timeline/)

## Cities
"""+"".join(f"- [{n_}]({SITE}/orange-county/{s}/)\n" for s,n_,_ in CITIES)+"""
## Key facts (California)
- Orange County probate hearings: Costa Mesa Justice Center, 3390 Harbor Blvd, Costa Mesa.
- Full authority under the IAEA allows sale of real property with a 15-day Notice of Proposed Action and no hearing; limited authority requires court confirmation with overbidding (minimum 10% of first $10,000 plus 5% of balance; accepted price at least 90% of probate referee appraisal).
- Creditor claim period: four months from issuance of Letters.
- Inherited real property receives a stepped-up tax basis to fair market value at date of death.
- Change in Ownership Statement (BOE-502-D) due to the county assessor within 150 days of death.
- Statutory attorney and personal representative fees: 4% of first $100,000, 3% of next $100,000, 2% of next $800,000, 1% of next $9,000,000.
- Simplified succession petition available for a primary residence valued at $750,000 or less (deaths on or after April 1, 2025).
""")
write("/vercel.json",json.dumps({"cleanUrls":True,"trailingSlash":True,"headers":[{"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"}]}]},indent=2))
write("/README.md",f"""# ocprobate.solutions

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
- Create a Google Business Profile for {NAME} with Orange County service area, linking here.
- Match the bio and DRE number exactly on Zillow, Realtor.com, LinkedIn, and the {BROKER} site, all linking here.
- Add one new FAQ or guide a month; update the "Last reviewed" date when you do.
""")
print("pages:",len(urls))
