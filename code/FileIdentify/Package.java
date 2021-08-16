package summer2021;

import java.io.File;
import java.io.FilenameFilter;
import java.util.ArrayList;

public class Package {
    private String packageName_;
    private String packageAddress_;
    private ArrayList<String>filenameVec_;

//    Package构造函数，输入软件包初始化Package类
    Package(String packageAddress){
        this.packageAddress_=formatPackageAddress(packageAddress);
        this.packageName_=getPackageName(packageAddress_);
        this.filenameVec_=new ArrayList<String>();
        this.getShellFileList(packageAddress_);
    }
//    Package构造函数，通过精确模式初始化Package类,isAccurate为true采用精确识别，否则仍然为粗略识别
    Package(String packageAddress,boolean isAccurate){
    this.packageAddress_=formatPackageAddress(packageAddress);
    this.packageName_=getPackageName(packageAddress_);
    this.filenameVec_=new ArrayList<String>();
    if(isAccurate){
        this.getAccurateShellFileList(packageAddress_);
    }
    else{
        this.getShellFileList(packageAddress_);
    }
}
//    通过软件包地址获得软件包名称
    private static String getPackageName(String packageAddress_){
        return packageAddress_.substring(packageAddress_.lastIndexOf("/")+1);
    }

//    将文件路径统一为反斜杠格式
    private static String formatPackageAddress(String packageAddress){
        packageAddress = packageAddress.replaceAll("\\\\", "/");
        return packageAddress;
    }
//    获取当前文件中的所有shell文件目录,默认只进行后缀识别
    private void getShellFileList(String path){
        try{
            File file=new File(path);
            if(file.isDirectory()){
                String[] pathList=file.list();
                for(String x:pathList){
                    this.getShellFileList(path+"/"+x);
                }
            }
            else{
                if (IsShellFile.idetifyFilePostfix(path)){
                    System.out.println(path);
                    this.filenameVec_.add(path);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    //    获取当前文件中的所有shell文件目录,默认只进行后缀识别
    private void getAccurateShellFileList(String path){
        try{
            File file=new File(path);
            if(file.isDirectory()){
                String[] pathList=file.list();
                for(String x:pathList){
                    this.getAccurateShellFileList(path+"/"+x);
                }
            }
            else{
                if (IsShellFile.idetifyFilePostfix(path)&&IsShellFile.identifyMagic(path)){
                    this.filenameVec_.add(path);
                    System.out.println(path);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String []args){
        Package pack=new Package("C:\\Users\\fx\\Desktop\\summer_test\\mongo-java-driver2-2.14.3-1.oe1.src\\mongo-java-driver-r2.14.3",true);
    }
}
