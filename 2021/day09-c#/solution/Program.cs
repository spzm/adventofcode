using System.Collections;

namespace SmokeBasin
{

  class FileReader
  {
    static public List<List<int>> readFile(string path)
    {
      List<List<int>> field = new List<List<int>>();

      foreach (string line in File.ReadLines(path))
      {
        List<int> numbers = new List<int>(line.ToCharArray().Select(v => Int32.Parse(v.ToString())));
        field.Add(numbers);
      }

      return field;
    }
  }

  class SmokeBasinDetector
  {
    const int StopValue = 9;
    List<List<int>> field;

    public SmokeBasinDetector(List<List<int>> field)
    {
      this.field = field;
    }

    public int calculateRiskLevel()
    {
      return findLocalBasins().Sum(c => field[c[0]][c[1]] + 1);
    }

    public int multiplyTopBasins(int bassinsLimit)
    {
      var basins = new List<List<int[]>>();

      var localBasins = findLocalBasins();

      foreach (var c in localBasins)
      {
        var basin = new List<int[]>();
        findBasinSizeForCoordinate(basin, new HashSet<string>(), c[0], c[1]);

        if (basin.Count > 0)
        {
          basins.Add(basin);
        }
      }

      int result = 1;
      foreach (var basin in basins.OrderBy(x => x.Count).TakeLast(bassinsLimit))
      {
        printBasin(basin);
        result *= basin.Count;
      }

      return result;
    }

    string getKey(int i, int j)
    {
      return i + "," + j;
    }

    Boolean isInBoundaries(int i, int j)
    {
      return i >= 0 && i < field.Count && j >= 0 && j < field[0].Count;
    }

    void findBasinSizeForCoordinate(List<int[]> solution, HashSet<string> visited, int i, int j)
    {
      if (visited.Contains(getKey(i, j)) || !isInBoundaries(i, j) || field[i][j] == StopValue)
      {
        return;
      }

      solution.Add(new int[] { i, j });
      visited.Add(getKey(i, j));

      findBasinSizeForCoordinate(solution, visited, i - 1, j);
      findBasinSizeForCoordinate(solution, visited, i + 1, j);
      findBasinSizeForCoordinate(solution, visited, i, j - 1);
      findBasinSizeForCoordinate(solution, visited, i, j + 1);
    }

    private List<int[]> findLocalBasins()
    {
      var minimumPoints = new List<int[]>();

      for (var i = 0; i < field.Count; i++)
      {
        for (var j = 0; j < field[0].Count; j++)
        {
          if (validateLocalMinimum(i, j))
          {
            minimumPoints.Add(new int[] { i, j });
          }
        }
      }

      return minimumPoints;
    }

    private bool validateLocalMinimum(int i, int j)
    {
      var currentValue = field[i][j];

      if (i > 0)
      {
        if (currentValue >= field[i - 1][j]) return false;
      }

      if (j > 0)
      {
        if (currentValue >= field[i][j - 1]) return false;
      }

      if (i < (field.Count - 1))
      {
        if (currentValue >= field[i + 1][j]) return false;
      }

      if (j < (field[0].Count - 1))
      {
        if (currentValue >= field[i][j + 1]) return false;
      }

      return true;
    }

    void printBasin(List<int[]> basin)
    {
      int iMin = basin[0][0];
      int iMax = iMin;
      int jMin = basin[0][1];
      int jMax = jMin;

      var dict = new Dictionary<string, int>();
      foreach (int[] c in basin)
      {
        if (c[0] < iMin) iMin = c[0];
        if (c[0] > iMax) iMax = c[0];

        if (c[1] < jMin) jMin = c[1];
        if (c[1] > jMax) jMax = c[1];

        if (!dict.ContainsKey(getKey(c[0], c[1]))) dict.Add(getKey(c[0], c[1]), field[c[0]][c[1]]);
      }

      Console.WriteLine("-----------");
      for (var i = iMin; i <= iMax; i++)
      {
        for (var j = jMin; j <= jMax; j++)
        {
          if (j != jMin) Console.Write(" ");
          if (dict.ContainsKey(getKey(i, j)))
          {
            Console.Write(dict[getKey(i, j)]);
          }
          else
          {
            Console.Write(".");
          }
        }
        Console.WriteLine();
      }
      Console.WriteLine("Basin size: " + dict.Count);
      Console.WriteLine("-----------");
    }
  }

  class Program
  {

    static void Main(string[] args)
    {
      if (args.Length == 0)
      {
        Console.WriteLine("No file name provided");
        Environment.Exit(-1);
      }

      String path = args[0];
      Console.WriteLine("Processing results for path: " + path);

      var field = FileReader.readFile(path);

      var smokeBasinDetector = new SmokeBasinDetector(field);
      var riskLevel = smokeBasinDetector.calculateRiskLevel();
      var largestBasinsMultiplier = smokeBasinDetector.multiplyTopBasins(3);

      Console.WriteLine("Risk level: " + riskLevel);
      Console.WriteLine("Size of three largest basins multiplied: " + largestBasinsMultiplier);
    }
  }
}
