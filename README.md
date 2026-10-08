# ShizuSU-Xposed

ShizuSU 管理器的 **LSPosed (Xposed) 模块仓库镜像**。本仓库镜像官方 LSPosed OnlineModule 列表，供管理器「Xposed 仓库」页直接读取，无需依赖官方源在国内的可达性。

## 数据来源
- 主源：`https://backup.modules.lsposed.org/modules.json`（官方备份镜像，PC 实测 HTTP 200）
- 备源：`https://modules.lsposed.org/modules.json`（官方主源，部分网络下 403）
- 数据结构：官方 OnlineModule JSON 数组，字段与官方完全对齐（`name / description / url / homepageUrl / collaborators / summary / sourceUrl / scope / releases / latestReleaseTime` 等），未做裁剪。

## 同步机制
- `.github/workflows/xposed-sync.yml`：每日定时（cron）+ 手动 `workflow_dispatch`。
- 拉取主源 → 失败回退备源 → 与当前根 `modules.json` 对比 → 有变化才 commit + push 到 `main`（使用 `GITHUB_TOKEN`）。
- 无变化不产生提交。

## 格式说明
根目录 `modules.json` 为 **JSON 数组**（OnlineModule[]），单条示例：
```json
{
  "name": "io.github.example.module",
  "description": "...",
  "summary": "...",
  "url": "https://github.com/...",
  "sourceUrl": "...",
  "releases": [ ... ],
  "latestReleaseTime": "2026-..."
}
```

## 使用
- 商店源（Pages）：`https://qianyumeng0228.github.io/ShizuSU-Xposed/`
- 原始数据：`https://raw.githubusercontent.com/qianyumeng0228/ShizuSU-Xposed/main/modules.json`

> 本仓库为只读镜像，请勿直接提 PR 修改 `modules.json`（会被下次同步覆盖）。
