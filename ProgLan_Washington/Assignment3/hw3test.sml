(* Homework3 Simple Test*)
(* These are basic test cases. Passing these tests does not guarantee that your code will pass the actual homework grader *)
(* To run the test, add a new line to the top of this file: use "homeworkname.sml"; *)
(* All the tests should evaluate to true. For example, the REPL should say: val test1 = true : bool *)

val test1 = only_capitals ["A","B","C"] = ["A","B","C"]

val test2 = longest_string1 ["A","bc","C"] = "bc"

val test3 = longest_string2 ["A","bc","C"] = "bc"

val test4a= longest_string3 ["A","bc","C"] = "bc"

val test4b= longest_string4 ["A","B","C"] = "C"

val test5 = longest_capitalized ["A","bc","C"] = "A";

val test6 = rev_string "abc" = "cba";

val test7 = first_answer (fn x => if x > 3 then SOME x else NONE) [1,2,3,4,5] = 4

val test8a = all_answers (fn x => if x = 1 then SOME [x] else NONE) [2,3,4,5,6,7] = NONE

val test8b = all_answers (fn x => if x < 10 then SOME [x,x+1] else NONE) [2,3,4,5] = SOME [2,3,3,4,4,5,5,6]

val test9a = count_wildcards Wildcard = 1

val test9b = count_wild_and_variable_lengths (Variable("a")) = 1

val test9c = count_some_var ("x", Variable("x")) = 1;

val test10 = check_pat (Variable("x")) = true

val test11a = match (Const(1), UnitP) = NONE

val test11b = match(Const(1), Variable("x")) = SOME [("x", Const(1))]

val test11c = match(Tuple [Unit, Constructor("A", Const(1))], 
		    TupleP [Wildcard, ConstructorP("A", Wildcard)]) = SOME []

val test11d = match(Tuple [Unit, Constructor("A", Const(1))], 
		    TupleP [Wildcard, ConstructorP("B", Wildcard)]) = NONE

val test11e = match(Tuple [Const(5), Constructor("A", Const(1))], 
		    TupleP [Wildcard, ConstructorP("A", Variable("x"))]) = SOME [("x", Const(1))]

val test11f = match(Tuple [Unit, Constructor("A", Const(1))], 
		    Variable("t")) = SOME [("t", Tuple [Unit, Constructor("A", Const(1))])]

val test12a = first_match Unit [UnitP] = SOME []

val test12b = first_match Unit [Variable("x"), Variable("y")] = SOME [("x", Unit)]

val test12c = first_match (Constructor("A", Unit)) [TupleP [Wildcard], Variable("x")] = SOME [("x", Constructor("A", Unit))] 
