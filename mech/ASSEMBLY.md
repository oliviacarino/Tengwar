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


## References
- XY-Plotter STL files (Thingiverse): https://www.thingiverse.com/thing:4200863/files