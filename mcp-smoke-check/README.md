# LessonLoop MCP smoke check

A small, dependency-free Node.js command that verifies a running [LessonLoop](https://github.com/rajab-rajab/lessonloop-alexa-mcp) MCP server from an independent process. It uses JSON-RPC over Streamable HTTP, negotiates protocol version `2025-11-25`, discovers tools, starts a variables lesson, requests a hint, submits the answer, and reads the saved progress. It exits nonzero when any step fails.

## Run

Start LessonLoop (`npm start`) in one terminal. With Node.js 20 or later, run in another:

```powershell
node .\mcp-smoke-check\check.mjs http://127.0.0.1:3000/mcp
```

The result includes `PASS`, the discovered tool names, and the completed test session. A pseudonym (`Smoke Test`) is saved in the local LessonLoop session store. The script does not call Amazon Bedrock or connect to an Alexa device. It assumes the original LessonLoop tool names and the variables exercise answer; it is intended as a focused interoperability test, not a general MCP certification suite.

This contribution is in the public [BAIG repository](https://github.com/rajab-rajab/BAIG) under its GPL-3.0 license. It helps developers confirm that the lesson workflow works beyond the browser interface.
