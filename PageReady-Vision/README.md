# PageReady Vision

PageReady Vision is an agentic document-quality gate. It inspects an uploaded page, uses OpenCV evidence to choose a corrective or escalation tool, verifies any correction, and emits an auditable trace.

## Golden path

1. Analyze a document's visual evidence.
2. If the page has a confident, recoverable small skew, call `auto_correct`.
3. Re-analyze the corrected output with `verify_corrected_page`.
4. Approve only when verification succeeds; otherwise route it to human review.

The first milestone deliberately limits automatic correction to small skew. Blur, content near a frame edge, low contrast, conflicting evidence, and failed correction are fail-safe routes to human review or rescan.

## Local setup

Use a working Python 3.11+ installation, then install the package and tests:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

Run an image through the local golden path:

```powershell
python -m pageready.cli analyze .\example.png --output-dir .\runs
```

## Deployment note

The source uses stable OpenCV APIs so it can be tested locally. The competition deployment must run its core image workload with OpenCV 5 and, for the COOL track, verify the COOL runtime on AWS Graviton before claiming a benchmark result. Do not label a local development wheel as COOL.
