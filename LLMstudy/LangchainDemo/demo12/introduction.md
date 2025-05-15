# 文本摘要

    总结文档里的内容

- demo介绍
    - abstract_stuff.py: 用stuff方式总结论文
        - 直接输入整个文章总结，输入超过最大限制导致不完整
    - abstract_map_reduce.py: 用map_reduce方式总结论文
        - 分而治之，一组一组总结，在几组进行合并
    - abstract_refine.py: 用refine方式总结论文
        - 遍历多组，上一步输出和当前组一起输入

