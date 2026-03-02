const { execFile } = require('child_process');
const path = require('path');

const PYTHON_SCRIPT = path.resolve(__dirname, '../cooder_agent.py');

module.exports = {
  name: 'cooder-agent',
  version: '1.0.0',
  description: 'Multi-role Cooder agent skills',

  async developer(context, codeDesc) {
    const result = await this.runPython('developer', { codeDesc });
    return result;
  },

  async dataAnalyst(context, csvPath) {
    const result = await this.runPython('data-analyst', { csvPath });
    return result;
  },

  async devops(context, dockerSpec) {
    const result = await this.runPython('devops', { dockerSpec });
    return result;
  },

  async contentWriter(context, topic) {
    const result = await this.runPython('content-writer', { topic });
    return result;
  },

  async designer(context, htmlCssSpec) {
    const result = await this.runPython('designer', { htmlCssSpec });
    return result;
  },

  async runPython(mode, params = {}) {
    return new Promise((resolve, reject) => {
      const args = ['--mode', mode];
      Object.entries(params).forEach(([k, v]) => args.push(`--${k}`, v));
      execFile('python3', [PYTHON_SCRIPT, ...args], (error, stdout, stderr) => {
        if (error) {
          reject(error);
          return;
        }
        try {
          const json = JSON.parse(stdout);
          resolve(json);
        } catch (e) {
          reject(new Error(stderr || 'Invalid JSON output'));
        }
      });
    });
  }
};