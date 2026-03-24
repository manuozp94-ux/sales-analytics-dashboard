# Release Bundle Checklist

Use this checklist before treating a Fabric engagement release as implementation-complete.

## Required Contracts

- `engagement_manifest`
- `environment_contract`
- `semantic_model_contract`
- `governance_pack`

## Required Build and Validation Artifacts

- Warehouse SQL pack or Fabric deploy manifest
- latest Fabric inventory diff
- latest Warehouse probe report
- latest parity comparison report
- rollback notes or recovery path

## Required Review Gates

- SQL guardrails passed
- environment target confirmed
- semantic-model assumptions reviewed
- governance/security pack reviewed
- production approver sign-off recorded when production is in scope

## Required Continuity Artifacts

- change summary note
- updated project memory or engagement memory
- resume point for next operator
