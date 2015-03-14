(* Homework1 Simple Test *)
(* These are basic test cases. Passing these tests does not guarantee that your code will pass the actual homework grader *)
(* To run the test, add a new line to the top of this file: use "homeworkname.sml"; *)
(* All the tests should evaluate to true. For example, the REPL should say: val test1 = true : bool *)


val test1 = is_older((1,2,3),(2,3,4)) = true

val test2 = number_in_month([(2012,2,28),(2013,12,1)],2) = 1

val test3 = number_in_months([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = 3

val test4 = dates_in_month([(2012,2,28),(2013,12,1)],2) = [(2012,2,28)]

val test5 = dates_in_months([(2012,2,28),(2013,12,1),(2011,3,31),(2011,4,28)],[2,3,4]) = [(2012,2,28),(2011,3,31),(2011,4,28)]

val test6 = get_nth(["hi", "there", "how", "are", "you"], 2) = "there"

val test7 = date_to_string((2013, 6, 1)) = "June 1, 2013"

val test8 = number_before_reaching_sum(10, [1,2,3,4,5]) = 3

val test9 = what_month(70) = 3

val test10 = month_range(31, 34) = [1,2,2,2]

val test11 = oldest([(2012,2,28),(2011,3,31),(2011,4,28)]) = SOME (2011,3,31)

val test12 = dedup([1, 2, 3, 3, 2, 1]) = [1, 2, 3]

val test13 = number_in_months_challenge([(2012,2,2),(2014,12,1),(2010,11,31),(2011,4,28)],[2,3,4,2,2]) = 2

val test14 = dates_in_months_challenge([(2012,12,1),(2013,3,18),(2000,2,14)],[3,2, 3]) = [(2013,3,18),(2000,2,14)] 

val test15 = not (reasonable_date(~1, 1, 1))

val test16 = not (reasonable_date(2010, 13, 1))

val test17 = not (reasonable_date(2015, 2, 29))

val test18 = reasonable_date(2016, 2, 29)
