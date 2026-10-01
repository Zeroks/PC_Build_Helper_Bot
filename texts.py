start_text = "Hello! I am PC-Builder Bot"
select_components_text = "Select a component to add to your build:"

def build_check_status(build):
    COMPONENT_ICONS = {
        "CPU": "🧠",
        "MOTHERBOARD": "🔌",
        "RAM": "⚡",
        "GPU": "🎮",
        "PU": "🔋",
        "CASE": "📦",
    }
    def line(key, component):
        icon = COMPONENT_ICONS.get(key, "❓")
        if component is None:
            return f"⬜ {icon} {key}: not selected"
        return f"✅ {icon} {key}: {component['name']}"
    text = (
    f"🖥️ Your PC Build\n\n"
    f"{line('CPU', build['CPU'])}\n"
    f"{line('MOTHERBOARD', build['MOTHERBOARD'])}\n"
    f"{line('RAM', build['RAM'])}\n"
    f"{line('GPU', build['GPU'])}\n"
    f"{line('PU', build['PU'])}\n"
    f"{line('CASE', build['CASE'])}\n\n"
    f"Select another component:"
    )
    return text

