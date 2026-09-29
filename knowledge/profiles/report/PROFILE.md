---
name: report
description: Write a short report from the documents in the knowledge store - reading only, no telemetry.
skills: []
context: lean
---

# Report

This task is a report, not a diagnosis. Do not call telemetry tools: everything the report needs
is in documents.

1. List `knowledge://system` and `knowledge://tenant/current` to see which documents exist.
2. Read the documents the request is about with `read_document`.
3. Write the report as Markdown to `workspace://current/report.md` with `write_file`: a title, a
   few short sections, and a closing list of the documents you read.
4. Finish with a two-sentence summary of the report, citing `read_document` and `write_file`.
