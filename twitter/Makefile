.PHONY: all

# First Chrome found: macOS app, then Linux binaries, then a Playwright download.
CHROME ?= $(shell for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
                    google-chrome chromium $(HOME)/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell; do \
                    command -v "$$c" >/dev/null 2>&1 && { echo "$$c"; break; }; done)
SHOT = "$(CHROME)" --headless --no-sandbox --disable-gpu --hide-scrollbars --virtual-time-budget=5000

# Site figures attached to the thread (see README.md), as PNGs since Twitter rejects SVG.
FIGS = impact shift autonomy
# Terminal images drawn for the thread, one HTML page each.
TERMS = staging selfcorrect

all: ../og.png $(FIGS:%=%.png) $(TERMS:%=%.png)

# The 1200x630 social card, served from the site root.
../og.png: og.html
	$(SHOT) --window-size=1200,630 --screenshot=$(abspath $@) file://$(abspath $<) 2>/dev/null

$(TERMS:%=%.png): %.png: %.html term.css
	$(SHOT) --window-size=1200,675 --screenshot=$(abspath $@) file://$(abspath $<) 2>/dev/null

# Window height = SVG height scaled to 1120px wide, plus 40px padding on each side.
$(FIGS:%=%.png): %.png: ../fig/%.svg fig.html
	h=$$(grep -o '<svg[^>]*' $< | sed 's/.* width="\([0-9.]*\)" height="\([0-9.]*\)".*/\1 \2/' | awk '{printf "%d", 1120*$$2/$$1+80}'); \
	$(SHOT) --window-size=1200,$$h --screenshot=$(abspath $@) "file://$(abspath fig.html)?$(abspath $<)" 2>/dev/null
