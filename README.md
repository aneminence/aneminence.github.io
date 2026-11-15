# aneminence

Independent Creative & Technology Label — ASPIRE TO EMINENCE

迎风而立 · 坚定前行 · 追求卓越

官网：https://aneminence.github.io/ | 联系：https://github.com/aneminence

基于用户提供的 V1.0 源码完善，保留 AE 原标志与主要视觉交互。纯 HTML / CSS / JavaScript，无运行时依赖或构建工具。Studio、Labs、Craft 为平级业务，Works 为作品集。

## 目录与本地运行

- index.html：页面结构与原版作品视觉模板。
- styles.css：品牌变量和响应式样式。
- projects.js：作品内容唯一数据源。
- main.js：渲染、筛选、详情、移动导航。
- assets/：原品牌素材、WebP 图片及概念示意图。
- .github/workflows/deploy.yml：语法检查及 Pages 自动部署。

在本目录执行 `python -m http.server 8000 --bind 127.0.0.1`，访问 http://127.0.0.1:8000/ 。无需安装网站依赖。

## 添加或更新作品

编辑 projects.js 数组。每项包含唯一 id、category（studio/labs/craft）、type、title、subtitle、description、field、status、image、alt，可选 url 和 linkLabel。图片放入 assets，推荐 WebP，只使用可信 HTTPS 外链与授权素材。

新增作品自动使用图片卡片，分类及计数自动更新，无需改页面结构。原有四项保留原版视觉模板；如需替换对应卡片图，可移除 index.html 中 visual-ID 模板。概念、研究、原型和已发布项目必须如实标注，未经确认不可描述为已完成或在售商业产品。

## 品牌变量

styles.css 的 :root 定义 --warm: #F7F7F5（雪域白）、--black: #151719（石墨黑）、--red: #C8102E（Studio）、--blue: #315F83（Labs）、--steel: #77838B（Craft）。母品牌统一黑白，红蓝少量辅助；不得改造 AE 标志轮廓。

## 自动部署及更新

仓库：aneminence/aneminence.github.io，默认分支 main。
Settings → Pages → Build and deployment → Source 选择 GitHub Actions。
推送 main 自动检查并部署；可在 Actions → Deploy website to GitHub Pages → Run workflow 手动触发。

```sh
git add index.html styles.css main.js projects.js assets
git commit -m "Update portfolio"
git push origin main
```

工作流只上传明确列出的公开文件，排除 Git 配置、README、测试报告和缓存。部署后实际检查 HTTPS 页面和资源。

## 素材与内容

AE 标志及品牌、服装、山岳图来自用户提供的源码 ZIP；原包说明为既有品牌 VI 图裁切与处理。保留标志位图，仅将展示图片压缩为 WebP，从原标志生成 favicon 和分享图。数据曲线与收纳几何为 SVG/CSS 概念示意，不是真实测量或实物照片。使用系统字体，无第三方字体或外部脚本。不公开私人联系方式，不暗示其他项目的权属。

## 验证规范

提交前运行 `node --check main.js` 和 `node --check projects.js`。
检查 320/390/768/1440 像素布局、三类筛选、详情图片、Tab 焦点循环和恢复、Escape、移动导航、内部锚点、资源请求和控制台错误。尊重减少动态效果偏好，跑马灯静止以避免持续运动干扰。

GitHub 官方部署文档：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
