# Assembly Guide
**NOTE -- this guide is in-progress**
## Design Overview
While initially designing V1.0 of Tengwar, I wanted to keep things as light and simple as possible. I considered following an H-bot design:

<p align="center">
  <img src="../images/h_bot.jpg" width="300"/>
</p>

I really liked the H-bot kinetics, but I really didn't want to use *three* different bar fixtures due to the added weight. I ended up finding an alternative, open source design that only uses two, (see [References](#references) for linked Thingiverse files).

<table align="center">
  <tr>
  <td align="center">
      <img src="../images/v1_physical.png" alt="Render V2" width="390"><br>
      <em>Original V1 prototype</em>
    </td>
    <td align="center">
      <img src="../images/render_V1.png" alt="Render V1" width="350"><br>
      <em>Check out an interactive view <a href="https://a360.co/4dBvp7I">here</a>!</em>
    </td>
  </tr>
</table>

- Cartesian layout
    - The x-axis is a length of **2060 V-slot** extrusion, a **wheeled gantry plate** rides on it, and the y-axis arm is carried on the gantry.
        - The x belt runs over and under the 2060 extrusion, which is why the x-axis uses a larger **30T pulley** and sits slightly raised.
    - Y-axis arm runs on **8 mm rods** with LM8UU bearings.
- The pen gantry uses a SG90 servo, that move vertically on two short **5 mm rods**.

## Physical Assembly

### 1 Prep hardware
- [ ] Print all required parts. See [Printed Parts](#printed-parts) for full list.
- [ ] **Tap M5 threads into both ends of the 2060** (the center bores used for the end brackets)
- [ ] Cut the 5 mm pen-lifter rods to ~7 cm
- [ ] Cut the 8 mm y rods to length if needed, and deburr the ends
- [ ] Clean the printed holes, ream them to size, and seat any captive nuts
- [ ] Cut polypropylene strips for the wire guides

### 2 X-axis

- [ ] Bolt the motor-end bracket to the tapped extrusion end (M5×8). Mount the x stepper (M3×6 ×4) with the **30T pulley** (set screw on the shaft flat).
- [ ] Bolt the idler-end bracket to the other end (M5×10 countersunk). Mount the idler (M5×25 countersunk, washers, nyloc).
- [ ] Fit the feet, bolted from underneath into the V-slot with T-nuts (M5×10)
- [ ] Fit the motor-end shield

### 3 Gantry

- [ ] Assemble the gantry plate: wheels + spacers, with the **eccentric spacers on one side**
- [ ] Slide the gantry onto the 2060 from one end, **before** both end brackets are permanently tight if access requires it
- [ ] Turn the eccentric spacers until the gantry rolls smoothly with **zero rock or play**, but no drag
- [ ] Mount the printed gantry case
- [ ] Mount the y stepper + 20T pulley to the gantry plate (M5×35 + nuts; trim them if they hit anything)

### 4 Y-axis arm

- [ ] Press the 4× LM8UU bearings into their housings
- [ ] Fit the 8 mm rods through the bearings, then clamp them into the pen-end and other-end brackets (M3×12 + nuts)
- [ ] Fit the 2× small y idler pulleys
- [ ] Slide the full y travel by hand to check for binding and droop at full reach

### 5 Pen lifter

- [ ] Mount the SG90 servo
- [ ] Assemble the lifter on the 5 mm rods; check the vertical slide is smooth with no rattle
- [ ] Fit the pen clamp (M3×30 + printed bolt cap)
- [ ] **Leave the servo horn off for now.** This will be calibrated in a later step.

### 6 Belts

- [ ] X belt: run it over and under the 2060, around the 30T pulley and idler, then clip both ends to the gantry
- [ ] Y belt: run it around the 20T pulley and idlers, then clip it to the arm bracket
- [ ] The y-axis brackets are designed so the belt can be removed or re-tensioned easily
- [ ] Tension: firm, with no slack when the direction changes. It should not be guitar-string tight!

### 7 Mount to base

- [ ] Screw the feet down to the base board (wood screws). This adds a lot of stiffness and reduces pen droop.
- [ ] If you're using a cutting mat, align the x-axis square to the mat rebate

## Electronics & Wiring
[tbd]

## First Motion & Calibration
[tbd]

## Bill of Materials
*Note: Prices will be added later.*
### X-axis
| Qty | Part | Notes |
|-----|------|-------|
| 1 | 2060 V-slot extrusion | 40+ cm |
| ~2.5× V-slot extrusion length | GT2 belt| 6 mm |
| 1 | 30T GT2 pulley | 5 mm bore, for 6 mm belt |
| 1 | Smooth idler pulley | Similar diameter to the 30T. OpenBuilds smooth idler kit or similar |

### Y-axis
| Qty | Part | Notes |
|-----|------|-------|
| 1 | Large V-slot gantry plate kit | Wheels, **eccentric spacers**, bolts |
| 2 | 8 mm linear rod | ~500 mm |
| 4 | LM8UU linear bearing | |
| 1 | 20T GT2 pulley | 5 mm bore; for the y motor |
| 2 | Small idler pulley | 5 mm bore, for 6 mm belt; not the large OpenBuilds ones |

### Pen Gantry
| Qty | Part | Notes |
|-----|------|-------|
| 2 | 5 mm smooth rod | Cut to ~7 cm |
| 1 | 3-wire servo extension | |

### Misc Hardware
| Qty | Part | Used for |
|-----|------|----------|
| 17 | M3×6 | NEMA mounts (8), top of Arduino lid/housing (2), x-axis wire holder (2) |
| 4 | M3×8 | Wire guide (2), fastens base of Arduino to its box-housing (2) |
| 4 | M3×12 pan head | Linear rod clamps |
| 1 | M3×30 socket head | Pen holder |
| 14 | M3 nut | |
| 2 | M5×8 pan head | Stepper end to 2060 |
| 4 | M5×10 pan head | Feet / base mounts |
| 3 | M5×10 countersunk | Idler bracket to 2060 |
| 3 | M5×25 countersunk | Idler pulleys |
| 4 | M5×35 pan head | Y motor assembly to gantry plate (may need cutting down for clearance) |
| 8 | M5 nut | |
| 2 | M5 nyloc nut | Idlers |
| 10 | M5 washer | |
| 4 | Drop-in M5 T-nut | |
| — | Low-profile M5 bolts | Bracket to V-slot |
| — | Belt clips | Zip ties or printed (see References) |
| 1 | Thin polypropylene sheet | Wire guides |
| 1 + ~6 | Base board + wood screws | |
| 1 | **M5 tap** | For the extrusion ends |

### Tools & Supplies
| Category | Item | Purpose |
|---|---|---|
| Hand tools | Metric hex key set (1.5–5 mm) | All bolts and pulley set screws |
| Hand tools | Small wrench set (5.5, 8, 10 mm) | |
| Measuring | Steel ruler + square | Squaring frame, calibration, wall placement |
| Metalwork | M5 × 0.8 tap + handle | Threading extrusion ends |
| Metalwork | Vise or clamps | Holding parts for tapping and cutting |
| Metalwork | Hacksaw | Cutting rods (wear PPE!) |
| Metalwork | Drill + bits (3, 5, 8 mm) | Cleaning printed holes, pilot holes |
| Printing | Filament (PETG brackets, PLA box/lid) | Printed parts |
| Electronics | Soldering iron + solder + heat-shrink | Wire joins, limit switches |
| Consumables | Light machine oil | Tapping lubricant + rods & bearings |
| Consumables | Blue threadlocker | Set screws, wheel bolts |
| Consumables | Zip ties + double-sided tape | Cable management, test fitting |
| Wall mount | Backboard + wood screws | Mounting surface |
| Wall mount | French cleat or wall anchors + stud finder + level | Hanging the plotter |
| Testing | Pens + paper | Drawing materials |

## Printed Parts
Associated files can be found within `/mech/STL`:
- [X end bracket – motor end](../mech/STL/files/2060_x-axis_motor-end-bracket.stl)
- [X end bracket – idler end](../mech/STL/files/2060_x-axis_other-end-bracket.stl)
- Motor-end shield (optional cosmetic) 
- [Feet](../mech/STL/files/2060_x-axis_foot.stl)
- [Arduino box](../mech/STL/files/2060_arduino-box.stl)
- [Arduino lid](../mech/STL/files/2060_arduino-box-lid.stl)
- [Gantry case](../mech/STL/files/y-axis_gantry.stl)
- [Y-axis pen-end bracket](../mech/STL/files/y-axis_pen-end.stl)
- [Y-axis other-end bracket](../mech/STL/files/y-axis_other-end.stl)
- [Pen lifter](../mech/STL/files/y-axis_pen-lifter.stl)
- [M3 bolt cap](../mech/STL/files/m3_screw_cap.stl)

Notes:
- **Pen lifter tolerance:** adding about 0.1 mm extra clearance may give smoother sliding with no wobble on 5 mm rods.
- Bearing pockets should press-fit firmly.

## References
- XY-Plotter STL files (Thingiverse): https://www.thingiverse.com/thing:4200863/files