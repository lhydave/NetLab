0.如果视频本身没有声音，则无需进行此测试

1.安装所需要的包：pip install -r requirements.txt

2.执行 python myrun_pipeline.py --videofile 视频路径（如./path/to/video.mp4) --reference 视频标识符（可以起成类似DingTalk, Tencent等） --data_dir 存储中间过程的路径(如./path/to/output)

3.执行 python myrun_syncnet.py --videofile 视频路径 --reference 视频标识符 --data_dir 存储中间路径

（和2.中相比仅仅改变文件名）

4.对生成的ID_offset.txt中的内容进行绘图，绘图代码可以参考draw_offset.py

txt中的内容是每4s为单位的音画偏移量，单位为秒

5.如果同一视频产生了多个offset.txt，可能为1）场景变化 2）有多个speaker

​	此时如果是情况1，请在处理时合并绘图， 如果是情况2，请选择合适的speaker对应的文件

