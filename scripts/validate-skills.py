#!/usr/bin/env python3
"""
Skill 验证脚本

检查所有 Skill 是否符合项目规范

Usage:
    python scripts/validate-skills.py
    python scripts/validate-skills.py --verbose
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"

# 必需文件
REQUIRED_FILES = ["README.md", "SKILL.md"]

# 可选但推荐的文件
RECOMMENDED_FILES = ["CHANGELOG.md"]


def check_frontmatter(skill_path: Path) -> List[str]:
    """检查 SKILL.md 的 frontmatter 格式"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return ["缺少 SKILL.md 文件"]
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 检查 frontmatter 开始
    if not content.startswith("---"):
        errors.append("SKILL.md 缺少 frontmatter 开始标记 '---'")
        return errors
    
    # 提取 frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter 格式不正确")
        return errors
    
    frontmatter = parts[1].strip()
    
    # 检查必需字段
    if "name:" not in frontmatter:
        errors.append("SKILL.md frontmatter 缺少 'name:' 字段")
    
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter 缺少 'description:' 字段")
    
    return errors


def check_required_sections(skill_path: Path) -> List[str]:
    """检查 SKILL.md 是否包含必需章节"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return errors
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 移除 frontmatter 后检查
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
    
    # 必需章节
    required_sections = [
        "## Purpose",
        "## Prerequisites",
        "## Usage",
        "## Architecture",
        "## Error Handling"
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"SKILL.md 缺少章节: {section}")
    
    return errors


def check_scripts_directory(skill_path: Path) -> List[str]:
    """检查 scripts 目录"""
    errors = []
    scripts_dir = skill_path / "scripts"
    
    if not scripts_dir.exists():
        errors.append("缺少 scripts/ 目录")
        return errors
    
    # 检查是否有可执行脚本
    script_files = list(scripts_dir.glob("*.py")) + \
                   list(scripts_dir.glob("*.js")) + \
                   list(scripts_dir.glob("*.ps1")) + \
                   list(scripts_dir.glob("*.sh"))
    
    if not script_files:
        errors.append("scripts/ 目录中没有可执行脚本")
    
    return errors


def validate_skill(skill_name: str, verbose: bool = False) -> Dict:
    """验证单个 Skill，返回验证结果"""
    skill_path = SKILLS_DIR / skill_name
    
    result = {
        "name": skill_name,
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    if verbose:
        print(f"\n📁 检查 Skill: {skill_name}")
    
    # 检查必需文件
    for file in REQUIRED_FILES:
        file_path = skill_path / file
        if not file_path.exists():
            result["errors"].append(f"缺少必需文件: {file}")
            result["valid"] = False
        elif verbose:
            print(f"  ✅ 找到 {file}")
    
    # 检查推荐文件
    for file in RECOMMENDED_FILES:
        file_path = skill_path / file
        if not file_path.exists():
            result["warnings"].append(f"缺少推荐文件: {file}")
        elif verbose:
            print(f"  ✅ 找到 {file}")
    
    # 检查 frontmatter
    frontmatter_errors = check_frontmatter(skill_path)
    if frontmatter_errors:
        result["errors"].extend(frontmatter_errors)
        result["valid"] = False
    elif verbose:
        print(f"  ✅ Frontmatter 格式正确")
    
    # 检查必需章节
    section_errors = check_required_sections(skill_path)
    if section_errors:
        result["errors"].extend(section_errors)
        result["valid"] = False
    elif verbose:
        print(f"  ✅ 包含所有必需章节")
    
    # 检查 scripts 目录
    script_errors = check_scripts_directory(skill_path)
    if script_errors:
        result["errors"].extend(script_errors)
        result["valid"] = False
    elif verbose:
        print(f"  ✅ Scripts 目录检查通过")
    
    return result


def print_result(result: Dict):
    """打印验证结果"""
    status = "✅" if result["valid"] else "❌"
    print(f"\n{status} {result['name']}")
    
    if result["errors"]:
        print("  错误:")
        for error in result["errors"]:
            print(f"    ❌ {error}")
    
    if result["warnings"]:
        print("  警告:")
        for warning in result["warnings"]:
            print(f"    ⚠️  {warning}")
    
    if result["valid"] and not result["warnings"]:
        print("  ✅ 所有检查通过")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="验证 Trae Agent Skills")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="显示详细输出")
    parser.add_argument("--skill", "-s", type=str,
                        help="只验证指定的 Skill")
    args = parser.parse_args()
    
    print("🔍 开始验证 Skills...")
    print("=" * 50)
    
    if not SKILLS_DIR.exists():
        print(f"❌ Skills 目录不存在: {SKILLS_DIR}")
        sys.exit(1)
    
    results = []
    
    if args.skill:
        # 只验证指定 Skill
        skill_path = SKILLS_DIR / args.skill
        if not skill_path.exists():
            print(f"❌ Skill 不存在: {args.skill}")
            sys.exit(1)
        results.append(validate_skill(args.skill, args.verbose))
    else:
        # 验证所有 Skills
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                result = validate_skill(skill_dir.name, args.verbose)
                results.append(result)
    
    # 打印结果摘要
    if not args.verbose:
        for result in results:
            print_result(result)
    
    # 最终摘要
    print("\n" + "=" * 50)
    total = len(results)
    valid = sum(1 for r in results if r["valid"])
    
    print(f"总计: {total} 个 Skill")
    print(f"通过: {valid} 个")
    print(f"失败: {total - valid} 个")
    
    if valid == total:
        print("\n✨ 所有 Skills 验证通过！")
        return 0
    else:
        print("\n⚠️  存在验证错误，请修复后重试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
