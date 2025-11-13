import json
import os
from flask import g, request, session
from typing import Dict

_translations: Dict[str, Dict[str, str]] = {}
_translations_mtime: Dict[str, float] = {}
_base_dir = None
_default_lang = "pt-br"
_supported_langs = ["pt-br", "en", "es"]


def init_i18n(app):
    global _default_lang, _supported_langs, _base_dir
    _default_lang = app.config.get("DEFAULT_LANG", _default_lang)
    _supported_langs = app.config.get("LANGUAGES", _supported_langs)
    _base_dir = os.path.join(os.getcwd(), "locales")
    for lang in _supported_langs:
        path = os.path.join(_base_dir, f"{lang}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _translations[lang] = json.load(f)
            _translations_mtime[lang] = os.path.getmtime(path)
        except FileNotFoundError:
            _translations[lang] = {}
            _translations_mtime[lang] = 0.0


def set_lang_from_request():
    _reload_if_changed()
    lang = request.args.get("lang")
    if lang and lang in _supported_langs:
        session["lang"] = lang
    g.lang = session.get("lang") or _negotiate_language(request.headers.get("Accept-Language")) or _default_lang


def _reload_if_changed():
    # Lightweight dev hot-reload: if locale files changed, reload them.
    if not _base_dir:
        return
    for lang in _supported_langs:
        path = os.path.join(_base_dir, f"{lang}.json")
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            continue
        if _translations_mtime.get(lang, 0) < mtime:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _translations[lang] = json.load(f)
                _translations_mtime[lang] = mtime
            except Exception:
                # keep previous translations on error
                pass


def _negotiate_language(header: str):
    if not header:
        return None
    try:
        parts = [p.split(";")[0].strip().lower() for p in header.split(",")]
    except Exception:
        return None
    for p in parts:
        if p in _supported_langs:
            return p
        # fallback for regional variants e.g., en-US -> en
        base = p.split("-")[0]
        for s in _supported_langs:
            if s.split("-")[0] == base:
                return s
    return None


def get_current_lang():
    return getattr(g, "lang", _default_lang)


def t(key: str, **kwargs) -> str:
    # Ensure latest translations are loaded in dev
    _reload_if_changed()
    lang = get_current_lang()
    val = _translations.get(lang, {}).get(key)
    if val is None:
        val = _translations.get("en", {}).get(key, key)
    try:
        return val.format(**kwargs)
    except Exception:
        return val
