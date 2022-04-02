#!/usr/bin/env python
# coding=utf-8

import os
import sys

bam=sys.argv[1]
file=sys.argv[2]
name=sys.argv[3]
path=sys.argv[4]

if not os.path.exists(path):
    os.mkdir(path)

my_path='/aegis/staff/huyu/sWGS_CNV_20220106/result-20220315/sWGS-CNV-pipeline-V1.0/'
ref=my_path+'ref_30kb.npz'
black_list=my_path+'black-list.txt'

def blacklist():
    bl_dict={}
    for i in open(black_list):
        arr=i.strip().split('\t')
        if arr[0] not in bl_dict.keys():
            bl_dict[arr[0]]=[]
        bl_dict[arr[0]].append(arr[1]+'-'+arr[2])
    return bl_dict

def WisecondorX():
    wx={}
    for i in open('./'+name+'-out_aberrations.bed'):
        arr=i.strip().split('\t')
        if arr[0]!='chr':
            if arr[0] not in wx.keys():
                wx[arr[0]]=[]
            wx[arr[0]].append(arr[1]+'-'+arr[2])
    return wx

def bl_check_one(chr,start,end):
    bl_dict=blacklist()
    if chr not in bl_dict.keys():
        return 'no'
    loc_dict={}
    for i in bl_dict[chr]:
        loc_dict[int(i.split('-')[0])]=int(i.split('-')[1])
    if min(loc_dict.keys())>int(end):
        return 'no'
    if max(loc_dict.values())<int(start):
        return 'no'
    for i in loc_dict.keys():
        if int(end)>i and int(start)<loc_dict[i]:
            return 'yes'
    return 'no'

def WX_check_one(chr,start,end):
    wx=WisecondorX()
    if chr not in wx.keys():
        return 'no'
    for i in wx[chr]:
        a=int(i.split('-')[0])
        b=int(i.split('-')[1])
        if int(start)<b and int(end)>a:
            return chr+':'+str(a)+'-'+str(b)
    return 'no'

def WX_new_result(other):
    wx=WisecondorX()
    new={}
    for i in wx.keys():
        if i in other.keys():
            delta=list(set(wx[i]).difference(set(other[i])))
            if delta!=[]:
                new[i]=delta
        else:
            new[i]=wx[i]
    return new

def main():
    #WisecondorX
    os.chdir(path)
    os.system('WisecondorX convert '+bam+' '+name+'.npz')
    os.system('WisecondorX predict --plot --bed '+name+'.npz '+ref+' '+name+'-out')

    #结果整合
    out_final=open('./'+name+'.new_final.txt',mode='w+')
    loc0=''
    wx_other_result={}
    for i in open(file):
        arr=i.strip().split('\t')
        loc=arr[0].split(',')[-1].strip(')').strip('"')
        if loc=='AnnotSV ID':
            continue
        if loc!=loc0:
            loc0=loc
            chr=loc.split(':')[0]
            start=loc.split(':')[1].split('-')[0]
            end=loc.split(':')[1].split('-')[1]
            bl_result=bl_check_one(chr,start,end)
            wx_result=WX_check_one(chr,start,end)
            if wx_result!='no':
                if wx_result.split(':')[0] not in wx_other_result.keys():
                    wx_other_result[wx_result.split(':')[0]]=[]
                if wx_result.split(':')[1] not in wx_other_result[wx_result.split(':')[0]]:
                    wx_other_result[wx_result.split(':')[0]].append(wx_result.split(':')[1])
            if wx_result!='no':
                result_print='WisecondorX result support.'
            elif bl_result!='no':
                result_print='At WisecondorX\'s black-list means not support.'
            else:
                result_print='WisecondorX havenot any result.'
            out_final.writelines([i.strip()+'\t'+result_print+'\n'])
        else:
            out_final.writelines([i.strip()+'\t'+result_print+'\n'])

    #WisecondorX新结果
    out_WX=open('./'+name+'.WisecondorX.txt',mode='w+')
    wx_new=WX_new_result(wx_other_result)
    wx_new2=[]
    for i in wx_new.keys():
        for j in wx_new[i]:
            wx_new2.append(i+':'+j)
    for i in open('./'+name+'-out_aberrations.bed'):
        if i.strip()[:3]=='chr':
            out_WX.writelines([i.strip()+'\n'])
            continue
        arr=i.strip().split('\t')
        if arr[0]+':'+arr[1]+'-'+arr[2] in wx_new2:
            out_WX.writelines([i.strip()+'\n'])

if __name__ == "__main__":
    main()
