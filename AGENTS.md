# PSA Role

This repository is a PSA Runtime Provider.

## Responsibilities

MUST:

- implement PSA Runtime Contract
- maintain runtime execution evidence
- preserve semantic provenance
- run `psa-validator` before submitting changes

MUST NOT:

- redefine PSA Core Semantic Model primitives
- author domain ontologies
- implement business application behavior
- bypass PSA Registry governance

## Before Changes

1. Read PSA Engineering Baseline v0.1.0
2. Assess contract impact
3. Run `./tools/psa-validator check .`
4. Update ADR when architecture changes
