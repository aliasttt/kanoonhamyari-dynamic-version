# Compatibility workaround for Python 3.14 + Django 5.0.x admin template context copy crash
# See: AttributeError: 'super' object has no attribute 'dicts' on Context.__copy__
try:
    from django.template.context import Context

    def _safe_context_copy(self):
        """
        Minimal clone of django.template.Context used by inclusion tags.
        Avoids calling super().__copy__ which crashes on Python 3.14.
        """
        # Create a new empty Context with the same autoescape flag
        new_ctx = Context(autoescape=getattr(self, "autoescape", True))
        # Copy internal dict stack shallowly
        try:
            new_ctx.dicts = [d.copy() for d in getattr(self, "dicts", [])]
        except Exception:
            # Fallback: if dicts not present for any reason, initialize to [{}]
            new_ctx.dicts = [{}]
        # Preserve current_app if present (admin relies on it)
        if hasattr(self, "current_app"):
            new_ctx.current_app = self.current_app
        return new_ctx

    # Monkey patch once
    if not hasattr(Context.__copy__, "_kh_patched"):  # type: ignore[attr-defined]
        Context.__copy__ = _safe_context_copy  # type: ignore[assignment]
        setattr(Context.__copy__, "_kh_patched", True)  # mark as patched
except Exception:
    # If Django not loaded yet or signature changed, silently ignore
    pass







