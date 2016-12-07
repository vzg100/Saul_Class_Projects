/**
 * Created by mark on 12/5/16.
 */

import edu.illinois.cs.cogcomp.core.io.LineIO;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

public class reader {
    public List<dataClass> dataClasses;
    public reader(String data){
        dataClasses = new ArrayList<>();
        List<String> lines = null;
        try{
            lines = LineIO.read(data);
        }
        catch (FileNotFoundException e){
            System.err.println("File not found");
        }
        for (String line : lines){
            if(!line.isEmpty())
                dataClasses.add(new dataClass(line.split(",")));
        }
    }
}