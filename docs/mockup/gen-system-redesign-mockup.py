#!/usr/bin/env python3
"""ES-DE-honest Steam system+gamelist mockup with FAITHFUL type scaling.

Typography is sized as a fraction of the stage height (exactly how ES-DE sizes fonts), driven by
the real values from _inc/scale.xml, with a Medium/Large/X-Large switch — so readability on a small
screen can be judged honestly. Only effects the engine can render are used (rect corners, carousel
focus = scale+dim, grid focus = frame, baked panels/blooms). Real colour logos are inlined.
"""
import json, re, pathlib

REPO = pathlib.Path("/Users/igorzamyslov/Projects/es-de-steam-theme/.claude/worktrees/awesome-proskuriakova-61191f/steam-bigpicture-es-de")
COLOR = REPO / "system-logos" / "system-logo-color"
OUT = pathlib.Path("/Users/igorzamyslov/Projects/es-de-steam-theme/.claude/worktrees/awesome-proskuriakova-61191f/docs/mockup/steam-system-redesign.html")

SYSTEMS = [
    ("nes",       "Nintendo Entertainment System", "Home console · Nintendo · 1983", 312,  "c43d41", "The 8-bit machine that revived the industry — Mario, Zelda and Metroid were all born here."),
    ("snes",      "Super Nintendo",                "Home console · Nintendo · 1990", 268,  "df5142", "16-bit powerhouse with Mode 7 scaling and a library many still call the greatest ever."),
    ("n64",       "Nintendo 64",                   "Home console · Nintendo · 1996", 94,   "0da25e", "The cartridge-based leap into 3D — analog stick, four controller ports, Super Mario 64."),
    ("gc",        "Nintendo GameCube",             "Home console · Nintendo · 2001", 147,  "958bf4", "Compact, purple, and stacked with Metroid Prime, Wind Waker and Smash Bros. Melee."),
    ("gba",       "Game Boy Advance",              "Handheld · Nintendo · 2001",     1142, "4875db", "32-bit handheld that carried the SNES library in your pocket — Pokémon Emerald and beyond."),
    ("gb",        "Game Boy",                      "Handheld · Nintendo · 1989",     576,  "3c528d", "The handheld that defined portable gaming and refused to die for over a decade."),
    ("megadrive", "Sega Mega Drive",               "Home console · Sega · 1988",     748,  "0374d1", "Blast processing, Sonic, and the console that took the fight straight to Nintendo."),
    ("saturn",    "Sega Saturn",                   "Home console · Sega · 1994",     63,   "567ddd", "Dual-CPU 2D monster with a cult library of shooters and fighters."),
    ("dreamcast", "Sega Dreamcast",                "Home console · Sega · 1998",     88,   "497ed9", "Ahead of its time — built-in modem, VMU, and a swansong of brilliant games."),
    ("ps2",       "PlayStation 2",                 "Home console · Sony · 2000",     0,    "2a68c3", "The best-selling console of all time. No games yet — add ROMs or scrape this system."),
    ("pcengine",  "PC Engine",                     "Home console · NEC · 1987",      41,   "c64c3f", "Tiny console, big sound — the CD-ROM pioneer with a stellar shmup catalogue."),
    ("neogeo",    "Neo Geo",                       "Home console · SNK · 1990",      37,   "7c818c", "Arcade-perfect at home for a king's ransom — fighters and run-and-guns in their purest form."),
]
GAMES = [
    ("Metroid Prime", "Action-Adventure", "Retro Studios", "1", 2002, 5, True,
     "Samus Aran explores the planet Tallon IV in a first-person adventure blending exploration, puzzle-solving and combat."),
    ("Super Smash Bros. Melee", "Fighting", "HAL Laboratory", "1-4", 2001, 5, True,
     "The definitive platform fighter — Nintendo all-stars battling across iconic stages at breakneck speed."),
    ("The Legend of Zelda: The Wind Waker", "Action-Adventure", "Nintendo EAD", "1", 2002, 5, False,
     "Cel-shaded seafaring Zelda — sail the Great Sea, raise the wind, and rescue your sister from the Forsaken Fortress."),
    ("Resident Evil 4", "Survival Horror", "Capcom", "1", 2005, 5, True,
     "Leon Kennedy heads to rural Spain to rescue the president's daughter in the genre-redefining over-the-shoulder shooter."),
    ("F-Zero GX", "Racing", "Amusement Vision", "1-4", 2003, 4, False,
     "Blistering anti-grav racing at 60fps — punishing, gorgeous, and still unmatched two decades later."),
    ("Paper Mario: The Thousand-Year Door", "RPG", "Intelligent Systems", "1", 2004, 5, False,
     "A papercraft RPG with timing-based combat, a stage-play framing, and some of the sharpest writing on the system."),
    ("Pikmin 2", "Strategy", "Nintendo EAD", "1-2", 2004, 4, False,
     "Command armies of plant-creatures to recover treasure from a hostile garden world against the clock."),
    ("Luigi's Mansion", "Action", "Nintendo EAD", "1", 2001, 4, False,
     "Luigi vacuums up ghosts in a haunted mansion in this quirky, atmospheric launch title."),
    ("Mario Kart: Double Dash!!", "Racing", "Nintendo EAD", "1-4", 2003, 4, False,
     "Two racers per kart, co-op item chaos, and LAN play — the most experimental Mario Kart."),
    ("Eternal Darkness", "Action-Adventure", "Silicon Knights", "1", 2002, 4, False,
     "A Lovecraftian horror with a sanity meter that messes with the game — and the player — as it drains."),
    ("Tales of Symphonia", "RPG", "Namco Tales Studio", "1-4", 2003, 4, False,
     "A beloved action-RPG with real-time battles and a sprawling two-world story."),
    ("Star Fox Adventures", "Action-Adventure", "Rare", "1", 2002, 3, False,
     "Rare's last Nintendo game — a Zelda-like adventure starring Fox McCloud on Dinosaur Planet."),
]

def load_svg(key):
    raw = (COLOR / f"{key}.svg").read_text(encoding="utf-8")
    raw = re.sub(r"<\?xml.*?\?>", "", raw, flags=re.S)
    raw = re.sub(r"<!DOCTYPE.*?>", "", raw, flags=re.S)
    raw = re.sub(r"<svg\b[^>]*>", lambda m: re.sub(r'\s(width|height)="[^"]*"', "", m.group(0)), raw, count=1, flags=re.S)
    return raw.strip()

data = [dict(key=k, name=n, spec=s, count=c, color=col, desc=d, svg=load_svg(k)) for (k,n,s,c,col,d) in SYSTEMS]
games = [dict(t=t, genre=g, dev=dev, players=p, year=y, rating=r, fav=f, desc=d) for (t,g,dev,p,y,r,f,d) in GAMES]
DATA = json.dumps(data); GAMES_JSON = json.dumps(games)

HTML = r"""<meta charset="utf-8">
<title>Steam Big Picture — ES-DE System & Game View</title>
<style>
  :root{
    --ink-1:#0b0e12; --ink-2:#13171d; --line:#2b313a;
    --accent:#33a8ff; --green-1:#a1cd44; --green-2:#5f9626;
    --text:#e8edf2; --text-2:#aab4c0; --muted:#7c8794; --star:#f5c518;
    --font:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
    --rad:0px;
    /* font roles — set by JS from scale.xml fractions × stage height (defaults ~Large @720) */
    --fsHero:46px; --fsHeader:32px; --fsTitle:26px; --fsCount:22px; --fsButton:20px;
    --fsLabel:14px; --fsMeta:18px; --fsTab:18px; --fsClock:19px;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{font-family:var(--font);color:var(--text);background:#04060a;-webkit-font-smoothing:antialiased;
    overflow:hidden;display:flex;flex-direction:column;height:100vh}

  .mockbar{flex:none;display:flex;align-items:center;gap:12px;flex-wrap:wrap;
    padding:8px 16px;background:#04060a;border-bottom:1px solid #ffffff10;font-size:11px}
  .mockbar .lab{color:#56697a;text-transform:uppercase;letter-spacing:.6px;font-weight:800}
  .seg{display:flex;gap:4px;background:#ffffff0d;padding:3px;border-radius:999px;border:1px solid #ffffff14}
  .seg button{border:none;background:transparent;color:#9fb3c4;font-weight:800;font-size:11px;padding:5px 11px;border-radius:999px;cursor:pointer;font-family:var(--font)}
  .seg button.on{background:#cfd9e3;color:#0c1722}
  .mockbar .note{color:#46566a;margin-left:auto;max-width:42%;text-align:right}

  .stage-wrap{flex:1;min-height:0;display:grid;place-items:center}
  .stage{position:relative;width:100%;height:100%;overflow:hidden;display:flex;flex-direction:column;background:var(--ink-1)}
  .view{position:absolute;inset:0;display:none;flex-direction:column}
  .view.show{display:flex}

  /* top bar (section-strip) */
  .topbar{position:absolute;top:0;left:0;right:0;height:7.2%;z-index:30;display:flex;align-items:center;
    gap:2.4%;padding:0 3%;background:#070a0ecc;border-bottom:1px solid #ffffff0d}
  .topbar .tab{font-size:var(--fsTab);font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:var(--text-2);
    position:relative;opacity:.82;height:100%;display:flex;align-items:center}
  .topbar .tab.on{color:#fff;opacity:1}
  .topbar .tab.on::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--tabcol,var(--accent))}
  .topbar .status{margin-left:auto;display:flex;align-items:center;gap:14px;color:var(--text-2);font-size:var(--fsClock);font-weight:600}
  .topbar .clock{font-variant-numeric:tabular-nums}
  .batt{width:1.7em;height:.85em;border:1.5px solid currentColor;border-radius:3px;position:relative;padding:1.5px;opacity:.85}
  .batt::after{content:"";position:absolute;right:-4px;top:25%;width:2px;height:45%;background:currentColor;border-radius:0 2px 2px 0}
  .batt i{display:block;height:100%;width:74%;background:var(--green-1);border-radius:1px}

  /* SYSTEM VIEW */
  .hero{position:absolute;inset:0;z-index:0;transition:background .4s ease}
  .hero-bloom{position:absolute;inset:0;z-index:1;transition:background .4s ease}
  .hero-vignette{position:absolute;inset:0;z-index:2;pointer-events:none;
    background:radial-gradient(125% 110% at 64% 40%, transparent 52%, #04060a 122%)}
  .hero-scrim{position:absolute;inset:0;z-index:3;pointer-events:none;
    background:linear-gradient(90deg,#04060aF2 0%, #04060abf 28%, transparent 60%),
               linear-gradient(0deg,#04060aF7 0%, #04060a40 26%, transparent 48%)}
  .hero-logo{position:absolute;right:5%;top:37%;transform:translateY(-50%);width:52%;max-width:720px;height:44%;
    z-index:4;display:grid;place-items:center;transition:opacity .35s ease,filter .35s ease}
  .hero-logo svg{width:100%;height:100%;max-height:100%}
  .hero-logo.empty{opacity:.4;filter:grayscale(.55)}

  .sysfg{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;padding-top:7.2%}
  .spacer{flex:1;min-height:0}
  .infocard{align-self:flex-start;margin:0 0 2.4% 3%;max-width:46%;
    background:linear-gradient(180deg,#11151bF2,#0b0e13F7);border:1px solid #ffffff12;
    border-radius:var(--rad);padding:1.6em 1.4em 1.5em;box-shadow:0 18px 44px #00000066}
  .infocard .kind{font-size:var(--fsLabel);letter-spacing:1.4px;text-transform:uppercase;font-weight:800;color:var(--accent);margin-bottom:.6em}
  .infocard h1{margin:0 0 .22em;font-size:var(--fsHero);line-height:1.03;font-weight:800;letter-spacing:-.5px;text-wrap:balance;text-shadow:0 3px 16px #000a}
  .infocard .meta{display:flex;align-items:center;gap:.6em;font-size:var(--fsCount);color:var(--text-2);font-weight:600;margin-bottom:.55em;flex-wrap:wrap}
  .infocard .count{color:#fff;font-weight:800}
  .infocard .count.zero{color:#e0a23c}
  .infocard .dot{width:4px;height:4px;border-radius:50%;background:var(--muted)}
  .infocard .desc{margin:0;font-size:var(--fsMeta);line-height:1.5;color:var(--text-2);
    display:-webkit-box;-webkit-line-clamp:3;line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}

  .shelf-wrap{flex:none;position:relative;z-index:5}
  .shelf-head{display:flex;align-items:baseline;gap:12px;padding:0 3% .5em}
  .shelf-head .sl{font-size:var(--fsTab);letter-spacing:1px;text-transform:uppercase;font-weight:800;color:var(--muted)}
  .shelf-head .pos{margin-left:auto;font-size:var(--fsTab);font-weight:700;color:var(--text-2);font-variant-numeric:tabular-nums;
    background:#0b0e12cc;border:1px solid #ffffff14;padding:.15em .7em;border-radius:999px}
  .shelf{display:flex;align-items:center;gap:1.6%;padding:1.4% 3% 2%;overflow-x:auto;scrollbar-width:none;
    -webkit-mask:linear-gradient(90deg,transparent,#000 2.5%,#000 97.5%,transparent)}
  .shelf::-webkit-scrollbar{display:none}
  .tile{flex:none;width:21vh;height:11.7vh;min-width:150px;min-height:84px;border-radius:var(--rad);position:relative;cursor:pointer;overflow:hidden;
    display:grid;place-items:center;padding:1.6vh 1.9vh;border:1px solid #ffffff0e;
    transition:transform .16s ease,opacity .16s ease,filter .16s ease;opacity:.5;filter:grayscale(.45) brightness(.72)}
  .tile .plate{position:absolute;inset:0;z-index:0}
  .tile .logo{position:relative;z-index:2;width:100%;height:100%;display:grid;place-items:center}
  .tile .logo svg{width:100%;height:100%;max-height:7.2vh}
  .tile .empty-flag{position:absolute;z-index:3;bottom:6px;right:8px;font-size:9px;font-weight:800;letter-spacing:.5px;
    text-transform:uppercase;color:#e0a23c;background:#1a130aE0;border:1px solid #e0a23c44;padding:2px 6px;border-radius:4px}
  .tile.empty .logo{filter:grayscale(.6)}
  .tile.active{opacity:1;filter:brightness(1.06);transform:translateY(-6px) scale(1.07);z-index:4;border-color:#ffffff2e}

  /* GAMELIST VIEW */
  .glwrap{position:absolute;inset:0;display:grid;grid-template-columns:1fr var(--panelW,42%);background:var(--ink-2)}
  .glleft{min-height:0;display:flex;flex-direction:column;padding:7.2% 0 0 3%}
  .glhead{flex:none;padding:.5em 0 .6em}
  .glhead b{font-size:var(--fsHeader);font-weight:800;letter-spacing:-.4px;display:block;line-height:1.05}
  .glhead .c{font-size:var(--fsTab);color:var(--text-2);font-weight:600;margin-top:.3em;display:flex;align-items:center;gap:.5em}
  .glgrid{flex:1;min-height:0;overflow:auto;display:flex;flex-wrap:wrap;gap:var(--capGap,14px);
    align-content:start;padding:6px 1.6% 64px 2px;scrollbar-width:thin;scrollbar-color:#39424d transparent}
  .cap{position:relative;border-radius:var(--rad);overflow:hidden;cursor:pointer;flex:none;
    width:var(--capW,150px);height:var(--capH,225px);
    background:#0d1117;box-shadow:0 8px 16px #00000055;transition:transform .15s ease;filter:saturate(.7) brightness(.82)}
  .cap .art{position:absolute;inset:0;display:flex;align-items:flex-end;padding:.7em}
  .cap .art::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 42%,#000000d6)}
  .cap .nm{position:relative;z-index:2;font-size:var(--fsTab);font-weight:800;line-height:1.15;color:#fff;text-shadow:0 2px 5px #000b;
    display:-webkit-box;-webkit-line-clamp:3;line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .cap .favm{position:absolute;z-index:3;top:.5em;right:.5em;color:var(--star);font-size:var(--fsTab);text-shadow:0 1px 3px #000}
  .cap.sel{filter:none;transform:scale(1.04);box-shadow:0 0 0 3px var(--accent),0 12px 26px #000a}

  .gldetail{background:linear-gradient(180deg,#14181eF7,#0b0e13);border-left:1px solid var(--line);
    padding:calc(7.2% + 6px) 1.5% 60px;display:flex;flex-direction:column;gap:.7em;min-height:0;overflow:hidden}
  .gldetail h3{margin:0;font-size:var(--fsTitle);font-weight:800;letter-spacing:-.3px;line-height:1.18;text-wrap:balance}
  .gldetail .shot{aspect-ratio:16/9;border-radius:var(--rad);background-size:cover;box-shadow:0 10px 22px #0009;flex:none}
  .gldetail .stars{color:var(--star);letter-spacing:2px;font-size:var(--fsCount)}
  .gldetail .mg{display:grid;grid-template-columns:auto 1fr;gap:.45em 1em;font-size:var(--fsMeta)}
  .gldetail .mg .k{color:var(--muted)}
  .gldetail .dlab{font-size:var(--fsMeta);letter-spacing:1px;text-transform:uppercase;color:var(--muted);font-weight:800}
  .gldetail .desc{margin:0;font-size:var(--fsMeta);line-height:1.5;color:var(--text-2);flex:1;min-height:24px;overflow:hidden;
    -webkit-mask:linear-gradient(180deg,#000 calc(100% - 16px),transparent)}
  .play{flex:none;display:flex;align-items:center;justify-content:center;gap:.5em;padding:.75em;border-radius:var(--rad);
    border:none;font-weight:800;font-size:var(--fsButton);color:#0d2406;cursor:pointer;
    background:linear-gradient(180deg,var(--green-1),var(--green-2));box-shadow:0 8px 20px #5f962655}

  .helpbar{position:absolute;bottom:0;left:0;right:0;z-index:30;display:flex;align-items:center;gap:1.6%;padding:.7em 3%;
    border-top:1px solid #ffffff0d;background:#04060acc;color:var(--text-2);font-size:var(--fsTab);font-weight:600}
  .help{display:flex;align-items:center;gap:.5em}
  .gly{width:1.5em;height:1.5em;border-radius:50%;display:grid;place-items:center;font-size:.8em;font-weight:900;color:#0b121b}
  .gly.a{background:#6cc04a}.gly.b{background:#e05a4f}.gly.x{background:#3a9bff}.gly.y{background:#e7b94a}.gly.m{background:#39424d;color:#cfe}

  @media (prefers-reduced-motion: reduce){ .tile,.cap,.hero,.hero-bloom,.hero-logo{transition:none} }
</style>

<div class="mockbar">
  <span class="lab">ES-DE mockup</span>
  <div class="seg"><button id="bSys" class="on" onclick="showView('sys')">System</button><button id="bGl" onclick="showView('gl')">Game</button></div>
  <span class="lab" style="margin-left:6px">Font size</span>
  <div class="seg"><button data-fs="medium" onclick="setFs('medium')">Medium</button><button data-fs="large" class="on" onclick="setFs('large')">Large</button><button data-fs="xlarge" onclick="setFs('xlarge')">X-Large</button></div>
  <span class="note">type scales with the screen like ES-DE · README recommends Large/X-Large on 5–7″ · 16:9</span>
</div>

<div class="stage-wrap"><div class="stage" id="stage">
  <section class="view show" id="vSys">
    <div class="hero" id="hero"></div>
    <div class="hero-bloom" id="bloom"></div>
    <div class="hero-vignette"></div>
    <div class="hero-logo" id="heroLogo"></div>
    <div class="hero-scrim"></div>
    <div class="topbar">
      <span class="tab">Library</span><span class="tab">Favorites</span><span class="tab">Recent</span><span class="tab on" id="platTab">Platforms</span>
      <span class="status"><span class="clock">14:32</span><span class="batt"><i></i></span>74%</span>
    </div>
    <div class="sysfg">
      <div class="spacer"></div>
      <div class="infocard">
        <div class="kind">Platform</div>
        <h1 id="sName">Nintendo GameCube</h1>
        <div class="meta"><span class="count" id="sCount">147 games</span><span class="dot"></span><span id="sSpec"></span></div>
        <p class="desc" id="sDesc"></p>
      </div>
      <div class="shelf-wrap">
        <div class="shelf-head"><span class="sl">All platforms</span><span class="pos" id="sPos">4 / 12</span></div>
        <div class="shelf" id="shelf"></div>
      </div>
    </div>
  </section>

  <section class="view" id="vGl">
    <div class="glwrap">
      <div class="glleft">
        <div class="topbar" style="background:transparent;border:none;position:relative;height:auto;padding:0;margin-bottom:.3em">
          <span class="tab" style="height:auto;padding:.3em 0">Library</span><span class="tab" style="height:auto;padding:.3em 0">Favorites</span><span class="tab" style="height:auto;padding:.3em 0">Recent</span><span class="tab on" style="height:auto;padding:.3em 0;--tabcol:#958bf4">Platforms</span>
          <span class="status"><span class="clock">14:32</span><span class="batt"><i></i></span>74%</span>
        </div>
        <div class="glhead"><b>Nintendo GameCube</b><div class="c"><span>147 games</span><span class="dot" style="width:4px;height:4px;border-radius:50%;background:var(--muted);display:inline-block"></span><span>Sorted A–Z</span></div></div>
        <div class="glgrid" id="glgrid"></div>
      </div>
      <aside class="gldetail" id="glDetail"></aside>
    </div>
  </section>

  <div class="helpbar">
    <div class="help"><span class="gly a">A</span> <span id="hA">Open</span></div>
    <div class="help"><span class="gly b">B</span> Back</div>
    <div class="help"><span class="gly x">X</span> <span id="hX">Random</span></div>
    <div class="help"><span class="gly y">Y</span> Favorites</div>
    <div class="help" style="margin-left:auto"><span class="gly m">☰</span> Menu</div>
  </div>
</div></div>

<script>
const SYS = __DATA__;
const GAMES = __GAMES__;
let cur = 3, sel = 0, fs = 'large';

/* real scale.xml fractions of screen HEIGHT (+ derived 16:9 grid column count) */
const SCALE = {
  medium:{hero:.052,header:.032,title:.026,count:.022,button:.021,label:.018,meta:.0185,tab:.018,clock:.024,itemY:.240,panelW:.334},
  large: {hero:.064,header:.044,title:.036,count:.030,button:.028,label:.022,meta:.025, tab:.025,clock:.027,itemY:.236,panelW:.424},
  xlarge:{hero:.074,header:.052,title:.042,count:.035,button:.032,label:.026,meta:.029, tab:.029,clock:.030,itemY:.357,panelW:.328},
};
function applyScale(){
  const s = SCALE[fs], st = document.getElementById('stage'), h = st.clientHeight, w = st.clientWidth, r = document.documentElement.style;
  const set=(k,v)=>r.setProperty(k,(h*v).toFixed(2)+'px');
  set('--fsHero',s.hero);set('--fsHeader',s.header);set('--fsTitle',s.title);set('--fsCount',s.count);
  set('--fsButton',s.button);set('--fsLabel',s.label);set('--fsMeta',s.meta);set('--fsTab',s.tab);set('--fsClock',s.clock);
  const capH = h*s.itemY;                                  // 2:3 capsule sized off screen height, like the theme
  r.setProperty('--capH', capH.toFixed(1)+'px');
  r.setProperty('--capW', (capH*2/3).toFixed(1)+'px');
  r.setProperty('--capGap', (h*0.016).toFixed(1)+'px');
  r.setProperty('--panelW', (w*s.panelW).toFixed(1)+'px'); // detail panel width tracks the theme
}
function setFs(name){
  fs = name; applyScale();
  document.querySelectorAll('[data-fs]').forEach(b=>b.classList.toggle('on', b.dataset.fs===name));
}
window.addEventListener('resize', applyScale);

/* system view */
const shelf = document.getElementById('shelf');
shelf.innerHTML = SYS.map((s,i)=>{
  const c='#'+s.color, empty=s.count===0;
  return `<div class="tile ${empty?'empty':''}" data-i="${i}" onclick="selSys(${i})">
      <div class="plate" style="background:
        radial-gradient(135% 125% at 20% 8%, ${c}7a 0%, ${c}1f 40%, transparent 62%),
        linear-gradient(158deg, #1d2734 0%, #121925 50%, #0a0e15 100%)"></div>
      <div class="logo">${s.svg}</div>${empty?'<span class="empty-flag">Empty</span>':''}
    </div>`;
}).join('');
function selSys(i){
  cur=i; const s=SYS[i], c='#'+s.color, empty=s.count===0;
  document.querySelectorAll('.tile').forEach((t,j)=>t.classList.toggle('active',j===i));
  document.getElementById('hero').style.background = `radial-gradient(92% 104% at 66% 30%, ${c}${empty?'30':'59'} 0%, ${c}18 36%, #090c11 78%)`;
  document.getElementById('bloom').style.background = `radial-gradient(44% 56% at 72% 33%, ${c}${empty?'1f':'45'}, transparent 66%)`;
  document.getElementById('heroLogo').innerHTML = s.svg;
  document.getElementById('heroLogo').classList.toggle('empty', empty);
  document.getElementById('platTab').style.setProperty('--tabcol', c);
  document.getElementById('sName').textContent = s.name;
  const cnt=document.getElementById('sCount');
  cnt.textContent = empty ? 'No games yet' : s.count.toLocaleString()+' games'; cnt.classList.toggle('zero', empty);
  document.getElementById('sSpec').textContent = s.spec;
  document.getElementById('sDesc').textContent = s.desc;
  document.getElementById('sPos').textContent = (i+1)+' / '+SYS.length;
  const t=shelf.querySelector(`.tile[data-i="${i}"]`); if(t) t.scrollIntoView({inline:'center',block:'nearest',behavior:'smooth'});
}

/* game view */
function art(seed){let h=0;for(const ch of seed)h=(h*23+ch.charCodeAt(0))%360;return `linear-gradient(135deg,hsl(${h} 46% 34%),hsl(${(h+48)%360} 52% 16%))`;}
function stars(r){return '★'.repeat(r)+'☆'.repeat(5-r);}
const glgrid=document.getElementById('glgrid');
glgrid.innerHTML=GAMES.map((g,i)=>
  `<div class="cap ${i===sel?'sel':''}" data-i="${i}" onclick="selGame(${i})">
     <div class="art" style="background:${art(g.t)}"><div class="nm">${g.t}</div></div>
     ${g.fav?'<span class="favm">★</span>':''}
   </div>`).join('');
function selGame(i){
  sel=i; document.querySelectorAll('.cap').forEach((c,j)=>c.classList.toggle('sel',j===i));
  const g=GAMES[i];
  document.getElementById('glDetail').innerHTML=`
    <div class="shot" style="background:${art(g.t+'shot')}"></div>
    <h3>${g.t}</h3>
    <div class="stars">${stars(g.rating)}</div>
    <div class="mg">
      <span class="k">Genre</span><span>${g.genre}</span>
      <span class="k">Developer</span><span>${g.dev}</span>
      <span class="k">Players</span><span>${g.players}</span>
      <span class="k">Released</span><span>${g.year}</span>
    </div>
    <div class="dlab">Description</div>
    <p class="desc">${g.desc}</p>
    <button class="play">▶  Play</button>`;
  const c=glgrid.querySelector(`.cap[data-i="${i}"]`); if(c) c.scrollIntoView({block:'nearest'});
}

function showView(v){
  document.getElementById('vSys').classList.toggle('show', v==='sys');
  document.getElementById('vGl').classList.toggle('show', v==='gl');
  document.getElementById('bSys').classList.toggle('on', v==='sys');
  document.getElementById('bGl').classList.toggle('on', v==='gl');
  document.getElementById('hA').textContent = v==='sys' ? 'Open' : 'Play';
  document.getElementById('hX').textContent = v==='sys' ? 'Random' : 'View media';
}

document.addEventListener('keydown',e=>{
  const sysOn=document.getElementById('vSys').classList.contains('show');
  if(e.key==='ArrowRight'){ sysOn?selSys((cur+1)%SYS.length):selGame((sel+1)%GAMES.length); e.preventDefault(); }
  if(e.key==='ArrowLeft'){ sysOn?selSys((cur-1+SYS.length)%SYS.length):selGame((sel-1+GAMES.length)%GAMES.length); e.preventDefault(); }
});

applyScale(); selSys(3); selGame(0);
</script>
"""

OUT.write_text(HTML.replace("__DATA__", DATA).replace("__GAMES__", GAMES_JSON), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB)")
