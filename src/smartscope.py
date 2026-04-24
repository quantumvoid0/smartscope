#!/usr/bin/env python3
# this code has no comments bcz if it was hard to write , its gotta be hard to read

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, GLib, Gdk, Pango, PangoCairo

import subprocess, json, re, threading, math
from pathlib import Path

MD3 = """

button {
  background-image: none;
  background-color: #353B49;
  color: #E5E9F0;
  border: none;
  box-shadow: none;
}
window, .md-window {
    background-color: #1E222A;
}
.md-topbar {
    background-color: #282D38;
    border-bottom: 1px solid #353B49;
    padding: 0px 16px;
    min-height: 64px;
}
.md-topbar-title {
    font-size: 22px;
    font-weight: 400;
    color: #E5E9F0;
    letter-spacing: 0px;
}
.md-topbar-sub {
    font-size: 12px;
    color: #E5E9F0;
}
.md-toolbar {
    background-color: #282D38;
    padding: 8px 16px;
    border-bottom: 1px solid #353B49;
}
.md-card {
    background-color: #282D38;
    border-radius: 12px;
    border: none;
}
.md-card-outlined {
    background-color: #282D38;
    border-radius: 12px;
    border: 1px solid #353B49;
}
.md-label-large {
    font-size: 11px;
    font-weight: 500;
    color: #E5E9F0;
    letter-spacing: 1.5px;
}
.md-body {
    font-size: 13px;
    color: #E5E9F0;
}
.md-body-small {
    font-size: 11px;
    color: #E5E9F0;
}
.md-mono {
    font-size: 12px;
    color: #E5E9F0;
}
.md-mono-small {
    font-size: 11px;
    color: #E5E9F0;
}
.md-headline {
    font-size: 18px;
    font-weight: 400;
    color: #E5E9F0;
}
.md-display {
    font-size: 28px;
    font-weight: 300;
    color: #E5E9F0;
}
.md-chip {
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    border: 1px solid #353B49;
    background-color: #282D38;
    color: #E5E9F0;
}
.md-chip-primary {
    background-color: #353B49;
    border-color: #4A5160;
    color: #E5E9F0;
}
.md-chip-green {
    background-color: #1E3A2A;
    border-color: #2D6B43;
    color: #6FCF97;
}
.md-chip-yellow {
    background-color: #3A3010;
    border-color: #7A6520;
    color: #F2C94C;
}
.md-chip-red {
    background-color: #3A1E1E;
    border-color: #7A2D2D;
    color: #EB5757;
}
.md-chip-blue {
    background-color: #1A2A3A;
    border-color: #2D5280;
    color: #56A8F5;
}
.md-btn-filled {
    background-color: #353B49;
    color: #E5E9F0;
    border: none;
    box-shadow: none;
    border-radius: 20px;
    padding: 6px 24px;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.1px;
}
.md-btn-filled:hover { background-color: #282D38; }
.md-btn-filled:active { background-color: #282D38; }
.md-btn-tonal {
    background-color: #353B49;
    color: #E5E9F0;
    border: none;
    box-shadow: none;
    border-radius: 20px;
    padding: 6px 20px;
    font-size: 13px;
    font-weight: 500;
}
.md-btn-tonal:hover { background-color: #282D38; }
.md-btn-outlined {
    background-color: transparent;
    color: #E5E9F0;
    border: 1px solid #353B49;
    box-shadow: none;
    border-radius: 20px;
    padding: 6px 20px;
    font-size: 13px;
    font-weight: 500;
}
.md-btn-outlined:hover { background-color: #282D38; }
.md-divider { background-color: #353B49; min-height: 1px; }
.md-list-row {
    padding: 10px 16px;
    border-bottom: 1px solid #353B49;
}
.md-list-row:last-child { border-bottom: none; }
.md-list-row:hover { background-color: #282D38; }
progressbar trough {
    background-color: #353B49;
    border-radius: 4px;
    min-height: 6px;
}
progressbar.md-progress-green progress {
    background-color: #E5E9F0;
    border-radius: 4px;
}
progressbar.md-progress-yellow progress {
    background-color: #E5E9F0;
    border-radius: 4px;
}
progressbar.md-progress-red progress {
    background-color: #E5E9F0;
    border-radius: 4px;
}
progressbar.md-progress-blue progress {
    background-color: #E5E9F0;
    border-radius: 4px;
}
scrollbar slider {
    background-color: #353B49;
    border-radius: 4px;
    min-width: 6px;
    min-height: 6px;
}
scrollbar slider:hover { background-color: #E5E9F0; }
combobox button {
    background-color: #1E222A;
    color: #E5E9F0;
    border: 1px solid #353B49;
    box-shadow: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
}
combobox button:hover { background-color: #282D38; }
.combo-popup, menu {
    background-color: #282D38;
    color: #E5E9F0;
    border: 1px solid #353B49;
    border-radius: 8px;
    padding: 4px 0;
}
menu > menuitem, .combo-popup > menuitem {
    background-color: transparent;
    color: #E5E9F0;
    padding: 8px 16px;
    font-size: 12px;
}
menu > menuitem:hover, .combo-popup > menuitem:hover {
    background-color: #353B49;
}
menu > menuitem:selected, .combo-popup > menuitem:selected {
    background-color: #353B49;
    color: #E5E9F0;
}
.md-statusbar {
    background-color: #1E222A;
    border-top: 1px solid #353B49;
    padding: 4px 16px;
    font-size: 11px;
    color: #E5E9F0;
}
dialog, dialog > box, dialog > box > box {
    background-color: #282D38;
    color: #E5E9F0;
}
dialog .dialog-action-area {
    background-color: #282D38;
    padding: 8px 16px 16px;
    border-top: 1px solid #353B49;
}
entry {
    background-color: #282D38;
    color: #E5E9F0;
    border: 1px solid #353B49;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    caret-color: #E5E9F0;
}
entry:focus {
    border-color: #E5E9F0;
    outline: none;
}
spinner { color: #E5E9F0; }
.md-table-header {
    background-color: #282D38;
    border-bottom: 1px solid #353B49;
    padding: 8px 16px;
}
.md-table-cell-bad {
    background-color: #353B49;
}

"""

def find_block_devices():
    devs = []
    try:
        out = subprocess.check_output(
            ["lsblk", "-o", "NAME,TYPE", "--json"],
            stderr=subprocess.DEVNULL, text=True)
        for dev in json.loads(out).get("blockdevices", []):
            if dev.get("type") == "disk":
                devs.append(f"/dev/{dev['name']}")
    except Exception:
        for p in sorted(Path("/dev").iterdir()):
            if re.match(r"^(sd[a-z]|nvme\d+n\d+|hd[a-z]|vd[a-z])$", p.name):
                devs.append(str(p))
    return devs or ["/dev/sda"]

def run_smartctl(device, password=None):
    def _try(cmd, inp=None):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15, input=inp)
        try:
            data = json.loads(r.stdout) if r.stdout.strip() else None
        except json.JSONDecodeError:
            data = None
        return data, r.returncode

    def _ok(data, code):
        return data is not None and "device" in data and not (code & 0x02)

    base = ["smartctl", "-ax", device, "--json=o"]
    try:
        data, code = _try(base)
        if _ok(data, code):
            return data, code
    except FileNotFoundError:
        return {"_error": "smartctl not found.\n  sudo pls get smartmon"}, -1           
    except subprocess.TimeoutExpired:
        return {"_error": f"Timeout reading {device}"}, -1

    try:
        data, code = _try(["sudo", "-n"] + base)
        if _ok(data, code):
            return data, code
    except Exception:
        pass

    if password:
        try:
            su_cmd = ["su", "-c", " ".join(base), "root"]
            data, code = _try(su_cmd, inp=password + "\n")
            if _ok(data, code):
                return data, code
            return {"_error": "_bad_password"}, -1
        except subprocess.TimeoutExpired:
            return {"_error": f"Timeout reading {device}"}, -1

    return {"_error": "_needs_password"}, -1

def fmt_bytes(b, d=1):
    if b is None: return "-"
    for u in ("B","KiB","MiB","GiB","TiB","PiB"):
        if abs(b) < 1024: return f"{b:.{d}f} {u}"
        b /= 1024
    return f"{b:.{d}f} EiB"

def fmt_hours(h):
    if h is None: return "-"
    d = h // 24
    if d > 365: return f"{d//365}y {(d%365)//30}mo"
    if d > 30:  return f"{d//30}mo {d%30}d"
    if d > 0:   return f"{d}d {h%24}h"
    return f"{h}h"

def fmt_int(v):
    if v is None: return "-"
    return f"{v:,}"
# this was hell
def extract(data):
    d = {}
    if not data or "_error" in data:
        d["_error"] = data.get("_error", "No data") if data else "No data"
        return d
    dev = data.get("device", {})
    d["protocol"]      = dev.get("protocol", "Unknown")
    d["model"]         = data.get("model_name", data.get("scsi_model_name", "Unknown"))
    d["family"]        = data.get("model_family", "")
    d["serial"]        = data.get("serial_number", "-")
    d["firmware"]      = data.get("firmware_version", "-")
    cap                = data.get("user_capacity", {})
    d["capacity_bytes"]= cap.get("bytes")
    d["capacity_str"]  = fmt_bytes(d["capacity_bytes"])
    rot                = data.get("rotation_rate")
    d["is_ssd"]        = (rot is not None and rot == 0) or d["protocol"] == "NVMe"
    if d["protocol"] == "NVMe":
        d["rotation"] = "NVMe"
    elif d["is_ssd"]:
        d["rotation"] = "SSD"
    else:
        d["rotation"] = f"{rot} RPM" if rot else "-"
    d["form_factor"]   = data.get("form_factor", {}).get("name", "-")
    ss                 = data.get("smart_status", {})
    d["passed"]        = ss.get("passed")
    t                  = data.get("temperature", {})
    d["temp"]          = t.get("current")
    d["temp_trip"]     = t.get("op_limit_max")
    d["power_hours"]   = data.get("power_on_time", {}).get("hours")
    d["power_cycles"]  = data.get("power_cycle_count")

    d["temp_lifetime_min"]    = t.get("lifetime_min")
    d["temp_lifetime_max"]    = t.get("lifetime_max")
    d["temp_cycle_min"]       = t.get("power_cycle_min")
    d["temp_cycle_max"]       = t.get("power_cycle_max")
    sct_status_temp = data.get("ata_sct_status", {}).get("temperature", {})
    d["temp_over_limit_count"] = sct_status_temp.get("over_limit_count") or t.get("lifetime_over_limit_minutes")
    d["temp_critical_limit"]  = t.get("critical_limit_max")                 

    nvme = data.get("nvme_smart_health_information_log", {})
    if nvme:
        d["nvme_pct_used"]          = nvme.get("percentage_used")
        d["nvme_avail_spare"]       = nvme.get("available_spare")
        d["nvme_avail_spare_thr"]   = nvme.get("available_spare_threshold", 5)
        d["nvme_data_read"]         = nvme.get("data_units_read")
        d["nvme_data_written"]      = nvme.get("data_units_written")
        d["nvme_host_reads"]        = nvme.get("host_reads")
        d["nvme_host_writes"]       = nvme.get("host_writes")
        d["nvme_ctrl_busy"]         = nvme.get("controller_busy_time")
        d["nvme_unsafe_shutdowns"]  = nvme.get("unsafe_shutdowns")
        d["nvme_media_errors"]      = nvme.get("media_errors")
        d["nvme_err_log"]           = nvme.get("num_err_log_entries")
        d["nvme_warn_temp_time"]    = nvme.get("warning_temp_time")
        d["nvme_crit_temp_time"]    = nvme.get("critical_comp_time")
        def u2tb(u): return (u * 512000) / (1024**4) if u else None
        d["data_read_tb"]    = u2tb(d.get("nvme_data_read"))
        d["data_written_tb"] = u2tb(d.get("nvme_data_written"))
        pct = d.get("nvme_pct_used")
        wtb = d.get("data_written_tb")
        if pct and pct > 0 and wtb:
            d["tbw_pct_used"]  = float(pct)
        elif pct is not None:
            d["tbw_pct_used"]  = float(pct)

        cw = nvme.get("critical_warning", 0)
        if cw:
            bits = []
            if cw & 0x01: bits.append("Available spare below threshold")
            if cw & 0x02: bits.append("Temperature above threshold")
            if cw & 0x04: bits.append("NVM subsystem degraded (read-only)")
            if cw & 0x08: bits.append("Volatile memory backup failed")
            if cw & 0x10: bits.append("PMR persistent memory region unreliable")
            d["nvme_critical_warning_bits"] = bits
        d["nvme_critical_warning"] = cw

        ctt = data.get("nvme_composite_temperature_threshold", {})
        d["nvme_temp_warn_threshold"]  = ctt.get("warning")
        d["nvme_temp_crit_threshold"]  = ctt.get("critical")

        ns_list = data.get("nvme_namespaces", [])
        if ns_list:
            ns = ns_list[0]
            util = ns.get("utilization", {})
            cap  = ns.get("capacity", {})
            util_bytes = util.get("bytes")
            cap_bytes  = cap.get("bytes")
            d["nvme_ns_used_bytes"]  = util_bytes
            d["nvme_ns_cap_bytes"]   = cap_bytes
            if util_bytes is not None and cap_bytes:
                d["nvme_ns_used_frac"] = util_bytes / cap_bytes

        stl = data.get("nvme_self_test_log", {})
        table = stl.get("table", [])
        if table:
            last = table[0]
            d["self_test_last_type"]   = last.get("self_test_code", {}).get("string")
            d["self_test_last_result"] = last.get("self_test_result", {}).get("string")
            d["self_test_last_passed"] = last.get("self_test_result", {}).get("passed", False) if "self_test_result" in last else None
            d["self_test_last_hours"]  = last.get("power_on_hours")
            d["self_test_log"]         = table

        d["error_count"] = nvme.get("media_errors", 0)

        eu = data.get("endurance_used", {})
        if eu.get("current_percent") is not None:
            d["endurance_used_pct"] = eu["current_percent"]
        sa = data.get("spare_available", {})
        if sa.get("current_percent") is not None:
            d["spare_available_pct"] = sa["current_percent"]
            d["spare_threshold_pct"] = sa.get("threshold_percent", 5)

        nv = data.get("nvme_version", {})
        if nv.get("string"):
            d["nvme_version"] = nv["string"]

    attrs = data.get("ata_smart_attributes", {}).get("table", [])
    d["ata_attrs"] = attrs
    am = {a["id"]: a for a in attrs}
    def rv(i): return am.get(i, {}).get("raw", {}).get("value")
    def rv_str(i):
        a = am.get(i, {}).get("raw", {})
        s = a.get("string")
        return s if s else a.get("value")
    if attrs and not nvme:
        d["ata_reallocated"]   = rv(5)
        d["ata_pending"]       = rv(197)
        d["ata_uncorrectable"] = rv(198)
        lbaw = rv(241); lbar = rv(242)
        def l2tb(l): return (l * 512) / (1024**4) if l else None
        d["data_written_tb"] = l2tb(lbaw)
        d["data_read_tb"]    = l2tb(lbar)
        wear = rv(177) or rv(173)
        life = rv(231) or rv(233)
        if wear is not None or life is not None:
            d["ata_wear"] = wear
            d["ata_life"] = life
            pct = wear if wear is not None else (100 - life if life is not None else None)
            if pct is not None:
                d["tbw_pct_used"] = float(pct)

        d["error_count"] = data.get("ata_smart_error_log", {}).get("extended", {}).get("count", 0)

        stl = data.get("ata_smart_self_test_log", {})
        table = stl.get("extended", {}).get("table") or stl.get("standard", {}).get("table", [])
        if table:
            last = table[0]
            d["self_test_last_type"]   = last.get("type", {}).get("string")
            d["self_test_last_result"] = last.get("status", {}).get("string")
            d["self_test_last_passed"] = last.get("status", {}).get("passed")
            d["self_test_last_hours"]  = last.get("lifetime_hours")
            d["self_test_log"]         = table

        phy_table = data.get("sata_phy_event_counters", {}).get("table", [])
        if phy_table:
            d["sata_phy_counters"] = phy_table
            error_ids = {1, 3, 4, 5, 6, 7, 8}                        
            d["sata_phy_errors"] = any(
                e.get("value", 0) > 0 for e in phy_table
                if e.get("id") in error_ids
            )

        iface = data.get("interface_speed", {})
        max_s = iface.get("max", {}).get("string")
        cur_s = iface.get("current", {}).get("string")
        if max_s or cur_s:
            d["interface_max_speed"] = max_s
            d["interface_cur_speed"] = cur_s
            d["interface_negotiated_full"] = (max_s == cur_s) if (max_s and cur_s) else None
        sata_ver = data.get("sata_version", {})
        d["sata_version"] = sata_ver.get("string")

        for attr in attrs:
            raw = attr.get("raw", {})
            if raw.get("string") and raw.get("string") != str(raw.get("value", "")):
                raw["_display"] = raw["string"]
            else:
                raw["_display"] = str(raw.get("value", ""))

        dev_stats = data.get("ata_device_statistics", {})
        stat_map = {}                 
        for page in dev_stats.get("pages", []):
            for item in page.get("table", []):
                name = item.get("name")
                val  = item.get("value")
                if name and val is not None:
                    stat_map[name] = val
        if stat_map:
            d["stat_head_load_events"]     = stat_map.get("Head Load Events")
            d["stat_read_recovery"]        = stat_map.get("Read Recovery Attempts")
            d["stat_mech_start_failures"]  = stat_map.get("Number of Mechanical Start Failures")
            d["stat_time_over_temp"]       = stat_map.get("Time in Over-Temperature")
            d["stat_time_under_temp"]      = stat_map.get("Time in Under-Temperature")
            d["stat_highest_temp"]         = stat_map.get("Highest Temperature")
            d["stat_lowest_temp"]          = stat_map.get("Lowest Temperature")
            d["stat_avg_lt_temp"]          = stat_map.get("Average Long Term Temperature")
            d["stat_highest_avg_st_temp"]  = stat_map.get("Highest Average Short Term Temperature")
            d["stat_lowest_avg_st_temp"]   = stat_map.get("Lowest Average Short Term Temperature")
            d["stat_realloc_sectors"]      = stat_map.get("Number of Reallocated Logical Sectors")
            d["stat_uncorrectable"]        = stat_map.get("Number of Reported Uncorrectable Errors")
            d["stat_map"] = stat_map

        sct_hist = data.get("ata_sct_temperature_history", {})
        hist_table = sct_hist.get("table", [])
        if hist_table:
            d["sct_temp_history"] = hist_table
            d["sct_temp_interval_min"] = sct_hist.get("logging_interval_minutes", 30)

        sec = data.get("ata_security", {})
        if sec:
            d["ata_security_enabled"] = sec.get("enabled", False)
            d["ata_security_frozen"]  = sec.get("frozen", False)
            d["ata_security_string"]  = sec.get("string")
        wc = data.get("write_cache", {})
        if wc: d["write_cache_enabled"] = wc.get("enabled")
        rl = data.get("read_lookahead", {})
        if rl: d["read_lookahead_enabled"] = rl.get("enabled")
        trim = data.get("trim", {})
        if trim:
            d["trim_supported"]    = trim.get("supported")
            d["trim_deterministic"]= trim.get("deterministic")
            d["trim_zeroed"]       = trim.get("zeroed")
        apm = data.get("ata_apm", {})
        if apm:
            d["apm_enabled"] = apm.get("enabled")
            d["apm_level"]   = apm.get("level")
            d["apm_string"]  = apm.get("string")

        smart_data = data.get("ata_smart_data", {})
        polling = smart_data.get("self_test", {}).get("polling_minutes", {})
        if polling:
            d["selftest_short_minutes"]    = polling.get("short")
            d["selftest_extended_minutes"] = polling.get("extended")

        sct_erc = data.get("ata_sct_erc", {})
        if sct_erc:
            d["sct_erc_read_enabled"]  = sct_erc.get("read", {}).get("enabled")
            d["sct_erc_write_enabled"] = sct_erc.get("write", {}).get("enabled")

        sa = data.get("spare_available", {})
        if sa.get("current_percent") is not None:
            d["spare_available_pct"] = sa["current_percent"]
            d["spare_threshold_pct"] = sa.get("threshold_percent", 5)

        ata_ver = data.get("ata_version", {})
        if ata_ver.get("string"):
            d["ata_version"] = ata_ver["string"]

    nvme_err_log = data.get("nvme_error_information_log", {})
    err_table = nvme_err_log.get("table", [])
    if err_table:
        d["nvme_error_table"] = [
            {
                "count":  e.get("error_count"),
                "status": e.get("status_field", {}).get("string", "Unknown"),
                "do_not_retry": e.get("status_field", {}).get("do_not_retry", False),
            }
            for e in err_table
        ]

    return d

def lbl(text, css=None, xalign=0.0, wrap=False, selectable=False):
    w = Gtk.Label(label=str(text))
    w.set_xalign(xalign)
    if css:
        for c in css.split():
            w.get_style_context().add_class(c)
    if wrap:
        w.set_line_wrap(True)
        w.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
    if selectable:
        w.set_selectable(True)
    return w

def chip(text, style=""):
    b = Gtk.Label(label=text)
    b.get_style_context().add_class("md-chip")
    if style:
        b.get_style_context().add_class(f"md-chip-{style}")
    return b

def divider():
    s = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    s.get_style_context().add_class("md-divider")
    return s

def section_card(inner_widget, margin_h=16, margin_v=6):
    box = Gtk.Box()
    box.set_margin_start(margin_h)
    box.set_margin_end(margin_h)
    box.set_margin_top(margin_v)
    box.set_margin_bottom(margin_v)
    box.get_style_context().add_class("md-card")
    box.pack_start(inner_widget, True, True, 0)
    return box

def progress_bar(frac, style="blue"):
    pb = Gtk.ProgressBar()
    pb.set_fraction(min(1.0, max(0.0, frac or 0)))
    pb.get_style_context().add_class(f"md-progress-{style}")
    pb.set_show_text(False)
    return pb

def list_row(key_text, val_widget_or_text, icon=None):
    row = Gtk.Box(spacing=0, orientation=Gtk.Orientation.HORIZONTAL)
    row.get_style_context().add_class("md-list-row")
    left = Gtk.Box(spacing=8)
    if icon:
        left.pack_start(lbl(icon, "md-body-small"), False, False, 0)
    left.pack_start(lbl(key_text, "md-body-small"), False, False, 0)
    row.pack_start(left, True, True, 0)
    if isinstance(val_widget_or_text, str):
        v = lbl(val_widget_or_text, "md-mono", xalign=1.0)
    else:
        v = val_widget_or_text
    row.pack_end(v, False, False, 0)
    return row

def card_section_header(title):
    box = Gtk.Box()
    box.set_margin_start(16)
    box.set_margin_end(16)
    box.set_margin_top(16)
    box.set_margin_bottom(4)
    box.pack_start(lbl(title, "md-label-large"), False, False, 0)
    return box

class CircularGauge(Gtk.DrawingArea):
    def __init__(self, size=96, track_w=7):
        super().__init__()
        self.set_size_request(size, size)
        self._size    = size
        self._track_w = track_w
        self._frac    = 0.0
        self._label   = ""
        self._sublbl  = ""
        self._color   = (0.816, 0.737, 1.0) 
        self._track   = (0.286, 0.271, 0.310)
        self.connect("draw", self._draw)

    def set_value(self, frac, label, sublabel="", color=None):
        self._frac   = min(1.0, max(0.0, frac or 0))
        self._label  = label
        self._sublbl = sublabel
        if color: self._color = color
        self.queue_draw()

    def _draw(self, widget, cr):
        s  = self._size
        cx = cy = s / 2
        r  = (s - self._track_w * 2) / 2 - 2
        cr.set_line_width(self._track_w)
        cr.set_source_rgb(*self._track)
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.stroke()
        if self._frac > 0:
            cr.set_source_rgb(*self._color)
            cr.arc(cx, cy, r, -math.pi/2, -math.pi/2 + 2*math.pi*self._frac)
            cr.stroke()
        layout = self.create_pango_layout(self._label)
        fd = Pango.FontDescription("FiraCode 13")
        fd.set_weight(Pango.Weight.MEDIUM)
        layout.set_font_description(fd)
        lw, lh = layout.get_pixel_size()
        cr.set_source_rgb(0.902, 0.878, 0.914)
        cr.move_to(cx - lw/2, cy - lh/2 - (6 if self._sublbl else 0))
        PangoCairo.show_layout(cr, layout)
        if self._sublbl:
            sl = self.create_pango_layout(self._sublbl)
            sf = Pango.FontDescription("FiraCode 9")
            sl.set_font_description(sf)
            sw, sh = sl.get_pixel_size()
            cr.set_source_rgb(0.792, 0.769, 0.816)
            cr.move_to(cx - sw/2, cy + lh/2 - 4)
            PangoCairo.show_layout(cr, sl)

class _TempHistoryChart(Gtk.DrawingArea):
    def __init__(self, temps, height=80):
        super().__init__()
        self._temps = [t for t in temps if isinstance(t, (int, float))]
        self.set_size_request(-1, height)
        self.connect("draw", self._draw)

    def _draw(self, widget, cr):
        if not self._temps: return
        alloc = widget.get_allocation()
        w, h = alloc.width, alloc.height
        pad = 4
        mn = min(self._temps); mx = max(self._temps)
        rng = max(mx - mn, 1)

        def yx(i, t):
            x = pad + (i / max(len(self._temps) - 1, 1)) * (w - pad * 2)
            y = h - pad - ((t - mn) / rng) * (h - pad * 2)
            return x, y

        cr.set_source_rgba(0.420, 0.831, 0.627, 0.12)
        cr.move_to(*yx(0, self._temps[0]))
        for i, t in enumerate(self._temps[1:], 1):
            cr.line_to(*yx(i, t))
        x_last, y_last = yx(len(self._temps) - 1, self._temps[-1])
        cr.line_to(x_last, h - pad)
        cr.line_to(pad, h - pad)
        cr.close_path(); cr.fill()

        cr.set_source_rgb(0.420, 0.831, 0.627)
        cr.set_line_width(1.5)
        cr.move_to(*yx(0, self._temps[0]))
        for i, t in enumerate(self._temps[1:], 1):
            cr.line_to(*yx(i, t))
        cr.stroke()

        def draw_label(text, x, y):
            layout = widget.create_pango_layout(text)
            layout.set_font_description(Pango.FontDescription("FiraCode 8"))
            lw, lh = layout.get_pixel_size()
            cr.set_source_rgb(0.792, 0.769, 0.816)
            cr.move_to(max(0, min(x - lw/2, w - lw)), y)
            PangoCairo.show_layout(cr, layout)

        mx_i = self._temps.index(mx)
        mn_i = self._temps.index(mn)
        hx, hy = yx(mx_i, mx)
        lx, ly = yx(mn_i, mn)
        draw_label(f"{mx}°C", hx, hy - 12)
        draw_label(f"{mn}°C", lx, ly + 2)

class ContentBuilder:
    def build(self, d, win=None):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        if "_error" in d:
            outer.pack_start(self._error_card(d["_error"]), False, False, 16)
            return outer
        outer.pack_start(self._hero_card(d),      False, False, 0)
        outer.pack_start(self._gauge_row(d),      False, False, 0)
        outer.pack_start(self._identity_card(d),  False, False, 0)
        outer.pack_start(self._endurance_card(d), False, False, 0)
        if d.get("nvme_critical_warning"):
            outer.pack_start(self._nvme_warning_card(d), False, False, 0)
        if d.get("nvme_media_errors") is not None or d.get("nvme_err_log") is not None:
            outer.pack_start(self._nvme_health_card(d), False, False, 0)
        if d.get("nvme_error_table"):
            outer.pack_start(self._nvme_error_table_card(d), False, False, 0)
        if d.get("self_test_log"):
            outer.pack_start(self._self_test_card(d, win), False, False, 0)
        if d.get("sct_temp_history"):
            outer.pack_start(self._sct_temp_chart_card(d), False, False, 0)
        if d.get("sata_phy_counters"):
            outer.pack_start(self._phy_counters_card(d), False, False, 0)
        if d.get("stat_map"):
            outer.pack_start(self._ata_device_stats_card(d), False, False, 0)
        if any(d.get(k) is not None for k in ("write_cache_enabled","trim_supported","apm_enabled","ata_security_string")):
            outer.pack_start(self._ata_features_card(d), False, False, 0)
        if d.get("ata_attrs"):
            outer.pack_start(self._ata_card(d), False, False, 0)
        outer.pack_start(Gtk.Box(), False, False, 16)
        return outer

    def _error_card(self, msg):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.get_style_context().add_class("md-card-outlined")
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(16);   box.set_margin_bottom(8)
        box.set_border_width(16)
        box.pack_start(lbl("  Permission error", "md-body", wrap=False), False, False, 0)
        for line in msg.strip().split("\n"):
            box.pack_start(lbl(line, "md-mono-small", wrap=True), False, False, 0)
        return box

    def _hero_card(self, d):
        passed  = d.get("passed")
        proto   = d.get("protocol", "")
        is_nvme = "nvme" in proto.lower()

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        outer.get_style_context().add_class("md-card")
        outer.set_margin_start(16); outer.set_margin_end(16)
        outer.set_margin_top(16);   outer.set_margin_bottom(4)

        inner = Gtk.Box(spacing=12)
        inner.set_border_width(20)

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left.pack_start(lbl(d.get("model","Unknown"), "md-headline"), False, False, 0)
        if d.get("family"):
            left.pack_start(lbl(d["family"], "md-body-small"), False, False, 0)

        badges = Gtk.Box(spacing=8)
        badges.set_margin_top(6)
        proto_style = "primary" if is_nvme else "blue"
        badges.pack_start(chip(proto, proto_style), False, False, 0)
        if d.get("is_ssd"):
            badges.pack_start(chip("SSD", "blue"), False, False, 0)
        badges.pack_start(chip(d.get("capacity_str","-")), False, False, 0)
        left.pack_start(badges, False, False, 0)
        inner.pack_start(left, True, True, 0)

        if passed is True:
            health_chip = chip("  PASSED", "green")
        elif passed is False:
            health_chip = chip("  FAILED", "red")
        else:
            health_chip = chip("  UNKNOWN")
        right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        right.set_valign(Gtk.Align.CENTER)
        right.set_halign(Gtk.Align.END)
        right.pack_start(health_chip, False, False, 0)
        err = d.get("error_count")
        if err is not None and err > 0:
            right.pack_start(chip(f" {fmt_int(err)} errors", "red"), False, False, 0)
        elif err == 0:
            right.pack_start(chip("0 errors", "green"), False, False, 0)
        inner.pack_end(right, False, False, 0)

        outer.pack_start(inner, False, False, 0)
        return outer

    def _gauge_row(self, d):
        temp      = d.get("temp") or 0
        hours     = d.get("power_hours") or 0
        cycles    = d.get("power_cycles") or 0
        pct_used  = d.get("nvme_pct_used") or d.get("tbw_pct_used") or 0

        row = Gtk.Box(spacing=8, homogeneous=True)
        row.set_margin_start(16); row.set_margin_end(16)
        row.set_margin_top(4);    row.set_margin_bottom(4)

        def gauge_card(gauge, title, sub):
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            card.get_style_context().add_class("md-card")
            card.set_border_width(20)
            g_box = Gtk.Box(); g_box.set_halign(Gtk.Align.CENTER)
            g_box.set_margin_top(4); g_box.set_margin_bottom(4)
            g_box.pack_start(gauge, False, False, 0)
            card.pack_start(g_box, False, False, 0)
            card.pack_start(lbl(title, "md-label-large", xalign=0.5), False, False, 0)
            if sub:
                sl = lbl(sub, "md-body-small", xalign=0.5)
                sl.set_margin_bottom(15)
                card.pack_start(sl, False, False, 0)
            return card

        t_frac  = temp / 70
        t_col   = (0.420,0.831,0.627) if temp < 40 else ((0.941,0.800,0.431) if temp < 55 else (1,0.702,0.729))
        g_temp  = CircularGauge(116)
        temp_sub = ""
        lt_min = d.get("temp_lifetime_min"); lt_max = d.get("temp_lifetime_max")
        if lt_min is not None and lt_max is not None:
            temp_sub = f"lifetime {lt_min}-{lt_max}°C"
        elif d.get("temp_trip"):
            temp_sub = f"trip {d.get('temp_trip')}°C"
        g_temp.set_value(t_frac, f"{temp}°C", "TEMP", t_col)
        row.pack_start(gauge_card(g_temp, "Temperature", temp_sub or None), True, True, 0)

        if pct_used > 0 or d.get("nvme_pct_used") is not None or d.get("tbw_pct_used") is not None:
            e_col = (0.420,0.831,0.627) if pct_used < 50 else ((0.941,0.800,0.431) if pct_used < 80 else (1,0.702,0.729))
            g_end  = CircularGauge(116)
            g_end.set_value(pct_used/100, f"{pct_used:.0f}%", "USED", e_col)
            row.pack_start(gauge_card(g_end, "Endurance Used", None), True, True, 0)

        g_hrs  = CircularGauge(116)
        g_hrs.set_value(min(hours/50000, 1.0), fmt_hours(hours), "UPTIME")
        row.pack_start(gauge_card(g_hrs, "Power-On Time", f"{hours:,} hours" if hours else None), True, True, 0)

        g_cyc  = CircularGauge(116)
        g_cyc.set_value(min((cycles or 0)/100000, 1.0), fmt_int(cycles), "CYCLES")
        row.pack_start(gauge_card(g_cyc, "Power Cycles", None), True, True, 0)

        return row

    def _identity_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")

        box.pack_start(self._card_header("Device Identity"), False, False, 0)
        box.pack_start(divider(), False, False, 0)

        for key, val in [
            ("Serial number",  d.get("serial","-")),
            ("Firmware",       d.get("firmware","-")),
            ("Interface",      d.get("rotation","-")),
            ("Form factor",    d.get("form_factor","-")),
            ("Protocol",       d.get("protocol","-")),
        ]:
            box.pack_start(list_row(key, val), False, False, 0)

        if d.get("sata_version"):
            box.pack_start(list_row("SATA version", d["sata_version"]), False, False, 0)
        if d.get("interface_max_speed") and d.get("interface_cur_speed"):
            speed_str = d["interface_cur_speed"]
            if d.get("interface_negotiated_full") is False:
                speed_str += f"  (max: {d['interface_max_speed']})"
            vw = chip(speed_str, "green" if d.get("interface_negotiated_full") else "yellow")
            box.pack_start(list_row("Link speed", vw), False, False, 0)

        return box

    def _endurance_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")

        box.pack_start(self._card_header("Endurance & Lifetime"), False, False, 0)
        box.pack_start(divider(), False, False, 0)

        has_content = False

        pct_used    = d.get("nvme_pct_used") or d.get("tbw_pct_used")
        avail_spare = d.get("nvme_avail_spare")
        spare_thr   = d.get("nvme_avail_spare_thr", 5)
        written_tb  = d.get("data_written_tb")
        read_tb     = d.get("data_read_tb")
        hrs_used    = d.get("power_hours")

        def bar_row(label, frac, val_str, style):
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            row.set_margin_start(16); row.set_margin_end(16)
            row.set_margin_top(10);   row.set_margin_bottom(2)
            head = Gtk.Box()
            head.pack_start(lbl(label, "md-body-small"), True, True, 0)
            head.pack_end(lbl(val_str, "md-mono", xalign=1.0), False, False, 0)
            row.pack_start(head, False, False, 0)
            row.pack_start(progress_bar(frac, style), False, False, 0)
            return row

        if pct_used is not None:
            style = "red" if pct_used > 80 else ("yellow" if pct_used > 50 else "green")
            box.pack_start(bar_row("Endurance used", pct_used/100, f"{pct_used:.0f}%", style), False, False, 0)
            has_content = True

        ns_frac = d.get("nvme_ns_used_frac")
        if ns_frac is not None:
            used_str = fmt_bytes(d.get("nvme_ns_used_bytes")) + " used"
            cap_str  = fmt_bytes(d.get("nvme_ns_cap_bytes"))
            ns_style = "red" if ns_frac > 0.9 else ("yellow" if ns_frac > 0.75 else "blue")
            box.pack_start(bar_row(f"Namespace fill  (of {cap_str})", ns_frac, used_str, ns_style), False, False, 0)
            has_content = True

        if written_tb is not None:
            frac = (pct_used / 100) if pct_used is not None else 0
            style = "red" if frac > 0.8 else ("yellow" if frac > 0.5 else "blue")
            box.pack_start(bar_row("Total written", frac, f"{written_tb:.2f} TB", style), False, False, 0)

        if has_content:
            box.pack_start(Gtk.Box(), False, False, 6)
            box.pack_start(divider(), False, False, 0)

        kv_items = []
        if avail_spare is not None:
            spare_style = "red" if avail_spare <= spare_thr else ("yellow" if avail_spare <= spare_thr*2 else "green")
            kv_items.append((f"Available spare  (min {spare_thr}%)", f"{avail_spare}%", spare_style))
        if read_tb is not None:
            kv_items.append(("Total read", f"{read_tb:.2f} TB", None))
        if hrs_used:
            kv_items.append(("Hours used", fmt_hours(hrs_used), None))

        for key, val, col in kv_items:
            vw = chip(val, col) if col else lbl(val, "md-mono", xalign=1.0)
            box.pack_start(list_row(key, vw), False, False, 0)

        if not has_content and not kv_items:
            box.pack_start(lbl("No endurance data available.", "md-body-small",
                               xalign=0.5), False, False, 12)

        return box

    def _nvme_health_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header("NVMe Health Log"), False, False, 0)
        box.pack_start(divider(), False, False, 0)
        def fmt_minutes(m):
            if m is None: return "-"
            if m == 0: return "0"
            h = m // 60; mins = m % 60
            if h == 0: return f"{mins}m"
            return f"{h}h {mins}m" if mins else f"{h}h"

        rows = [
            ("Media / ECC errors",    d.get("nvme_media_errors"),     True,  fmt_int),
            ("Error log entries",     d.get("nvme_err_log"),          False, fmt_int),                           
            ("Unsafe shutdowns",      d.get("nvme_unsafe_shutdowns"), False, fmt_int),
            ("Host reads",            d.get("nvme_host_reads"),       False, fmt_int),
            ("Host writes",           d.get("nvme_host_writes"),      False, fmt_int),
            ("Controller busy time",  d.get("nvme_ctrl_busy"),        False, fmt_minutes),
            ("Warning temp time",     d.get("nvme_warn_temp_time"),   True,  fmt_minutes),
            ("Critical temp time",    d.get("nvme_crit_temp_time"),   True,  fmt_minutes),
        ]
        for key, val, is_error, fmt in rows:
            if val is None: continue
            col = "red" if (is_error and val > 0) else None
            vw  = chip(fmt(val), "red") if (col and val > 0) else lbl(fmt(val), "md-mono", xalign=1.0)
            box.pack_start(list_row(key, vw), False, False, 0)

        warn_thr = d.get("nvme_temp_warn_threshold")
        crit_thr = d.get("nvme_temp_crit_threshold")
        if warn_thr or crit_thr:
            box.pack_start(divider(), False, False, 0)
            if warn_thr:
                box.pack_start(list_row("Temp warning threshold", f"{warn_thr}°C"), False, False, 0)
            if crit_thr:
                box.pack_start(list_row("Temp critical threshold", f"{crit_thr}°C"), False, False, 0)

        if d.get("nvme_err_log") and d.get("nvme_err_log", 0) > 0 and not d.get("nvme_media_errors"):
            note = lbl("Note: error log entries are often routine command completions, not drive failures.",
                       "md-body-small", wrap=True)
            note.set_margin_start(16); note.set_margin_end(16)
            note.set_margin_top(8); note.set_margin_bottom(8)
            box.pack_start(note, False, False, 0)
        return box

    def _ata_card(self, d):
        attrs = d.get("ata_attrs", [])
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header("ATA SMART Attributes"), False, False, 0)

        hrow = Gtk.Box(spacing=0)
        hrow.get_style_context().add_class("md-table-header")
        for text, expand, width in [
            ("ID", False, 36), ("Attribute", True, -1),
            ("Val", False, 44), ("Worst", False, 44),
            ("Thr", False, 44), ("Raw", False, 90),
        ]:
            h = lbl(text, "md-label-large")
            if width > 0: h.set_size_request(width, -1)
            hrow.pack_start(h, expand, expand, 8)
        box.pack_start(hrow, False, False, 0)

        for attr in attrs:
            aid    = str(attr.get("id",""))
            name   = attr.get("name","").replace("_"," ")
            val    = attr.get("value","")
            worst  = attr.get("worst","")
            thresh = attr.get("thresh","")
            raw    = attr.get("raw",{}).get("_display") or str(attr.get("raw",{}).get("value",""))
            try:
                is_bad = isinstance(val,int) and isinstance(thresh,int) and thresh > 0 and val <= thresh
            except Exception:
                is_bad = False

            row = Gtk.Box(spacing=0)
            row.get_style_context().add_class("md-list-row")
            if is_bad:
                row.get_style_context().add_class("md-table-cell-bad")

            for text, expand, width, css in [
                (aid,      False, 36,  "md-mono-small"),
                (name,     True,  -1,  "md-body-small"),
                (str(val), False, 44,  "md-chip-red md-mono" if is_bad else "md-mono"),
                (str(worst),False,44,  "md-mono-small"),
                (str(thresh),False,44, "md-mono-small"),
                (str(raw), False, 90,  "md-mono-small"),
            ]:
                c = lbl(text, css)
                if width > 0: c.set_size_request(width, -1)
                row.pack_start(c, expand, expand, 8)
            box.pack_start(row, False, False, 0)

        return box

    def _nvme_warning_card(self, d):
        bits = d.get("nvme_critical_warning_bits", [])
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header(" NVMe Critical Warning"), False, False, 0)
        box.pack_start(divider(), False, False, 0)
        for b in bits:
            vw = chip("ACTIVE", "red")
            box.pack_start(list_row(b, vw), False, False, 0)
        if not bits:
            box.pack_start(lbl("No active warnings.", "md-body-small", xalign=0.5), False, False, 12)
        return box

    def _self_test_card(self, d, win=None):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")

        hdr = Gtk.Box(spacing=8)
        hdr.set_border_width(16)
        hdr.pack_start(lbl("Self-Test Log", "md-label-large"), True, True, 0)
        run_btn = Gtk.Button(label="  Run Short Test")
        run_btn.get_style_context().add_class("md-btn-outlined")
        if win and d.get("_device") in win._running_tests:
            pct = win._running_tests[d["_device"]]
            label = f"Running... ({pct}% left)" if pct is not None else "Running..."
            run_btn.set_label(label)
            run_btn.set_sensitive(False)
        run_btn.connect("clicked", lambda _: self._run_self_test(d.get("_device",""), run_btn, win))
        hdr.pack_end(run_btn, False, False, 0)
        box.pack_start(hdr, False, False, 0)
        box.pack_start(divider(), False, False, 0)

        hours_now = d.get("power_hours") or 0
        table = d.get("self_test_log", [])
        for entry in table[:5]:
            t_type   = entry.get("type", entry.get("self_test_code", {})).get("string", "-")
            t_result = entry.get("status", entry.get("self_test_result", {})).get("string", "-")
            t_passed = entry.get("status", entry.get("self_test_result", {})).get("passed")
            t_hours  = entry.get("lifetime_hours") or entry.get("power_on_hours")

            ago = ""
            if t_hours is not None and hours_now:
                diff = hours_now - t_hours
                ago = f"  ({fmt_hours(diff)} ago)"

            result_chip = chip(t_result, "green" if t_passed else ("red" if t_passed is False else ""))
            row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            row.get_style_context().add_class("md-list-row")
            top = Gtk.Box()
            top.pack_start(lbl(t_type, "md-body-small"), True, True, 0)
            top.pack_end(result_chip, False, False, 0)
            row.pack_start(top, False, False, 0)
            if t_hours is not None:
                row.pack_start(lbl(f"{t_hours:,} hours{ago}", "md-mono-small"), False, False, 0)
            box.pack_start(row, False, False, 0)
        return box

    def _run_self_test(self, device, btn, win, mins=2):
        if not device: return
        btn.set_sensitive(False)
        btn.set_label(f"Running... (~{mins}min)")
        if win:
            win._running_tests[device] = None                       
        password = win._sudo_password if win else None

        def _ok(stdout):
            low = stdout.lower()
            return "has begun" in low or "in progress" in low or "already in progress" in low

        def _do():
            import time
            cmd = ["smartctl", "-t", "short", device]
            success = False
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if r.returncode == 0 or _ok(r.stdout):
                    success = True
            except Exception:
                pass
            if not success:
                try:
                    r = subprocess.run(["sudo", "-n"] + cmd, capture_output=True, text=True, timeout=15)
                    if r.returncode == 0 or _ok(r.stdout):
                        success = True
                except Exception:
                    pass
            if not success and password:
                try:
                    r = subprocess.run(["su", "-c", " ".join(cmd), "root"],
                                       input=password + "\n", capture_output=True, text=True, timeout=15)
                    if r.returncode == 0 or _ok(r.stdout):
                        success = True
                except Exception:
                    pass

            if success:
                pcmd = ["smartctl", "-c", "--json=o", device]
                until = time.time() + (mins + 1) * 60
                while time.time() < until:
                    time.sleep(20)
                    cmds = [pcmd, ["sudo", "-n"] + pcmd]
                    if password:
                        cmds.append(["su", "-c", " ".join(pcmd), "root"])
                    for cmd in cmds:
                        try:
                            inp = (password + "\n") if cmd[0] == "su" else None
                            pr = subprocess.run(cmd, input=inp,
                                                capture_output=True, text=True, timeout=15)
                            pdata = json.loads(pr.stdout) if pr.stdout.strip() else {}
                            pct = pdata.get("self_test_execution", {}).get("remaining_percent")
                            if pct is not None:
                                if win:
                                    win._running_tests[device] = pct
                                GLib.idle_add(btn.set_label, f"Runnin... ({pct}% left)")
                                if pct == 0:
                                    until = 0                        
                                break
                        except Exception:
                            pass

            def _done():
                if win:
                    win._running_tests.pop(device, None)
                btn.set_label(" Run Short Test")
                btn.set_sensitive(True)
                if success and win:
                    idx = win.combo.get_active()
                    if 0 <= idx < len(win._devices) and win._devices[idx] == device:
                        win._load_data()
            GLib.idle_add(_done)
        threading.Thread(target=_do, daemon=True).start()

    def _nvme_error_table_card(self, d):
        table = d.get("nvme_error_table", [])
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header("NVMe Error Log Detail"), False, False, 0)
        box.pack_start(divider(), False, False, 0)
        for e in table:
            status = e.get("status", "Unknown")
            count  = e.get("count")
            dnr    = e.get("do_not_retry", False)
            benign = not dnr
            vw = chip(status, "" if benign else "red")
            label = f"{fmt_int(count)} occurrence{'s' if (count or 0) != 1 else ''}"
            if benign:
                label += "  (benign)"
            box.pack_start(list_row(label, vw), False, False, 0)
        note = lbl("'Invalid Field in Command' errors are typically benign ATA passthrough probes by the OS.",
                   "md-body-small", wrap=True)
        note.set_margin_start(16); note.set_margin_end(16)
        note.set_margin_top(8); note.set_margin_bottom(10)
        box.pack_start(note, False, False, 0)
        return box

    def _sct_temp_chart_card(self, d):
        hist   = d.get("sct_temp_history", [])
        interv = d.get("sct_temp_interval_min", 30)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header(f"Temperature History  ({interv}min intervals)"), False, False, 0)
        box.pack_start(divider(), False, False, 0)

        chart = _TempHistoryChart(hist)
        chart.set_margin_start(16); chart.set_margin_end(16)
        chart.set_margin_top(8);   chart.set_margin_bottom(12)
        box.pack_start(chart, False, False, 0)
        return box

    def _ata_device_stats_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header("ATA Device Statistics"), False, False, 0)
        box.pack_start(divider(), False, False, 0)

        rows = [
            ("Head load events",      d.get("stat_head_load_events"),    False),
            ("Read recovery attempts",d.get("stat_read_recovery"),       True),
            ("Mech. start failures",  d.get("stat_mech_start_failures"), True),
            ("Reallocated sectors",   d.get("stat_realloc_sectors"),     True),
            ("Uncorrectable errors",  d.get("stat_uncorrectable"),       True),
            ("Time over-temp (min)",  d.get("stat_time_over_temp"),      True),
            ("Time under-temp (min)", d.get("stat_time_under_temp"),     False),
            ("Highest temp ever",     d.get("stat_highest_temp") and f"{d['stat_highest_temp']}°C", False),
            ("Lowest temp ever",      d.get("stat_lowest_temp") and f"{d['stat_lowest_temp']}°C", False),
            ("Avg long-term temp",    d.get("stat_avg_lt_temp") and f"{d['stat_avg_lt_temp']}°C", False),
        ]
        has_any = False
        for key, val, is_error in rows:
            if val is None: continue
            has_any = True
            val_str = str(val) if isinstance(val, str) else fmt_int(val)
            vw = chip(val_str, "red") if (is_error and isinstance(val, int) and val > 0) else lbl(val_str, "md-mono", xalign=1.0)
            box.pack_start(list_row(key, vw), False, False, 0)
        if not has_any:
            box.pack_start(lbl("No device statistics available.", "md-body-small", xalign=0.5), False, False, 12)
        return box

    def _ata_features_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        box.pack_start(self._card_header("ATA Features & Security"), False, False, 0)
        box.pack_start(divider(), False, False, 0)

        def bool_chip(val, true_style="green", false_style=""):
            if val is None: return lbl("-", "md-mono", xalign=1.0)
            return chip("Enabled" if val else "Disabled", true_style if val else false_style)

        sec_str = d.get("ata_security_string")
        if sec_str:
            box.pack_start(list_row("ATA security", sec_str), False, False, 0)

        rows = [
            ("Write cache",     d.get("write_cache_enabled"),    True,  ""),
            ("Read lookahead",  d.get("read_lookahead_enabled"), True,  ""),
            ("TRIM supported",  d.get("trim_supported"),         True,  ""),
        ]
        for key, val, ts, fs in rows:
            if val is None: continue
            box.pack_start(list_row(key, bool_chip(val, ts, fs)), False, False, 0)

        apm_level = d.get("apm_level")
        apm_str   = d.get("apm_string")
        if apm_level is not None:
            apm_label = f"{apm_level}"
            if apm_str: apm_label += f"  ({apm_str})"
            box.pack_start(list_row("APM level", apm_label), False, False, 0)

        return box

    def _phy_counters_card(self, d):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_start(16); box.set_margin_end(16)
        box.set_margin_top(4);    box.set_margin_bottom(4)
        box.get_style_context().add_class("md-card")
        has_errors = d.get("sata_phy_errors", False)
        title = "  SATA Phy Counters - errors detected" if has_errors else "SATA Phy Event Counters"
        box.pack_start(self._card_header(title), False, False, 0)
        box.pack_start(divider(), False, False, 0)
        error_ids = {1, 3, 4, 5, 6, 7, 8}
        for e in d.get("sata_phy_counters", []):
            val = e.get("value", 0)
            is_err = e.get("id") in error_ids
            vw = chip(str(val), "red") if (is_err and val > 0) else lbl(str(val), "md-mono", xalign=1.0)
            box.pack_start(list_row(e.get("name", "-"), vw), False, False, 0)
        return box

    def _card_header(self, title, icon=None):
        box = Gtk.Box(spacing=8)
        box.set_border_width(16)
        box.set_margin_bottom(0)
        if icon:
            box.pack_start(lbl(icon, "md-body-small"), False, False, 0)
        box.pack_start(lbl(title, "md-label-large"), False, False, 0)
        return box

class PasswordDialog(Gtk.Dialog):
    def __init__(self, parent, bad=False):
        super().__init__(title="Authentication required", transient_for=parent,
                         modal=True, destroy_with_parent=True)
        self.set_default_size(360, -1)
        self.set_resizable(False)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Unlock", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        ok_btn = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_btn.get_style_context().add_class("md-btn-filled")
        cancel_btn = self.get_widget_for_response(Gtk.ResponseType.CANCEL)
        cancel_btn.get_style_context().add_class("md-btn-tonal")

        area = self.get_content_area()
        area.set_spacing(0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(24)

        title_row = Gtk.Box(spacing=12)
        title_row.set_valign(Gtk.Align.CENTER)
        icon = lbl(" ", "md-headline")
        title_row.pack_start(icon, False, False, 0)
        title_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        title_col.pack_start(lbl("Root access required", "md-body"), False, False, 0)
        title_col.pack_start(lbl("Enter root password to read disk data",
                                 "md-body-small", wrap=True), False, False, 0)
        title_row.pack_start(title_col, True, True, 0)
        box.pack_start(title_row, False, False, 0)

        self._err_lbl = lbl("Incorrect password, try again.", "md-body-small")
        self._err_lbl.get_style_context().add_class("md-chip-red")
        self._err_lbl.set_xalign(0.0)
        self._err_lbl.set_visible(bad)
        self._err_lbl.set_no_show_all(True)
        box.pack_start(self._err_lbl, False, False, 0)

        entry_lbl = lbl("Root password", "md-body-small")
        entry_lbl.set_xalign(0.0)
        box.pack_start(entry_lbl, False, False, 0)

        self._entry = Gtk.Entry()
        self._entry.set_visibility(False)
        self._entry.set_activates_default(True)
        box.pack_start(self._entry, False, False, 0)

        area.pack_start(box, True, True, 0)
        area.show_all()

    def get_password(self):
        return self._entry.get_text()

class SmartmonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Disks")
        self.set_default_size(720, 900)
        self.set_resizable(True)
        self._devices = []
        self._builder = ContentBuilder()
        self._content_child = None
        self._sudo_password = None                                                                                         
        self._running_tests = {}                                                              
        self._apply_css()
        self._build_ui()
        GLib.idle_add(self._initial_scan)

    def _apply_css(self):
        p = Gtk.CssProvider()
        p.load_from_data(MD3.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), p,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _build_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(root)

        tb = Gtk.Box(spacing=10)
        tb.get_style_context().add_class("md-toolbar")

        tb.pack_start(lbl("Device", "md-body-small"), False, False, 0)

        self.combo = Gtk.ComboBoxText()
        tb.pack_start(self.combo, False, False, 0)

        scan = Gtk.Button(label="⟳  Scan")
        scan.get_style_context().add_class("md-btn-outlined")
        scan.connect("clicked", lambda _: self._scan_devices())
        tb.pack_start(scan, False, False, 0)
        self.refresh_btn = Gtk.Button(label=" Run")
        self.refresh_btn.get_style_context().add_class("md-btn-filled")
        self.refresh_btn.connect("clicked", lambda _: self._load_data())
        tb.pack_end(self.refresh_btn, False, False, 0)

        root.pack_start(tb, False, False, 0)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)

        self.viewport = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.viewport.set_margin_bottom(16)
        self.scroll.add(self.viewport)
        root.pack_start(self.scroll, True, True, 0)

        self.statusbar = lbl("Ready", "md-statusbar")
        self.statusbar.set_margin_start(16)
        self.statusbar.set_margin_top(4)
        self.statusbar.set_margin_bottom(4)
        root.pack_end(self.statusbar, False, False, 0)
        root.pack_end(divider(), False, False, 0)

    def _set_content(self, widget):
        if self._content_child:
            self.viewport.remove(self._content_child)
        self._content_child = widget
        self.viewport.pack_start(widget, True, True, 0)
        widget.show_all()
        adj = self.scroll.get_vadjustment()
        adj.set_value(0)

    def _show_spinner(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)
        box.set_margin_top(80)
        sp = Gtk.Spinner()
        sp.set_size_request(48, 48)
        sp.start()
        box.pack_start(sp, False, False, 0)
        box.pack_start(lbl("Reading SMART data...", "md-body-small", xalign=0.5), False, False, 0)
        self._set_content(box)

    def _initial_scan(self):
        self._scan_devices(); return False

    def _scan_devices(self):
        self.statusbar.set_text("Scanning block devices...")
        threading.Thread(target=self._do_scan, daemon=True).start()

    def _do_scan(self):
        devs = find_block_devices()
        GLib.idle_add(self._populate_combo, devs)

    def _populate_combo(self, devs):
        self._devices = devs
        self.combo.remove_all()
        for d in devs: self.combo.append_text(d)
        if devs:
            self.combo.set_active(0)
            self._load_data()
        else:
            self.statusbar.set_text("No block devices found.")
        return False

    def _load_data(self):
        idx = self.combo.get_active()
        if idx < 0 or idx >= len(self._devices):
            self.statusbar.set_text("No device selected."); return
        device = self._devices[idx]
        self.statusbar.set_text(f"Reading {device}...")
        self.refresh_btn.set_sensitive(False)
        self._show_spinner()
        threading.Thread(target=self._do_load, args=(device,), daemon=True).start()

    def _do_load(self, device):
        raw, code = run_smartctl(device, self._sudo_password)
        d = extract(raw)
        d["_device"] = device                              
        GLib.idle_add(self._render, device, d, code)

    def _render(self, device, d, code):
        err_val = d.get("_error", "")

        if err_val in ("_needs_password", "_bad_password"):
            bad = (err_val == "_bad_password")
            self._sudo_password = None  
            dlg = PasswordDialog(self, bad=bad)
            resp = dlg.run()
            pw   = dlg.get_password()
            dlg.destroy()
            if resp == Gtk.ResponseType.OK and pw:
                self._sudo_password = pw
                self.statusbar.set_text(f"Reading {device}...")
                import threading
                threading.Thread(target=self._do_load, args=(device,), daemon=True).start()
            else:
                self.refresh_btn.set_sensitive(True)
                self.statusbar.set_text("Authentication cancelled.")
            return False

        self.refresh_btn.set_sensitive(True)
        content = self._builder.build(d, win=self)
        self._set_content(content)
        proto = d.get("protocol","")
        err   = " error" if "_error" in d else f"exit {code}"
        self.statusbar.set_text(f"{device}  ·  {proto}  ·  smartctl {err}")
        return False

def main():
    win = SmartmonWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
