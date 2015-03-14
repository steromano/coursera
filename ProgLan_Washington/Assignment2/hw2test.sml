(* Homework2 Simple Test *)
(* These are basic test cases. Passing these tests does not guarantee that your code will pass the actual homework grader *)
(* To run the test, add a new line to the top of this file: use "homeworkname.sml"; *)
(* All the tests should evaluate to true. For example, the REPL should say: val test1 = true : bool *)

val test1 = all_except_option("string", ["string"]) = SOME []

val test2 = get_substitutions1([["foo"],["there"]], "foo") = []

val test3 = get_substitutions2([["foo"],["there"]], "foo") = []


val test4 = similar_names([["Fred","Fredrick"],["Elizabeth","Betty"],["Freddie","Fred","F"]], {first="Fred", middle="W", last="Smith"}) =
	    [{first="Fred", last="Smith", middle="W"}, {first="Fredrick", last="Smith", middle="W"},
	     {first="Freddie", last="Smith", middle="W"}, {first="F", last="Smith", middle="W"}]

val test5 = card_color((Clubs, Num 2)) = Black

val test6 = card_value((Clubs, Num 2)) = 2

val test7 = remove_card([(Hearts, Ace)], (Hearts, Ace), IllegalMove) = []

val test8 = all_same_color([(Hearts, Ace), (Hearts, Ace)]) = true

val test9 = sum_cards([(Clubs, Num 2),(Clubs, Num 2)]) = 4

val test10 = score([(Hearts, Num 2),(Clubs, Num 4)],10) = 4

val test11 = officiate([(Hearts, Num 2),(Clubs, Num 4)],[Draw], 15) = 6

val test12 = officiate([(Clubs,Ace),(Spades,Ace),(Clubs,Ace),(Spades,Ace)],
                       [Draw,Draw,Draw,Draw,Draw],
                       42)
             = 3

val test13 = ((officiate([(Clubs,Jack),(Spades,Num(8))],
                         [Draw,Discard(Hearts,Jack)],
                         42);
               false) 
              handle IllegalMove => true)

val test14 = score_challenge([(Hearts, Num 2),(Clubs, Num 4)],10) = 4

val test15 = score_challenge([(Hearts, Num 10), (Clubs, Ace)], 12) = 1

val test16 = score_challenge([(Hearts, Num 8), (Clubs, Ace), (Diamonds, Ace)], 19) = 3
             
val test17 = score_challenge([(Hearts, Num 4), (Hearts, Ace), (Diamonds, Ace)], 8) = 1   

val test18 = officiate_challenge([(Clubs,Ace),(Spades,Ace),(Clubs,Ace),(Spades,Ace)],
				 [Draw,Draw,Draw,Draw,Draw],
				 38)
             = 2

val test19 = careful_player([], 5) = []

val test20 = careful_player([(Clubs, King)], 23) = [Draw, Draw] 

val test21 = careful_player([(Hearts, Num 3), (Diamonds, Ace)], 14) = [Draw, Draw]  

val test22 = careful_player([(Spades, King), (Hearts, Num 2), 
			     (Clubs, Num 6), (Hearts, Ace), 
			     (Hearts, Num 3)], 27) 
	     = [Draw, Draw, Draw, Discard (Hearts, Num 2), Draw]       
