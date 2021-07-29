package summer2021;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

public class IsShellFile {
//    获取文件输入流
    private static  String getFileContent(String filePath)throws IOException{
        byte[] bytes=new byte[30];
        InputStream inputStream=null;
        try{
            inputStream=new FileInputStream(filePath);
            inputStream.read(bytes,0,30);
        } catch (IOException e) {
            e.printStackTrace();
            throw e;
        }finally {
            if(inputStream!=null){
                try{
                    inputStream.close();
                }catch (IOException e){
                    e.printStackTrace();
                    throw e;
                }
            }
        }
        return bytesToHexString(bytes);
    }

//    将文件头转换为16进制字符串
    private static String bytesToHexString(byte[] src){
        StringBuilder stringBuilder = new StringBuilder();
        if (src == null || src.length <= 0) {
            return null;
        }
        for (int i = 0; i < src.length; i++) {
            int v = src[i] & 0xFF;
            String hv = Integer.toHexString(v);
            if (hv.length() < 2) {
                stringBuilder.append(0);
            }
            stringBuilder.append(hv);
        }
        return stringBuilder.toString();
    }
//    判断文件头是否为Shell文件文件头
    public static boolean identifyMagic(String filePath) throws IOException{
        String fileHead=getFileContent(filePath);
        return fileHead.startsWith("2321202f62696e2f73683")  //#! /bin/sh
                ||fileHead.startsWith("23212f7573722f62696e2f656e76");  //#!/usr/bin/env bash
    }
//    判断文件名是否为.sh
    public static boolean idetifyFilePostfix(String filePath){
        return filePath.endsWith(".sh");
    }

}