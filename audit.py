"""reads the finished svg and checks that nothing collides by accident.

rebuilds every moving object's real path, pace and visibility window straight
out of assets/header.svg, then measures every pair of them across the loop.
the only overlaps that should ever print are the ones i choreographed.
"""
import os, re, math

SVG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "header.svg")

# how big each thing actually is: left, right, top, bottom from its own origin
BOX = {
    "reaper":  (-85, 72, -42, 23),
    "jet":     (-93, 86, -47, 37),
    "drone":   (-38, 38, -29, 21),
    "missile": (-24, 21, -9, 9),
}
INTENDED = {  # the hits that are supposed to happen
    ("drone", "missile"),
    ("jet", "missile"),
    ("drone", "drone"),
}


def sample(d):
    """walk an svg path into points. handles M / L / C / Q."""
    pts, cur = [], (0.0, 0.0)
    for cmd, args in re.findall(r"([MLCQ])([^MLCQZ]*)", d):
        v = [float(x) for x in args.replace(",", " ").split()]
        if cmd == "M":
            cur = (v[0], v[1]); pts.append(cur)
        elif cmd == "L":
            for i in range(0, len(v), 2):
                e = (v[i], v[i + 1])
                for k in range(1, 13):
                    pts.append((cur[0] + (e[0] - cur[0]) * k / 12, cur[1] + (e[1] - cur[1]) * k / 12))
                cur = e
        elif cmd == "C":
            for i in range(0, len(v), 6):
                c1, c2, e = (v[i], v[i + 1]), (v[i + 2], v[i + 3]), (v[i + 4], v[i + 5])
                for k in range(1, 25):
                    t = k / 24
                    pts.append(((1 - t) ** 3 * cur[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * e[0],
                                (1 - t) ** 3 * cur[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * e[1]))
                cur = e
        elif cmd == "Q":
            for i in range(0, len(v), 4):
                c, e = (v[i], v[i + 1]), (v[i + 2], v[i + 3])
                for k in range(1, 25):
                    t = k / 24
                    pts.append(((1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * c[0] + t * t * e[0],
                                (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]))
                cur = e
    return pts


def motion(d, keypoints, keytimes):
    """position at loop fraction t, matching how animateMotion spaces a path by length."""
    pts = sample(d)
    run = [0.0]
    for i in range(len(pts) - 1):
        run.append(run[-1] + math.dist(pts[i], pts[i + 1]))
    total = run[-1] or 1.0
    run = [r / total for r in run]
    kp = [float(x) for x in keypoints.split(";")] if keypoints else [0.0, 1.0]
    kt = [float(x) for x in keytimes.split(";")] if keytimes else [0.0, 1.0]

    def at(t):
        frac = kp[-1] if t > kt[-1] else kp[0]
        for i in range(len(kt) - 1):
            if kt[i] <= t <= kt[i + 1]:
                u = (t - kt[i]) / max(1e-9, kt[i + 1] - kt[i])
                frac = kp[i] + (kp[i + 1] - kp[i]) * u
                break
        for i in range(len(run) - 1):
            if run[i] <= frac <= run[i + 1]:
                u = (frac - run[i]) / max(1e-9, run[i + 1] - run[i])
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u,
                        pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u)
        return pts[-1]

    return at


def enclosing_group(src, pos):
    """span of the <g> that directly wraps the tag at pos."""
    depth = 0
    i = pos
    while i > 0:
        i -= 1
        if src.startswith("</g", i):
            depth += 1
        elif src.startswith("<g", i):
            if depth == 0:
                start = i
                break
            depth -= 1
    else:
        return None
    depth, j = 0, start
    while j < len(src):
        if src.startswith("</g", j):
            if depth == 1:
                return src[start:j]
            depth -= 1
        elif src.startswith("<g", j):
            depth += 1
        j += 1
    return src[start:]


def load():
    src = open(SVG).read()
    actors, counts = [], {}
    for m in re.finditer(r"<animateMotion[^>]*>", src):
        tag, blk = m.group(0), enclosing_group(src, m.start())
        if blk is None:
            continue
        path = re.search(r'path="([^"]+)"', tag)
        if not path:
            continue
        kp = re.search(r'keyPoints="([^"]+)"', tag)
        kt = re.search(r'keyTimes="([^"]+)"', tag)
        op = re.search(r'<animate attributeName="opacity"[^>]*values="([^"]+)"[^>]*keyTimes="([^"]+)"', blk)
        kind = ("jet" if "M86 -2L64 -9" in blk else
                "reaper" if "C64 -14" in blk or "M64 -3" in blk else
                "missile" if "prop" not in blk and len(blk) < 1500 else
                "drone")
        counts[kind] = counts.get(kind, 0) + 1
        actors.append({
            "kind": kind,
            "name": f"{kind}{counts[kind]}",
            "at": motion(path.group(1), kp.group(1) if kp else None, kt.group(1) if kt else None),
            "vis": ([float(x) for x in op.group(1).split(";")], [float(x) for x in op.group(2).split(";")]) if op else None,
        })
    return actors


def visible(a, t):
    if not a["vis"]:
        return True
    vals, ts = a["vis"]
    for i in range(len(ts) - 1):
        if ts[i] <= t <= ts[i + 1]:
            u = (t - ts[i]) / max(1e-9, ts[i + 1] - ts[i])
            return vals[i] + (vals[i + 1] - vals[i]) * u > 0.35
    return vals[-1] > 0.35


def main(steps=6000):
    actors = load()
    print("moving objects:", ", ".join(a["name"] for a in actors))
    worst = {}
    for s in range(steps):
        t = s / steps
        live = [a for a in actors if visible(a, t)]
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i], live[j]
                pa, pb = a["at"](t), b["at"](t)
                ea, eb = BOX[a["kind"]], BOX[b["kind"]]
                gx = max(pa[0] + ea[0], pb[0] + eb[0]) - min(pa[0] + ea[1], pb[0] + eb[1])
                gy = max(pa[1] + ea[2], pb[1] + eb[2]) - min(pa[1] + ea[3], pb[1] + eb[3])
                gap = max(gx, gy)
                key = (a["name"], b["name"])
                if key not in worst or gap < worst[key][0]:
                    worst[key] = (gap, t, pa, pb)

    bad = 0
    for (x, y), (gap, t, pa, pb) in sorted(worst.items(), key=lambda kv: kv[1][0]):
        if gap > 120:
            continue
        note = ""
        if gap < 0:
            pair = tuple(sorted((re.sub(r"\d+$", "", x), re.sub(r"\d+$", "", y))))
            if pair in INTENDED:
                note = "  <- on purpose"
            else:
                note = "  <- ACCIDENT"
                bad += 1
        print(f"{x:9}/{y:9} gap={gap:7.1f}px  at t={t:.3f}  "
              f"{tuple(round(v) for v in pa)} {tuple(round(v) for v in pb)}{note}")
    print("\naccidental collisions:", bad)
    return bad


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
