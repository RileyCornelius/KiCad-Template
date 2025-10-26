# KiCad Template

A KiCad project template with DRC rules optimized for JLCPCB/PCBWAY fabrication, automated jobset outputs, and a bundled user-defined library for symbols, footprints, and 3D models.

## Features

- **Design Rule Constraints**: Compatible with JLCPCB/PCBWAY low-cost fabrication
- **DRC Rules**: Pre-configured `.kicad_dru` file for JLCPCB/PCBWAY compliance
- **Jobset Outputs**: Automated generation of PDFs, 3D models, renders, and BOMs
- **Footprint Importer**: Easy import of symbols, footprints, and 3D models
- **Minimalistic Drawing Sheet**: Clean, simple template with essential information only

## Getting Started

1. Copy or clone this template into your system or user template directory:
   
   **Windows Directories** (Replace `9.0` with your KiCad version):
   - System Templates: `%APPDATA%/kicad/9.0/templates`
   - User Templates: `C:\Users\<YOUR_NAME>\Documents\KiCad\9.0\template\`

2. Launch KiCad → **File → New Project From Template** → select `KiCad-Template`

3. Update project metadata in the schematic and PCB (title blocks, revision text, company name)

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
├── Fab/                         # Fabrication gerbers, BOMs, and pick-and-place files
├── Sheet.kicad_wks              # Minimal drawing sheet template
├── fp-lib-table                 # Footprint library table
├── sym-lib-table                # Symbol library table
└── README.md
```

## Hotkeys

Optionally use my custom KiCad hotkey bindings to speed up schematic and PCB work. The bindings and cheat sheet live here:

- [KiCad-Hotkey-Binds](https://github.com/RileyCornelius/KiCad-Hotkey-Binds)

## Plugins

### Required Plugins for Document and Fabrication Generation

Install via **KiCad → Tools → Plugin and Content Manager**:

- `InteractiveHtmlBom` — Generate interactive BOMs
- `Fabrication Toolkit` — Generate JLCPCB production files
- `PCBWay Fabrication Toolkit` — Generate PCBWAY production files

### Footprint Importer Plugin

For importing footprints, symbols, and 3D models:

- `Footprint Importer` — Import components from major sites with a single click

**Manual Installation:**

1. Download the latest release from the [GitHub releases page](https://github.com/RileyCornelius/KiCad-Footprint-Importer-Plugin/releases)
2. In KiCad, open **Tools → Plugin and Content Manager**
3. Choose **Install from File...**, select `KiCad-Footprint-Importer.zip`, and confirm
4. See the [plugin documentation](https://github.com/RileyCornelius/KiCad-Footprint-Importer-Plugin) for usage instructions

## Generating Documents with Jobset

1. Open `KiCad-Template.kicad_pro` in KiCad
2. Navigate to **File → Open Jobset File...** and select `<PROJECT_NAME>.kicad_jobset`
3. Click **Generate All Destinations** to create schematics, PCB drawings, renders, and BOMs

## Generate Fabrication Files

### JLCPCB

1. Install `Fabrication Toolkit` via Plugin Manager
2. Open `<PROJECT_NAME>.kicad_pcb` in KiCad
3. Navigate to **Tools → External Plugins → Fabrication Tools**
4. Click **Generate**
5. Output files will be saved to `production/`:
   - Gerber files: `<PROJECT_NAME>.zip`
   - Pick-and-place: `positions.csv`
   - BOM: `bom.csv`

### PCBWAY

1. Install `PCBWay Fabrication Toolkit` via Plugin Manager
2. Open `<PROJECT_NAME>.kicad_pcb` in KiCad
3. Navigate to **Tools → External Plugins → PCBWay Fabrication Tools**
4. Output files will be saved to `pcbway_production/`:
   - Gerber files: `<PROJECT_NAME>.kicad_pcb_gerber.zip`
   - Pick-and-place: `<PROJECT_NAME>.kicad_pcb_positions.csv`
   - BOM: `<PROJECT_NAME>.kicad_pcb_bom.csv`