(function(){
var S=window.SITE||{},d=document;
var tel=S.phone?"tel:"+S.phone.replace(/[^\d+]/g,""):"",wa=S.whatsapp?"https://wa.me/"+S.whatsapp.replace(/\D/g,""):"",mail=S.email?"mailto:"+S.email:"";
d.querySelectorAll("[data-cfg]").forEach(function(el){
 var v=S[el.getAttribute("data-cfg")];if(!v)return;el.textContent=v;
 var l=el.getAttribute("data-cfg-link");
 if(l==="tel")el.href=tel;if(l==="mail")el.href=mail;if(l==="wa")el.href=wa;
});
var css=d.createElement("style");
css.textContent=".fab{position:fixed;right:20px;bottom:20px;z-index:50;display:flex;gap:10px}.fab a{padding:12px 18px;border-radius:999px;font:600 15px 'Public Sans',sans-serif;text-decoration:none;color:#fff;background:#0E2233;box-shadow:0 2px 8px rgba(0,0,0,.25)}.fab a.w{background:#1B8F4B}@media(max-width:860px){body{padding-bottom:56px}.fab{left:0;right:0;bottom:0;gap:0}.fab a{flex:1;text-align:center;border-radius:0;box-shadow:none;padding:16px 8px}}";
d.head.appendChild(css);
var b='<a href="book.html">Book a call</a>';
if(tel)b='<a href="'+tel+'">Call</a>'+b;
if(wa)b='<a class="w" href="'+wa+'" target="_blank" rel="noopener">WhatsApp</a>'+b;
var fab=d.createElement("div");fab.className="fab";fab.innerHTML=b;d.body.appendChild(fab);
var so=S.social||{},L=[['linkedin','LinkedIn'],['facebook','Facebook'],['instagram','Instagram'],['x','X'],['youtube','YouTube']].filter(function(p){return so[p[0]]}).map(function(p){return '<a href="'+so[p[0]]+'" target="_blank" rel="noopener noreferrer">'+p[1]+'</a>'}).join(' &nbsp; ');
var f=d.querySelector("footer .wrap");
if(f){var c=[];if(S.phone)c.push('<a href="'+tel+'">'+S.phone+'</a>');if(S.phone2)c.push('<a href="tel:'+S.phone2.replace(/[^\d+]/g,"")+'">'+S.phone2+'</a>');if(S.email)c.push('<a href="'+mail+'">'+S.email+'</a>');if(S.address)c.push(S.address);
f.insertAdjacentHTML("afterbegin",'<p style="margin:0 0 12px"><a href="certifications.html">Certifications</a> &nbsp; <a href="locations.html">Locations</a> &nbsp; <a href="book.html">Book a call</a> &nbsp; <a href="contact.html">Contact</a></p>'+(c.length?'<p style="margin:0 0 12px">'+c.join(" &nbsp; ")+'</p>':"")+(L?'<p style="margin:0 0 12px">Follow us: '+L+'</p>':"")+'<p style="margin:0 0 12px">Qualitance India is a private compliance consultancy. It is not affiliated with the Bureau of Indian Standards or any government body.</p>');}
})();
