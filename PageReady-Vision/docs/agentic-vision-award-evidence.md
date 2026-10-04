# Agentic Vision Award Evidence

## Workflow diagram

```text
Document image
      |
      v
OpenCV perception: skew, confidence, blur, contrast, frame-edge evidence
      |
      v
Deterministic policy / orchestration
      |-------------------------|-------------------------|
      v                         v                         v
auto_correct deskew       request_rescan           send_to_human_review
      |                                                   |
      v                                                   v
verify_corrected_page                              clerk reviews evidence
      |                                                   |
      v                                                   v
approve, or escalate --------------------------> approve with required note
      |
      v
Auditable, image-free event trace
```

## Trace demonstration

The `council-minutes-skewed.png` fixture proves that a vision measurement
changes later behavior:

1. OpenCV measures a skew angle and confidence.
2. Policy selects `auto_correct` only in its validated range.
3. The deskew tool receives the measured angle as its parameter.
4. OpenCV re-analyzes the tool output.
5. The post-correction skew result determines whether the page is approved or
   sent to human review.

Every trace now includes a `runtime_provenance` event with the exact OpenCV
version used to produce that run. This makes it possible to distinguish an
OpenCV 5 demonstration from local development evidence.

Run and retain the artifact:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py --output runs\evaluation.json
```

The report records fixture-level expected/observed actions, tool sequences,
failure counts, unsafe-approval count, and runtime provenance. It is a smoke
evaluation only; do not present it as the 150-page holdout evaluation in
`docs/evaluation.md`.

## Human control and failure handling

- Blur triggers a rescan request rather than an invented correction.
- Low contrast, weak evidence, frame-edge content, or failed correction go to
  human review.
- A clerk can approve a review item only with a non-empty override note.
- The decision trace retains both machine evidence and the clerk action.

## Submission checklist

- Show this diagram or the equivalent architecture diagram.
- Show the skewed fixture's initial evidence, `auto_correct` tool event,
  verification event, and changed final action in one continuous capture.
- Show `runtime_provenance` reporting OpenCV 5.x. Do not claim OpenCV 5 until
  that captured value is actually 5.x.
- Include `runs/evaluation.json`, labeled with its recorded environment and
  limited scope.
