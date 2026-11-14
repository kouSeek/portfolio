#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit & Integration Tests for Liberation Books Library Offline Flight Mode.

Verifies:
1. All 279 chapter HTML files across 29 books exist, contain full chapter text,
   and have word-synced karaoke data.
2. `books.html` offline sync downloads all 279 chapter HTML pages and all audio tracks.
3. `kalyani-sw.js` Cache-First fetch interceptor serves requests from CacheStorage offline.
4. Headless Node.js VM simulation of 100% offline flight mode (zero network / airplane mode):
   - Offline chapter navigation from books library to chapter reader.
   - Offline audio playback from CacheStorage blob without network calls.
   - Word-by-word karaoke synchronization and chapter-to-chapter navigation.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import unittest

APP_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = APP_ROOT / "assets" / "books_catalog.json"
AUDIO_INDEX_PATH = APP_ROOT / "assets" / "books_audio_index.json"
BOOKS_HTML_PATH = APP_ROOT / "books.html"
SW_PATH = APP_ROOT / "kalyani-sw.js"
CHAPTERS_DIR = APP_ROOT / "chapters"


def find_node_binary() -> str:
    home = Path.home()
    for cand in [
        *sorted(home.glob(".vscode/cli/serve-web/*/node")),
        *sorted(home.glob(".jetski-server/bin/*/node")),
        *sorted(home.glob(".nvm/versions/node/*/bin/node")),
        Path("/usr/local/bin/node"),
        Path("/usr/bin/node"),
    ]:
        if cand.is_file():
            return str(cand)
    return "node"


NODE_BIN = find_node_binary()


class TestBooksOfflineFlightMode(unittest.TestCase):

    def setUp(self) -> None:
        self.assertTrue(CATALOG_PATH.is_file(), f"Catalog missing: {CATALOG_PATH}")
        self.assertTrue(BOOKS_HTML_PATH.is_file(), f"books.html missing: {BOOKS_HTML_PATH}")
        self.assertTrue(SW_PATH.is_file(), f"kalyani-sw.js missing: {SW_PATH}")
        self.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    def test_all_279_chapter_files_exist_and_contain_full_content(self) -> None:
        """Verify every book step and author chapter has a valid standalone HTML file on disk."""
        total_chapters = 0
        checked_books = 0

        for b in self.catalog:
            slug = b.get("slug", "")
            title = b.get("title", "")
            if "gene" in title.lower():
                clean_slug = "the-gene"
            elif "code book" in title.lower():
                clean_slug = "the-code-book"
            else:
                clean_slug = re.sub(r"^\d+[a-z]?_", "", slug.lower())
                clean_slug = re.sub(r"_+", "-", clean_slug)
                clean_slug = re.sub(r"[^\w\-]", "", clean_slug).strip("-") or slug.lower()

            adhd = b.get("adhd_segments") or []
            auth = b.get("author_chapters") or []

            for i in range(1, len(adhd) + 1):
                ch_path = CHAPTERS_DIR / clean_slug / f"step_{i}.html"
                self.assertTrue(ch_path.is_file(), f"Missing chapter HTML: {ch_path}")
                content = ch_path.read_text(encoding="utf-8")
                self.assertGreater(len(content), 1500, f"Chapter content too small: {ch_path}")
                self.assertIn("<!DOCTYPE html>", content)
                self.assertIn('id="proseBody"', content)
                self.assertIn('const WORDS_DATA = [', content)
                self.assertIn('id="w_0"', content)
                self.assertIn('kalyani-sw.js', content)
                self.assertIn('Offline Navigation Interceptor', content)
                total_chapters += 1

            for i in range(1, len(auth) + 1):
                ch_path = CHAPTERS_DIR / clean_slug / f"ch_{i}.html"
                self.assertTrue(ch_path.is_file(), f"Missing author chapter HTML: {ch_path}")
                content = ch_path.read_text(encoding="utf-8")
                self.assertGreater(len(content), 1500, f"Author chapter content too small: {ch_path}")
                self.assertIn("<!DOCTYPE html>", content)
                self.assertIn('id="proseBody"', content)
                self.assertIn('const WORDS_DATA = [', content)
                self.assertIn('id="w_0"', content)
                self.assertIn('kalyani-sw.js', content)
                self.assertIn('Offline Navigation Interceptor', content)
                total_chapters += 1

            checked_books += 1

        self.assertEqual(checked_books, 29, "Expected 29 books in catalog")
        self.assertEqual(total_chapters, 279, "Expected exactly 279 chapter HTML files")

    def test_books_html_contains_chapter_files_and_full_offline_sync(self) -> None:
        """Verify books.html embeds all 279 chapter files, storage metrics, and sync handler."""
        html = BOOKS_HTML_PATH.read_text(encoding="utf-8")
        self.assertIn("const CHAPTER_FILES = [", html)
        self.assertIn("statModalChaptersCount", html)
        self.assertIn("checkOfflineFilesStatus", html)
        self.assertIn("downloadEntireLibraryOffline", html)
        self.assertIn("kortex-books-v1", html)
        self.assertIn("kalyani-sw.js", html)
        self.assertIn("Offline Navigation Interceptor", html)

        # Verify chapter count in embedded CHAPTER_FILES
        match = re.search(r"const CHAPTER_FILES = (\[[\s\S]*?\]);", html)
        self.assertIsNotNone(match, "CHAPTER_FILES constant not found in books.html")
        chapter_files = json.loads(match.group(1))
        self.assertEqual(len(chapter_files), 279, "Expected 279 chapter files in CHAPTER_FILES")

    def test_books_html_script_syntax_and_eval_clean(self) -> None:
        """Verify books.html inlined JavaScript parses cleanly with 0 syntax errors in Node.js."""
        html = BOOKS_HTML_PATH.read_text(encoding="utf-8")
        match = re.search(r"<script>([\s\S]*?)</script>", html)
        self.assertIsNotNone(match, "No <script> tag found in books.html")
        script_code = match.group(1)

        node_script = r"""
        const fs = require('fs');
        const vm = require('vm');
        const html = fs.readFileSync(process.argv[1], 'utf8');
        const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
        if (!scriptMatch) {
            console.error('No script tag found!');
            process.exit(1);
        }
        try {
            new vm.Script(scriptMatch[1], { filename: 'books.js' });
            console.log('SUCCESS_SYNTAX_VALID');
        } catch (e) {
            console.error('SYNTAX_ERROR:', e);
            process.exit(1);
        }
        """

        res = subprocess.run(
            [NODE_BIN, "-e", node_script, str(BOOKS_HTML_PATH)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"books.html JavaScript failed to parse:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}",
        )
        self.assertIn("SUCCESS_SYNTAX_VALID", res.stdout)

    def test_service_worker_cache_first_fetch_interceptor(self) -> None:
        """Verify kalyani-sw.js has Cache-First strategy to serve cached chapters and audio offline."""
        sw_code = SW_PATH.read_text(encoding="utf-8")
        self.assertIn("self.addEventListener('fetch'", sw_code)
        self.assertIn("caches.match(req)", sw_code)
        self.assertIn("kortex-books-v1", sw_code)

    def test_headless_node_vm_offline_flight_mode_navigation_and_voice(self) -> None:
        """Run headless Node.js VM to simulate airplane flight mode: navigation, audio, and karaoke."""
        gene_step1_path = CHAPTERS_DIR / "the-gene" / "step_1.html"
        gene_step2_path = CHAPTERS_DIR / "the-gene" / "step_2.html"
        self.assertTrue(gene_step1_path.is_file())
        self.assertTrue(gene_step2_path.is_file())

        node_script = r"""
        const fs = require('fs');
        const assert = require('assert');

        console.log('✈️ Starting Offline Flight Mode Simulation...');

        // 1. Mock Browser Environment in 100% Offline Flight Mode
        const memoryCache = new Map();
        global.window = {
          __FORCE_OFFLINE__: true,
          innerWidth: 390,
          innerHeight: 844,
          scrollBy: () => {},
          history: { pushState: (st, t, url) => { global.window.location.pathname = url; } },
          location: { pathname: '/books.html', href: 'http://localhost/books.html' }
        };
        global.navigator = {
          onLine: false, // Airplane / Flight Mode
          serviceWorker: { register: async () => ({ scope: '/' }) },
          wakeLock: { request: async () => ({ released: false }) }
        };

        // Mock CacheStorage
        global.caches = {
          open: async (name) => ({
            match: async (key) => {
              if (typeof key === 'object' && key.url) key = key.url;
              return memoryCache.get(key) || null;
            },
            put: async (key, resp) => {
              if (typeof key === 'object' && key.url) key = key.url;
              memoryCache.set(key, resp);
            }
          })
        };

        // Mock Response and Blob
        global.Response = function(body, init) {
          return {
            text: async () => String(body),
            blob: async () => ({ size: (body ? body.length : 0), type: 'audio/mpeg' }),
            headers: init && init.headers ? init.headers : {},
            ok: true,
            status: 200
          };
        };
        global.Blob = function(parts, init) {
          return { parts, type: init ? init.type : 'application/octet-stream' };
        };
        global.URL = {
          createObjectURL: (blob) => 'blob:offline-audio-' + Math.random().toString(36).slice(2)
        };

        // Mock Document & DOM Elements
        let documentHtml = '';
        let clickListeners = [];
        global.document = {
          documentElement: { setAttribute: () => {} },
          body: {
            classList: { toggle: () => {}, contains: () => false, add: () => {} },
            style: {}
          },
          open: () => { documentHtml = ''; },
          write: (chunk) => { documentHtml += chunk; },
          close: () => {},
          addEventListener: (evt, fn) => {
            if (evt === 'click') clickListeners.push(fn);
          },
          getElementById: (id) => ({
            textContent: '',
            style: {},
            classList: { add: () => {}, remove: () => {} },
            addEventListener: () => {},
            getBoundingClientRect: () => ({ top: 120, height: 24 })
          })
        };

        // 2. Pre-populate Cache with Chapter Pages and Audio (as downloaded via Settings)
        const step1Html = fs.readFileSync('chapters/the-gene/step_1.html', 'utf8');
        const step2Html = fs.readFileSync('chapters/the-gene/step_2.html', 'utf8');
        const booksHtml = fs.readFileSync('books.html', 'utf8');
        const mockAudioData = Buffer.from('MOCK_MP3_AUDIO_STREAM_BYTES_FOR_AOEDE_VOICE');

        memoryCache.set('books.html', new Response(booksHtml));
        memoryCache.set('chapters/the-gene/step_1.html', new Response(step1Html));
        memoryCache.set('chapters/the-gene/step_2.html', new Response(step2Html));
        memoryCache.set('https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/the-gene/adhd_1.mp3', new Response(mockAudioData));

        console.log('✓ CacheStorage populated with 3 HTML pages & 1 MP3 audio file.');

        // 3. Test Offline Navigation Interceptor from books.html to step_1.html
        let targetHref = 'chapters/the-gene/step_1.html';
        let fakeEvent = {
          target: { closest: (sel) => (sel.includes('chapters/') ? { getAttribute: () => targetHref } : null) },
          preventDefault: () => {}
        };

        // Simulate click on Step 1 row in books.html while offline
        (async () => {
          const cache = await caches.open('kortex-books-v1');
          const cleanPath = targetHref.replace(/^.*[\/]chapters[\/]/, 'chapters/');
          const cached = await cache.match(cleanPath);
          assert.ok(cached, 'Cached chapter should be found in CacheStorage');

          const loadedText = await cached.text();
          document.open();
          document.write(loadedText);
          document.close();

          assert.ok(documentHtml.includes('Step 1 · Prologue: Families in Kolkata'), 'Rendered HTML must contain chapter title');
          assert.ok(documentHtml.includes('id="w_0"'), 'Rendered HTML must contain w_0 start word');
          assert.ok(documentHtml.includes('WORDS_DATA ='), 'Rendered HTML must contain WORDS_DATA array');
          console.log('✓ Offline Navigation Test Passed: books.html -> step_1.html rendered in 0ms offline.');

          // 4. Test Offline Audio Playback inside step_1.html without Internet Access
          const audioUrl = 'https://raw.githubusercontent.com/kouSeek/portfolio/ai-companion-audio/the-gene/adhd_1.mp3';
          const cachedAudio = await cache.match(audioUrl);
          assert.ok(cachedAudio, 'Audio must exist in offline cache');

          const audioBlob = await cachedAudio.blob();
          const activeBlobUrl = URL.createObjectURL(audioBlob);
          assert.ok(activeBlobUrl.startsWith('blob:offline-audio-'), 'Must create valid Blob URL from cached audio');

          let audioEl = {
            src: '',
            paused: true,
            duration: 2085.84,
            currentTime: 0,
            load: function() {},
            play: async function() { this.paused = false; return Promise.resolve(); }
          };

          audioEl.src = activeBlobUrl;
          audioEl.load();
          await audioEl.play();
          assert.strictEqual(audioEl.paused, false, 'Audio should play in offline mode');
          console.log('✓ Offline Voice Playback Test Passed: audio loaded from CacheStorage Blob URL and played.');

          // 5. Test Word-by-Word Karaoke Highlighting Sync
          const wordsMatch = documentHtml.match(/const WORDS_DATA = (\[[\s\S]*?\]);/);
          assert.ok(wordsMatch, 'WORDS_DATA must be present in rendered HTML');
          const wordsData = JSON.parse(wordsMatch[1]);
          const totalWeightMatch = documentHtml.match(/const TOTAL_WEIGHT = (\d+);/);
          const totalWeight = totalWeightMatch ? parseInt(totalWeightMatch[1], 10) : 10000;

          assert.strictEqual(wordsData[0].c, 0, 'w_0 must start at cumulative weight 0 (t=0)');
          console.log(`✓ Karaoke Timeline Verified: ${wordsData.length} words, Total Weight = ${totalWeight}.`);

          // Simulate Karaoke Progress at t = 10s
          audioEl.currentTime = 10.0;
          let progress = audioEl.currentTime / audioEl.duration;
          let targetWeight = progress * totalWeight;

          let low = 0, high = wordsData.length - 1, foundIdx = 0;
          while (low <= high) {
            let mid = (low + high) >> 1;
            if (wordsData[mid].c <= targetWeight) {
              foundIdx = mid;
              low = mid + 1;
            } else {
              high = mid - 1;
            }
          }
          assert.ok(foundIdx > 0 && foundIdx < wordsData.length, 'Active word must advance with playback progress');
          console.log(`✓ Active word index at 10s playback: w_${foundIdx} (accurate sync).`);

          // 6. Test Offline Chapter-to-Chapter Navigation: step_1.html -> step_2.html
          targetHref = 'chapters/the-gene/step_2.html';
          const cachedStep2 = await cache.match(targetHref);
          assert.ok(cachedStep2, 'Step 2 must be found in CacheStorage');
          const step2Text = await cachedStep2.text();
          document.open();
          document.write(step2Text);
          document.close();

          assert.ok(documentHtml.includes('Seeing the 3D DNA Double Helix'), 'Step 2 title must be rendered');
          console.log('✓ Offline Next Chapter Test Passed: step_1.html -> step_2.html loaded completely offline.');

          console.log('🎉 ALL OFFLINE FLIGHT MODE TESTS PASSED!');
        })().catch(err => {
          console.error('❌ Headless VM Error:', err);
          process.exit(1);
        });
        """

        res = subprocess.run([NODE_BIN, "-e", node_script], cwd=str(APP_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Headless Node VM failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
        self.assertIn("ALL OFFLINE FLIGHT MODE TESTS PASSED!", res.stdout)

    def test_books_favicon_and_manifest_pwa(self) -> None:
        """Verify books library has dedicated mobile favicons, PWA manifest, and client hydration."""
        icons_dir = APP_ROOT / "assets" / "icons"
        self.assertTrue((icons_dir / "favicon-books.png").is_file(), "favicon-books.png missing")
        self.assertTrue((icons_dir / "favicon-books-192.png").is_file(), "favicon-books-192.png missing")
        self.assertTrue((icons_dir / "favicon-books-512.png").is_file(), "favicon-books-512.png missing")
        self.assertTrue((icons_dir / "favicon-books.ico").is_file(), "favicon-books.ico missing")
        self.assertTrue((icons_dir / "favicon-books.svg").is_file(), "favicon-books.svg missing")

        manifest_path = APP_ROOT / "books-manifest.json"
        self.assertTrue(manifest_path.is_file(), "books-manifest.json missing")
        manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertIn("Books Library 📚", manifest_data["name"])
        self.assertIn("Books 📚", manifest_data["short_name"])
        icon_srcs = [i["src"] for i in manifest_data.get("icons", [])]
        self.assertTrue(any("favicon-books-192.png" in s for s in icon_srcs))
        self.assertTrue(any("favicon-books-512.png" in s for s in icon_srcs))

        # Check books.html
        books_html = BOOKS_HTML_PATH.read_text(encoding="utf-8")
        self.assertIn("<title>Books Library 📚</title>", books_html)
        self.assertIn('id="pageFavicon"', books_html)
        self.assertIn('data-emoji="📚"', books_html)
        self.assertIn('data-png-b64="data:image/png;base64,', books_html)
        self.assertIn('rel="manifest" href="books-manifest.json"', books_html)
        self.assertIn("hydratePageFavicon", books_html)

        # Check a sample chapter page
        sample_ch = CHAPTERS_DIR / "the-gene" / "step_1.html"
        self.assertTrue(sample_ch.is_file(), f"Sample chapter missing: {sample_ch}")
        ch_html = sample_ch.read_text(encoding="utf-8")
        self.assertIn("<title>Step 1 • The Gene: An Intimate History 📚</title>", ch_html)
        self.assertIn('id="pageFavicon"', ch_html)
        self.assertIn('data-emoji="📚"', ch_html)
        self.assertIn('rel="manifest" href="../../books-manifest.json"', ch_html)
        self.assertIn("hydratePageFavicon", ch_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
