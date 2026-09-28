.PHONY: clean

# First Chrome found: macOS app, then Linux binaries, then a Playwright download.
CHROME ?= $(shell for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
                    google-chrome chromium $(HOME)/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell; do \
                    command -v "$$c" >/dev/null 2>&1 && { echo "$$c"; break; }; done)

# Print to a 48"x36" PDF and fail if content spills onto a second page.
poster.pdf: index.html index.css $(wildcard fig/*)
	"$(CHROME)" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
	  --virtual-time-budget=10000 --print-to-pdf=$@ file://$(abspath index.html) 2>/dev/null
	@pages=$$(pdfinfo $@ | awk '/^Pages:/ {print $$2}'); \
	  if [ "$$pages" != 1 ]; then echo "error: content overflows onto $$pages pages" >&2; exit 1; fi

clean:
	rm -f poster.pdf
