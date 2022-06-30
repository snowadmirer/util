# 获取xml文档中的所有文本
```python
html_obj =etree.HTML(xml_content,etree.HTMLParser())
for text in html_obj.itertext():
  print(text)
```
