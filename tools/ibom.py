"""Generate an Interactive HTML BOM for this project.

    python tools/ibom.py <board.kicad_pcb> <dest-dir>

Run it with KiCad's bundled python; it needs pcbnew. The jobset does this already
because KiCad puts its bin folder first on PATH. Requires the InteractiveHtmlBom
plugin from the Plugin and Content Manager.

The plugin ignores ibom.config.ini when run from the command line, so options are
set here. See `generate_interactive_bom.py --help` for the full list.
"""
import glob
import os
import runpy
import sys

NAME_FORMAT = "%f-iBOM"      # %f = pcb file name without extension
EXTRA_FIELDS = "MPN"         # symbol fields to show and group by, comma separated
DNP_FIELD = "kicad_dnp"      # KiCad's built-in DNP flag
EXTRA_ARGS = []              # e.g. ["--dark-mode", "--highlight-pin1", "all", "--include-nets"]

PLUGIN_ID = "org_openscopeproject_InteractiveHtmlBom"
PLUGIN_SCRIPT = "generate_interactive_bom.py"


def find_plugin():
    # KICAD<major>_3RD_PARTY is set by whichever KiCad runs the job.
    for key, val in sorted(os.environ.items()):
        if key.startswith("KICAD") and key.endswith("_3RD_PARTY"):
            path = os.path.join(val, "plugins", PLUGIN_ID, PLUGIN_SCRIPT)
            if os.path.isfile(path):
                return path
    hits = glob.glob(os.path.expanduser(
        f"~/Documents/KiCad/*/3rdparty/plugins/{PLUGIN_ID}/{PLUGIN_SCRIPT}"))
    if hits:
        return sorted(hits)[-1]
    sys.exit("InteractiveHtmlBom plugin not found. "
             "Install it from KiCad -> Tools -> Plugin and Content Manager.")


def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: {os.path.basename(sys.argv[0])} <board.kicad_pcb> <dest-dir>")
    pcb, dest = sys.argv[1:3]

    # Without this the plugin insists on creating a wx app.
    os.environ["INTERACTIVE_HTML_BOM_NO_DISPLAY"] = "1"

    sys.argv = [
        find_plugin(),
        "--no-browser",
        "--dest-dir", dest,
        "--name-format", NAME_FORMAT,
        "--extra-fields", EXTRA_FIELDS,
        "--dnp-field", DNP_FIELD,
        *EXTRA_ARGS,
        pcb,
    ]
    runpy.run_path(sys.argv[0], run_name="__main__")


if __name__ == "__main__":
    main()
