# 微信小程序部署指南 (WeChat Mini Program Deployment Guide)

目前的 Web 应用是基于 **React + Vite + Tailwind CSS** 构建的。微信小程序 (WeChat Mini Program) 使用的是一套私有的技术栈（WXML, WXSS, JavaScript），因此**不能直接将现有的 Web 代码部署到小程序**。

为了将这个应用移植到微信小程序，您有以下几种主要方案。我们强烈推荐方案一。

---

## 方案一：使用 Taro 框架进行迁移（推荐）

[Taro](https://taro-docs.jd.com/) 是一个开放式跨端跨框架解决方案，支持使用 React 语法开发小程序。因为您的项目已经是 React 的，这是最自然的迁移路径。

### 1. 初始化 Taro 项目

首先，在你的电脑上安装 Taro CLI：

```bash
# 使用 npm 安装 CLI
npm install -g @tarojs/cli

# 初始化项目
taro init attachment-test-mini
```

在初始化向导中，请做如下选择以匹配现有技术栈：
- **框架**：React
- **语言**：JavaScript (或者 TypeScript，如果你想升级)
- **CSS 预处理器**：Sass/Less (或者 PostCSS)
- **编译器**：Webpack5 或 Vite

### 2. 迁移核心逻辑

您的核心数据和逻辑都在 `src` 目录下，这部分很容易复用。

1.  **复制 `translations.js`**：直接将现有的 `src/translations.js` 复制到 Taro 项目的 `src/` 目录下。
2.  **复制逻辑代码**：`App.jsx` 中的 `calculateAndShowResult` 等纯逻辑函数可以直接复用。

### 3. 迁移 UI 组件

这是工作量最大的部分。您需要将 HTML 标签转换为 Taro 的组件。

**映射关系表：**

| Web (React) | Taro (Mini Program) |
| :--- | :--- |
| `<div>`, `<span>` | `<View>`, `<Text>` |
| `<img>` | `<Image>` |
| `<button>` | `<Button>` |
| `onClick` | `onClick` (Taro 做了适配) |

**代码示例对比：**

*Web (App.jsx):*
```jsx
<div className="bg-white p-4">
  <h1 className="text-2xl">标题</h1>
  <button onClick={handleStart}>开始</button>
</div>
```

*Taro (pages/index/index.jsx):*
```jsx
import { View, Text, Button } from '@tarojs/components'

// ... inside render
<View className="bg-white p-4">
  <View className="text-2xl">标题</View>
  <Button onClick={handleStart}>开始</Button>
</View>
```

### 4. 处理 Tailwind CSS

微信小程序对 CSS 选择器有严格限制（不支持 `*` 通配符，不支持部分复杂的类名转义）。要在 Taro 中使用 Tailwind CSS，推荐使用 [Weapp-Tailwind](https://weapp-tw.icebreaker.top/)。

1.  在 Taro 项目中安装 Tailwind 和适配插件：
    ```bash
    npm install -D tailwindcss postcss autoprefixer weapp-tailwindcss-webpack-plugin
    ```
2.  配置 `tailwind.config.js` (参考 weapp-tailwindcss 文档)。
3.  现在您可以直接复制大部分 `className` 样式了。

---

## 方案二：使用 Web-View 组件（最快，但有门槛）

微信小程序提供了一个 `<web-view>` 组件，可以直接加载网页。

**代码示例：**
```html
<!-- pages/index/index.wxml -->
<web-view src="https://your-domain.com/attachment-test/"></web-view>
```

**严重限制：**
1.  **域名要求**：您加载的 URL (`src`) 必须是配置在微信小程序后台的**业务域名**。
2.  **ICP 备案**：该域名必须经过 ICP 备案。
3.  **GitHub Pages**：GitHub Pages 的域名 (`*.github.io`) **无法** 配置为业务域名。因此，您不能直接在小程序里用 `web-view` 打开您目前的 GitHub Pages 链接。您必须购买自己的服务器和域名，完成备案后才能使用此方案。

---

## 总结建议

1.  **如果是个人练习/展示**：建议继续使用 Web 版本 (GitHub Pages)，并在微信中以“阅读原文”或链接分享的形式打开。
2.  **如果要正式上线小程序**：请使用 **方案一 (Taro)**。您现有的 `translations.js` 和 React 状态逻辑都可以保留，主要是把 `div` 换成 `View`，并重新调整一下样式。
