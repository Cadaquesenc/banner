import os, math, random, re
FONT = """@font-face { font-family:"JetBrains Mono"; font-weight:800; src:url(data:font/woff2;base64,d09GMgABAAAAAAWcABAAAAAACtwAAAU/AAI2BAAAAAAAAAAAAAAAAAAAAAAAAAAAGiIbIByBCgZgP1NUQVRMAFwRCAqJFIdJATYCJANECyQABCAFhFAHIAwHG9kIAJ6DceNc4lJEXLRalvG/Dz52TSjx8GT39edWD6uWREZFYAj2ixb6QpJISoXspzs/vKe9Qc61U4pt6eSOhbilyl2WHeVPWF/Cl2Dgtdu0aALYr1lchY8qXMFk7mc7YH7+mOl/W4MNs8GGQ4wqzbSoq7akI4tKiraJDU/PDohOw7x2ZI7jTz0m0AmQVEIlNGsWWnUSAtkg+YJWdQuVEKkJOgQEsnnkgnmuFn/cRgUgWTyy2CIXIJB8o9EsQyoN6aDNR0lUEw4fpAIOt6BeXYtRghDaJJ1UOmvVhYeO9sQU/ChpKAc3pV0hiDDSdaoFsHF569gHnGgDSLSbKIYdN6wA8AaGoao/d+/R+YPFt2kak55gmDDhU4ReCRpVc7qvnwoCHrSpCUoQmvSjryVaq2Eg/ceyxvf5KbrZh4Qqt16pJq0MtQ7oYufwFsPYuOAIVIdg1D4BZD+8jdZZa7WVhUkohNTjuyJ0BxgB9ARxBiA+RD+gVzCnVhM1c7KEQkPpDWJwyc4FXTJyeo/49MkpyZnx8Z22zn4Qja+UaHR5dtEv+uH3MTceKUeeWt/bduNmRL7eqNuDsx98FxQNlif6FnRSH+VGPTDm3jeGmDTl6zvbtwbF3OgjaHt0a30vXxdRZSWWFHVMKGrexeBudDpVeUMJK7aUpoZNa0VcK5UoVY7OqWAaIOvmy8r1/Y1atbcsy6hyNE7bIEkpdVmMNR6q5nRDKj5V7pQTY07WLtRhtur+fajv3Nn9nXOUKIqsZjEORXSGbFT3it6gfq8t129EYytFvu7VoVKtz3ukOLTtZjsR7XE3Ij5Vbj0m9+43FvX8S9Rmq06kILU+EkXOF9NfCu6NlI+3OvHRbg25SJ85uUXbm+RnzS9uJGjLEdoDmNTO89U02LmTuQvKlTCP5wHexynLr0rl0Hc4lyT1jNeEd2dVvsKwiMquV8M98Zk1jMtFaUH9dFqPSNypcAw4nHYHpegMp+yh0UP7l2fqR/d5IhToC6ae+QJl3OiKbsCKn5YfpbtZh39d+pdLrYTJsVzJvIGWnmAqofvqib7bZkxfv/GqFWMW4XxxZjvP6ynyAl8LIM//O4n1gjmZ9ZzF/MSazPwMm8bMxYsP6GQ6icHpd7I30tlB6MTTbCWktne6GHWCyuWZe2ksdF9Olp767u5k4gmlfo2n2DVCw1+e2o8UF2VmZbxJ7Yzsi3WKRMoB3TDo32KxKD8smnHv4w89/umV63+z2ctnOPBebchcuUCljMuWDnaUYXWdFejZbaGsU6UlX6pkHFnikKSEgeRcZnoMu+z5TXyzmddZhdXw2pub58EarKpdrakr62kGlvEkK+vJuM5TmHgBjSocFYVmpdAyRjjp3G691rcMgzUgTauylr/33L+JAmlO09dn90+wJDT9HxlS/QE/n9tXw2/duA8wskOYGqosoEUCwS3NmXZwkO6OXkSQiak71aRPTNgc3wRc+W4btwM5cIBu2xZ/AuArBLpjC9ZHsB0ddlhxHZVoascrsM4KgxxjJV38wKos8prVZFLQWM0GhJjZYkL0iwSd4j5Wqx6xntVVp3jift1ExytYiTDUKCRcn34UBEdFGkIoUXA9HZ8LhYtkgwsYgBAhBBAQUiSCh4tDx3rtBlH6EUhuS6nuEGUoEmpQPo30wbn6PMiujAPBr5ylAXGD7cmjnoXkXKnsIB8bEoeXA4NpXC5Xo+5x2PKDT8ZDyoiaa7stOM8oxPZw2QSN/nhkuoxEWf/juAg+TjwUGx+cgxzBzyYgBOgYDhAm5S+Q/9OuaR4AAAA=) format("woff2"); }"""
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "header.svg")


def smooth(pts, tension=0.55):
    d=f"M{pts[0][0]} {pts[0][1]}"
    n=len(pts)
    for i in range(n-1):
        p0=pts[i-1] if i>0 else pts[i]
        p1=pts[i]; p2=pts[i+1]
        p3=pts[i+2] if i+2<n else pts[i+1]
        c1=(p1[0]+(p2[0]-p0[0])/6*tension, p1[1]+(p2[1]-p0[1])/6*tension)
        c2=(p2[0]-(p3[0]-p1[0])/6*tension, p2[1]-(p3[1]-p1[1])/6*tension)
        d+=f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]} {p2[1]}"
    return d

A_PTS=[(-110,292),(90,250),(185,155),(360,140),(520,162),(660,140),(700,162),(560,162),
       (400,150),(250,162),(140,288),(92,292),(200,258),(330,162),(470,140),(600,162),
       (700,140),(620,162),(480,158),(360,140),(300,162),(430,162),(600,152),(750,140)]
B_PTS=[(1610,292),(1410,250),(1315,155),(1140,140),(980,162),(840,140),(800,162),(940,162),
       (1100,150),(1250,162),(1360,162),(1408,292),(1300,162),(1170,162),(1030,140),(900,162),
       (800,140),(880,162),(1020,158),(1140,140),(1200,162),(1070,162),(900,152),(750,142),(600,158),(430,140),(300,160),(180,286),(120,292),(320,150),(560,162),(820,140),(1120,158),(1360,150),(1470,292),(1610,292)]



def pace(seed, tb=0.82):
    import random
    r=random.Random(seed)
    segs=[]
    fast=True
    while sum(a for a,b in segs) < 0.999:
        if fast: segs.append((r.uniform(.10,.16), r.uniform(.045,.070)))
        else:    segs.append((r.uniform(.010,.028), r.uniform(.030,.048)))
        fast = not fast
    dp=sum(a for a,b in segs); dt=sum(b for a,b in segs)
    kp=[0.0]; kt=[0.0]
    for a,b in segs:
        kp.append(min(1.0, kp[-1]+a/dp)); kt.append(kt[-1]+b/dt*tb)
    kp[-1]=1.0; kt[-1]=tb
    kp.append(1.0); kt.append(1.0)
    return ";".join(f"{v:.4f}" for v in kp), ";".join(f"{v:.4f}" for v in kt)

KPA,KTA=pace(7)
KPB,KTB=pace(23, 1.0)

PA=smooth(A_PTS)
PB=smooth(B_PTS)

def debris(bx,by,t0,shards):
    out=[]
    for i,(dx,dy) in enumerate(shards):
        a=t0+i*0.001
        out.append(f'''    <rect x="{bx}" y="{by}" width="7" height="7" fill="currentColor" opacity="0">
      <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.85;0;0" keyTimes="0;{a:.4f};{a+0.004:.4f};{a+0.03:.4f};1"/>
      <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;{dx} {dy};{dx} {dy}" keyTimes="0;{a:.4f};{a+0.03:.4f};1"/>
    </rect>''')
    return "\n".join(out)

T1,T2,TB=0.462,0.569,0.820

def strike(x,y,t):
    return f'''  <circle cx="{x}" cy="{y}" r="0" fill="currentColor" opacity="0">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="0;0;30;46;46" keyTimes="0;{t:.4f};{t+0.005:.4f};{t+0.020:.4f};1"/>
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.95;0;0" keyTimes="0;{t-0.0005:.4f};{t+0.003:.4f};{t+0.020:.4f};1"/>
  </circle>
  <circle cx="{x}" cy="{y}" r="0" fill="none" stroke="currentColor" stroke-width="3" opacity="0">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="0;6;64;64" keyTimes="0;{t:.4f};{t+0.032:.4f};1"/>
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.75;0;0" keyTimes="0;{t:.4f};{t+0.005:.4f};{t+0.032:.4f};1"/>
  </circle>
  <circle cx="{x-14}" cy="{y-10}" r="0" fill="currentColor" opacity="0">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="0;8;26;26" keyTimes="0;{t+0.004:.4f};{t+0.060:.4f};1"/>
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.2;0;0" keyTimes="0;{t+0.004:.4f};{t+0.012:.4f};{t+0.060:.4f};1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;-6 -34;-6 -34" keyTimes="0;{t+0.004:.4f};{t+0.060:.4f};1"/>
  </circle>
  <circle cx="{x+16}" cy="{y-4}" r="0" fill="currentColor" opacity="0">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="0;7;23;23" keyTimes="0;{t+0.008:.4f};{t+0.064:.4f};1"/>
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.18;0;0" keyTimes="0;{t+0.008:.4f};{t+0.016:.4f};{t+0.064:.4f};1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;8 -40;8 -40" keyTimes="0;{t+0.008:.4f};{t+0.064:.4f};1"/>
  </circle>'''


# explosion pieces
shard_dirs=[(-86,-54),(84,-62),(-96,26),(92,34),(-14,-98),(22,96),(-58,74),(64,-96)]
ex=[]
for i,(dx,dy) in enumerate(shard_dirs):
    a=TB+i*0.0006
    ex.append(f'''  <rect x="746" y="136" width="8" height="8" fill="currentColor" opacity="0">
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{a:.4f};{a+0.004:.4f};{a+0.034:.4f};{a+0.050:.4f};1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;{dx} {dy};{dx} {dy+34};{dx} {dy+34}" keyTimes="0;{a:.4f};{a+0.026:.4f};{a+0.050:.4f};1"/>
  </rect>''')
fall=[]
for i,(dx,dy) in enumerate([(-40,150),(30,170),(-8,190)]):
    a=TB+0.004+i*0.002
    fall.append(f'''  <rect x="747" y="137" width="6" height="6" fill="currentColor" opacity="0">
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.9;0;0" keyTimes="0;{a:.4f};{a+0.006:.4f};{a+0.072:.4f};1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;{dx} {dy};{dx} {dy}" keyTimes="0;{a:.4f};{a+0.072:.4f};1"/>
  </rect>''')
smoke=[]
for i,(cx,cy,r1,r2,dy) in enumerate([(730,130,12,44,-40),(772,140,10,38,-52),(748,154,11,40,-30)]):
    a=TB+0.006+i*0.003
    smoke.append(f'''  <circle cx="{cx}" cy="{cy}" r="0" fill="currentColor" opacity="0">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="0;{r1};{r2};{r2}" keyTimes="0;{a:.4f};{a+0.085:.4f};1"/>
    <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.22;0;0" keyTimes="0;{a:.4f};{a+0.012:.4f};{a+0.085:.4f};1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;0 {dy};0 {dy}" keyTimes="0;{a:.4f};{a+0.085:.4f};1"/>
  </circle>''')

FPV_A_BODY='''<g class="wob" fill="currentColor" stroke="currentColor">
      <path d="M-15 -6L-34 -21M15 -6L34 -21" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M-13 8L-17 20M13 8L17 20M-23 20L-11 20M11 20L23 20" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <rect x="-19" y="-7" width="38" height="15" rx="7" stroke="none"/>
      <circle cx="0" cy="11" r="6" stroke="none"/>
      <rect x="-38" y="-27" width="9" height="9" rx="2" stroke="none"/><rect x="29" y="-27" width="9" height="9" rx="2" stroke="none"/>
      <ellipse class="prop" cx="-33.5" cy="-29" rx="22" ry="2.6" stroke="none"/><ellipse class="prop" cx="33.5" cy="-29" rx="22" ry="2.6" stroke="none"/>
    </g>'''

FPV_B_BODY='''<g class="wob2" fill="currentColor" stroke="currentColor">
      <g opacity=".45">
        <path d="M-11 -9L-25 -21M11 -9L25 -21" stroke-width="3" fill="none" stroke-linecap="round"/>
        <rect x="-29" y="-26" width="8" height="8" rx="2" stroke="none"/><rect x="21" y="-26" width="8" height="8" rx="2" stroke="none"/>
        <ellipse class="prop-s" cx="-25" cy="-27" rx="15" ry="2.2" stroke="none"/><ellipse class="prop-s" cx="25" cy="-27" rx="15" ry="2.2" stroke="none"/>
      </g>
      <path d="M-14 -4L-33 -15M14 -4L33 -15" stroke-width="4" fill="none" stroke-linecap="round"/>
      <rect x="-37" y="-21" width="9" height="9" rx="2" stroke="none"/><rect x="28" y="-21" width="9" height="9" rx="2" stroke="none"/>
      <ellipse class="prop-s" cx="-32.5" cy="-23" rx="20" ry="2.5" stroke="none"/><ellipse class="prop-s" cx="32.5" cy="-23" rx="20" ry="2.5" stroke="none"/>
      <rect x="-17" y="-6" width="34" height="14" rx="5" stroke="none"/>
      <path d="M17 -3L27 -10L29 -4L19 3Z" stroke="none"/>
      <path d="M-12 8L-15 19M12 8L15 19M-21 19L-9 19M9 19L21 19" stroke-width="3.2" fill="none" stroke-linecap="round"/>
    </g>'''

REAPER='''<g class="bobslow" fill="currentColor" stroke="none">
      <path d="M-30 -9L-6 -9L-12 -18L-26 -18Z" opacity=".85"/>
      <path d="M64 -3C64 -14 55 -20 43 -20C31 -20 23 -13 21 -7L-42 -8L-70 -3L-77 0L-70 4L-42 9L27 9C41 9 53 8 60 5C63 4 64 2 64 -3Z"/>
      <rect x="40" y="6" width="8" height="7" rx="2"/><circle cx="44" cy="15" r="8"/>
      <rect x="-26" y="-6" width="58" height="5.5" rx="2.5"/>
      <path d="M-56 -6L-73 -31L-64 -31L-48 -7Z"/>
      <path d="M-54 4L-70 24L-62 26L-46 6Z"/>
      <path d="M-50 4L-38 26L-31 23L-42 5Z" opacity=".5"/>
      <ellipse class="prop-v" cx="-81" cy="0" rx="2.6" ry="17"/>
      <rect x="-13" y="8" width="4" height="9" rx="1"/><rect x="13" y="8" width="4" height="9" rx="1"/>
      <g opacity="1"><rect x="-21" y="16" width="19" height="5.5" rx="2.75"/><path d="M-2 16L4 18.75L-2 21.5Z"/><path d="M-21 16L-25 12L-22.5 16ZM-21 21.5L-25 25.5L-22.5 21.5Z"/>
        <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.4380;0.4390;1"/></g>
      <g opacity="1"><rect x="5" y="16" width="19" height="5.5" rx="2.75"/><path d="M24 16L30 18.75L24 21.5Z"/><path d="M5 16L1 12L3.5 16ZM5 21.5L1 25.5L3.5 21.5Z"/>
        <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.5435;0.5445;1"/></g>
    </g>
    <g opacity=".12" fill="#9aa0a6"><animate attributeName="fill" dur="14s" repeatCount="indefinite" values="#9aa0a6;#9aa0a6;#e0564e;#e0564e;#9aa0a6;#9aa0a6;#e0564e;#e0564e;#9aa0a6;#9aa0a6" keyTimes="0;0.2620;0.2680;0.3250;0.3320;0.5760;0.5800;0.6100;0.6180;1"/><animate attributeName="opacity" dur="14s" repeatCount="indefinite" values=".12;.12;.28;.14;.28;.14;.28;.12;.12;.26;.13;.26;.12;.12" keyTimes="0;0.2620;0.2700;0.2780;0.2860;0.2940;0.3020;0.3320;0.5760;0.5840;0.5920;0.6000;0.6180;1"/><animateTransform attributeName="transform" type="rotate" dur="7s" repeatCount="indefinite" values="-15 44 13;15 44 13;-15 44 13" calcMode="spline" keyTimes="0;0.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/><path d="M44 13L15 224L73 224Z"/></g>
    <g opacity=".3" fill="none" stroke="#9aa0a6" stroke-width="1.6"><animate attributeName="stroke" dur="14s" repeatCount="indefinite" values="#9aa0a6;#9aa0a6;#e0564e;#e0564e;#9aa0a6;#9aa0a6;#e0564e;#e0564e;#9aa0a6;#9aa0a6" keyTimes="0;0.2620;0.2680;0.3250;0.3320;0.5760;0.5800;0.6100;0.6180;1"/><animateTransform attributeName="transform" type="rotate" dur="7s" repeatCount="indefinite" values="-15 44 13;15 44 13;-15 44 13" calcMode="spline" keyTimes="0;0.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/><ellipse cx="44" cy="224" rx="29" ry="5.5"/></g>'''

def missile(x0,y0,cx_,cy_,x1,y1,t0,t1):
    return f'''<g opacity="0">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{t0-0.0005:.4f};{t0:.4f};{t1-0.001:.4f};{t1:.4f};1"/>
  <animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" rotate="auto" keyPoints="0;0;1;1" keyTimes="0;{t0:.4f};{t1:.4f};1" path="M{x0} {y0}Q{cx_} {cy_} {x1} {y1}"/>
  <g fill="currentColor"><rect x="-24" y="-1.6" width="16" height="3.2" rx="1.6" opacity=".35"/><rect x="-13" y="-3.5" width="26" height="7" rx="3.5"/><path d="M13 -3.5L21 0L13 3.5Z"/><path d="M-13 -3.5L-19 -9.5L-15 -3.5ZM-13 3.5L-19 9.5L-15 3.5Z"/></g>
</g>'''


# --- finance: green up / red down, drawn left to right, over a volume panel ---
random.seed(11)
_pts=[]; _y=452
for _i in range(27):
    _x=-40+_i*62
    _y += random.uniform(-26,20) - (1.6 if _i>18 else 0)
    _y = max(392, min(468, _y)); _pts.append((_x, round(_y,1)))
_pts[-3]=(_pts[-3][0],430); _pts[-2]=(_pts[-2][0],404); _pts[-1]=(_pts[-1][0],376)
UP="#86ac86"; DOWN="#9c6b6b"
_L=[math.dist(_pts[i],_pts[i+1]) for i in range(len(_pts)-1)]
_TOT=sum(_L); DRAW=0.86
_segs=[]; _bars=[]; _run=0.0
for i,l in enumerate(_L):
    t0=DRAW*_run/_TOT; _run+=l; t1=DRAW*_run/_TOT
    up=_pts[i+1][1] < _pts[i][1]; col=UP if up else DOWN
    _segs.append(f'<path d="M{_pts[i][0]} {_pts[i][1]}L{_pts[i+1][0]} {_pts[i+1][1]}" fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="butt" opacity=".6" stroke-dasharray="{l+3:.0f}" stroke-dashoffset="{l+3:.0f}"><animate attributeName="stroke-dashoffset" dur="14s" repeatCount="indefinite" values="{l+3:.0f};{l+3:.0f};0;0;{l+3:.0f}" keyTimes="0;{t0:.4f};{t1:.4f};0.950;1"/></path>')
    _sub=[]
    _move=abs(_pts[i+1][1]-_pts[i][1])
    for k in range(5):
        x=_pts[i][0]+(_pts[i+1][0]-_pts[i][0])*(k+0.5)/5
        if not (-8 <= x <= 1496): continue
        h=5+min(24, _move*0.75)*(0.45+0.55*((i*7+k*13)%10)/9)
        _sub.append(f'<rect x="{x-2.5:.0f}" y="{(470-h) if up else 472:.0f}" width="5" height="{h:.0f}" rx="1"/>')
    if _sub:
        _bars.append(f'<g fill="{col}" opacity="0">{"".join(_sub)}<animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.42;.42;0" keyTimes="0;{t0:.4f};{min(0.999,t0+0.012):.4f};0.950;1"/></g>')
_full="M"+" L".join(f"{x} {y}" for x,y in _pts)
_dot=f'<circle r="3.4" fill="currentColor" opacity="0"><animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;.75;.75;0;0" keyTimes="0;0.02;{DRAW:.2f};{DRAW+0.02:.2f};1"/><animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{DRAW:.2f};1" path="{_full}"/></circle>'

# --- tiny callouts at the highs and lows ---
_ext=[]
for i in range(1,len(_pts)-1):
    y0,y1,y2=_pts[i-1][1],_pts[i][1],_pts[i+1][1]
    if y1<y0 and y1<y2: _ext.append((i,"high",y0-y1+y2-y1))
    if y1>y0 and y1>y2: _ext.append((i,"low", y1-y0+y1-y2))
_hi=sorted([e for e in _ext if e[1]=="high"],key=lambda e:-e[2])[:2]
_lo=sorted([e for e in _ext if e[1]=="low"], key=lambda e:-e[2])[:2]
_words={"high":["we're so back","up only"],"low":["it's over","buy the dip"]}
_labels=[]
_n={"high":0,"low":0}
for i,kind,_m in sorted(_hi+_lo):
    x,y=_pts[i]
    if x<70 or x>1430: continue
    w=_words[kind][_n[kind]%2]; _n[kind]+=1
    t0=DRAW*sum(_L[:i])/_TOT
    dy=-14 if kind=="high" else 20
    col=UP if kind=="high" else DOWN
    _labels.append(f'<text x="{x:.0f}" y="{y+dy:.0f}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13" fill="{col}" opacity="0">{w}<animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.75;.75;0;0" keyTimes="0;{t0:.4f};{min(0.99,t0+0.006):.4f};{min(0.994,t0+0.045):.4f};{min(0.997,t0+0.055):.4f};1"/></text>')

CHART=('<line x1="0" y1="476" x2="1500" y2="476" stroke="currentColor" stroke-width="1" opacity=".1"/>' + chr(10)
       + chr(10).join(_bars) + chr(10) + chr(10).join(_segs) + chr(10) + _dot + chr(10) + chr(10).join(_labels))


# --- searchlight colour tracks the segment of tape the reaper is over ---
_stops=[]
for i in range(len(_pts)-1):
    x0,x1=_pts[i][0],_pts[i+1][0]
    t0=max(0.0,min(1.0,(x0+150)/1800)); t1=max(0.0,min(1.0,(x1+150)/1800))
    if t1<=t0: continue
    col = UP if _pts[i+1][1] < _pts[i][1] else DOWN
    _stops.append((t0,col)); _stops.append((max(t0,t1-0.005),col))
if _stops[0][0] > 0: _stops.insert(0,(0.0,_stops[0][1]))
if _stops[-1][0] < 1: _stops.append((1.0,_stops[-1][1]))
BEAMV=";".join(c for t,c in _stops)
BEAMT=";".join(f"{t:.4f}" for t,c in _stops)
BEAM0=_stops[0][1]
REAPER=REAPER.replace("{BEAM0}",BEAM0).replace("{BEAMV}",BEAMV).replace("{BEAMT}",BEAMT)


SAM = """
<g opacity="0">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;0.2700;0.2710;0.2755;0.2765;1"/>
  <rect x="744" y="202" width="16" height="16" rx="3" fill="currentColor">
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;0 -3;0 -9" keyTimes="0;0.2700;0.2740;1"/>
  </rect>
</g>
<g opacity="0">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.9;0;0" keyTimes="0;0.2710;0.2760;0.2900;1"/>
  <ellipse cx="752" cy="222" rx="20" ry="8" fill="currentColor"/>
</g>
<g opacity="0">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.22;0;0" keyTimes="0;0.2740;0.2830;0.3600;1"/>
  <circle cx="740" cy="232" r="14" fill="currentColor">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="4;4;30;30" keyTimes="0;0.2740;0.3600;1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;-16 22;-16 22" keyTimes="0;0.2740;0.3600;1"/>
  </circle>
  <circle cx="766" cy="232" r="12" fill="currentColor">
    <animate attributeName="r" dur="14s" repeatCount="indefinite" values="4;4;26;26" keyTimes="0;0.2760;0.3600;1"/>
    <animateTransform attributeName="transform" type="translate" dur="14s" repeatCount="indefinite" values="0 0;0 0;18 20;18 20" keyTimes="0;0.2760;0.3600;1"/>
  </circle>
</g>
<path d="M752 200L360 150" stroke="currentColor" stroke-width="2.4" fill="none" opacity="0" stroke-linecap="round" stroke-dasharray="396" stroke-dashoffset="396">
  <animate attributeName="stroke-dashoffset" dur="14s" repeatCount="indefinite" values="396;396;0;0;-396;-396" keyTimes="0;0.2760;0.3180;0.3300;0.3700;1"/>
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;.34;.34;0;0" keyTimes="0;0.2760;0.2800;0.3300;0.3700;1"/>
</path>
<g opacity="0">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;0.2755;0.2760;0.3170;0.3180;1"/>
  <animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" rotate="auto" keyPoints="0;0;1;1" keyTimes="0;0.2760;0.3180;1" path="M752 200L360 150"/>
  <g fill="currentColor"><rect x="-20" y="-1.3" width="13" height="2.6" rx="1.3" opacity=".45"/><rect x="-8" y="-4" width="16" height="8" rx="4"/><path d="M8 -4L16 0L8 4Z"/><path d="M-8 -4L-14 -9L-11 -4ZM-8 4L-14 9L-11 4Z"/></g>
</g>"""

STRIKES=strike(360,150,0.3180)+chr(10)+strike(690,252,T1)+chr(10)+strike(880,246,T2)

svg=f'''<svg class="banner" width="1500" height="500" viewBox="0 0 1500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <style>
    {FONT}
    .banner {{ color: hsl(0 0% 100%); }}
    @media (prefers-color-scheme: light) {{ .banner {{ color: hsl(0 0% 8%); }} }}
    .word {{ font-family:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace; font-weight:800; font-size:100px; fill:currentColor; }}
    .prop   {{ transform-box:fill-box; transform-origin:center; animation: prop .17s linear infinite; }}
    .prop-s {{ transform-box:fill-box; transform-origin:center; animation: prop .19s linear infinite; }}
    .prop-v {{ transform-box:fill-box; transform-origin:center; animation: propv .26s linear infinite; }}
    .wob  {{ transform-box:fill-box; transform-origin:center; animation: wob 1.2s ease-in-out infinite; }}
    .wob2 {{ transform-box:fill-box; transform-origin:center; animation: wob 0.9s ease-in-out infinite; }}
    .bobslow {{ animation: bobslow 3.1s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{ .prop,.prop-s,.prop-v,.wob,.wob2,.bobslow {{ animation:none; }} }}
    @keyframes wob   {{ 0%,100%{{transform:rotate(-9deg)}} 50%{{transform:rotate(9deg)}} }}
    @keyframes bobslow {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-9px)}} }}
    @keyframes prop  {{ 0%,100%{{transform:scaleX(1)}} 50%{{transform:scaleX(.12)}} }}
    @keyframes propv {{ 0%,100%{{transform:scaleY(1)}} 50%{{transform:scaleY(.12)}} }}
  </style>

  <mask id="tittle">
    <rect x="700" y="180" width="80" height="140" fill="#fff"/>
    <rect x="736" y="194" width="32" height="32" fill="#000" opacity="0"><animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;0.2700;0.2710;0.9550;0.9650;1"/></rect>
  </mask>

</defs>


{CHART}

<text class="word" x="300" y="285">ethan</text><text class="word" x="660" y="285" opacity="1"><animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0;1;1" keyTimes="0;{T1:.4f};{T1+0.0015:.4f};0.900;0.912;1"/>g</text><text class="word" x="720" y="285" mask="url(#tittle)">i</text><text class="word" x="780" y="285">a</text><text class="word" x="840" y="285" opacity="1"><animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0;1;1" keyTimes="0;{T2:.4f};{T2+0.0015:.4f};0.900;0.912;1"/>n</text><text class="word" x="900" y="285">naros</text>

  <g>
{debris(690,236,T1,[(-34,-26),(30,-32),(-40,18),(36,22),(2,-44),(-52,-6),(48,-4),(14,40)])}
  </g>
  <g>
{debris(870,236,T2,[(-30,-28),(34,-22),(-36,20),(28,26),(-2,-40),(-46,-2),(44,8),(10,38)])}
  </g>

{missile(640,82,672,148,690,252,0.4390,T1)}
{missile(830,82,862,146,880,244,0.5445,T2)}

<g>
  <animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" path="M-150 62L1650 62"/>
  {REAPER}
</g>

<g opacity="1">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;0.3175;0.3180;1"/>
  <animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" keyPoints="{KPA}" keyTimes="{KTA}" path="{PA}"/>
  <g><animateTransform attributeName="transform" type="rotate" dur="14s" repeatCount="indefinite" values="0 0 0;0 0 0;360 0 0;360 0 0" keyTimes="0;0.395;0.428;1"/>
  {FPV_A_BODY}</g>
</g>

<g opacity="1">
  <animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;1;1" keyTimes="0;0.3;0.6;1"/>
  <animateMotion dur="14s" repeatCount="indefinite" calcMode="linear" keyPoints="{KPB}" keyTimes="{KTB}" path="{PB}"/>
  <g><animateTransform attributeName="transform" type="rotate" dur="14s" repeatCount="indefinite" values="0 0 0;0 0 0;-360 0 0;-360 0 0" keyTimes="0;0.655;0.688;1"/>
  {FPV_B_BODY}</g>
</g>

{SAM}

{STRIKES}

</svg>
'''

# --- trim the output: no inter-tag whitespace, no needless precision ---
svg=re.sub(r'(\d+\.\d{3,})', lambda m: f"{float(m.group(1)):.2f}".rstrip('0').rstrip('.'), svg)
svg=re.sub(r'>\s+<', '><', svg).strip()+"\n"

open(OUT,"w").write(svg)
print("wrote",OUT,len(svg),"bytes")
