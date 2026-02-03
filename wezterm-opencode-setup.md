# WezTerm setup (opencode-friendly)

This is a quick recipe for getting WezTerm configured the way I like it:

- Dark theme
- Wombat-like colors (close to Vim/iTerm2 Wombat)
- Inconsolata as the primary font
- Good TUI behavior (truecolor, `clear` works, predictable keyboard)

## Key point: terminfo matters

This setup sets `TERM` to `wezterm` in the WezTerm config:

- Pros: apps can use WezTerm-specific capabilities.
- Cons: `TERM=wezterm` requires that a `wezterm` terminfo entry exists.

If the terminfo entry is missing, commands like `clear` can break and TUIs may fall back to basic/incorrect capabilities.

## macOS install

### 1) Install WezTerm

```bash
brew install --cask wezterm
```

### 2) Install the Inconsolata font

I used the Nerd Font variant so prompts/icons render well.

```bash
brew tap homebrew/cask-fonts
brew install --cask font-inconsolata-nerd-font
```

### 3) Create WezTerm config

Create `~/.wezterm.lua`:

```lua
local wezterm = require("wezterm")

local config = wezterm.config_builder()

-- Make TUIs like opencode/neovim look right.
config.term = "wezterm"

-- Wombat-like palette (based on common iTerm2 Wombat colors).
config.color_schemes = {
  Wombat = {
    foreground = "#dedede",
    background = "#171717",
    cursor_bg = "#bbbbbb",
    cursor_fg = "#ffffff",
    selection_bg = "#45454a",
    selection_fg = "#b7bbb8",

    ansi = {
      "#000000", -- black
      "#ff6161", -- red
      "#b1e969", -- green
      "#ebd99c", -- yellow
      "#5da9f6", -- blue
      "#e967ef", -- magenta
      "#82fff3", -- cyan
      "#deede0", -- white
    },
    brights = {
      "#313131", -- bright black
      "#f59a8f", -- bright red
      "#ddf9a1", -- bright green
      "#eee5b3", -- bright yellow
      "#a4c7ff", -- bright blue
      "#ddb5ff", -- bright magenta
      "#bffcff", -- bright cyan
      "#fffffe", -- bright white
    },
  },
}
config.color_scheme = "Wombat"

config.font = wezterm.font_with_fallback({
  -- Mono variant avoids any proportional surprises in TUIs.
  "Inconsolata Nerd Font Mono",
  "Symbols Nerd Font Mono",
  "Noto Color Emoji",
})
config.font_size = 13.0
config.line_height = 1.0

config.audible_bell = "Disabled"
config.scrollback_lines = 20000
config.hide_tab_bar_if_only_one_tab = true
config.use_fancy_tab_bar = false

config.native_macos_fullscreen_mode = true

-- Helps with key chords in TUIs (vim-like behavior).
config.send_composed_key_when_left_alt_is_pressed = true
config.send_composed_key_when_right_alt_is_pressed = true

config.window_close_confirmation = "AlwaysPrompt"

return config
```

### 4) Install `wezterm` terminfo (fixes `clear`)

On macOS the `wezterm` terminfo wasn’t present by default.

```bash
curl -fsSL "https://raw.githubusercontent.com/wez/wezterm/main/termwiz/data/wezterm.terminfo" | tic -x -
```

### 5) Verify

In a new WezTerm window/tab:

```bash
echo $TERM
clear
printf '\e[38;2;255;100;0mtruecolor\e[0m\n'
```

Expected:

- `TERM` prints `wezterm`
- `clear` works
- the word `truecolor` shows in an orange-ish color

## Windows notes

### Install

- Install WezTerm (recommended: `winget install wez.wezterm`)
- Install an Inconsolata Nerd Font (either via Nerd Fonts release or a Windows font package).

### Config location

WezTerm looks for (one of):

- `%USERPROFILE%\.wezterm.lua`

Copy the same config and adjust the font name if needed.

### WSL note (terminfo)

If you run opencode inside WSL, WSL/Linux apps will see `TERM=wezterm` and you may need to install the terminfo entry inside your WSL distro:

```bash
curl -fsSL "https://raw.githubusercontent.com/wez/wezterm/main/termwiz/data/wezterm.terminfo" | tic -x -
```

## Linux notes

### Install

Use your distro’s package for WezTerm (or the upstream tarball if needed). Install a Nerd Font Inconsolata variant for best glyph coverage.

### terminfo

Same concept: if `TERM=wezterm` and `clear`/capabilities look wrong, install terminfo:

```bash
curl -fsSL "https://raw.githubusercontent.com/wez/wezterm/main/termwiz/data/wezterm.terminfo" | tic -x -
```

## Troubleshooting

- `clear` fails with `unknown terminal type`:
  - `infocmp wezterm` should succeed.
  - If it fails, install terminfo using the `tic` command above.
- Colors look “basic”:
  - Verify `echo $TERM` is `wezterm`.
  - Verify truecolor output with the `printf` test above.
- `wezterm ls-fonts | head` crashes:
  - That’s just a broken pipe from piping to `head`; run `wezterm ls-fonts` without piping.
