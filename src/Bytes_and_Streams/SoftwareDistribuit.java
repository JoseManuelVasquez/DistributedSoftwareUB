package Bytes_and_Streams;

import java.io.File;
import java.io.IOException;

/**
 *
 * @author j053
 */
public class SoftwareDistribuit {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        File file = new File("fichero.txt");
          try {
              file.createNewFile();
              ComUtils cmUtils = new ComUtils(file);
              /*cmUtils.writeTest();
              System.out.println(cmUtils.readTest());*/
              
              cmUtils.writeChar('c');
              System.out.println(cmUtils.readChar());
            }
            catch(IOException e)
            {
                System.out.println("Error Found during Operation:" + e.getMessage());
                e.printStackTrace();
            }
        
    }
    
}
