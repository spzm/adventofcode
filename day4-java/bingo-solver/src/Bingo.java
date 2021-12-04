import java.util.ArrayList;

public class Bingo {
    private int size = 0;
    private final ArrayList<ArrayList<Integer>> data;
    private final ArrayList<Integer> rows;
    private final ArrayList<Integer> cols;
    private boolean isWinner = false;
    private int sumOfMarked = 0;

    public Bingo(ArrayList<ArrayList<Integer>> inputData, int size) {
        this.size = size;
        data = new ArrayList<>();
        rows = new ArrayList<>();
        cols = new ArrayList<>();

        for (int i = 0; i < size; i++) {
            data.add(new ArrayList<>());
            for (int j = 0; j < size; j++) {
                data.get(i).add(inputData.get(i).get(j));
            }
            rows.add(size);
            cols.add(size);
        }
    }

    public boolean markNumber(int value) {
        if (size == 0) throw new IllegalArgumentException("Class wasn't properly initialized");

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (data.get(i).get(j) == value && !isWinner) {
                    int leftElementsInRow = rows.get(i);
                    int leftElementsInColumn = cols.get(j);

                    if (leftElementsInRow == 1 || leftElementsInColumn  == 1) {
                        isWinner = true;
                    }

                    sumOfMarked += value;
                    rows.set(i, leftElementsInRow - 1);
                    cols.set(j, leftElementsInColumn - 1);
                    break;
                }
            }
        }

        return isWinner();
    }

    public int getSumOfUnmarked() {
        int sum = 0;
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                sum += data.get(i).get(j);
            }
        }

        return sum - sumOfMarked;
    }

    public boolean isWinner() {
       return isWinner;
    }

}
