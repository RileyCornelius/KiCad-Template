# KiCad Template

A KiCad template for creating projects, complete with DRC rules optimized for JLCPCB or PCBWAY fabrication, automated jobset outputs, and bundled user defined library for symbol, footprints and 3D models.

## Features

- **Design Rule Constraints**: Compatible with JLCPCB or PCBWAY low cost fabrication
- **DRC Rules**: Compatible with JLCPCB or PCBWAY low cost fabrication `.kicad_dru`
- **Jobset Outputs**: Generates PDFs, 3D models, renders, and BOMs
- **User Defined Library**: Custom symbol, footprint, and 3D assets in `Lib/Custom`
- **Minimalistic Drawing Sheet**: Simple drawing sheet with only necessary info

## Getting Started

1. Copy or clone this template into either system or user template directory
    **Directory on Windows (Replace `9.0` with your KiCad Version):**
    System Tempates: `%APPDATA%/kicad/9.0/templates`
    User Tempates: `C:\Users\<YOUR_NAME>\Documents\KiCad\9.0\template\`
2. Launch KiCad → **File → New Project From Template** → select `KiCad-Template`
3. Update project metadata inside the schematic and PCB (title blocks, revision text, company name)

## Project Structure

```
Project/
├── KiCad-Template.kicad_pro     # Project main file
├── KiCad-Template.kicad_sch     # Main schematic
├── KiCad-Template.kicad_pcb     # PCB layout
├── KiCad-Template.kicad_dru     # DRC rules tuned for JLCPCB/PCBWAY
├── KiCad-Template.kicad_jobset  # Automated document generation
├── Docs/                        # Jobset generated documentation output folder
│   ├── 3D/
│   ├── BOM/
│   ├── Images/
│   │   └── Render/
│   ├── PCB/
│   └── Schematic/
├── Lib/                         # User-defined symbols, footprints, and 3D models
│   └── Custom/
│       ├── Custom.kicad_sym
│       ├── Custom.pretty/
│       └── Custom.3dshapes/
├── Fab/                         # Fabrication gerbers, bom, and pick and place
├── Sheet.kicad_wks              # Minimal drawing sheet template
├── fp-lib-table                 # Footprint library table
├── sym-lib-table                # Symbol library table
└── README.md
```

## Plugins

The following plugins are required for generating documents and fabrication files.

Install via **KiCad → Tools → Plugin and Content Manager**:

- `InteractiveHtmlBom` — generate interactive BoMs
- `Fabrication Toolkit` — generate JLCPCB production files
- `PCBWay Fabrication Toolkit` — generate PCBWAY production files

## Generating Documents with Jobset

1. Open `KiCad-Template.kicad_pro` in KiCad
2. Go to **File → Open Jobset File...** and choose `<PROJECT_NAME>.kicad_jobset`
3. Press **Generate All Destinations** to create schematics, PCB drawings, renders, and BOMs

## Generate Fabrication Files

To generate production files for JLCPCB.

1. Install `Fabrication Toolkit` via Plugin Manager
2. Open `<PROJECT_NAME>.kicad_pcb` in KiCad
3. Go to **Tools → External Plugins → Fabrication Tools**
4. Press **Generate**
5. Outputs will be written to `production/`:
   - Gerber (`<PROJECT_NAME>.zip`)
   - Pick-and-place (`positions.csv`)
   - BOM (`bom.csv`)

To generate production files for PCBWAY.

1. Install `PCBWay Fabrication Toolkit` via Plugin Manager
2. Open `<PROJECT_NAME>.kicad_pcb` in KiCad
3. Go to **Tools → External Plugins → PCBWay Fabrication Tools**
4. Outputs will be written to `pcbway_production/`:
   - Gerber (`<PROJECT_NAME>.kicad_pcb_gerber.zip`)
   - Pick-and-place (`<PROJECT_NAME>.kicad_pcb_positions.csv`)
   - BOM (`<PROJECT_NAME>.kicad_pcb_bom.csv`)