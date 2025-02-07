# 文件名加密脚本
用于windows系统环境下，将文件夹内的视频文件的文件名进行加密以此起到隐藏的作用，并且可以按照原文件名进行恢复

使用前提示：
1、使用前请一定要备份好相关文件，防止出bug导致文件不能正常恢复。
2、使用前先要运行save.bat脚本，用于将文件夹内的视频文件名全部记录保存下来，再使用encrypt.bay脚本进行加密，需要解密时用decrypt.bat脚本进行解密。以上bat脚本的代码需要根据自己的Python环境进行修改，才可以使用。
3、本项目还不成熟，个人在使用的过程中曾经出现过保存原文件名的txt文件莫名其妙的变成乱码的情况，尝试了很多恢复方法都不能恢复，导致被加密的文件名不能再被恢复成原样，只能自己手动慢慢重命名。因此使用此脚本前请一定要备份重要文件，以及保存原文件名的txt文件最好也要备份。
4、若bat脚本无法启用项目，可以通过在main.py文件中运行，通过调用函数的方法直接调用相关函数。
