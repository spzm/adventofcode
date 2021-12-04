import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;


public class FileParser {
    public static ArrayList<Integer> readLineOfNumbers(String line) {
        ArrayList<Integer> numbers = new ArrayList<>();

        Scanner scanner = new Scanner(line);
        scanner.useDelimiter("\\D+");
        while (scanner.hasNext()) {
            numbers.add(scanner.nextInt());
        }
        scanner.close();

        return numbers;
    }

    public void parse(String path, NumbersChooser numbersChooser, ArrayList<Bingo> bingos) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {

            numbersChooser.setNumbers(readLineOfNumbers(br.readLine()));
            br.readLine();

            String line;
            while ((line = br.readLine()) != null) {
                ArrayList<ArrayList<Integer>> bingoLines = new ArrayList<>();
                if (line.equals("")) continue;

                do {
                    ArrayList<Integer> values = readLineOfNumbers(line);
                    bingoLines.add(values);
                } while ((line = br.readLine()) != null && !line.equals(""));

                bingos.add(new Bingo(bingoLines, bingoLines.size()));
            }
        }
    }
}
