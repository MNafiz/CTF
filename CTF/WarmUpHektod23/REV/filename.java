import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;

class Malware
{
    public static void main(String[] args)
    {
        try 
        {
        File myObj = new File(args[0]);
        Scanner myReader = new Scanner(myObj);
        String data = "";
        while (myReader.hasNextLine())
        {
            data = data.concat(myReader.nextLine());
        }
        
        char[] datachar = data.toCharArray();
        String cipher = "";
        int res = 0;
        for(int i = 0; i < data.length(); i++)
        {
            // System.out.println(datachar[i]);
            char tmp = (char)(datachar[i]);
            if((tmp >= 65) && (tmp <= 90))
            {
                res = ((tmp - 65 + 13) % 26) + 65;
            }
            if((tmp >= 97) && (tmp <= 122))
            {
                res = ((tmp - 97 + 13) % 26) + 97;
            }
            System.out.println(res);
            // cipher = cipher.concat((char)(res));
        }

        // System.out.println(cipher);

        } catch (FileNotFoundException e)
        {
            System.out.println("hehe");
        }
        
        
    }
}