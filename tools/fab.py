"""Generate JLCPCB and/or PCBWay production files with the installed KiCad plugins.

    python tools/fab.py <board.kicad_pcb> <dest-dir> [jlcpcb|pcbway|all] [--keep-extras]

Writes <dest-dir>/JLCPCB and <dest-dir>/PCBWay, each with a gerber zip, bom.csv and
positions.csv. Run it with KiCad's bundled python; it needs pcbnew. The jobset does
this already because KiCad puts its bin folder first on PATH.

Requires the "Fabrication Toolkit" and "PCBWay Fabrication Toolkit" plugins from
the Plugin and Content Manager.
"""
import glob
import importlib
import os
import shutil
import sys
import tempfile
import types

import pcbnew

JLC_PLUGIN = "com_github_bennymeg_JLC-Plugin-for-KiCad"
JLC_ARCHIVE_NAME = "{name}-JLCPCB-Gerbers"
JLC_OPTIONS = {
    "auto_translate": True,      # JLC rotation/offset corrections from the plugin's database
    "auto_fill": True,           # refill zones before plotting; the board file is not saved
    "exclude_dnp": True,
    "extra_layers": "",          # e.g. "User.Drawings,User.Comments"
    "user1_vcut": False,
    "user2_alt_edge": False,
    "all_active_layers": False,
}

PCBWAY_PLUGIN = "com_github_pcbway_PCBWay-Fabrication-Toolkit-for-KiCad"
PCBWAY_ARCHIVE_NAME = "{name}-PCBWay-Gerbers"

# netlist.ipc and designators.csv are not needed to order. --keep-extras overrides.
KEEP_EXTRAS = False
EXTRA_FILES = ("netlist.ipc", "designators.csv")


def plugins_dir():
    # KICAD<major>_3RD_PARTY is set by whichever KiCad runs the job.
    for key, val in sorted(os.environ.items()):
        if key.startswith("KICAD") and key.endswith("_3RD_PARTY"):
            p = os.path.join(val, "plugins")
            if os.path.isdir(p):
                return p
    hits = glob.glob(os.path.expanduser("~/Documents/KiCad/*/3rdparty/plugins"))
    if hits:
        return sorted(hits)[-1]
    sys.exit("KiCad 3rd party plugin folder not found.")


def load_plugin_module(plugin, submodule):
    pdir = plugins_dir()
    if not os.path.isdir(os.path.join(pdir, plugin)):
        sys.exit(f"Plugin '{plugin}' not found in {pdir}. "
                 "Install it from KiCad -> Tools -> Plugin and Content Manager.")
    if pdir not in sys.path:
        sys.path.insert(0, pdir)
    if plugin not in sys.modules:
        # Both plugins register a pcbnew ActionPlugin in __init__.py, which asserts
        # outside the editor. A stub package keeps __init__.py from running.
        pkg = types.ModuleType(plugin)
        pkg.__path__ = [os.path.join(pdir, plugin)]
        pkg.__package__ = plugin
        sys.modules[plugin] = pkg
    return importlib.import_module(f"{plugin}.{submodule}")


def fresh_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path


def remove_extras(out, keep):
    if keep:
        return
    for f in os.listdir(out):
        if f.endswith(EXTRA_FILES):
            os.remove(os.path.join(out, f))


def make_jlcpcb(board, name, dest, keep_extras):
    process = load_plugin_module(JLC_PLUGIN, "process")
    out = fresh_dir(os.path.join(dest, "JLCPCB"))
    work = tempfile.mkdtemp(prefix="jlc_")
    gerbers = os.path.join(work, "gerbers")
    os.makedirs(gerbers)
    o = JLC_OPTIONS
    try:
        # Same steps as the plugin's own cli.py, minus its fixed output folder.
        pm = process.ProcessManager(board)
        if o["auto_fill"]:
            pm.update_zone_fills()
        pm.generate_gerber(gerbers, o["extra_layers"], o["user1_vcut"],
                           o["user2_alt_edge"], o["all_active_layers"])
        pm.generate_drills(gerbers)
        pm.generate_netlist(work)
        pm.generate_tables(work, o["auto_translate"], o["exclude_dnp"])
        pm.generate_positions(work)
        pm.generate_bom(work)
        archive = shutil.make_archive(
            os.path.join(work, JLC_ARCHIVE_NAME.format(name=name)), "zip", gerbers)
        shutil.move(archive, out)
        for f in os.listdir(work):
            if f.endswith((".csv", ".ipc")):
                shutil.move(os.path.join(work, f), out)
        remove_extras(out, keep_extras)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return out


def make_pcbway(board, name, dest, keep_extras):
    # The PCBWay plugin has no CLI and reads the board via pcbnew.GetBoard(),
    # which returns nothing outside the editor.
    pcbnew.GetBoard = lambda: board
    process = load_plugin_module(PCBWAY_PLUGIN, "process")
    out = fresh_dir(os.path.join(dest, "PCBWay"))
    work = tempfile.mkdtemp(prefix="pcbway_")
    gerbers = os.path.join(work, "gerber")
    os.makedirs(gerbers)
    try:
        proc = process.PCBWayProcess()
        proc.get_gerber_file(gerbers)
        proc.get_netlist_file(work)
        proc.get_components_file(work)
        archive = shutil.make_archive(
            os.path.join(work, PCBWAY_ARCHIVE_NAME.format(name=name)), "zip", gerbers)
        shutil.move(archive, out)
        # The plugin prefixes files with "<file>.kicad_pcb_". Swap that for "<name>-PCBWay-".
        base = os.path.basename(board.GetFileName()) + "_"
        for f in os.listdir(work):
            if f.endswith((".csv", ".ipc")):
                nice = f"{name}-PCBWay-{f[len(base):]}" if f.startswith(base) else f
                shutil.move(os.path.join(work, f), os.path.join(out, nice))
        remove_extras(out, keep_extras)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return out


def main():
    args = sys.argv[1:]
    keep_extras = KEEP_EXTRAS or "--keep-extras" in args
    args = [a for a in args if a != "--keep-extras"]
    if len(args) not in (2, 3):
        sys.exit(f"usage: {os.path.basename(sys.argv[0])} <board.kicad_pcb> <dest-dir> [jlcpcb|pcbway|all] [--keep-extras]")
    pcb, dest = os.path.abspath(args[0]), os.path.abspath(args[1])
    which = args[2].lower() if len(args) == 3 else "all"
    if which not in ("jlcpcb", "pcbway", "all"):
        sys.exit("third argument must be jlcpcb, pcbway or all")
    if not os.path.isfile(pcb):
        sys.exit(f"Board not found: {pcb}")

    board = pcbnew.LoadBoard(pcb)
    name = os.path.splitext(os.path.basename(pcb))[0]
    os.makedirs(dest, exist_ok=True)

    if which in ("jlcpcb", "all"):
        print("JLCPCB  ->", make_jlcpcb(board, name, dest, keep_extras))
    if which in ("pcbway", "all"):
        print("PCBWay  ->", make_pcbway(board, name, dest, keep_extras))


if __name__ == "__main__":
    main()
