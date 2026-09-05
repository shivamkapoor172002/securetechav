/* ── LANGUAGE SWITCHER ──────────────────────────────────────────────
   Turns the "IN (EN)" label in the header into a real picker.

   Translation is done by Google's Translate Element, which is what makes
   "any language" possible without maintaining ~130 sets of copy. The
   third-party script is loaded lazily: not at all for an English visitor
   who never opens the picker.

   The chosen language lives in the `googtrans` cookie, which is what the
   widget itself reads, so the choice survives navigation between pages.  */
(function () {
    'use strict';

    var LANGS = [
        ['en', 'English', 'English'], ['hi', 'Hindi', 'हिन्दी'],
        ['bn', 'Bengali', 'বাংলা'], ['te', 'Telugu', 'తెలుగు'],
        ['mr', 'Marathi', 'मराठी'], ['ta', 'Tamil', 'தமிழ்'],
        ['gu', 'Gujarati', 'ગુજરાતી'], ['kn', 'Kannada', 'ಕನ್ನಡ'],
        ['ml', 'Malayalam', 'മലയാളം'], ['pa', 'Punjabi', 'ਪੰਜਾਬੀ'],
        ['or', 'Odia', 'ଓଡ଼ିଆ'], ['as', 'Assamese', 'অসমীয়া'],
        ['ur', 'Urdu', 'اردو'], ['ne', 'Nepali', 'नेपाली'],
        ['si', 'Sinhala', 'සිංහල'], ['sa', 'Sanskrit', 'संस्कृतम्'],
        ['ar', 'Arabic', 'العربية'], ['fa', 'Persian', 'فارسی'],
        ['he', 'Hebrew', 'עברית'], ['tr', 'Turkish', 'Türkçe'],
        ['zh-CN', 'Chinese (Simplified)', '简体中文'],
        ['zh-TW', 'Chinese (Traditional)', '繁體中文'],
        ['ja', 'Japanese', '日本語'], ['ko', 'Korean', '한국어'],
        ['th', 'Thai', 'ไทย'], ['vi', 'Vietnamese', 'Tiếng Việt'],
        ['id', 'Indonesian', 'Bahasa Indonesia'], ['ms', 'Malay', 'Bahasa Melayu'],
        ['tl', 'Filipino', 'Filipino'], ['my', 'Burmese', 'မြန်မာ'],
        ['km', 'Khmer', 'ខ្មែរ'], ['lo', 'Lao', 'ລາວ'],
        ['fr', 'French', 'Français'], ['de', 'German', 'Deutsch'],
        ['es', 'Spanish', 'Español'], ['pt', 'Portuguese', 'Português'],
        ['it', 'Italian', 'Italiano'], ['nl', 'Dutch', 'Nederlands'],
        ['ru', 'Russian', 'Русский'], ['uk', 'Ukrainian', 'Українська'],
        ['pl', 'Polish', 'Polski'], ['ro', 'Romanian', 'Română'],
        ['el', 'Greek', 'Ελληνικά'], ['cs', 'Czech', 'Čeština'],
        ['sk', 'Slovak', 'Slovenčina'], ['hu', 'Hungarian', 'Magyar'],
        ['sv', 'Swedish', 'Svenska'], ['no', 'Norwegian', 'Norsk'],
        ['da', 'Danish', 'Dansk'], ['fi', 'Finnish', 'Suomi'],
        ['is', 'Icelandic', 'Íslenska'], ['bg', 'Bulgarian', 'Български'],
        ['sr', 'Serbian', 'Српски'], ['hr', 'Croatian', 'Hrvatski'],
        ['bs', 'Bosnian', 'Bosanski'], ['sl', 'Slovenian', 'Slovenščina'],
        ['mk', 'Macedonian', 'Македонски'], ['sq', 'Albanian', 'Shqip'],
        ['lt', 'Lithuanian', 'Lietuvių'], ['lv', 'Latvian', 'Latviešu'],
        ['et', 'Estonian', 'Eesti'], ['ga', 'Irish', 'Gaeilge'],
        ['cy', 'Welsh', 'Cymraeg'], ['gl', 'Galician', 'Galego'],
        ['ca', 'Catalan', 'Català'], ['eu', 'Basque', 'Euskara'],
        ['mt', 'Maltese', 'Malti'], ['be', 'Belarusian', 'Беларуская'],
        ['ka', 'Georgian', 'ქართული'], ['hy', 'Armenian', 'Հայերեն'],
        ['az', 'Azerbaijani', 'Azərbaycan'], ['kk', 'Kazakh', 'Қазақ'],
        ['ky', 'Kyrgyz', 'Кыргызча'], ['uz', 'Uzbek', 'Oʻzbek'],
        ['tg', 'Tajik', 'Тоҷикӣ'], ['mn', 'Mongolian', 'Монгол'],
        ['ps', 'Pashto', 'پښتو'], ['ku', 'Kurdish', 'Kurdî'],
        ['sw', 'Swahili', 'Kiswahili'], ['am', 'Amharic', 'አማርኛ'],
        ['ha', 'Hausa', 'Hausa'], ['yo', 'Yoruba', 'Yorùbá'],
        ['ig', 'Igbo', 'Igbo'], ['zu', 'Zulu', 'isiZulu'],
        ['xh', 'Xhosa', 'isiXhosa'], ['st', 'Sesotho', 'Sesotho'],
        ['sn', 'Shona', 'chiShona'], ['ny', 'Chichewa', 'Chichewa'],
        ['so', 'Somali', 'Soomaali'], ['rw', 'Kinyarwanda', 'Kinyarwanda'],
        ['mg', 'Malagasy', 'Malagasy'], ['af', 'Afrikaans', 'Afrikaans'],
        ['la', 'Latin', 'Latina'], ['eo', 'Esperanto', 'Esperanto'],
        ['haw', 'Hawaiian', 'ʻŌlelo Hawaiʻi'], ['mi', 'Maori', 'Māori'],
        ['sm', 'Samoan', 'Gagana Samoa'], ['jw', 'Javanese', 'Basa Jawa'],
        ['su', 'Sundanese', 'Basa Sunda'], ['ceb', 'Cebuano', 'Cebuano'],
        ['hmn', 'Hmong', 'Hmoob'], ['yi', 'Yiddish', 'ייִדיש'],
        ['lb', 'Luxembourgish', 'Lëtzebuergesch'], ['fy', 'Frisian', 'Frysk'],
        ['gd', 'Scots Gaelic', 'Gàidhlig'], ['co', 'Corsican', 'Corsu'],
        ['ht', 'Haitian Creole', 'Kreyòl Ayisyen'], ['sd', 'Sindhi', 'سنڌي'],
        ['ug', 'Uyghur', 'ئۇيغۇرچە']
    ];

    var COOKIE = 'googtrans';
    var SOURCE = 'en';
    var scriptLoading = false;

    // ── cookie helpers ────────────────────────────────────────────────
    // The widget writes googtrans on the registrable domain, so on
    // www.securetechav.com the cookie lands on ".securetechav.com" while the
    // page is served from "www.securetechav.com". Deleting only the exact
    // hostname left that one alive and every reload re-translated. Walk the
    // whole suffix chain instead; writes to a public suffix are simply
    // ignored by the browser.
    function domainVariants() {
        var host = location.hostname;
        var out = [null];                     // host-only cookie
        if (host.indexOf('.') === -1) return out;          // localhost
        if (/^[0-9.]+$/.test(host)) return out;            // bare IP
        var parts = host.split('.');
        for (var i = 0; i <= parts.length - 2; i++) {
            var d = parts.slice(i).join('.');
            out.push(d, '.' + d);
        }
        return out;
    }

    function readLang() {
        // several googtrans cookies can coexist across domain scopes; the
        // language is whatever the last well-formed one says
        var found = SOURCE;
        var all = document.cookie.split(';');
        for (var i = 0; i < all.length; i++) {
            var kv = all[i].split('=');
            if (kv.shift().trim() !== COOKIE) continue;
            var parts = decodeURIComponent(kv.join('=')).split('/');
            if (parts[2]) found = parts[2];
        }
        return found;
    }

    function clearLang() {
        var doms = domainVariants();
        var paths = ['/', location.pathname];
        for (var i = 0; i < doms.length; i++) {
            for (var j = 0; j < paths.length; j++) {
                var c = COOKIE + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=' + paths[j];
                if (doms[i]) c += ';domain=' + doms[i];
                document.cookie = c;
            }
        }
        // Google also honours a #googtrans(..) fragment
        if (location.hash.indexOf('googtrans') !== -1) {
            history.replaceState(null, '', location.pathname + location.search);
        }
    }

    function writeLang(code) {
        clearLang();                          // never leave a stale scope behind
        if (code === SOURCE) return;
        var value = '/' + SOURCE + '/' + code;
        var doms = domainVariants();
        for (var i = 0; i < doms.length; i++) {
            var c = COOKIE + '=' + value + ';path=/';
            if (doms[i]) c += ';domain=' + doms[i];
            document.cookie = c;
        }
    }

    function labelFor(code) {
        for (var i = 0; i < LANGS.length; i++) {
            if (LANGS[i][0] === code) return LANGS[i];
        }
        return LANGS[0];
    }

    function shortCode(code) {
        return code.split('-')[0].toUpperCase();
    }

    // ── Google Translate Element ──────────────────────────────────────
    window.googleTranslateElementInit = function () {
        if (!window.google || !google.translate) return;
        new google.translate.TranslateElement(
            { pageLanguage: SOURCE, autoDisplay: false },
            'google_translate_element'
        );
    };

    function loadTranslate() {
        if (scriptLoading || document.getElementById('goog-translate-script')) return;
        scriptLoading = true;
        if (!document.getElementById('google_translate_element')) {
            var holder = document.createElement('div');
            holder.id = 'google_translate_element';
            document.body.appendChild(holder);
        }
        var sc = document.createElement('script');
        sc.id = 'goog-translate-script';
        sc.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        sc.async = true;
        document.head.appendChild(sc);
    }

    // Drive the widget's own <select> when it exists, so switching between
    // two translated languages does not need a page reload.
    function applyNow(code) {
        var sel = document.querySelector('select.goog-te-combo');
        if (!sel) return false;
        sel.value = code;
        sel.dispatchEvent(new Event('change'));
        return true;
    }

    function setLang(code) {
        var current = readLang();
        if (code === current) return;
        writeLang(code);
        try { localStorage.setItem('stav-lang', code); } catch (e) { }

        if (code === SOURCE) {
            // Reload to the clean URL. The widget rewrote the DOM in place and
            // there is no reliable way to put the original text back.
            location.replace(location.pathname + location.search);
            return;
        }
        if (!applyNow(code)) location.reload();
        else paintTriggers(code);
    }

    // ── UI ────────────────────────────────────────────────────────────
    function paintTriggers(code) {
        var entry = labelFor(code);
        var labels = document.querySelectorAll('[data-lang-label]');
        for (var i = 0; i < labels.length; i++) {
            labels[i].textContent = 'IN (' + shortCode(entry[0]) + ')';
        }
    }

    function buildPanel(wrap, btn) {
        var panel = document.createElement('div');
        // the list is language names in their own scripts - never translate it
        panel.className = 'lang-panel notranslate';
        panel.setAttribute('translate', 'no');
        panel.setAttribute('role', 'dialog');
        panel.setAttribute('aria-label', 'Choose a language');

        var search = document.createElement('input');
        search.type = 'search';
        search.className = 'lang-search';
        search.placeholder = 'Search languages';
        search.setAttribute('aria-label', 'Search languages');

        var list = document.createElement('ul');
        list.className = 'lang-list';

        var empty = document.createElement('p');
        empty.className = 'lang-empty';
        empty.textContent = 'No language matches that search.';
        empty.hidden = true;

        var note = document.createElement('p');
        note.className = 'lang-note';
        note.textContent = 'Translations are machine generated. English is the original.';

        var current = readLang();
        var rows = [];

        for (var i = 0; i < LANGS.length; i++) {
            (function (lang) {
                var li = document.createElement('li');
                var b = document.createElement('button');
                b.type = 'button';
                b.setAttribute('aria-current', String(lang[0] === current));
                b.innerHTML = '<span>' + lang[1] + '</span>' +
                    (lang[1] !== lang[2] ? '<span class="lang-native">' + lang[2] + '</span>' : '');
                b.addEventListener('click', function () {
                    close();
                    setLang(lang[0]);
                });
                li.appendChild(b);
                list.appendChild(li);
                rows.push({ li: li, hay: (lang[1] + ' ' + lang[2] + ' ' + lang[0]).toLowerCase() });
            })(LANGS[i]);
        }

        search.addEventListener('input', function () {
            var q = search.value.trim().toLowerCase();
            var hits = 0;
            for (var i = 0; i < rows.length; i++) {
                var show = !q || rows[i].hay.indexOf(q) !== -1;
                rows[i].li.hidden = !show;
                if (show) hits++;
            }
            empty.hidden = hits > 0;
        });

        panel.appendChild(search);
        panel.appendChild(list);
        panel.appendChild(empty);
        panel.appendChild(note);
        wrap.appendChild(panel);

        function open() {
            // only reach for Google's script once someone actually wants it
            loadTranslate();
            panel.classList.add('open');
            btn.setAttribute('aria-expanded', 'true');
            search.value = '';
            search.dispatchEvent(new Event('input'));
            search.focus();
        }

        function close() {
            panel.classList.remove('open');
            btn.setAttribute('aria-expanded', 'false');
        }

        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            panel.classList.contains('open') ? close() : open();
        });

        document.addEventListener('click', function (e) {
            if (!wrap.contains(e.target)) close();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && panel.classList.contains('open')) {
                close();
                btn.focus();
            }
        });
    }

    function init() {
        var wraps = document.querySelectorAll('.lang-wrap');
        for (var i = 0; i < wraps.length; i++) {
            var btn = wraps[i].querySelector('.nav-lang');
            if (btn) buildPanel(wraps[i], btn);
        }
        var active = readLang();
        paintTriggers(active);
        // a language is already chosen, so the widget has to come up with the page
        if (active !== SOURCE) loadTranslate();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
