# Session 8 Pydantic Structured Output Design

## Goal

Expand the structured output section in `material/Session 8/notebooks/01_llm_api_access.ipynb` so students see both the raw JSON Schema pattern and two Python-friendly Pydantic patterns.

## Design

Keep the existing JSON Schema example as the first structured-output example because it exposes the underlying contract clearly. Add a short explanatory markdown cell after it that explains why Python applications often prefer typed objects over raw JSON strings.

Then add two complementary Pydantic examples:

1. `client.responses.parse(...)` with a Pydantic `BaseModel`
   - Shows the highest-level Python workflow.
   - Emphasizes that the SDK can return a validated object directly via `output_parsed`.

2. `client.responses.create(...)` plus `BaseModel.model_validate_json(...)`
   - Shows how to keep the lower-level response object while still validating the generated JSON with Pydantic.
   - Emphasizes that this is useful when the caller wants raw response access, explicit validation steps, or compatibility with existing code that already uses `responses.create(...)`.

## Supporting Changes

- Add `pydantic` to `requirements.txt` because it becomes a direct instructional dependency.
- Keep all rendering notebook-friendly with Markdown display rather than raw `print` for model content.

## Verification

- Confirm the edited notebook still parses as valid JSON.
- Confirm `pydantic` is listed in `requirements.txt`.
