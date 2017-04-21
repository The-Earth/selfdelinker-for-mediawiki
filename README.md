# selfdelinker-for-mediawiki

## 描述
基于mwclient模块编写的python脚本，用以去除中文维基百科中指向自身的链接。
识别[[link]]和[[link|text]]，将[[title]]改为title，[[title|content]]改为content

## 已知问题
- 可能无法识别某些有特殊格式的标题链接，例如[[小行星/13241]]。
- 无法识别通过重定向指向自身的链接。
