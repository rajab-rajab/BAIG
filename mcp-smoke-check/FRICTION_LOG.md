# LessonLoop hackathon friction log

Rajab Baig · Build, Ship, Shape: Amazon Developer Hackathon

## 1. First MCP endpoint check

- **Task attempted:** Confirm that the local LessonLoop MCP server was working and discover its tools.
- **Steps taken:** Started the Node.js server and opened `http://127.0.0.1:3000/mcp` in a browser.
- **Expected:** A visible tool list or a clear way to call a tool.
- **Actual:** The browser sent GET and showed a status page. MCP initialization and tool calls require HTTP POST, so I initially could not tell whether I had tested the protocol correctly.
- **Severity:** Important for onboarding; the project itself still worked.
- **Workaround:** Sent JSON-RPC initialization and `tools/list` requests in PowerShell, then completed a lesson with an independent MCP client.
- **Actionable suggestion:** Add a copyable “first five minutes” example showing initialization, tool discovery, and one tool call, with a note explaining what a browser GET to an MCP endpoint should show.

## 2. Local AWS setup on Windows

- **Task attempted:** Confirm local AWS identity before calling Amazon Bedrock from LessonLoop.
- **Steps taken:** Installed `@aws-sdk/client-bedrock-runtime`, then ran `aws sts get-caller-identity` in PowerShell.
- **Expected:** An AWS identity result that would confirm local credentials.
- **Actual:** PowerShell reported that `aws` was not recognized. Installing the project's JavaScript SDK did not also install the separate AWS CLI.
- **Severity:** Minor; it delayed the optional AWS test without affecting the core lessons.
- **Workaround:** Installed AWS CLI v2, signed in through the browser with `aws login`, and listed text models in the selected Region.
- **Actionable suggestion:** Provide a Windows walkthrough that distinguishes application SDK installation, AWS CLI installation, local sign-in, model selection, and the first Bedrock Converse call.

## 3. Distinguishing the primary project from the open source contribution

- **Task attempted:** Enter the Open Source mini challenge alongside the Alexa+ primary project.
- **Steps taken:** Read the mini challenge requirement, created a separate MCP smoke checker in my public [BAIG repository](https://github.com/rajab-rajab/BAIG), and opened [pull request #1](https://github.com/rajab-rajab/BAIG/pull/1).
- **Expected:** Initially, I thought the primary project repository might cover both parts of the entry.
- **Actual:** The mini challenge requires an additional public project or contribution and asks for its URL separately from the primary project repository URL.
- **Severity:** Important for submission clarity; misreading it could lead to an ineligible mini challenge entry.
- **Workaround:** Used the public pull request as the contribution URL and the [LessonLoop repository](https://github.com/rajab-rajab/lessonloop-alexa-mcp) as the project repository URL.
- **Actionable suggestion:** Show a short example beside the form fields that labels the primary project repository, the separate public contribution, and the GitHub username.

## Verification boundary

The original LessonLoop workflow passed automated tests and an independent MCP client check. The optional Bedrock code passed a simulated-response test. A live Bedrock response has not yet been confirmed, so I am not reporting AWS runtime reliability as a tested outcome.
