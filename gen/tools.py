# Interactive tools for the probate site. Kept out of build.py's f-strings because the
# client JS uses ${} / {} which would collide with Python formatting. Each tool submission
# posts to /api/lead/ (or the ocprobate-cma fn) and is filed as a probate lead for Vennessa.
from content import NAME, EMAIL, PHONE, PHONE_TEL, DRE, BROKER, BROKER_LIC, SITE

SUPA = "https://jqbtbftwmlkikvpwyqgv.supabase.co"
ANON = "sb_publishable_JD2RtlMt2pg13lZzmP4Cug_xxLGXfSd"

HP = '<div style="position:absolute;left:-9999px" aria-hidden="true"><label>Leave this blank<input id="hp" tabindex="-1" autocomplete="off"></label></div>'

JS_HEAD = (
    'var SUPA="' + SUPA + '",ANON="' + ANON + '",EMAILTO="' + EMAIL + '";'
    'var $=function(i){return document.getElementById(i);};'
    'var money=function(n){return (n||n===0)?"$"+Math.round(Number(n)).toLocaleString("en-US"):"\\u2014";};'
    'var num=function(i){var v=parseFloat(String($(i).value).replace(/[,$\\s%]/g,""));return isNaN(v)?0:v;};'
)


def emit_tools(page, schema, PERSON, ASIDE):
    # ---------------------------------------------------------------- HUB
    hub = (
        '<span class="eyebrow">Free tools</span>'
        '<h1>Tools for executors, heirs &amp; buyers</h1>'
        '<p class="lede">Real answers in seconds — the same professional tools I use, free for you to try. '
        'Nothing to sign, and no one calls unless you ask.</p>'
        '<ul class="index toolgrid">'
        '<li><a href="/tools/home-value/"><b>What’s the home worth — and what would the estate net?</b>'
        '<span>Instant estimated value, then adjust for the mortgage payoff and selling costs to see the estate’s net proceeds.</span></a></li>'
        '<li><a href="/tools/market-analysis/"><b>Instant market analysis (CMA)</b>'
        '<span>Estimated value, recent comparable sales nearby, and the local market — instantly — plus a full CMA prepared by hand.</span></a></li>'
        '<li><a href="/tools/mortgage-calculator/"><b>Mortgage calculator</b>'
        '<span>For an heir keeping the home, or a buyer — estimate the full monthly payment including taxes and insurance.</span></a></li>'
        '<li><a href="/tools/dscr-calculator/"><b>DSCR calculator (for investors)</b>'
        '<span>Buying a probate home as a rental? See the debt-service coverage ratio and whether it pencils.</span></a></li>'
        '<li><a href="/tools/find-a-home/"><b>Find a home</b>'
        '<span>Search homes for sale across Southern California, including probate and estate opportunities.</span></a></li>'
        '<li><a href="/glossary/"><b>Probate terms &amp; definitions</b>'
        '<span>Plain-English definitions of the words you’ll run into — Letters, authority, overbid, and more.</span></a></li>'
        '</ul>'
        '<h2>Prefer to just ask?</h2>'
        '<p>Every tool is optional. If you’d rather talk it through, email me a photo of your Letters and the property address and I’ll tell you what your authority means and what the house is likely worth. <a href="/contact/">Ask a question →</a></p>'
        + ASIDE
    )
    page("/tools/", "Free probate real-estate tools — home value, CMA, mortgage & DSCR | " + NAME,
         "Free instant tools for Orange County executors, heirs, and buyers: estimated home value and net proceeds, an instant market analysis with comps, a mortgage calculator, and a DSCR calculator for investors.",
         hub, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- HOME VALUE / NETVALUE
    hv = (
        '<span class="eyebrow">Free · instant · no obligation</span>'
        '<h1>What is the home worth — and what would the estate net?</h1>'
        '<p class="lede">Enter the property address for an instant estimated value, then adjust for any mortgage or lien payoff and typical selling costs to see the estate’s net proceeds. Nothing to sign; no one calls unless you ask.</p>'
        '<div class="tool">'
        '<label for="addr">Property address</label>'
        '<div class="trow"><input id="addr" placeholder="123 Main St, Santa Ana, CA 92701" autocomplete="off"><button class="primary" id="lookup" type="button">Get value</button></div>'
        '<div class="note" id="lmsg">We’ll pull an estimated value — you can adjust everything below.</div>'
        '</div>'
        '<div class="tool">'
        '<h3>The numbers — edit any of these</h3>'
        '<div class="grid">'
        '<div><label>Estimated value</label><input id="value" type="number" inputmode="numeric" oninput="calcNet()"></div>'
        '<div><label>Mortgage / liens payoff</label><input id="payoff" type="number" inputmode="numeric" value="0" oninput="calcNet()"></div>'
        '</div>'
        '<div class="g3">'
        '<div><label>Selling costs %</label><input id="sell" type="number" step="0.1" value="6" oninput="calcNet()"></div>'
        '<div><label>Repairs / cleanout $</label><input id="repairs" type="number" inputmode="numeric" value="0" oninput="calcNet()"></div>'
        '<div><label>Other costs $</label><input id="other" type="number" inputmode="numeric" value="0" oninput="calcNet()"></div>'
        '</div>'
        '<div id="breakdown"></div>'
        '<div class="result" id="net">—</div>'
        '<div class="note" id="netsub">Enter an address (or a value) to see the estate’s estimated net proceeds.</div>'
        '</div>'
        '<div class="tool accentbox">'
        '<h3>Get this in writing — plus a real market analysis</h3>'
        '<p>I’ll email you this breakdown and a proper comparative market analysis for the home, prepared by hand. Free, no obligation, and I coordinate directly with your attorney if you have one.</p>'
        + HP +
        '<div class="grid"><div><label>Your name</label><input id="n" autocomplete="name"></div><div><label>Email</label><input id="e" type="email" autocomplete="email"></div></div>'
        '<div class="grid"><div><label>Phone (optional)</label><input id="p" type="tel" autocomplete="tel"></div><div><label>City of the property</label><input id="c"></div></div>'
        '<button class="primary" id="send" type="button" style="margin-top:.9rem">Email me my report →</button>'
        '<div class="status" id="smsg" aria-live="polite"></div>'
        '<p class="note">Estimate only, from public data and an automated valuation. Actual value and net proceeds depend on condition, payoff, and final price. Not legal, tax, or financial advice.</p>'
        '</div>'
        '<script>(function(){' + JS_HEAD +
        'var PROP={};'
        'window.calcNet=function(){var value=num("value");'
        'if(!value){$("net").textContent="\\u2014";$("netsub").textContent="Enter an address (or a value) to see the estate\\u2019s estimated net proceeds.";$("breakdown").innerHTML="";return;}'
        'var payoff=num("payoff"),sellPct=num("sell"),repairs=num("repairs"),other=num("other");'
        'var sellCost=value*sellPct/100;var net=value-payoff-sellCost-repairs-other;'
        'window._NET={value:value,payoff:payoff,sellPct:sellPct,net:net};'
        'var line=function(k,v,m){return \'<div class="netline"><span>\'+k+\'</span><span>\'+(m?"\\u2212 ":"")+money(v)+\'</span></div>\';};'
        'var h=line("Estimated value",value,false)+line("Mortgage / liens payoff",payoff,true)+line("Selling costs ("+sellPct+"%)",sellCost,true);'
        'if(repairs>0)h+=line("Repairs / cleanout",repairs,true);if(other>0)h+=line("Other costs",other,true);'
        '$("breakdown").innerHTML=h;$("net").textContent="~ "+money(net);'
        '$("netsub").textContent="Estimated net proceeds to the estate after typical California selling costs.";};'
        '$("lookup").onclick=function(){var a=$("addr").value.trim();if(!a){$("lmsg").textContent="Enter the property address first.";return;}'
        '$("lmsg").textContent="Looking up\\u2026";$("lookup").disabled=true;'
        'fetch(SUPA+"/functions/v1/property-lookup",{method:"POST",headers:{apikey:ANON,Authorization:"Bearer "+ANON,"Content-Type":"application/json"},body:JSON.stringify({fullAddress:a,requestSource:"ocprobate_value"})})'
        '.then(function(r){return r.json();}).then(function(d){var p=(d&&d.success)?(d.property||{}):null;'
        'if(p){if(p.estimatedValue)$("value").value=Math.round(p.estimatedValue);if(p.loanBalance)$("payoff").value=Math.round(p.loanBalance);if(p.city&&!$("c").value)$("c").value=p.city;window.calcNet();'
        '$("lmsg").textContent=p.estimatedValue?("Estimated value ~$"+Number(p.estimatedValue).toLocaleString()+(p.city?(" \\u00b7 "+p.city):"")+" \\u2014 adjust anything below."):"Found it \\u2014 enter the value below.";}'
        'else{$("lmsg").textContent="Couldn\\u2019t auto-find it \\u2014 just enter the value below.";}$("lookup").disabled=false;})'
        '.catch(function(){$("lmsg").textContent="Enter the value manually below.";$("lookup").disabled=false;});};'
        '$("send").onclick=function(){var name=$("n").value.trim(),email=$("e").value.trim();$("smsg").textContent="";'
        'if(!name||!email){$("smsg").textContent="Please add your name and email so I can send it.";return;}'
        'var addr=$("addr").value.trim();var N=window._NET||{};'
        'var q="Home-value tool"+(addr?(" \\u2014 "+addr):"")+": est value "+(N.value?money(N.value):"n/a")+", payoff "+money(N.payoff||0)+", est net "+(N.net?money(N.net):"n/a")+". Requested the full CMA.";'
        '$("send").disabled=true;$("smsg").textContent="Sending\\u2026";'
        'fetch("/api/lead/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:name,email:email,phone:$("p").value.trim(),city:$("c").value.trim(),stage:"Just want a value on the house",question:q,page:location.pathname,hp:$("hp").value})})'
        '.then(function(r){if(!r.ok)throw 0;$("smsg").textContent="Sent. I\\u2019ll email your report to "+email+" within one business day.";})'
        '.catch(function(){$("smsg").textContent="That didn\\u2019t go through \\u2014 email me directly at "+EMAILTO+".";$("send").disabled=false;});};'
        '})();</script>'
    )
    page("/tools/home-value/", "What’s the home worth & what would the estate net? | " + NAME,
         "Instant estimated home value plus the estate’s net proceeds after mortgage payoff and selling costs. Free probate home-value tool for Orange County executors and heirs.",
         hv, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- MARKET ANALYSIS (instant CMA)
    stages = ["Just lost someone, haven’t done anything yet", "Talking to an attorney / about to file",
              "Appointed, have my Letters", "Not sure yet", "Ready to talk about selling", "Just want a value on the house"]
    opts = '<option value="">Choose one</option>' + "".join("<option>" + s + "</option>" for s in stages)
    ma = (
        '<span class="eyebrow">Free · instant + a full report by hand</span>'
        '<h1>Instant market analysis (CMA) for the property</h1>'
        '<p class="lede">Enter the property and your email. You’ll see an instant snapshot — estimated value, recent comparable sales nearby, and the local market — and I’ll follow up with a full comparative market analysis prepared by hand, weighting the right comps for condition. Free, no obligation, and it’s what the court and the other heirs will want to see.</p>'
        '<div class="tool">'
        '<h3>Get your market analysis</h3>'
        + HP +
        '<div class="grid"><div><label>Your name</label><input id="n" autocomplete="name"></div><div><label>Email</label><input id="e" type="email" autocomplete="email"></div></div>'
        '<div class="grid"><div><label>Phone (optional)</label><input id="p" type="tel" autocomplete="tel"></div><div><label>Property address</label><input id="a" placeholder="123 Main St, Santa Ana, CA 92701"></div></div>'
        '<div style="margin-top:.9rem"><label>Where are you in the process?</label><select id="st">' + opts + '</select></div>'
        '<div style="margin-top:.9rem"><label>Anything I should know? (optional)</label><textarea id="q"></textarea></div>'
        '<button class="primary" id="send" type="button" style="margin-top:.9rem">Get my analysis →</button>'
        '<div class="status" id="smsg" aria-live="polite"></div>'
        '</div>'
        '<div id="cma"></div>'
        '<div class="quiet"><p><strong>Your full report:</strong> a clear analysis with the right recent comparable sales weighted for condition, an as-is value range and a market-ready range, current days-on-market, and my honest read on timing. No pressure, and I’ll tell you if you’re better off keeping the home.</p></div>'
        + ASIDE +
        '<script>(function(){' + JS_HEAD +
        'function renderCma(d){var s=d.subject||{};'
        'var facts=[s.beds!=null?(s.beds+" bd"):null,s.baths!=null?(s.baths+" ba"):null,s.sqft?(Number(s.sqft).toLocaleString()+" sqft"):null,s.yearBuilt?("built "+s.yearBuilt):null].filter(Boolean).join(" \\u00b7 ");'
        'var rng=(d.low&&d.high)?(money(d.low)+" \\u2013 "+money(d.high)):"";'
        'var rows=(d.comps||[]).map(function(c){var bb=[(c.beds!=null?c.beds+"bd":""),(c.baths!=null?c.baths+"ba":"")].filter(Boolean).join("/");'
        'var st=c.status==="SOLD"?"Sold":(c.status==="FOR_SALE"?"For sale":(c.status==="PENDING"?"Pending":(c.status||"")));'
        'return \'<tr><td>\'+(c.address||"")+(c.city?(", "+c.city):"")+\'</td><td>\'+bb+\'</td><td style="text-align:right">\'+(c.sqft?Number(c.sqft).toLocaleString():"\\u2014")+\'</td><td style="text-align:right">\'+money(c.price)+\'</td><td style="text-align:right">\'+(c.ppsf?("$"+Math.round(c.ppsf)):"\\u2014")+\'</td><td>\'+st+\'</td></tr>\';}).join("");'
        'var mkt=d.market?(\'<div class="quiet" style="margin-top:1rem"><strong>Local market\'+(d.market.city?(" ("+d.market.city+")"):"")+\':</strong> average home value about \'+money(d.market.avg)+(d.market.vs_county!=null?(", "+(d.market.vs_county>0?"+":"")+d.market.vs_county+"% vs the county"):"")+\'.</div>\'):"";'
        '$("cma").innerHTML=\'<div class="tool"><span class="eyebrow">Instant snapshot</span><h2 style="margin-top:.3rem">\'+(d.address||"Your property")+\'</h2>\''
        '+(facts?\'<p class="note" style="margin-top:-.6rem">\'+facts+\'</p>\':"")'
        '+\'<div class="result">\'+money(d.value)+\'</div>\''
        '+\'<div class="note">Estimated value\'+(rng?(" \\u00b7 likely range "+rng):"")+(d.medianPpsf?(" \\u00b7 comps ~$"+Number(d.medianPpsf).toLocaleString()+"/sqft"):"")+\'</div>\''
        '+(rows?(\'<h3>Recent comparable sales nearby</h3><div style="overflow-x:auto"><table class="comps"><thead><tr><th>Address</th><th>Bd/Ba</th><th style="text-align:right">Sqft</th><th style="text-align:right">Price</th><th style="text-align:right">$/sqft</th><th>Status</th></tr></thead><tbody>\'+rows+\'</tbody></table></div>\'):"")'
        '+mkt+\'<p class="note">Automated snapshot from public data &amp; MLS comps. Your full, hand-prepared CMA is on its way by email.</p></div>\';}'
        '$("send").onclick=function(){var name=$("n").value.trim(),email=$("e").value.trim();$("smsg").textContent="";'
        'if(!name||!email){$("smsg").textContent="Please add your name and email so I can send it.";return;}'
        'var addr=$("a").value.trim();$("send").disabled=true;$("smsg").textContent="Preparing your analysis\\u2026 this can take a few seconds.";'
        'fetch(SUPA+"/functions/v1/ocprobate-cma",{method:"POST",headers:{apikey:ANON,Authorization:"Bearer "+ANON,"Content-Type":"application/json"},body:JSON.stringify({name:name,email:email,phone:$("p").value.trim(),fullAddress:addr,stage:$("st").value,note:$("q").value.trim(),page:location.pathname,hp:$("hp").value})})'
        '.then(function(r){return r.json();}).then(function(d){$("send").disabled=false;'
        'if(!d||!d.ok){$("smsg").textContent="That didn\\u2019t go through \\u2014 email me directly at "+EMAILTO+".";return;}'
        '$("smsg").textContent="Sent \\u2014 I\\u2019ll email your full analysis to "+email+" within one business day.";'
        'if(d.found){renderCma(d);$("cma").scrollIntoView({behavior:"smooth"});}else{$("cma").innerHTML=\'<div class="tool"><p>I couldn\\u2019t auto-pull that address, but I\\u2019ll prepare your analysis by hand and email it.</p></div>\';}})'
        '.catch(function(){$("send").disabled=false;$("smsg").textContent="Network error \\u2014 email me at "+EMAILTO+".";});};'
        '})();</script>'
    )
    page("/tools/market-analysis/", "Instant market analysis (CMA) for a probate home | " + NAME,
         "Instant comparative market analysis for an Orange County probate or inherited home — estimated value, recent comps, and the local market — plus a full CMA prepared by hand.",
         ma, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- MORTGAGE CALCULATOR
    mc = (
        '<span class="eyebrow">Free · instant</span>'
        '<h1>Mortgage calculator</h1>'
        '<p class="lede">For an heir who wants to keep the home, or a buyer sizing up a purchase — estimate the full monthly payment, including property taxes and insurance.</p>'
        '<div class="tool">'
        '<div class="g3">'
        '<div><label>Home price</label><input id="price" type="number" inputmode="numeric" value="900000" oninput="calc()"></div>'
        '<div><label>Down payment %</label><input id="down" type="number" step="1" value="20" oninput="calc()"></div>'
        '<div><label>Interest rate %</label><input id="rate" type="number" step="0.01" value="6.75" oninput="calc()"></div>'
        '</div>'
        '<div class="g3" style="margin-top:.9rem">'
        '<div><label>Loan term (years)</label><input id="term" type="number" step="1" value="30" oninput="calc()"></div>'
        '<div><label>Property tax %/yr</label><input id="tax" type="number" step="0.01" value="1.1" oninput="calc()"></div>'
        '<div><label>Insurance $/yr</label><input id="ins" type="number" inputmode="numeric" value="1800" oninput="calc()"></div>'
        '</div>'
        '<div id="breakdown" style="margin-top:1rem"></div>'
        '<div class="result" id="pay">—</div>'
        '<div class="note">Estimated total monthly payment (principal, interest, taxes &amp; insurance).</div>'
        '</div>'
        '<p class="note">Estimate only; excludes HOA, PMI, and Mello-Roos. Confirm figures with your lender.</p>'
        '<script>(function(){' + JS_HEAD +
        'window.calc=function(){var price=num("price"),downPct=num("down"),rate=num("rate"),term=num("term"),taxPct=num("tax"),ins=num("ins");'
        'if(!price){$("pay").textContent="\\u2014";$("breakdown").innerHTML="";return;}'
        'var loan=price*(1-downPct/100);var i=rate/100/12;var n=Math.max(1,Math.round(term*12));'
        'var pi=i>0?loan*(i*Math.pow(1+i,n))/(Math.pow(1+i,n)-1):loan/n;'
        'var tax=price*(taxPct/100)/12;var insM=ins/12;var total=pi+tax+insM;'
        'var line=function(k,v){return \'<div class="netline"><span>\'+k+\'</span><span>\'+money(v)+\'</span></div>\';};'
        '$("breakdown").innerHTML=line("Loan amount",loan)+line("Principal & interest",pi)+line("Property taxes",tax)+line("Insurance",insM);'
        '$("pay").textContent=money(total)+"/mo";};window.calc();})();</script>'
    )
    page("/tools/mortgage-calculator/", "Mortgage calculator | " + NAME,
         "Free mortgage calculator — estimate the full monthly payment (principal, interest, taxes, and insurance) for keeping or buying an Orange County home.",
         mc, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- DSCR CALCULATOR (investors)
    dscr = (
        '<span class="eyebrow">For investors · instant</span>'
        '<h1>DSCR calculator</h1>'
        '<p class="lede">Buying a probate or inherited home as a rental? A DSCR (debt-service coverage ratio) loan qualifies on the property’s rent, not your income. See the ratio and whether the deal pencils.</p>'
        '<div class="tool">'
        '<div class="g3">'
        '<div><label>Purchase price</label><input id="price" type="number" inputmode="numeric" value="800000" oninput="calc()"></div>'
        '<div><label>Down payment %</label><input id="down" type="number" step="1" value="25" oninput="calc()"></div>'
        '<div><label>Interest rate %</label><input id="rate" type="number" step="0.01" value="7.25" oninput="calc()"></div>'
        '</div>'
        '<div class="g3" style="margin-top:.9rem">'
        '<div><label>Expected rent $/mo</label><input id="rent" type="number" inputmode="numeric" value="4200" oninput="calc()"></div>'
        '<div><label>Property tax %/yr</label><input id="tax" type="number" step="0.01" value="1.1" oninput="calc()"></div>'
        '<div><label>Insurance $/yr</label><input id="ins" type="number" inputmode="numeric" value="2000" oninput="calc()"></div>'
        '</div>'
        '<div class="g3" style="margin-top:.9rem">'
        '<div><label>Loan term (years)</label><input id="term" type="number" step="1" value="30" oninput="calc()"></div>'
        '<div><label>HOA $/mo</label><input id="hoa" type="number" inputmode="numeric" value="0" oninput="calc()"></div>'
        '<div><label>Min DSCR required</label><input id="ratio" type="number" step="0.01" value="1.00" oninput="calc()"></div>'
        '</div>'
        '<div id="breakdown" style="margin-top:1rem"></div>'
        '<div class="result" id="dscr">—</div>'
        '<div class="note" id="verdict">Enter the deal to see the DSCR (rent ÷ PITIA).</div>'
        '</div>'
        '<p class="note">Estimate only. Lender DSCR programs, LTV caps, rates, and qualifying rent vary. Not lending or investment advice.</p>'
        '<script>(function(){' + JS_HEAD +
        'window.calc=function(){var price=num("price"),downPct=num("down"),rate=num("rate"),rent=num("rent"),taxPct=num("tax"),ins=num("ins"),term=num("term"),hoa=num("hoa"),ratio=num("ratio")||1;'
        'if(!price||!rent){$("dscr").textContent="\\u2014";$("breakdown").innerHTML="";$("verdict").textContent="Enter the deal to see the DSCR (rent \\u00f7 PITIA).";return;}'
        'var loan=price*(1-downPct/100);var i=rate/100/12;var n=Math.max(1,Math.round(term*12));'
        'var pi=i>0?loan*(i*Math.pow(1+i,n))/(Math.pow(1+i,n)-1):loan/n;'
        'var tax=price*(taxPct/100)/12;var insM=ins/12;var pitia=pi+tax+insM+hoa;var dscr=pitia>0?rent/pitia:0;'
        'var line=function(k,v){return \'<div class="netline"><span>\'+k+\'</span><span>\'+money(v)+\'</span></div>\';};'
        '$("breakdown").innerHTML=line("Loan amount",loan)+line("Monthly P&I",pi)+line("Taxes + insurance + HOA",tax+insM+hoa)+line("Monthly PITIA",pitia)+line("Monthly rent",rent);'
        '$("dscr").textContent=dscr.toFixed(2)+"\\u00d7 DSCR";'
        'var ok=dscr>=ratio;$("verdict").innerHTML=(ok?"\\u2705 ":"\\u26a0\\ufe0f ")+"Rent covers "+Math.round(dscr*100)+"% of the payment \\u2014 "+(ok?("meets your "+ratio.toFixed(2)+" target."):("below your "+ratio.toFixed(2)+" target; raise rent, add down payment, or lower the price."));};'
        'window.calc();})();</script>'
    )
    page("/tools/dscr-calculator/", "DSCR calculator for investors | " + NAME,
         "Free DSCR calculator — for investors buying a probate or inherited home as a rental. See the debt-service coverage ratio and whether the deal qualifies.",
         dscr, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- FIND A HOME
    SEARCH = "https://www.socalrealtyandinvestments.com/search"
    fah = (
        '<span class="eyebrow">Home search</span>'
        '<h1>Find a home</h1>'
        '<p class="lede">Search homes for sale across Southern California — including estate and probate opportunities. Enter an area or ZIP to browse current listings.</p>'
        '<div class="tool">'
        '<label for="q">City, ZIP, or address</label>'
        '<div class="trow"><input id="q" placeholder="Santa Ana, or 92701"><button class="primary" id="go" type="button">Search homes</button></div>'
        '<div class="note">Opens our Southern California home search in a new tab.</div>'
        '</div>'
        '<div class="quiet"><p><strong>Looking for probate deals specifically?</strong> Investors and buyers who want first look at estate and inherited-home opportunities can tell me what they’re after — <a href="/contact/">get in touch</a> and I’ll keep you posted.</p></div>'
        + ASIDE +
        '<script>(function(){var $=function(i){return document.getElementById(i);};'
        'var run=function(){var q=$("q").value.trim();window.open("' + SEARCH + '"+(q?("?q="+encodeURIComponent(q)):""),"_blank","noopener");};'
        '$("go").onclick=run;$("q").addEventListener("keydown",function(e){if(e.key==="Enter")run();});})();</script>'
    )
    page("/tools/find-a-home/", "Find a home in Southern California | " + NAME,
         "Search homes for sale across Southern California, including estate and probate opportunities.",
         fah, schema(PERSON), current="/tools/")

    # ---------------------------------------------------------------- GLOSSARY (Terms & Definitions)
    TERMS = [
        ("Probate", "The court-supervised process of settling a deceased person’s estate — validating the will (if any), paying debts and taxes, and transferring what’s left to the heirs. In California it runs through the Superior Court in the county where the person lived."),
        ("Personal representative", "The person the court authorizes to manage the estate. Called an <b>executor</b> when named in a will, or an <b>administrator</b> when there’s no will. They have the legal power — and duty — to handle estate property, including the house."),
        ("Executor", "The personal representative named in the will to carry out its instructions and manage the estate through probate."),
        ("Administrator", "The personal representative appointed by the court when there is no will, or the named executor can’t serve."),
        ("Letters", "Short for <b>Letters Testamentary</b> (with a will) or <b>Letters of Administration</b> (without one) — the court document proving you’re authorized to act for the estate. A title company or agent will ask to see them before a sale."),
        ("Full authority", "Authority under the Independent Administration of Estates Act (IAEA) that lets the personal representative sell the home <b>without a court confirmation hearing</b> — usually just a Notice of Proposed Action to the heirs. Faster and simpler."),
        ("Limited authority", "Authority that requires <b>court confirmation</b> of the sale, including a hearing and the possibility of overbidding. More steps, but common and very workable with the right preparation."),
        ("Notice of Proposed Action", "A written notice the personal representative with full authority sends to the heirs before selling. If no one objects within the notice period, the sale can close without a hearing."),
        ("Court confirmation", "The hearing where a judge approves a sale made under limited authority. The property is sold subject to the court’s approval, and other buyers may show up to overbid."),
        ("Overbid", "At a confirmation hearing, other buyers can bid above the accepted offer. California sets the first minimum overbid by formula (roughly 10% of the first $10,000 plus 5% of the balance above that). Your agent should prepare you for it."),
        ("Independent Administration of Estates Act (IAEA)", "The California law that grants full or limited authority, letting many estates sell property with less court involvement."),
        ("Trust / successor trustee", "If the home was held in a living trust, it usually avoids probate entirely. The <b>successor trustee</b> named in the trust can sell it directly, following the trust’s terms."),
        ("Heir / beneficiary", "The people entitled to inherit — under the will, the trust, or California’s intestacy rules if there’s neither."),
        ("Date-of-death value", "The property’s fair market value on the day the owner died. It matters for taxes and for the <b>stepped-up basis</b>, and a comparative market analysis can document it."),
        ("Stepped-up basis", "For tax purposes the home’s cost basis generally ‘steps up’ to its date-of-death value, which can greatly reduce capital-gains tax when the estate or heirs sell. Confirm specifics with a CPA."),
        ("Comparative market analysis (CMA)", "An agent’s analysis of what the home is worth now, based on recent comparable sales nearby, current competition, and days on market. Useful for pricing and for the court and heirs."),
        ("Simplified procedures", "California offers faster paths for smaller estates — a small-estate affidavit or spousal petition — that can avoid full probate when the estate’s value is under the current threshold. Ask an attorney whether you qualify."),
        ("As-is sale", "Selling the property in its current condition, without the estate making repairs. Common in probate; buyers price the home accordingly, and required disclosures still apply."),
    ]
    items = "".join('<dt>' + t + '</dt><dd>' + d + '</dd>' for t, d in TERMS)
    gl_schema = schema({"@type": "DefinedTermSet", "name": "Probate real-estate terms & definitions",
                        "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": _strip(d)} for t, d in TERMS]})
    glossary = (
        '<span class="eyebrow">Plain English</span>'
        '<h1>Probate terms &amp; definitions</h1>'
        '<p class="lede">The words you’ll run into as an executor or heir, explained simply. If something here still isn’t clear, <a href="/contact/">ask me</a> — no charge.</p>'
        '<dl class="glossary">' + items + '</dl>'
        '<div class="quiet"><p>This glossary is general information for Orange County families, not legal or tax advice. Figures and thresholds change — confirm current numbers with your attorney or CPA.</p></div>'
        + ASIDE
    )
    page("/glossary/", "Probate terms & definitions — a plain-English glossary | " + NAME,
         "Plain-English definitions of California probate real-estate terms for executors and heirs: Letters, full vs. limited authority, overbid, court confirmation, stepped-up basis, and more.",
         glossary, gl_schema + schema(PERSON), current="/glossary/")


def _strip(html_str):
    import re
    return re.sub("<[^>]+>", "", html_str)
