from libqtile import backend, bar, layout, widget, hook, qtile
from libqtile.widget import GenPollText
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.scripts.main import VERSION
import subprocess
import os
import re
import psutil

MOD = "mod4"
SHIFT = "shift"
CTRL = "control"
ALT = "mod1"
TERMINAL = "kitty"
BROWSER = "brave"
HOME = os.path.expanduser("~")

BAR_COLOR_1 = "#111111"
BAR_COLOR_2 = "#1B1B1B"
WHITE = "#FFFFFF"
GRAY = "#444444"

class Nerd:
    numbers = {
        1: "\U000F0B3A",
        2: "\U000F0B3B",
        3: "\U000F0B3C",
        4: "\U000F0B3D",
        5: "\U000F0B3E",
        6: "\U000F0B3F",
        7: "\U000F0B40",
        8: "\U000F0B41",
        9: "\U000F0B42",
    }
    
    icons = {
        "calendar": "\uf073",
        "clock": "\uf017",
        "volume_off": "\uf026",
        "volume_low": "\uf027",
        "volume_high": "\uf028",
        "volume_mute": "\ueee8",
        "headphones": "\U000f02cb",
        "linux": "\uf17c",
        "brightness": "\uf185",
        "brightness_20": "\U000f00de",
        "brightness_80": "\U000f00df",
        "brightness_100": "\U000f00e0",
        "battery_20": "\uf244",
        "battery_40": "\uf243",
        "battery_60": "\uf242",
        "battery_80": "\uf241",
        "battery_100": "\uf240",
        "charge": "\U000f140b",
        "arrow_up": "\ueaa1",
        "arrow_down": "\uea9a",
        "magnifier": "\uea6d",
        "cpu": "\uf4bc",
        "ram": "\uefc5",
        "power": "\u23fb",
        "wifi_connected": "\U000f05a9",
        "wifi_disconnected": "\U000f05aa",
        "layout_max": "\uebf5",
        "layout_columns": "\uebf3"

    }

    geometrical = {
        "vertical_dotted_line": "\ue621",
        "triangle_southeast": "\ue0ba",
        "triangle_northwest": "\ue0bc",
        "triangle_west_soft": "\ueb6f"
    }

    @classmethod
    def number(cls, n: int) -> str:
        return cls.numbers.get(n, "")

    @classmethod
    def icon(cls, name: str) -> str:
        return cls.icons.get(name, "")

    @classmethod
    def geometry(cls, name: str) -> str:
        return cls.geometrical.get(name, "")

class BatteryWidget(GenPollText):
    def poll(self):
        battery = psutil.sensors_battery()
        
        if not battery:
            return "N/A"
            
        percent = battery.percent
        plugged = battery.power_plugged

        if plugged:
            charge_icon = Nerd.icon("charge")
        else:
            charge_icon = ""
        
        if percent <= 20:
            icon = Nerd.icon("battery_20")
        elif percent <= 40:
            icon = Nerd.icon("battery_40")
        elif percent <= 60:
            icon = Nerd.icon("battery_60")
        elif percent <= 80:
            icon = Nerd.icon("battery_80")
        else:
            icon = Nerd.icon("battery_100")

        return f"{charge_icon} {icon} {percent:.0f}%"

class VolumeWidget(GenPollText):
    def poll(self):
        out = subprocess.run(
            ["amixer", "get", "Master"],
            capture_output=True, text=True
        ).stdout
        head = subprocess.run(
            ["amixer", "get", "Headphone"],
            capture_output=True, text=True
        ).stdout 
        
        m = re.search(r"(\d{1,3})%", out)
        m_mute = re.search(r"\[(on|off)\]", out, re.IGNORECASE)
        h = re.search(r"\[(on|off)\]", head, re.IGNORECASE)

        volume = int(m.group(1)) if m else 0
        muted = (m_mute.group(1).lower() == "off") if m_mute else False
        headphones = (h.group(1).lower() == "on") if h else False

        if muted:
            icon = Nerd.icon("volume_mute")
        elif volume == 0:
            icon = Nerd.icon("volume_off")
        elif volume <= 50:
            icon = Nerd.icon("volume_low")
        else:
            icon = Nerd.icon("volume_high")

        head_icon = Nerd.icon("headphones") if headphones else ""
        
        return f"{head_icon} {icon} {volume}%"

class BacklightWidget(GenPollText):
    def __init__(
        self,
        icon_fontsize=12,
        backlight_name="intel_backlight",
        **config
    ):
        super().__init__(**config)
        self.icon_fontsize = icon_fontsize
        self.backlight_name = backlight_name
        self.icon = None
        self.base_path = f"/sys/class/backlight/{self.backlight_name}"
        self.markup=True

    def poll(self):
        try:
            with open(os.path.join(self.base_path, "brightness")) as f:
                brightness = int(f.read().strip())
            with open(os.path.join(self.base_path, "max_brightness")) as f:
                max_brightness = int(f.read().strip())
            percent = round((brightness / max_brightness) * 100)
        except Exception:
            return None

        if percent < 20:
            self.icon = Nerd.icon("brightness_20")
        elif percent < 80:
            self.icon = Nerd.icon("brightness_80")
        else:
            self.icon = Nerd.icon("brightness_100")

        # return f"<span font_size='{self.icon_fontsize * 1024}'>{self.icon}</span> {percent}%"
        # return (
        #     f"<span font_size='{self.icon_fontsize * 1024}'>{self.icon}</span> "
        #     f"<span rise='4550'>{percent}%</span>"
        # )
        return f"{self.icon} {percent}%"

# ---- keys config ----
keys = [
    # Switch window focus
    Key([MOD], "h", lazy.layout.left()),
    Key([MOD], "l", lazy.layout.right()),
    Key([MOD], "j", lazy.layout.down()),
    Key([MOD], "k", lazy.layout.up()),
    Key([MOD], "Left", lazy.layout.left()),
    Key([MOD], "Right", lazy.layout.right()),
    Key([MOD], "Down", lazy.layout.down()),
    Key([MOD], "Up", lazy.layout.up()),

    # Move windows
    Key([MOD, SHIFT], "h", lazy.layout.shuffle_left()),
    Key([MOD, SHIFT], "l", lazy.layout.shuffle_right()),
    Key([MOD, SHIFT], "j", lazy.layout.shuffle_down()),
    Key([MOD, SHIFT], "k", lazy.layout.shuffle_up()),
    Key([MOD, SHIFT], "Left", lazy.layout.shuffle_left()),
    Key([MOD, SHIFT], "Right", lazy.layout.shuffle_right()),
    Key([MOD, SHIFT], "Down", lazy.layout.shuffle_down()),
    Key([MOD, SHIFT], "Up", lazy.layout.shuffle_up()),

    # Resize windows
    Key([MOD, CTRL], "h", lazy.layout.grow_left()),
    Key([MOD, CTRL], "l", lazy.layout.grow_right()),
    Key([MOD, CTRL], "j", lazy.layout.grow_down()),
    Key([MOD, CTRL], "k", lazy.layout.grow_up()),
    Key([MOD, CTRL], "Left", lazy.layout.grow_left()),
    Key([MOD, CTRL], "Right", lazy.layout.grow_right()),
    Key([MOD, CTRL], "Down", lazy.layout.grow_down()),
    Key([MOD, CTRL], "Up", lazy.layout.grow_up()),
    Key([MOD, CTRL], "n", lazy.layout.normalize()),

    # Spawn
    Key([MOD], "Return", lazy.spawn(TERMINAL)),
    Key([MOD], "b", lazy.spawn(BROWSER)),
    Key([MOD], "p", lazy.spawn("popcorntime")),
    Key([MOD], "Print", lazy.spawn("flameshot gui")),
    Key([], "Print", lazy.spawn("flameshot full")),
    Key([CTRL, SHIFT], "Escape", lazy.spawn(f"{TERMINAL} -e htop")),

    # Switch layouts
    Key([MOD], "Tab", lazy.next_layout()),

    # Other window controls
    Key([MOD], "w", lazy.window.kill()),
    Key([MOD], "f", lazy.window.toggle_fullscreen()),
    Key([MOD], "t", lazy.window.toggle_floating()),
    
    # Qtile controls
    Key([MOD, CTRL], "r", lazy.reload_config()),
    Key([MOD, CTRL], "q", lazy.shutdown()),
    Key([MOD], "r", lazy.spawncmd()),

    # Volume control (alsamixer)
    Key([], "XF86AudioMute", lazy.spawn("bash -c 'amixer set Master toggle; ~/.volume_notify.sh'")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("bash -c 'amixer set Master 5%- unmute; ~/.volume_notify.sh'")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("bash -c 'amixer set Master 5%+ unmute; ~/.volume_notify.sh'")),

    # Brightness control (brightnessctl)
    Key([], "XF86MonBrightnessUp", lazy.spawn("bash -c 'brightnessctl set +5% && ~/.brightness_notify.sh'")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("bash -c 'brightnessctl set 5%- && ~/.brightness_notify.sh'")),
]

# ---- groups or so called workspaces ----
groups = [
    Group(str(i), label=Nerd.number(i))
    for i in range(1, 9)
]

for i in groups:
    keys.extend(
        [
            # Switch to group
            Key([MOD], i.name, lazy.group[i.name].toscreen()),
            # Move focused window to group and switch
            Key([MOD, SHIFT], i.name, lazy.window.togroup(i.name, switch_group=True))
        ]
    )

# ---- layouts ----
layout_theme = dict(
    border_focus="#cccccc",
    border_normal=GRAY,
    border_width=1,
    margin=4
    )

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    # layout.Stack(num_stacks=3),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

layout_icons = {
    "columns": Nerd.icon("layout_columns"),
    "max": Nerd.icon("layout_max")
}

# ---- default appearance for widgets ---- 
margins = dict(
    margin_y=3,
    margin_x=4,
    padding_y=6,
    padding_x=6,
)

widget_defaults = dict(
    font="Dejavu Sans Mono",
    fontsize=10.5,
    padding=3,
    **margins
)

extension_defaults = widget_defaults.copy()

# ---- screen setup, like bar with widgets n shit ----
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=Nerd.icon("linux"),
                    font="Symbols Nerd Font",
                    fontsize=27,
                    foreground=WHITE,
                    padding=6
                ),
                # widget.Sep(
                #     linewidth=1,
                #     padding=4,
                #     size_percent=80
                # ),
                widget.GenPollText(
                    update_interval=0.5,
                    func=lambda: layout_icons.get(qtile.current_layout.name, "?"),
                    fontsize=14,
                    padding=6,
                    foreground=WHITE,
                    background=BAR_COLOR_1
                ),
                widget.Sep(
                    linewidth=1,
                    padding=4,
                    size_percent=80
                ),
                widget.GroupBox(
                    **margins,
                    font="Symbols Nerd Font", 
                    fontsize=20,
                    borderwidth=2,
                    disable_drag=True,
                    active=WHITE,
                    inactive=GRAY,
                    highlight_method="line",
                    this_current_screen_border=WHITE, # active group on current screen
                    this_screen_border=GRAY, # inactive groups on current screen
                    other_current_screen_border=WHITE, # active group on another screen
                    other_screen_border=GRAY, # incative group on another screen
                    highlight_color=BAR_COLOR_1,
                    use_mouse_wheel=True,
                    rounded=False
                ),

                widget.WindowName(
                    format="{name}",
                    fontsize=10.5,
                ),
                widget.Systray(
                    background=BAR_COLOR_1,
                    icon_size=17,
                    hide_crash=False
                ),
                widget.Prompt(
                    background=BAR_COLOR_1,
                    foreground=WHITE,
                    cursor=True,
                    cursor_color=WHITE,
                    ignore_dups_history=True,
                    prompt=Nerd.icon("magnifier")+" "
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_southeast"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.Memory(
                    format=Nerd.icon("ram") + " {MemUsed:.1f}G / {MemTotal:.0f}G",
                    measure_mem="G",
                    background=BAR_COLOR_2,
                    update_interval=1
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_northwest"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.CPU(
                    format=Nerd.icon("cpu") + " {load_percent:.0f}% |",
                    background=BAR_COLOR_1,
                    foreground=WHITE,
                    update_interval=1
                ),
                widget.ThermalSensor(
                    format="{temp:.0f}{unit}",
                    background=BAR_COLOR_1,
                    update_interval=1
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_southeast"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.KeyboardLayout(
                    configured_keyboards=['us', 'ru winkeys', 'am phonetic'],
                    background=BAR_COLOR_2    
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_northwest"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                BacklightWidget(
                    icon_fontsize=18,
                    backlight_name="intel_backlight",
                    foreground=WHITE,
                    background=BAR_COLOR_1,
                    update_interval=0.5
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_southeast"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.Wlan(
                    interface="wlp0s20u1",
                    background=BAR_COLOR_2,
                    format=Nerd.icon("wifi_connected") + " {essid}",
                    disconnected_message=Nerd.icon("wifi_disconnected"),
                    update_interval=0.5
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_northwest"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                VolumeWidget(
                    update_interval=0.5,
                    font="Symbols Nerd Font",
                    background=BAR_COLOR_1
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_southeast"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                BatteryWidget(
                    update_interval=1,
                    font="Symbols Nerd Font",
                    background=BAR_COLOR_2
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_northwest"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.Clock(
                    format=f"{Nerd.icon('calendar')} %d %b, %a %I:%M %p"
                ),
                widget.TextBox(
                    text=Nerd.geometry("triangle_southeast"),
                    foreground=BAR_COLOR_2,
                    fontsize=50,
                    padding=0
                ),
                widget.QuickExit(
                    default_text=Nerd.icon("power") + " ",
                    countdown_format="{}",
                    fontsize=20,
                    padding=0,
                    background=BAR_COLOR_2
                )
            ],
            size=30,
            margin=[0, 0, 0, 0],
            background=BAR_COLOR_1
        ),
    ),
]

# -------------------------------------- FLOATING WINDOWS ----------------------------------------
# ---- drag floating layouts ----
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

# ---- floating layout rules ----
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry")  # GPG key password entry
    ]
)
# ------------------------------------------------------------------------------------------------

# ---- dynamic groups(automatically assign windows to groups) ----
dgroups_key_binder = None
dgroups_app_rules = []

# ---- other ----
follow_mouse_focus = False # focus on mouse hover if true
bring_front_click = False # clicking floating window brings it to the front if true
floats_kept_above = False # floating windows always stay on top of tiling ones if true
cursor_warp = False # when switching windows via keyboard mouse cursor will move to active windows if true

auto_fullscreen = True # allow apps to automatically go full screen if they want to if true
focus_on_window_activation = "smart" # qtile decides whether to give focus or not to new opened window that requests focus if "smart"

reconfigure_screens = True # dynamically rebuilding screen layout when changing monitor setup(unplugging for example) if true
auto_minimize = True # some apps autominimize when losing focus, qtile respects that behaviour(for example steam or sum) if true

# ---- autostart config ----
@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([HOME + "/.config/qtile/.autostart.sh"])

# ---- name ----
match = re.match(r"(\d+\.\d+\.\d+)", VERSION)
wmname = f"Qtile {match.group(1) if match else None}"

