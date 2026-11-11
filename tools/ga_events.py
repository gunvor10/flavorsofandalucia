#!/usr/bin/env python3
"""Google Analytics 4 events: enquiry funnel, tour clicks, WhatsApp and affiliate clicks.

Run on the site folder after every new Claude Design download, AFTER
tools/analytics_consent.py and tools/google_ads.py. Adds one small script before </body>
(outside the page code, so it works whatever Design changes) that sends these GA4 events:

  contact_click    click on a link to the contact page ("Enquire", "Contact us")
                   params: link_text, page_path
  form_start       first time someone types in an enquiry form on a page
                   params: page_path, tour
  enquiry_submit   "Send" pressed (an attempt; may still fail)
                   params: page_path, tour
  generate_lead    the form service answered OK = enquiry really sent  (mark as key event)
                   params: page_path, tour, value 1, currency EUR
  whatsapp_click   click on a WhatsApp link             params: link_text, page_path
  tour_click       click on a link to a tour page       params: tour, link_text, page_path
  affiliate_click  click on a partner/affiliate link    params: partner, link_url, link_text, page_path

Safe to run twice (marker comment).

Usage:  python3 tools/ga_events.py [site_dir]
"""
import glob
import os
import sys

MARK = "<!-- ga-events (tools/ga_events.py) -->"

# Partner sites we earn a commission from. Add new affiliates here.
AFFILIATES = ["naturanda.com", "devourtours.com", "cookingpaella.com"]

SCRIPT = MARK + """
<script>
(function(){
function ev(n,p){try{if(window.gtag)gtag('event',n,p);}catch(e){}}
function page(){return location.pathname;}
function tourOf(f){var t=f&&f.querySelector&&f.querySelector('input[name="tour"]');var v=t?t.value:'';return v&&v.indexOf('{'+'{')<0?v:'';}
var AFF=%s;
function affiliate(h){for(var i=0;i<AFF.length;i++){var d=AFF[i];if(h===d||h.slice(-d.length-1)==='.'+d)return d;}return '';}
document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest&&e.target.closest('a[href]');if(!a)return;
  var u;try{u=new URL(a.getAttribute('href'),location.href);}catch(x){return;}
  var txt=(a.innerText||a.getAttribute('aria-label')||'').replace(/\\s+/g,' ').trim().slice(0,100);
  var aff=affiliate(u.hostname);
  if(u.hostname==='wa.me'||u.hostname==='api.whatsapp.com'){ev('whatsapp_click',{link_text:txt,page_path:page()});}
  else if(aff){ev('affiliate_click',{partner:aff,link_url:u.origin+u.pathname,link_text:txt,page_path:page()});}
  else if(u.hostname===location.hostname||u.hostname==='flavorsofandalucia.com'){
    var m=u.pathname.match(/\\/tour\\/([^\\/]+)/);
    if(m&&u.pathname!==location.pathname){ev('tour_click',{tour:m[1],link_text:txt,page_path:page()});}
    else if(/\\/contact\\/?$/.test(u.pathname)){ev('contact_click',{link_text:txt,page_path:page()});}
  }
},true);
var started={};
document.addEventListener('input',function(e){
  var f=e.target&&e.target.form;if(!f||started[page()])return;started[page()]=1;
  ev('form_start',{page_path:page(),tour:tourOf(f)});
},true);
var lastTour='';
document.addEventListener('submit',function(e){lastTour=tourOf(e.target);ev('enquiry_submit',{page_path:page(),tour:lastTour});},true);
window.__foaFetch=window.fetch;
if(window.__foaFetch){window.fetch=function(u,o){var p=window.__foaFetch.apply(this,arguments);
  try{if(o&&String(o.method).toUpperCase()==='POST'&&/formspree\\.io/.test(String(u))){var t=lastTour;
    p.then(function(r){if(r&&r.ok)ev('generate_lead',{page_path:page(),tour:t,value:1,currency:'EUR'});},function(){});}}catch(x){}
  return p;};}
})();
</script>
"""


def main():
    import json
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
    script = SCRIPT % json.dumps(AFFILIATES)
    pages = sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True))
    changed = 0
    for path in pages:
        text = open(path, encoding="utf-8").read()
        if MARK in text or "</body>" not in text:
            continue
        idx = text.rfind("</body>")
        open(path, "w", encoding="utf-8").write(text[:idx] + script + text[idx:])
        changed += 1
    print(f"{changed} of {len(pages)} pages updated")


if __name__ == "__main__":
    main()
