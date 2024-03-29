# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from os import path
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile, backend
from libqtile.backend.wayland.inputs import InputConfig
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, KeyChord, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration, PowerLineDecoration

#from settings.path import qtile_path

mod = "mod4"
terminal = guess_terminal()
browser = "brave"
fileManager = "pcmanfm"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
#    Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
    # Define a key chord for launching browsers
    KeyChord([mod], "b", [
        Key([], "b", lazy.spawn("mullvad-exclude brave"), desc='Brave Browser, split-tunneled'),
        Key([], "d", lazy.spawn("firedragon"), desc='FireDragon'),
        Key([], "f", lazy.spawn("firefox"), desc='Firefox'),
        Key([], "l", lazy.spawn("librewolf"), desc='LibreWolf'),
        Key([], "m", lazy.spawn("mullvad-browser"), desc='Mullvad Browser'),
        Key([], "t", lazy.spawn("mullvad-exclude torbrowser-launcher"), desc='Tor Browser'),
    ]),
#    Key([mod], "e", lazy.spawn(fileManager), desc="Launch File Manager"),
    # Define a key chord for launching file explorers
    KeyChord([mod], "e", [
        Key([], "l", lazy.spawn("foot -e lf"), desc='Launch lf in terminal'),
        Key([], "m", lazy.spawn("foot -e mc"), desc='Launch Midnight Commander in terminal'),
        Key([], "p", lazy.spawn("pcmanfm"), desc='Launch PCManFM'),
        Key([], "r", lazy.spawn("foot -e ranger"), desc='Launch Ranger in terminal'),
        Key([], "s", lazy.spawn("spacefm"), desc='Launch SpaceFM'),
        Key([], "v", lazy.spawn("foot -e vifm"), desc='Launch Vifm in terminal'),
    ]),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "control"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),
]

groups = [
    Group("1", label=">_", matches=[Match(wm_class=["lapce", "vscodium", "VSCodium"])]),
    Group("2", label="🌐", layout="columns", matches=[Match(wm_class=["Navigator", "firefox", "Tor Browser", "brave-browser", "Brave-browser", "mullvadbrowser"])]),
    Group("3", label="📧", layout="max", matches=[Match(wm_class=["Mail", "thunderbird"])]),
    Group("4", label="💬", layout="matrix"),
    Group("5", label="🎮"),
    Group("6", label="🎭"),
    Group("7", label="📁", matches=[Match(wm_class=["spacfm"])]),
    Group("8", label="🔑", matches=[Match(wm_class=["bitwarden", "protonmail-bridge", "protonvpn", "seahorse"])]),
    Group("9", label="🧅", matches=[Match(wm_class=["qbittorrent"])]),
    ]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Bsp(),
    layout.Columns(),
    layout.Floating(),
    layout.Matrix(),
    layout.Max(),
    layout.MonadTall(),
    layout.MonadThreeCol(),
    layout.MonadWide(),
    layout.RatioTile(),
    layout.Slice(),
    layout.Spiral(),
    layout.Stack(),
    layout.Tile(),
    layout.TreeTab(),
    layout.VerticalTile(),
    layout.Zoomy(),
]

widget_defaults = dict(
    font='FiraCode Nerd Font Mono',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
#        wallpaper=os.path.join(os.path.expanduser("~"), "Pictures/wallpapers/blackarch.jpg"),
#        wallpaper_mode="fill",
        top=bar.Bar(
            [
               # widget.Image(
               #         filename = "~/.config/qtile/logo.png",
               #         scale = "false",
               #         ),
                widget.GroupBox(
                    borderwidth=2,
                    font="FiraCode Nerd Font Mono",
                    hide_unused="True",
                    highlight_color="6298e0",
                    highlight_method="border",
                    this_current_screen_border="6298e0",
                    this_screen_border="888800",
                    urgent_alert_method="border",
                    urgent_border="ff0000",
                    urgent_text="ff0000"

                ),
                widget.Prompt(),
                widget.TaskList(
                    border="6298e0",
                    borderwidth=2,
                    font="serif",
                    highlight_method="border",
                    theme_mode="preferred"
                ),
                # widget.ThermalSensor(
                #     foreground='880000',
                #     foreground_alrt='ff0000',
                #     metric=False,
                #     threshold=160
                # ),
                # widget.CPU(
                #     foreground='008800'
                # ),
                # widget.Memory(
                #     foreground='888800'
                # ),
                # widget.Net(
                #     foreground='000088'
                # ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.PulseVolume(
                #     foreground='880088'
                #     ),
               widget.CheckUpdates(
                    colour_have_updates='ffffff', #'00ffff',
                    colour_no_updates='008080',
                    distro='Arch_checkupdates',
                    font='FiraCode Nerd Font Mono',
                    foreground='33ff33',
                    no_update_string='', #'Updates: 0',
                ),
                widget.StatusNotifier(
                        icon_theme='beautyline'
                        ),
                # widget.Systray(),
                widget.Clock(
                    # foreground='33ff33',
                    format='⏱ %a %Y%m%d %T'
                ),
               # widget.QuickExit(
               #      default_text='[X]',
               #      countdown_format='[{}]'
               #  ),
                widget.CurrentLayoutIcon(),
            ],
            24,
            border_width=[1, 0, 1, 0],  # Draw top and bottom borders
            border_color=["316ab7", "316ab7", "316ab7", "316ab7"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(role="AlarmWindow"), # Thunderbird's calendar.
        Match(role="ConfigManager"), # Thunderbird's about:config.
        Match(role="pop-up"),
        Match(title="branchdialog"),  # gitk
        Match(title="Event Tester"), # xev
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Arandr"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="copyq"), #Includes session name in class
        Match(wm_class="DTA"), # Firefox addon DownThemAll
        Match(wm_class="Gpick"),
        Match(wm_class="Kruler"),
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="MessageWin"), # kalarm
        Match(wm_class="pinentry"),
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="Sxiv"),
        Match(wm_class="Tor Browser"), # Needs a fixed window size to avoid fingerprinting by screen size.
        Match(wm_class="veromix"),
        Match(wm_class="Wpa_gui"),
        Match(wm_class="xtightvncviewer"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:touchpad": InputConfig(tap=True),
}

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
