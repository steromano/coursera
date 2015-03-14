package streams

object test {;import org.scalaide.worksheet.runtime.library.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(64); 
	val game = Bloxorz.InfiniteLevel;System.out.println("""game  : streams.Bloxorz.InfiniteLevel.type = """ + $show(game ));$skip(29); 
	val start = game.startBlock;System.out.println("""start  : streams.test.game.Block = """ + $show(start ));$skip(37); 
	val moves: List[game.Move] = List();System.out.println("""moves  : List[streams.test.game.Move] = """ + $show(moves ));$skip(38); 
	val initial = Stream((start, moves));System.out.println("""initial  : scala.collection.immutable.Stream[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(initial ));$skip(27); 
	val explored = Set(start);System.out.println("""explored  : scala.collection.immutable.Set[streams.test.game.Block] = """ + $show(explored ));$skip(30); val res$0 = 
	game.from(initial, explored);System.out.println("""res0: Stream[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(res$0));$skip(141); 
	val more1 = initial flatMap {
      case (block, history) => game.newNeighborsOnly(game.neighborsWithHistory(block, history), explored)
  };System.out.println("""more1  : scala.collection.immutable.Stream[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(more1 ));$skip(39); val res$1 = 
  
  (initial ++ more1 take 10) toList;System.out.println("""res1: List[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(res$1));$skip(55); 
  val explored1 = explored ++ (more1 map (_._1)).toSet;System.out.println("""explored1  : scala.collection.immutable.Set[streams.test.game.Block] = """ + $show(explored1 ));$skip(134); 
	val more2 = more1 flatMap {
		case (block, history) => game.newNeighborsOnly(game.neighborsWithHistory(block, history), explored)
	};System.out.println("""more2  : scala.collection.immutable.Stream[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(more2 ));$skip(46); val res$2 = 
	
	(initial ++ more1 ++ more2 take 30) toList;System.out.println("""res2: List[(streams.test.game.Block, List[streams.test.game.Move])] = """ + $show(res$2));$skip(36); 
	def str1: Stream[Int] = 1 #:: str1;System.out.println("""str1: => Stream[Int]""");$skip(33); val res$3 = 
	
	(str1 ++ str1 take 10) toList;System.out.println("""res3: List[Int] = """ + $show(res$3))}
}
