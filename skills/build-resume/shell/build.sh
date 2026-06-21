#!/bin/bash
# 编译简历 LaTeX 为 PDF
# 依赖：XeTeX（MiKTeX / TeX Live）
# 用法：bash build.sh

# 导航到项目根目录
cd "$(dirname "$0")/../../../.."
TEMPLATE_DIR=".claude/skills/build-resume/template"

# ============ 自清理：编译后移除根目录的模板副本 ============
cleanup() {
    for f in "$TEMPLATE_DIR"/*.cls "$TEMPLATE_DIR"/*.sty; do
        base=$(basename "$f")
        [ -f "./$base" ] && rm -f "./$base"
    done
}
trap cleanup EXIT

# ============ 检查 xelatex 是否存在 ============
if ! command -v xelatex &> /dev/null; then
    echo "错误: 未检测到 LaTeX 编译环境 (xelatex)"
    echo ""
    echo "请先安装 MiKTeX:"
    echo "  winget install MiKTeX.MiKTeX"
    echo ""
    echo "或访问: https://miktex.org/download"
    echo ""
    exit 1
fi

# ============ 快速检查关键宏包 ============
if command -v mpm &> /dev/null; then
    missing=""
    for pkg in xecjk geometry ctex fontspec; do
        if ! mpm --list 2>/dev/null | grep -qi "$pkg"; then
            missing="$missing $pkg"
        fi
    done
    if [ -n "$missing" ]; then
        echo "关键宏包缺失或未确认:$missing"
        echo "请先运行初始化脚本:"
        echo "  bash .claude/skills/build-resume/shell/install-packages.sh"
        echo ""
        exit 1
    fi
fi

# ============ MiKTeX 自动安装配置 ============
initexmf --set-config-value "[MPM]AutoInstall=1" 2>/dev/null || true

# ============ 创建 build 目录 ============
mkdir -p build

# ============ 复制模板文件到根目录（MiKTeX 不支持 TEXINPUTS）============
cp "$TEMPLATE_DIR"/*.cls "$TEMPLATE_DIR"/*.sty ./

# ============ 编译简历 ============
echo "编译 resume.tex ..."
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build resume.tex 2>&1 | tail -15
echo ""
echo "再次编译以解决交叉引用 ..."
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build resume.tex 2>&1 | tail -15

# ============ 复制 PDF 到根目录 ============
if [ -f build/resume.pdf ]; then
    cp build/resume.pdf ./resume.pdf 2>/dev/null || true
    echo ""
    echo "✓ PDF 生成成功: resume.pdf"
    ls -lh build/resume.pdf
else
    echo ""
    echo "✗ 编译失败，请检查上方错误信息"
    exit 1
fi
