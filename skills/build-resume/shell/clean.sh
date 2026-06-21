#!/bin/bash
# 清理 LaTeX 编译产物
# 用法：bash clean.sh

cd "$(dirname "$0")/../../../.."

# 清理 build/ 目录
if [ -d build ]; then
    rm -rf build/*
    echo "✓ build/ 已清理"
else
    echo "build/ 目录不存在，无需清理"
fi

# 归档 resume.tex 到 build/ 后删除根目录的
if [ -f resume.tex ]; then
    mkdir -p build
    cp resume.tex build/resume.tex
    rm -f resume.tex
    echo "✓ resume.tex 已归档至 build/ 并从根目录移除"
fi

# 清理 build.sh 复制到根目录的模板文件
TEMPLATE_DIR=".claude/skills/build-resume/template"
for f in "$TEMPLATE_DIR"/*.cls "$TEMPLATE_DIR"/*.sty; do
    base=$(basename "$f")
    if [ -f "./$base" ]; then
        rm -f "./$base"
        echo "✓ 已清理 ./$base"
    fi
done
