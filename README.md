# sWGS-CNV：基于WisecondorX项目优化（V1.0）

#### 胡煜-20220330

## 1. 介绍 Introduction
&emsp;&emsp;低层深全基因组测序（sWGS）的CNV检测工作，目前使用的原有流程核心算法，是CNVkit软件的call变异结果。在使用过程中发现，CNVkit的call变异结果精准度较差，后在文献调研中发现了软件WisecondorX。WisecondorX和CNVkit二者均基于RD算法（目前公认最好、使用最广泛的CNV检测算法），但二者结果略有差异，主要差异在：CNVkit敏感度优于WisecondorX、WisecondorX精准度优于CNVkit。故本次项目优化使用WisecondorX结果对原流程的CNVkit结果进行加权注释，方便下游报告解读对原流程中各结果的可靠度更有把握。

## 2. 命令行和参数 Usage and Option
    >python sWGS-CNV-WisecondorX-pipeline.py [bam] [yixuezu.txt] [out_name] [out_path]
参数：  
&emsp;&emsp;&emsp;[bam]：待分析样本的bam文件（要求同路径下含有相应的bai索引文件）  
&emsp;&emsp;&emsp;[yixuezu.txt]：原分析流程的结果文件  
&emsp;&emsp;&emsp;[out_name]：输出结果的文件名前缀  
&emsp;&emsp;&emsp;[out_path]：输出结果文件夹路径（如无此文件夹则自动新建）  

    e.g.：>python sWGS-CNV-WisecondorX-pipeline.py AS123.bam AS123.final.call.cn.yixuezu.annotated.txt AS123 ./AS123

## 3. 配置要求 Requirements
软件使用python3编写，配置环境为：

    >source /aegis/env/miniconda3/bin/activate ngs-bits
该环境已设置python为python3，已安装WisecondorX等所需软件/软件包。

## 4. 输入与输出 STDIN and STDOUT
### 4.1 输入文件
1、bam文件：为原流程中生成的bam文件，一般存放于/agdisk/backup/clinic/\*/bam/\*.recaled.bam，同时需要同路径下存放有该bam文件对应的bai文件；  
2、原流程结果文件：为原流程致医学组的结果文件，一般存放于/agdisk/backup/clinic/\*/variant/cnv/anno/\*.final.call.cn.yixuezu.annotated.txt。

### 4.2 输出文件
输出文件均在命令参数设定的路径文件夹下。

    out_path/
    ├── out_name.npz #WisecondorX分析的二进制文件
    ├── out_name-out_bins.bed #WisecondorX输出的逐bin结果文件
    ├── out_name-out_segments.bed #WisecondorX输出的中间结果文件
    ├── out_name-out_aberrations.bed #WisecondorX输出的最终结果文件
    ├── out_name-out_statistics.txt #WisecondorX输出的统计log文件
    ├── out_name-out.plots #WisecondorX输出的结果图文件夹
    ├── out_name.new_final.txt #带有WisecondorX结果注释的致医学组结果文件（重要）
    └── out_name.WisecondorX.txt #WisecondorX输出的原流程结果中不存在的新变异（重要）

## 5. 程序文件夹和参考基因组 Software and Reference

    sWGS-CNV-pipeline-V1.0/
    ├── sWGS-CNV-WisecondorX-pipeline.py #主程序
    ├── ref_30kb.npz #WisecondorX的reference数据库
    └── black-list.txt #黑名单bed文件

## 6. 程序测试 Software Test
每样本大约需15min。
