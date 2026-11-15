# aneminence

Independent Creative & Technology Label — ASPIRE TO EMINENCE

官网：[aneminence.github.io](https://aneminence.github.io/) · [GitHub](https://github.com/aneminence)

轻量 HTML / CSS / JavaScript 网站，无运行时依赖。维护位置为 `D:\ANEMINENCE\aneminence.github.io`；VI 源项目位于同级 `aneminence-brand`。Studio / Labs / Craft 为平级业务，Works 是作品集栏目。

## 本地预览

```sh
python scripts/build.py
python scripts/check_site.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

访问 http://127.0.0.1:8000/ 。源码也可直接通过静态服务器预览。`_site` 是自动生成且忽略的发布目录，只包含页面、资产和 robots/sitemap，不包含工具、报告或完整 VI 工程。

## 目录

- `index.html`：页面结构；保留原 IDEAS INTO REALITY、灰色山体与网格构图。
- `styles.css`：品牌变量、字体、响应式和交互状态。
- `projects.js`：作品内容唯一来源。
- `main.js`：作品生成、分类、弹窗、移动导航与图片失败回退。
- `assets/brand`：来自 VI 的原几何 SVG 与色彩记录。
- `assets/projects`：当前作品展示，均按真实状态标注。
- `assets/fonts`：本地 WOFF2 子集、来源记录与 OFL 授权。
- `scripts/build.py`：输出带内容摘要的 CSS/JS 与页面版本标识。
- `scripts/check_site.py`：本地资源/锚点检查，或实际 HTTPS 发布检查。
- `scripts/browser_check.py`：可选开发测试，覆盖 Edge、Firefox、WebKit。
- `.github/workflows/deploy.yml`：语法检查、打包、发布、公共页面与资源验证。

## 更新作品

在 `projects.js` 增加或修改条目，必需字段为 id、category、type、title、subtitle、description、field、status、image、alt；外链使用可选 url 和 linkLabel。id 必须唯一，category 只能是 studio / labs / craft。

新作品自动生成图片卡片，筛选计数自动更新。收纳概念保留一个 CSS 视觉模板，其余使用数据中的图片。图片需授权，优先 SVG / WebP。概念、原型、设计评审和已发布项目必须区别标注。

**CMTS**：介绍站已上线：https://aneminence.github.io/cmts-website/zh/ 。Labs 条目 id 为 `cmts`，入口为「访问 CMTS 网站」，封面为公网界面。硬件图片仍标注为概念展示；后续更新修改该项 url、linkLabel、description、status 和 image 即可。不要发布 localhost / 127.0.0.1 预览链接。本网站的改动不涉及 CMTS 项目仓库。

## 品牌与字体

核心色：雪域白 #F7F7F5、石墨黑 #151719、Studio 性能红 #C8102E、Labs 冷钢蓝 #315F83；Craft 辅助灰 #737B83。灰色正文使用可读的 #59646B。正式 Logo 使用 V5 原路径，禁止以普通字体重新排字或改造轮廓。

字体为 Inter / Noto Sans SC，网页使用 OFL 授权的本地子集，完整许可证保存在 assets/fonts。新增中文内容后，重新执行以下可选维护步骤；未收录字形会退回系统中文字体，不会丢失文字：

```sh
python -m pip install -r requirements-dev.txt
python scripts/prepare_fonts.py --brand ../aneminence-brand
```

浏览器测试同样使用开发依赖。Windows 默认使用已安装 Edge，Firefox/WebKit 需要 `python -m playwright install firefox webkit`。运行 `python scripts/browser_check.py --report ../website-reports`。测试产物放在仓库外，不上传到官网。

## 自动发布与404排查

推送 main 后 GitHub Actions 自动检查并发布。也可在 Actions → Deploy website to GitHub Pages → Run workflow 手动发布。

```sh
git add index.html styles.css projects.js main.js assets scripts .github README.md requirements-dev.txt docs
git commit -m "Update portfolio"
git push origin main
```

Settings → Pages → Build and deployment → Source 应为 **GitHub Actions**。默认网站地址为 https://aneminence.github.io/ ，要求仓库名保持 `aneminence.github.io`。

2026-11-15 的404源于仓库改为私有后 Pages 被停用；仓库恢复公开后，已重新启用 Pages 并触发发布。GitHub Free 的 Pages 适用于公开仓库；支持私有仓库的计划见 [GitHub 官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。改回公开后仍须检查 Pages 是否已启用，不应只等待浏览器刷新。

部署工作流会校验公共 HTTPS 页面版本与资源。若失败，先看 Actions 日志、仓库可见性和 Pages Source，再检查最新提交是否已发布。

## 无障碍与配色

提供键盘焦点、跳转主内容、移动菜单、弹窗焦点循环与返回、图片替代文本、缺图回退和空态。尊重减少动态效果。`color-scheme: only light` 保留作者指定的黑白区块；不禁用系统高对比度辅助功能，第三方扩展仍可能覆盖样式。

本次验证 320 / 390 / 768 / 1440px 布局、三类筛选、六项详情、内链、资源和控制台；使用 Edge、Firefox 与 Playwright WebKit（不等同于所有真实 Safari 设备）。
