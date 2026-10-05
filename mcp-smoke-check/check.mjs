#!/usr/bin/env node
// Reusable, dependency-free MCP interoperability check for the LessonLoop project.
const endpoint = process.argv[2] || 'http://127.0.0.1:3000/mcp';
const protocolVersion = '2025-11-25';
let id = 0;
async function request(method, params = {}) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream', 'mcp-protocol-version': protocolVersion },
    body: JSON.stringify({ jsonrpc: '2.0', id: ++id, method, params })
  });
  if (!response.ok) throw new Error(`${method}: HTTP ${response.status}`);
  const rpc = await response.json();
  if (rpc.id !== id || rpc.error) throw new Error(`${method}: ${JSON.stringify(rpc.error || 'unexpected response ID')}`);
  return rpc.result;
}
async function call(name, args) {
  const result = await request('tools/call', { name, arguments: args });
  if (result.isError) throw new Error(`${name}: ${result.content?.[0]?.text}`);
  return JSON.parse(result.content[0].text);
}
try {
  const init = await request('initialize', { protocolVersion, capabilities: {}, clientInfo: { name: 'lessonloop-smoke-check', version: '1.0' } });
  if (init.protocolVersion !== protocolVersion) throw new Error('Unsupported negotiated protocol version');
  const listed = await request('tools/list');
  const names = listed.tools.map(tool => tool.name);
  for (const name of ['list_lessons', 'start_lesson', 'get_hint', 'submit_answer', 'get_progress']) {
    if (!names.includes(name)) throw new Error(`Missing tool: ${name}`);
  }
  const lessons = await call('list_lessons', {});
  if (!lessons.some(lesson => lesson.id === 'variables')) throw new Error('Variables lesson missing');
  const started = await call('start_lesson', { learner: 'Smoke Test', lessonId: 'variables' });
  const sessionId = started.session.id;
  const hinted = await call('get_hint', { sessionId });
  const answered = await call('submit_answer', { sessionId, answer: '5' });
  const progress = await call('get_progress', { sessionId });
  if (hinted.session.hints !== 1 || answered.session.status !== 'Completed' || progress.session.attempts !== 1) {
    throw new Error('Unexpected lesson progress');
  }
  console.log(JSON.stringify({ result: 'PASS', protocolVersion, discoveredTools: names, sessionId, status: progress.session.status }, null, 2));
} catch (error) {
  console.error(`FAIL: ${error.message}`);
  process.exitCode = 1;
}
