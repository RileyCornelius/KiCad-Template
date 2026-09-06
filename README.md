# KiCad Template

A KiCad project template with DRC rules for JLCPCB and PCBWay, a jobset that generates documents and production files, and a project library for symbols, footprints, and 3D models.

## Features

- Design rule constraints and a `.kicad_dru` file that pass JLCPCB and PCBWay low-cost fabrication checks
- A jobset that generates PDFs, STEP models, renders, BOMs, and JLCPCB and PCBWay production files
- A minimal drawing sheet with only the essential title block fields

## Getting started

1. Copy or clone this template into a KiCad template directory. Replace `10.0` with your KiCad version:
   - System templates: `%APPDATA%/kicad/10.0/templates`
   - User templates: `C:\Users\<YOUR_NAME>\Documents\KiCad\10.0\template\`
2. In KiCad, choose **File → New Project From Template** and select `KiCad-Template`.
3. Update the title blocks in the schematic and PCB: title, revision, and company.

## Project structure

```
Project/
├── KiCad-Template.kicad_pro     # Project file
├── KiCad-Template.kicad_sch     # Root schematic
├── KiCad-Template.kicad_pcb     # PCB layout
├── KiCad-Template.kicad_dru     # DRC rules for JLCPCB and PCBWay
├── KiCad-Template.kicad_jobset  # Document and production file generation
├── docs/                        # Written by the jobset Docs, Images, and 3D destinations
│   ├── 3D/                      # STEP models
│   ├── images/                  # PCB renders
│   ├── <PROJECT_NAME>-BOM.csv
│   ├── <PROJECT_NAME>-iBOM.html
│   ├── <PROJECT_NAME>-PCB.pdf
│   └── <PROJECT_NAME>-Schematics.pdf
├── manufacturing/               # Written by the jobset Fabrication destination
│   ├── JLCPCB/                  # Gerber zip, bom.csv, positions.csv
│   └── PCBWay/                  # Gerber zip, bom.csv, positions.csv
├── lib/                         # Project symbols, footprints, and 3D models
│   ├── 0_Project.kicad_sym
│   ├── 0_Project.pretty/
│   └── 0_Project.3dshapes/
├── tools/
│   ├── fab.py                   # Runs the JLCPCB and PCBWay plugins from the jobset
│   └── ibom.py                  # Runs the InteractiveHtmlBom plugin from the jobset
├── Sheet.kicad_wks              # Drawing sheet
├── fp-lib-table                 # Footprint library table
├── sym-lib-table                # Symbol library table
└── README.md
```

## Plugins

The jobset needs three plugins. Install them from **KiCad → Tools → Plugin and Content Manager**:

- `InteractiveHtmlBom` for the interactive BOM
- `Fabrication Toolkit` for JLCPCB production files
- `PCBWay Fabrication Toolkit` for PCBWay production files

## Generate documents and production files

1. Open `KiCad-Template.kicad_pro` in KiCad.
2. Choose **File → Open Jobset File...** and select `<PROJECT_NAME>.kicad_jobset`.
3. Click **Generate All Destinations**, or generate one destination on its own.

The Docs, Images, and 3D destinations write to `docs/`. The Fabrication destination writes to `manufacturing/`. Uncheck a job in the jobset editor to skip it.

### Interactive BOM

The `Generate iBOM .HTML` job runs `tools/ibom.py` with KiCad's bundled Python. The script finds the `InteractiveHtmlBom` plugin through the `KICAD<version>_3RD_PARTY` variable, so a KiCad upgrade does not break it. To change the fields shown, dark mode, or pin 1 highlighting, edit the constants at the top of `tools/ibom.py`. Run `generate_interactive_bom.py --help` for the full list of options.

### Production files

The `Generate JLCPCB production files` and `Generate PCBWay production files` jobs run `tools/fab.py` with KiCad's bundled Python. The script loads the board and calls the installed plugins directly, without the PCB editor. Each vendor gets a gerber zip, a `bom.csv`, and a `positions.csv` in its own folder under `manufacturing/`.
## Other useful repos

### Footprint importer plugin

[KiCad-Footprint-Importer-Plugin](https://github.com/RileyCornelius/KiCad-Footprint-Importer-Plugin) imports symbols, footprints, and 3D models from vendor sites in one click. To install it:

1. Download `KiCad-Footprint-Importer.zip` from the [releases page](https://github.com/RileyCornelius/KiCad-Footprint-Importer-Plugin/releases).
2. In KiCad, open **Tools → Plugin and Content Manager**.
3. Choose **Install from File...** and select the zip.

The [plugin README](https://github.com/RileyCornelius/KiCad-Footprint-Importer-Plugin) covers usage.
