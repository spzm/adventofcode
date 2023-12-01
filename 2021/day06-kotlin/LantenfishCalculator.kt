import java.io.File
import kotlin.system.exitProcess

object ReproduceConf {
    const val NEW_BORN_CYCLE = 8
    const val BORN_CYCLE = 6
}

class Fish {
    companion object {
        fun calculateFishesOnDay(initFishesMap: MutableMap<Int, Long>, days: Int) : Long {
            var fishesMap = initFishesMap

            for (day in 1.. days) {
                val newFishes = mutableMapOf<Int, Long>()
                for ((key, currentFishes) in fishesMap) {
                    if (key == 0) {
                        newFishes[ReproduceConf.BORN_CYCLE] = newFishes.getOrDefault(ReproduceConf.BORN_CYCLE, 0) + currentFishes
                        newFishes[ReproduceConf.NEW_BORN_CYCLE] = newFishes.getOrDefault(ReproduceConf.NEW_BORN_CYCLE, 0) + currentFishes
                    } else {
                        newFishes[key - 1] = newFishes.getOrDefault(key - 1, 0) + currentFishes
                    }
                }
                fishesMap = newFishes
            }

            var totalFishes = 0L
            for (( _, count ) in fishesMap) {
                totalFishes += count
            }

            return totalFishes
        }
    }
}

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("No file name provided")
        exitProcess(-1)
    }
    val path = args[0];

    val stringValues = File(path).readText()
    val initialFishes = stringValues.split(",").map { it.toInt() }

    val initialFishesMap = mutableMapOf<Int, Long>()
    for (fish: Int in initialFishes) {
        initialFishesMap[fish] = initialFishesMap.getOrDefault(fish, 0) + 1
    }

    println("Processing results for path: $path")
    println("Lanternfish produced on 80 days: ${Fish.calculateFishesOnDay(initialFishesMap, 80)}")
    println("Lanternfish produced on 256 days: ${Fish.calculateFishesOnDay(initialFishesMap, 256)}")
}
