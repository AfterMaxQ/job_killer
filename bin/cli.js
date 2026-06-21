#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const force = args.includes('--force') || args.includes('-f');
const help = args.includes('--help') || args.includes('-h');

if (help) {
  console.log(`
  Job Killer — 求职技能工具链

  用法:
    npx @ethan_ray/job-killer           在当前目录安装 6 个 Claude Code 技能
    npx @ethan_ray/job-killer --force   强制覆盖已有技能
    npx @ethan_ray/job-killer --help    显示帮助

  安装内容:
    .claude/skills/          ← 6 个技能定义文件
    个人信息/                 ← 个人信息档案模板（空目录）
    images/                  ← 照片目录（放 you.jpg）
  `);
  process.exit(0);
}

const targetDir = process.cwd();
const sourceSkills = path.join(__dirname, '..', 'skills');
const claudeSkillsDir = path.join(targetDir, '.claude', 'skills');

// Check if already installed
if (fs.existsSync(claudeSkillsDir) && !force) {
  const existing = fs.readdirSync(claudeSkillsDir).filter(f => !f.startsWith('.'));
  if (existing.length > 0) {
    console.log(`\n.claude/skills/ 已有技能：${existing.join(', ')}`);
    console.log('如需覆盖，运行 npx @ethan_ray/job-killer --force\n');
    process.exit(0);
  }
}

// Create directories
fs.mkdirSync(claudeSkillsDir, { recursive: true });
fs.mkdirSync(path.join(targetDir, '个人信息'), { recursive: true });
fs.mkdirSync(path.join(targetDir, 'images'), { recursive: true });

// Copy skills
const skillNames = fs.readdirSync(sourceSkills).filter(f => !f.startsWith('.'));
for (const name of skillNames) {
  const src = path.join(sourceSkills, name);
  const dest = path.join(claudeSkillsDir, name);
  copyRecursive(src, dest);
}

console.log(`\n✓ Job Killer 安装完成！`);
console.log(`\n已安装 6 个技能：`);
for (const name of skillNames) {
  console.log(`  ├── ${name}`);
}
console.log(`\n下一步：运行 Claude Code，说 "开始" 或 "帮我" 启动新手引导\n`);

function copyRecursive(src, dest) {
  if (fs.statSync(src).isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.copyFileSync(src, dest);
  }
}
