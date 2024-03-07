## General checks

- OpenAPI validated - OK
- Security check - bandit - OK
- format, linter, etc. - issues found (depends on the env settings)
- No tests (zero codecoverage) within the repo

## Endpoint analysis

- GET `api/v1/machines/`
  - when expecting a response (data type is valid), server respons funny and humorous but non-production response `418`!
- GET `api/v1/machines/{id}`
  - Same statu code as above. Getting  `404` would be appropriate return code for non-existing objects.
- POST `api/v1/machines/`
  - When payload contains `MacOS` parameter in `template`, it creates `Linux` object instead.
- DELETE `api/v1/machines/{ID}`
  - Object is not really deleted and this endpoint allows to "delete" the same object endlessly (still getting ret code `200`).
  - This operation only updates objects parameter with the latest delete action.
- GET `api/v1/machines/secret_machines/`
  - Always `403` error without any further docs about required auth method etc.

## DOCS check

- `READMME.md` - non-update text not corresponding with endpoint configuration:
  - `the_always_supported_DOS` - doesn't exist anymore
  - `the_never_known_ChromeOS` - different wording
  - parameter `custom_name` is required (even stated as optional here)
