# sizebased_img_compress

[WIP][Experimental] 一种基于稍加修改的二分查找调整JPEG压缩quailty的方法，将图片压缩到小于指定大小的同时，尽可能提高quailty。主要的目的是为了解决某些平台无法上传大图片的情况。

## ToDo

- [ ] 优先有损压缩
- [ ] 改进算法
- [ ] 给出算法描述
- [ ] 基于相对图片大小进行测试
- [ ] CLI
- [ ] GUI
- [ ] 如果实在太大就切图
- [ ] 用图片哈希进行损失过大的警告

## 引用与参考

- numpy
- opencv-python
- mozjpeg
- mozjpeg_lossless_optimization
- Photo by [Y K](https://unsplash.com/@yokeboy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/-e6Xu27_T50?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

## 许可 License

Copyright (C) [year] [name of author]
This program is free software: you can redistribute it and/or modify it under the terms of
the GNU Affero General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)
