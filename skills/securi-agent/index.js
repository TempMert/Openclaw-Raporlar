const { execFile } = require('child_process');
const path = require('path');

const PYTHON_SCRIPT = path.resolve(__dirname, '../securi_agent.py');

module.exports = {
  name: 'securi-agent',
  version: '1.0.0',
  description: 'Self-improvement, ontology, answeroverflow for Securi',

  async selfImprove(context) {
    const result = await this.runPython('self-improve');
    return result;
  },

  async ontology(context) {
    const result = await this.runPython('ontology');
    return result;
  },

  async answerOverflow(context) {
    const result = await this.runPython('answeroverflow');
    return result;
  },

  async runPython(mode) {
    return new Promise((resolve, reject) => {
      execFile('python3', [PYTHON_SCRIPT, '--mode', mode], (error, stdout, stderr) => {
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