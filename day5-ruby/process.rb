class Field
  def initialize
    @field = Hash.new
    @total_overlap = 0
  end

  def getKey(x, y)
    return "#{x}:#{y}"
  end

  def addStraight(x1, y1, x2, y2)
    if x1 != x2 && y1 != y2
      return
    end

    # swapping input arguments is not good idea
    # but here it for keeping simplicity
    if x2 < x1 
      x1, x2 = x2, x1
    end
    if y2 < y1
      y1, y2 = y2, y1
    end
  
    for x in x1..x2
      for y in y1..y2
        update(x, y)
      end
    end
  end

  def addDiagonal(x1, y1, x2, y2)
    symmetricDiagonal(x1, y1, x2, y2)
    asymetricDiagonal(x1, y1, x2, y2)
  end

  def asymetricDiagonal(x1, y1, x2, y2)
    if x2 < x1 
      x1, x2 = x2, x1
      y1, y2 = y2, y1
    end

    if ((x2 - x1).abs != (y2 - y1).abs)
      return
    end

    y = y1
    increment = y1 > y2 ? -1 : 1;

    for x in x1..x2
      update(x, y)
      y = y + increment
    end
  end

  def symmetricDiagonal(x1, y1, x2, y2)
    if !(x1 == y1 && x2 == y2)
      return
    end

    if x2 < x1 
      x1, x2 = x2, x1
    end

    for i in x1..x2
      update(i, i)
    end
  end

  def update(x, y) 
    key = getKey(x, y)

    if @field.has_key?(key)
      if @field[key] == 0
        @total_overlap = @total_overlap + 1
      end

      @field[key] = @field[key] + 1
    else
      @field[key] = 0
    end
  end

  def get_total_overlap
    return @total_overlap
  end

  def to_s
    @field.select { |key, value| value > 0 }
  end
end



arguments = ARGV
path = arguments[0]

if (!path)
  puts "No file name provided"
  exit(false)
end

puts "Processing results for path: #{path}"

actions = []
File.foreach(path).each do |line|
  actions << line.split(/ -> /).map {|s| s.split(',').map(&:to_i) }
end

field = Field.new

for action in actions
  field.addStraight(action[0][0], action[0][1], action [1][0], action[1][1])
end

puts "Straight overlap: #{field.get_total_overlap}"

for action in actions
  field.addDiagonal(action[0][0], action[0][1], action [1][0], action[1][1])
end

puts "Straight & Diagonal overlap #{field.get_total_overlap}"