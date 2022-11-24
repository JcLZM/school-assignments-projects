import java.util.*;
import java.io.*;
import java.nio.file.Paths;
import java.text.*;

class Student{
  private int subjs;
  private String name;
  private ArrayList<Subject> subArray = new ArrayList<Subject>();

  public Student(String n, int sub, ArrayList<Subject> subject){
    name = n;
    subjs = sub;
    subArray = new ArrayList<Subject>();
    for (Subject s: subject)
      subArray.add(s);
  }

  public String toString(){
    String str = name + ", " + subjs + ", [";
    for (Subject t:subArray){
      str += t.getName() + ", ";
    }
    return str.substring(0, str.length()-2) + "]";
    //removes the extra ", " at end
  }

  public String getName(){
    return name;
  }

  public ArrayList<Subject> getSubjs(){
    return subArray;
  }
}

class Subject{//point on the graph, 1 subject = 1 vertex
  private String name;
  private ArrayList<Subject> adjList = new ArrayList<Subject>();
  private int unconnectedTo;

  public Subject(String x){
     name = x;
     adjList = new ArrayList<Subject>();
  }

  public boolean checker(String y){
    //ensuring that i am referring to the correct subject lol..
    if (y == name){
      return true;
    }
    else {return false;}
  }

  public String getName(){
    return name;
  }

  public void addAdj(Subject sub){
    if (adjList.contains(sub) == false)
      adjList.add(sub);
  }

  public ArrayList<Subject> getAdjList(){
    return adjList;
  }

  public void addUnconnectedTo(int i){
    unconnectedTo+= i;
  }

  public int getUnconnectedTo(){
    return unconnectedTo;
  }

}

class TimeSlot{
  private static int counter = 0;
  private int myTime;
  private ArrayList<Subject> list;

  public TimeSlot(){
    counter++;
    myTime = counter;
    list = new ArrayList<Subject>();
  }

  public void addSubj(Subject s){
    list.add(s);
  }

  public ArrayList<Subject> getSubjList(){
    return list;
  }

  public int getTime(){
    return myTime;
  }
}

class UnconnectedSorter implements Comparator<Subject>{
  @Override
    public int compare(Subject s1, Subject s2){
      if (s1.getUnconnectedTo() > s2.getUnconnectedTo()){
        return -1;
      }
      else if (s1.getUnconnectedTo() < s2.getUnconnectedTo()){
        return 1;
      }
      else {
        return 0;
      }
      //return s1.getUnconnectedTo().compareTo(s2.getUnconnectedTo());
    }
}

class greedyAlgo{
  static Set<String> subStrings = new HashSet<String>();
  static int noStudents;
  static ArrayList<Student> stuArray = new ArrayList<Student>();
  static ArrayList<Subject> subjectsArray = new ArrayList<Subject>();
  static int[][] adjMatrix;
//  static ArrayList<Integer> unconnected = new ArrayList<Integer>();
  static ArrayList<TimeSlot> sched = new ArrayList<TimeSlot>();
  static ArrayList<Subject> conflicting = new ArrayList<Subject>();
  static ArrayList<Subject> currentList = new ArrayList<Subject>();
  static ArrayList<Student> thisSlot = new ArrayList<Student>();

  public static void main(String[] args) throws FileNotFoundException{
    // Getting filename from args
      String filename;
      if (args.length < 1) {
        // if no arguments is passed in
         // display error message
         System.out.println("No input file specified!");
         System.out.println("Usage: A3data.txt");
        } else {
         // Get the file name
         filename = args[0];
         processFile(filename);
         subjectsArray.sort(new UnconnectedSorter());
         /*TEST - print arraylist, show unconnected subjs to it*/
         for (Subject e: subjectsArray){
           System.out.println(e.getName() + " - " + e.getUnconnectedTo());
         }
         System.out.println();
         int time = 0; //exit condition, failsafe
         while (subjectsArray.size() > 0){ //exit condition 1
          greed();
          time++;
          if (time>20){
            System.out.println("time>20 exiting from loop"); //oopsie
            break;
          }
        }
        printSummary();
    }
  }

  private static void printSummary(){
    for (TimeSlot t:sched){
      System.out.print("Timeslot "+t.getTime()+": ");
      thisSlot = new ArrayList<Student>();
      for (Subject s: t.getSubjList()){
        System.out.print(s.getName()+ " ");
        for (Student u: stuArray){
          for (Subject w:u.getSubjs()){
          //if (u.getSubjs().getname.contains(s)){
            if(w.getName().equals(s.getName())){
              thisSlot.add(u);
              break;
            }
          }
        }
      }
      System.out.print("\nWho is in this slot: ");
      int counter = 0;
      for (Student v: thisSlot){
        if (counter > 0){
          System.out.print(", ");
        }
        counter++;
        System.out.print(v.getName());
      }
    System.out.println("\nNumber of people in this slot: "
      + thisSlot.size());
    System.out.println("");
    }
  }

  private static void greed(){
    int cwi = -1;//currentWorkingIndex
    int attemptIndex = 0;
    sched.add(new TimeSlot());
    cwi = sched.size()-1;
    sched.get(cwi).addSubj(subjectsArray.get(0));
    //remove sub from unused list.
    rmIndex(0);
    updateConfl(cwi);
    int time = 0;
    while(conflicting.size() != subjectsArray.size()){ //exit condition 1
      updateConfl(cwi);
      if (attemptIndex>subjectsArray.size()-1){
        //failsafe prevent outofboundsexception
        break;
      }
      if (conflicting.contains(subjectsArray.get(attemptIndex))==false){
        sched.get(cwi).addSubj(subjectsArray.get(attemptIndex));
        rmIndex(attemptIndex);
      }
      else{ //if not added, attempted Index incremented.
        attemptIndex++;
      }

      time++;
      if (time>15){ //failsafe
        System.out.println("time>15 exiting from loop");
        break;
      }

    }
    //System.out.println(conflicting.toString());
  }

  private static void updateConfl(int cwi){
    currentList = sched.get(cwi).getSubjList();
    conflicting = new ArrayList<Subject>();
    for (Subject a: currentList){
      for (Subject b: a.getAdjList()){
        conflicting.add(b);
      }
      conflicting.add(a);
    }
  }

  private static void rmIndex(int i){
    subjectsArray.remove(i);
    //unconnected.remove(i);
  }

  private static void processFile(String filename) throws FileNotFoundException{
    File file = new File (filename);
    Scanner reader = new Scanner(file);
    String aLine;
    String name;
    int numberSubj;
    ArrayList<Subject> subjArray = new ArrayList<Subject>();
    int emptyLines = 0;

    aLine = reader.nextLine();
    noStudents = Integer.valueOf(aLine);
    for (int count = 0; count < noStudents; count++){
      //Starts from 2nd line onwards.
      aLine = reader.nextLine();
      while (aLine.length()<1){
        //failsafe, should not ever run,
        //but might be necessary if any errors in
        //data file
        emptyLines++;
        aLine = reader.nextLine();
        if (emptyLines >= noStudents+1){
          break;
        }
      }
      String[] data = aLine.split(", ");
      name = data[0];
      numberSubj = Integer.valueOf(data[1]);
      ArrayList<String> tempSubjArray = new ArrayList<String>();
      subjArray = new ArrayList<Subject>();
      for (int i = 0; i <numberSubj; i++){
        aLine = reader.nextLine();
        tempSubjArray.add(aLine);
        subStrings.add(aLine);

      //  System.out.println("line 136" + tempSubjArray);
        for (String a:tempSubjArray){
          boolean isNew = true;
        //System.out.println("line 138" + subjectsArray);
          for (Subject b:subjectsArray){
            if(b.getName().equals(a)){
              isNew = false;
              break;
            }
          }
          if (isNew != false){
            subjectsArray.add(new Subject(a));
          }
        }
        }
        for (String str: tempSubjArray){
          boolean isThisNew = true; //ensuring no dupes
          for (Subject j: subjectsArray){
            if (j.getName().equals(str) && isThisNew == true){
              subjArray.add(j);
              isThisNew = false;
              break;
            }
          }
        }
      stuArray.add(new Student(name, numberSubj, subjArray));
    }
    zeroArray();
    fillAdjs();

    findEmpty();
  }
  //remove ensures array is filled with 0s
  private static void zeroArray(){
    adjMatrix = new int[subjectsArray.size()][subjectsArray.size()];
    for(int i = 0; i<subjectsArray.size(); i++)
      for(int j = 0; j<subjectsArray.size(); j++)
        adjMatrix[i][j] = 0;
  }

  private static void findEmpty(){
    //find the number of unconnected vertices/subjects
    int counter =0;
  //  unconnected = new ArrayList<Integer>();
    for (int i = 0; i<subjectsArray.size();i++){
      counter = 0;
      for(int j = 0; j<subjectsArray.size(); j++){
        if (adjMatrix[i][j] == 0){
          counter++;
        }
      }
      subjectsArray.get(i).addUnconnectedTo(counter);
    //  unconnected.add(counter);
    }
  }

  private static void fillAdjs(){
    /*all students in stuArray( which has all students)

    rolling through list of subjects the student has

    comparing list of subjects with subjects of the uni

    iterate over students subj list and increment adj matrix as needed

    lets not think about the complexity
      */
    for (Student x: stuArray){
      for (int i = 0; i < x.getSubjs().size(); i++){
        for (int j = 0; j<subjectsArray.size(); j++){
          if (x.getSubjs().get(i).equals(subjectsArray.get(j))){
            for (Subject v: x.getSubjs()){
              for (int k =0; k<subjectsArray.size(); k++){
                if(v.getName().equals(subjectsArray.get(k).getName())){
                  adjMatrix[j][k]+=1;
                  x.getSubjs().get(i).addAdj(v);
                }
              }
            }
          }
        }
      }
    }
  }
}
