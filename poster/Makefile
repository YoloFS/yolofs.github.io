.PHONY: serve clean

PORT   ?= 8080
CHROME ?= $(firstword $(wildcard $(HOME)/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell) \
                       $(shell command -v chromium google-chrome 2>/dev/null))

# Print to a 48"x36" PDF and fail if content spills onto a second page.
poster.pdf: index.html index.css $(wildcard fig/*)
	"$(CHROME)" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
	  --virtual-time-budget=10000 --print-to-pdf=$@ file://$(abspath index.html) 2>/dev/null
	@pages=$$(pdfinfo $@ | awk '/^Pages:/ {print $$2}'); \
	  if [ "$$pages" != 1 ]; then echo "error: content overflows onto $$pages pages" >&2; exit 1; fi

# View in a browser; the page scales to fit the window.
serve:
	@echo "Poster at http://localhost:$(PORT)/"
	python3 -m http.server $(PORT) --bind 127.0.0.1

clean:
	rm -f poster.pdf
