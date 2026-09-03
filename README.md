# banner

> the thing at the top of my profile is one svg file. no javascript, no gifs, no video.
> a reaper flies overwatch, two drones get shot down, and the dot of the "i" in my name
> is the missile that gets one of them.

![banner](assets/header.svg)

## the problem

github lets you put an image at the top of your profile readme and that is basically it.
you cannot ship javascript. you cannot load anything external. whatever you want the
banner to do has to already be inside one file, because github serves it through an
`<img>` tag and an svg loaded that way is sealed shut. no scripts run in it, ever.

so everything here is smil and css inside a single 49kb file.

## how it works

one clock. every animation in the file is `dur="18s"`, and each thing that happens is
written as a fraction of that: the first hellfire leaves at 0.438, the beam locks at
0.576, the f-22 fires at 0.615. change the loop length and the whole story stays in sync
because nothing has its own timeline.

what happens in 18 seconds:

- an mq-9 reaper crosses the top with a searchlight sweeping under it
- two hellfires come off its pylons and delete a whole letter each, then the letters come back
- fpv quads patrol above the name, punching out and hovering
- the light goes red when a drone is actually inside the cone
- an f-22 comes in, fires from standoff, kills one, and breaks away upward
- the dot of the "i" lifts off, trails smoke, and kills the other one
- a price tape draws itself along the floor, green up, red down, with volume blocks

the light going red is not on a timer. i solved for when a drone is geometrically inside
the beam: cone half-angle 7.8 degrees, sweeping plus or minus 15, apex riding the reaper.
the flashes sit exactly on the windows that maths spits out. one drone was passing through
the cone for 0.08 seconds, which is why it looked like it never got detected.

## what happened

nine things move on a 1500x500 canvas. "make sure nothing hits each other" is not
something you can check by watching it, so `audit.py` reads the finished svg, rebuilds
every object's real path, pace and visibility window, and measures every pair across
6000 samples of the loop.

```
moving objects: missile1, missile2, reaper1, drone1, drone2, jet1, missile3, missile4, drone3
drone2   /missile3  gap=  -18.0px  at t=0.637   <- on purpose
jet1     /missile3  gap=  -18.0px  at t=0.610   <- on purpose
drone1   /missile4  gap=  -18.0px  at t=0.737   <- on purpose
missile2 /drone2    gap=   29.0px  at t=0.564
reaper1  /drone1    gap=   36.0px  at t=0.287

accidental collisions: 0
```

the closest unintended pass in the whole loop is 29px, between a falling hellfire and a
drone. the three overlaps are the three kills.

the bugs were the actual work:

**github does not show you your new banner.** pushing a new svg changed nothing. github
proxies every image through its own cache, and the cache key is the url. i was pinning
the readme to a commit sha for a while so every push produced a url that had never
existed. `?v=1` on the raw url does the same job with one commit instead of two.

**chrome will not animate `animateMotion` inside a `clipPath`.** the plan was a second
copy of my name in red, clipped to the moving searchlight, so the letters lit up as it
passed. the clip stayed frozen at its start position. no error, no warning, it just does
not move. the beam itself is tinted instead.

**round line caps draw a dot out of nothing.** the price tape is 22 separate paths that
each wipe in with `stroke-dashoffset`. i rounded each dash length to a whole pixel, which
left a sub-pixel tail visible on segments that had not been drawn yet, and a round cap
turns that into a dot. there were little dots floating over the empty half of the chart
for two versions. the fix is overshooting the dash by 3px.

**a mask over the name repaints it every frame.** the letters were being deleted with an
animated `<mask>`, which meant the browser recomposited all 15 glyphs 60 times a second
for the whole loop. the font is monospace, so i split the name onto its own grid, 60px
per character, and gave the two dying letters plain opacity. now most of the name is
static and only the tittle of the "i" still needs a mask.

**scrolling away restarts it and there is nothing i can do.** an `<img>` svg has no
javascript and no memory, so it cannot know what time it is or where it left off. chrome
drops the image when it leaves the viewport and re-decodes it on the way back, from zero.
that is unfixable from inside the file, so the loop got shorter instead: 32 seconds down
to 18, so you see the whole thing before you scroll past.

**"crazier" flying looked random, not alive.** first attempt was long erratic paths and
it read as a screensaver. what fixed it was giving each drone a job: one patrols the left
half, one the right, they dip into the pockets either side of the name, and the character
comes from the pace rather than the path. hovers at 20px/s, dashes at 250px/s, one flip
each. because they own separate halves, they also cannot hit each other by accident until
the point where i want them to.

## what i learned

- if you cannot eyeball whether something is correct, write the checker. the collision
  auditor took twenty minutes and found three real overlaps i had already looked at and
  called fine
- deterministic beats random. everything on one clock means i can solve for when two
  things meet instead of hoping
- speed makes motion feel alive, shape does not. same path, varied pace, completely
  different animation
- a cache you did not know about will cost you an hour of "it didn't change"
- read the constraint first. half of what i tried failed because an svg in an `<img>` is
  a much smaller box than an svg in a page

## run

```
python3 build.py    # writes assets/header.svg
python3 audit.py    # checks nothing collides, exits 1 if anything does
```

no dependencies. `build.py` is the whole banner: the geometry, the choreography and the
timings are all in there, and the font is embedded as a base64 subset so the file has no
external requests.

## status

- ✅ live on my profile
- ✅ 18s loop, 49kb, 168 animations, no javascript, no filters
- ✅ 0 accidental collisions, checked every build
- ⬜ restarts when you scroll past it, and always will

---

font is [jetbrains mono](https://github.com/JetBrains/JetBrainsMono), subset to the
characters in my name, licensed ofl 1.1.
