import java.util.ArrayList;

public class NumbersChooser {
    private ArrayList<Integer> numbers;

    public void setNumbers(ArrayList<Integer> numbers) {
        this.numbers = new ArrayList<>();

        this.numbers.addAll(numbers);
    }

    public int getNextNumber() {
        if (numbers != null && numbers.size() > 0) {
            return numbers.remove(0);
        }

        return -1;
    }
}
