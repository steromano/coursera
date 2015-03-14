(* Coursera Programming Languages, Homework 3, Provided Code *)

(* filters strings beginning with a capital letter *)
fun only_capitals (strs : string list) = 
    List.filter (fn s => Char.isUpper (String.sub(s, 0))) strs

(* first longest string in a list *)
fun longest_string1(strs : string list) = 
    let fun longer (s, acc) = 
	    if (String.size(s) > String.size(acc))
	    then s
	    else acc
    in List.foldl longer "" strs
    end

(* last longest string in a list *)
fun longest_string2(strs : string list) = 
    let fun longer (s, acc) = 
	    if (String.size(s) >= String.size(acc))
	    then s
	    else acc
    in List.foldl longer "" strs
    end

(* as before but using a helper function that takes a length comparison as a parameter *)
fun longest_string_helper (condition: int*int -> bool) (strs: string list) =
    List.foldl (fn (s, acc) => if condition(String.size(s), String.size(acc)) then s else acc) "" strs

val longest_string3 = longest_string_helper (fn (x, y) => x > y)
val longest_string4 = longest_string_helper (fn (x, y) => x >= y)

(* composition *)
val longest_capitalized = longest_string1 o only_capitals
val rev_string = String.implode o rev o String.explode

exception NoAnswer

(* f is a function returning an option *)
(* given a f and a list, finds the first element of the list for which
   f returns SOME result, and returns that result *)
fun first_answer f xs = 
    case xs of
	[] => raise NoAnswer
      | x :: xs => case f(x) of
		       SOME ans => ans
		     | NONE => first_answer f xs
(* given f and a list, returns NONE if f returns NONE on some element, 
   and SOME lst otherwise, where lst is the concatenation of the values
   returned by f *)
fun all_answers f xs = 
    case xs of
	[] => SOME [] 
      | x :: xs => case (f x, all_answers f xs) of
		      (NONE, _) => NONE
		    | (_, NONE) => NONE
		    | (SOME ans, SOME answers) => SOME (ans @ answers)  

(* predefined datatypes *)
datatype pattern = Wildcard
		 | Variable of string
		 | UnitP
		 | ConstP of int
		 | TupleP of pattern list
		 | ConstructorP of string * pattern

datatype valu = Const of int
	      | Unit
	      | Tuple of valu list
	      | Constructor of string * valu

(* predefined helper function: given a pattern list,
  applies f1 to all Wildcards and f2 to all Variables,
  and takes the sum *)
fun g f1 f2 p =
    let 
	val r = g f1 f2 
    in
	case p of
	    Wildcard          => f1 ()
	  | Variable x        => f2 x
	  | TupleP ps         => List.foldl (fn (p,i) => (r p) + i) 0 ps
	  | ConstructorP(_,p) => r p
	  | _                 => 0
    end

(* simple functions using g *)
val count_wildcards = g (fn () => 1) (fn x => 0)
val count_wild_and_variable_lengths = g (fn () => 1) String.size
fun count_some_var (var: string, p) = g (fn () => 0) (fn x => if x = var then 1 else 0) p

(* checks that a pattern has no repeated variable names *)
fun check_pat (p: pattern) = 
    let fun extract_vars p =
	    case p of 
		Variable s => [s]
	      | ConstructorP (_, p') => extract_vars(p')
	      | TupleP ps => List.foldl (fn (p', acc) => (extract_vars p') @ acc) [] ps
	      | _ => []
	fun has_repeats x = 
	    case x of
		[] => false
	      | x :: xs => List.exists(fn y => y = x) xs orelse has_repeats xs
    in not (has_repeats (extract_vars p))
    end    

(* checks if a pattern matches a value *)
fun match (v: valu, p: pattern) = 
    case (v, p) of
	(_, Wildcard) => SOME []
      | (v, Variable s) => SOME [(s, v)]
      | (Unit, UnitP) => SOME []
      | (Const n, ConstP m) =>  if (n = m) 
				then SOME [] 
				else NONE
      | (Tuple vs, TupleP ps) => if(List.length(vs) = List.length(ps))
				 then all_answers match (ListPair.zip (vs, ps))
				 else NONE
      | (Constructor (s1, v), ConstructorP (s2, p)) => if (s1 = s2) 
						       then match (v, p) 
						       else NONE
      | _ => NONE 

(* returns the first pattern in a list that matches a value *)
(* apparently (from the tests) this is required in curried form *)
fun first_match (v: valu) (ps : pattern list) = 
    SOME (first_answer (fn p => match(v, p)) ps) 
    handle NoAnswer => NONE 
    

(**** Challenge ****)

(* predefined datatype *)
datatype typ = Anything
	     | UnitT
	     | IntT
	     | TupleT of typ list
	     | Datatype of string

(* takes a list of constructor types and a pattern and returns the type of the pattern *)
fun pattern_type (constructor_types: (string * string * typ) list) (p: pattern) = 
    case p of
	Wildcard => Anything
      | Variable _ => Anything 
      | UnitP => UnitT
      | ConstP _ => IntT
      | TupleP xs  => TupleT (List.map (pattern_type constructor_types) xs)
      | ConstructorP (name, p') => let val p_type = pattern_type constructor_types p'
				   in  first_answer (fn (nm, dt, t) =>
							if (nm = name andalso (p_type = t orelse p_type = Anything)) 
							then SOME (Datatype dt) 
							else NONE
						    ) constructor_types
				   end
(* takes two types and returs the most general common type *)
fun common_type (t1: typ, t2: typ) = 
    case (t1, t2) of
	(Anything, t2) => SOME t2
      | (t1, Anything) => SOME t1
      | (UnitT, UnitT) => SOME UnitT
      | (IntT, IntT) => SOME IntT
      | (TupleT t1s, TupleT t2s) => if (List.length t1s = List.length t2s)
				    then let val common_types = List.map common_type (ListPair.zip(t1s, t2s))  
					 in if (List.exists (not o isSome) common_types)
					    then NONE
					    else SOME (TupleT (map valOf common_types))
					 end 
				    else NONE
      | (Datatype s1, Datatype s2) => if (s1 = s2)
				      then SOME (Datatype s1)
				      else NONE
      | _ => NONE  

(* takes a list of constructor types and a list of patterns and return the most general common type of the list *)
fun typecheck_patterns (constructor_types: (string * string * typ) list, ps: pattern list) = 
    case ps of
	[] => SOME Anything
      | p :: ps => case typecheck_patterns (constructor_types, ps) of
		       NONE => NONE
		     | SOME t => common_type(t, pattern_type constructor_types p) 
