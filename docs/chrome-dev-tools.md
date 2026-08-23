# Chrome Dev Tools — Agent Usage Guide

Lazy-launch browser control for pi agents, powered by **Playwright driving your
system Chrome**. Use it to navigate pages, inspect the accessibility (AX) tree,
click/type, read DOM values with JS, screenshot, and manage tabs — all from
tools instead of a manual browser.

Source of truth: `node_modules/pi-chrome-dev-tools` (`skills/chrome-dev-tools/SKILL.md`,
`README.md`, `src/tools/*.ts`). This doc is a practical reference derived from that code.

---

## 1. Install & run

```bash
pi install npm:pi-chrome-dev-tools
```

That's the only setup step. **No Chrome flags, no remote-debugging config.**

- **Lazy launch:** Chrome starts on the *first* tool call (e.g. `chrome_navigate`).
- **Visible window:** the browser runs with `headless: false` — a real Chrome
  window opens and you can watch it work.
- **System Chrome:** uses your installed Google Chrome (`channel: "chrome"`),
  so there is no 150 MB Chromium download.
- **Stealth:** `@mr_ozio/playwright-stealth` patches `navigator.webdriver`,
  plugin arrays, permissions, etc. out of the box (helps with bot detection).
- **Persistent profile:** `~/.chrome-dev-tools/profile` — logins, cookies, and
  sessions survive across pi sessions.
- **Auto-cleanup:** the browser closes when the pi session ends (or via `chrome_close`).

### Prerequisites
- [pi](https://github.com/mariozechner/pi) (latest)
- Node.js ≥ 22
- Google Chrome installed on the system

---

## 2. Tool reference

All tools fail safe: on error they return an `errorResult` (text describing the
problem) rather than throwing. The "active page" is the **last page created** in
the browser context (see gotchas).

### Inspection (start here)
| Tool | Key params | Notes |
|------|-----------|-------|
| `chrome_snapshot` | `interestingOnly` (bool, default `true`), `maxNodes` (int 1–5000, default 1000) | **DEFAULT** for understanding a page. Returns the AX tree; interactive elements (button/link/textbox/checkbox/combobox/…) include `@(x,y)` center coordinates. |
| `chrome_execute_js` | `expression` (string JS; last expression is returned) | Surgical DOM reads. Result is `JSON.stringify`'d; `undefined` → `"undefined"`. |
| `chrome_page_info` | — | URL, title, viewport size, scroll position, full page size. |
| `chrome_screenshot` | `fullPage` (bool, default `false`), `path` (optional; defaults to a temp `.png`) | Visual verification **only**. Saves a PNG and returns the path. |

### Navigation
| Tool | Key params | Notes |
|------|-----------|-------|
| `chrome_navigate` | `url` (string) | Launches Chrome on first call. Waits until `domcontentloaded` (timeout 30s) — NOT `load`, so SPA content may still be rendering. |
| `chrome_wait_for_load` | `timeout` (seconds, default 15) | Waits for `document.readyState === "complete"`. Use after `navigate` for JS-heavy pages. |
| `chrome_wait` | `seconds` (0.1–30) | Fixed sleep. |
| `chrome_reload` | — | Reload, wait `domcontentloaded`. |
| `chrome_go_back` / `chrome_go_forward` | — | History nav (no-op message if none). |

### Interaction
| Tool | Key params | Notes |
|------|-----------|-------|
| `chrome_click` | `x`, `y` (CSS px), `button` (`left`/`right`/`middle`, default `left`), `clickCount` (1–3, default 1) | Click at **viewport coordinates**. Get `x,y` from a `chrome_snapshot` `@(x,y)` hint. |
| `chrome_type` | `text` (string) | Types into the **currently focused** element. Click the input first to focus it. |
| `chrome_press_key` | `key` (e.g. `Enter`, `Tab`, `Escape`, `ArrowDown`, `a`, `A`) | Playwright key names. |
| `chrome_scroll` | `x`, `y` (default 0), `deltaX` (default 0), `deltaY` (default 300, positive = down) | Wheel scroll; waits 200ms; returns new scroll position. |

### Tabs
| Tool | Key params | Notes |
|------|-----------|-------|
| `chrome_list_tabs` | — | Lists `[index] url — title` for all pages. |
| `chrome_switch_tab` | `index` (int) | `bringToFront()` on that tab. |
| `chrome_new_tab` | `url` (optional) | Opens a tab, optionally navigates. Newest tab = active. |
| `chrome_close_tab` | `index` (optional; default = last) | Closes a tab. |

### Lifecycle
| Tool | Notes |
|------|-------|
| `chrome_close` | Closes the browser; it relaunches on the next tool call. |

---

## 3. Canonical workflow

**Understand a page → act on it:**

```
chrome_navigate("https://example.com")   # launches Chrome, loads page
chrome_wait_for_load()                    # (optional) ensure JS finished
chrome_snapshot()                         # AX tree + @(x,y) for buttons/inputs
chrome_click({ x, y })                    # from a snapshot hint
chrome_type({ text: "hello" })            # into the now-focused field
chrome_press_key({ key: "Enter" })
chrome_execute_js("document.querySelector('.result').innerText")  # read result
```

**Prefer `chrome_snapshot` + `chrome_execute_js` over screenshots.** Screenshots are
only for confirming visual rendering.

---

## 4. Common patterns

### Log in / fill a form
```
chrome_navigate("https://site/login")
chrome_snapshot()                       # find email + password @(x,y)
chrome_click({ x: emailX, y: emailY })
chrome_type({ text: "admin@example.com" })
chrome_press_key({ key: "Tab" })        # move to next field
chrome_type({ text: "password123" })    # (or click password @(x,y) first)
chrome_click({ x: submitX, y: submitY })
```

### Read a value from the DOM
```
chrome_execute_js("document.querySelector('.price').innerText")
chrome_execute_js("Array.from(document.querySelectorAll('a')).map(a => a.href)")
```

### Get an element's geometry (if you must click by selector logic)
```
chrome_execute_js("JSON.stringify(document.querySelector('#cta').getBoundingClientRect())")
```

### Multi-tab research
```
chrome_new_tab({ url: "https://a.com" })   # newest = active
chrome_snapshot()
chrome_new_tab({ url: "https://b.com" })
chrome_list_tabs()
# interact with the active (last) tab directly
```

### Verify visually
```
chrome_screenshot({ path: "/tmp/login.png" })   # or omit path → temp file
```

---

## 5. Gotchas (read before debugging)

1. **"Active page" = last *created* page, not the frontmost one.** Every
   interaction tool (`click`, `type`, `press_key`, `execute_js`, `screenshot`,
   `snapshot`) acts on `pages[pages.length - 1]`. `chrome_switch_tab` only calls
   `bringToFront()` (z-order) — it does **not** change which page is "active" for
   the next tool call.
   → For reliable multi-tab work, open the target as a **new tab** (it becomes the
   last/active page), or close the tabs you're not using.

2. **`chrome_navigate` waits for `domcontentloaded`, not `load`.** On JS-heavy /
   SPA pages, content may still be rendering. Follow with `chrome_wait_for_load()`
   or `chrome_wait()` before snapshotting.

3. **Click coordinates are viewport CSS pixels from the snapshot.** If the target
   is below the fold, `chrome_scroll()` first, then `chrome_snapshot()` again to
   get fresh `@(x,y)`, then `chrome_click()`. (Snapshot coords are viewport-relative;
   scrolling changes them.)

4. **`chrome_type` needs a focused element.** It has no selector argument — you
   must `chrome_click` the input (or `chrome_press_key("Tab")`) to focus first.

5. **Viewport is `null`** (Chrome's real window size), not a fixed 1280×720.
   Layout/coords depend on the actual window. Don't assume a fixed viewport.

6. **Headless = false.** A visible Chrome window opens. On a headless server /
   remote box without a display this may fail — run where a desktop session exists.

7. **`chrome_execute_js` returns `JSON.stringify(result)`.** Functions, DOM nodes,
   and circular structures won't serialize cleanly — return primitives/arrays/objects
   (e.g. `.innerText`, `.href`, `.value`, or mapped arrays).

8. **Screenshots save to a temp file by default** (`os.tmpdir()`). Pass `path` to
   keep one you can reference.

9. **Persistent profile = shared logins.** Because `~/.chrome-dev-tools/profile`
   persists, a login done in one session carries to the next. Clear that folder if
   you need a clean slate.

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| "No page" / browser not launched | Call `chrome_navigate` once to trigger lazy launch. |
| Click hits the wrong element | Re-snapshot after scrolling; coords drift when the page moves. |
| Typed text goes nowhere | Click the input (or `Tab`) to focus before `chrome_type`. |
| Interactions affect the wrong tab | Remember rule #1 — interact with the *last created* tab; close others or open a new one. |
| Page looks unfinished after navigate | Add `chrome_wait_for_load()` / `chrome_wait()`. |
| `chrome_execute_js` returns `"undefined"` | The last expression had no value; return something explicit. |
| Window won't open (headless server) | Run on a machine with a display / desktop session. |

---

## 7. One-line mental model

> `chrome_navigate` opens Chrome → `chrome_snapshot` shows you the page with
> clickable `@(x,y)` → click/type/read with the other tools → it all runs against
> your real, stealth-patched, logged-in system Chrome, and closes when the session ends.
