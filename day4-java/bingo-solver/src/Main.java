import java.io.IOException;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
	    String path = args[0];

	    if (path == null) {
	        System.out.println("No file name provided.");
        }

        FileParser parser = new FileParser();
        NumbersChooser numbersChooser = new NumbersChooser();
        ArrayList<Bingo> bingos = new ArrayList<>();
        try {
            parser.parse(path, numbersChooser, bingos);
        } catch (IOException exception) {
            System.out.println("Can't read file.");
        }

        int number;
        Bingo bingoWinner = null;
        int bingoWinnerNumber = -1;
        Bingo lastBingoWinner = null;
        int lastBingoWinnerNumber = -1;

        while ((number = numbersChooser.getNextNumber()) != -1 && bingos.size() > 0) {
            ArrayList<Bingo> itemsToRemove = new ArrayList<>();

            for (Bingo bingo : bingos) {
                if (bingo.markNumber(number)) {
                    itemsToRemove.add(bingo);
                    if (bingoWinner == null) {
                        bingoWinner = bingo;
                        bingoWinnerNumber = number;
                    }

                    lastBingoWinner = bingo;
                    lastBingoWinnerNumber = number;
                }
            }

            for (Bingo bingo : itemsToRemove) {
               bingos.remove(bingo);
            }
        }

        if (bingoWinner == null || bingoWinnerNumber == -1) {
            System.out.println("Winner not found");
            return;
        }

        System.out.printf("Processing results for path: %s\n", path);
        System.out.println("First part");
        System.out.printf("Bingo winner sum: %d\n", bingoWinner.getSumOfUnmarked());
        System.out.printf("Final score: %d\n", bingoWinner.getSumOfUnmarked() * bingoWinnerNumber);
        System.out.println("Second part");
        System.out.printf("Last Bingo winner sum: %d\n", lastBingoWinner.getSumOfUnmarked());
        System.out.printf("Final score: %d\n", lastBingoWinner.getSumOfUnmarked() * lastBingoWinnerNumber);
    }
}
