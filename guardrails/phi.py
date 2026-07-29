"""PHI detection + redaction via Microsoft Presidio.

Presidio ships recognizers for names, SSNs, phone numbers, dates, locations, and
US medical identifiers. Run it on BOTH inputs (before anything leaves your app)
and outputs (defense in depth).
"""
_analyzer = None
_anonymizer = None


def _lazy():
    global _analyzer, _anonymizer
    if _analyzer is None:
        from presidio_analyzer import AnalyzerEngine
        from presidio_anonymizer import AnonymizerEngine
        _analyzer = AnalyzerEngine()
        _anonymizer = AnonymizerEngine()


def redact(text):
    """Return (redacted_text, found_bool)."""
    if not text:
        return text, False
    _lazy()
    results = _analyzer.analyze(text=text, language="en")
    if not results:
        return text, False
    out = _anonymizer.anonymize(text=text, analyzer_results=results)
    return out.text, True
