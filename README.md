# 你好！
请不要删除文件***中的内容，和现存的conda环境！非常感谢您！
如果您使用过程中报错空间不够，请查看df -Hl,若为/dev/mapper/ubuntu--vg-ubuntu--lv 空间使用到100%，可以通过
sudo lvextend -L ***G /dev/mapper/ubuntu--vg-ubuntu--lv 增加空间（请勿小于当前空间，以免文件丢失）
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
再次df -Hl能够看到可用容量增加，然后便可正常使用
可供分配的空间足足有1.7个TiB，请不要删除我的文件，谢谢您！
