# Platform Character Limits

Count the complete prompt, including spaces and excluding code fences.

## Maximum Characters

- **Default:** 5,000 characters
- **Dreamina:** 5,500 characters
- **Dreamina CLI:** 15,000 characters
- **Flova:** 4,500 characters
- **Artcraft:** 10,000 characters
- **OpenArt:** 8,000 characters
- **Vidu Q4:** 8,000 characters
- **Vidu Omni Pro:** 4,000 characters

## Selecting the Limit

- An explicit user-supplied character limit overrides the platform limit or default.
- When the user names a listed platform, use its limit. Dreamina and Dreamina CLI are separate entries.
- If no platform or explicit limit is supplied, use the 5,000-character default.
- If the named platform is not listed, use the 5,000-character default and identify it as the default, not a verified platform maximum.
