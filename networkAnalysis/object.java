package networkAnalysis;

class customObject{
    private static customObject[] list=new customObject[3];
    private static int id=0;
private String name;
    public customObject(String name){
this.name=name;
    }

public static customObject getInstance(String name){
    if(id<3){
    customObject hey=new customObject(name);
    list[id]=hey;
    id++;
    return hey;
    }
    else{
        return null;
    }
}

    public static int check(customObject object){
if(object==null){
    return -1;
}
else{
    for(int i=0; i<id; i++){
        if(list[i]==object){
            return i;
        }
    }

}
return -1;
    }
    public static void printOrder(){
        for(int i=0; i<id; i++){
            System.out.println(list[id].getName());
        }

    }
    public String getName(){
        return name;
    }
}


public class object{
    public static void main(String[] args){
customObject s1=customObject.getInstance("a");
    customObject s2=customObject.getInstance("b");
    
    customObject.printOrder();
    }
}