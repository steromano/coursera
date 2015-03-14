(* Dan Grossman, Coursera PL, HW2 Provided Code *)

(* if you use this function to compare two strings (returns true if the same
   string), then you avoid several of the functions in problem 1 having
   polymorphic types that may be confusing *)
fun same_string(s1 : string, s2 : string) =
    s1 = s2

(* put your solutions for problem 1 here *)

fun all_except_option (s, xs) = 
    case xs of
	[] => NONE
      | x :: xs' => if (same_string(s, x))
		    then SOME (xs')
		    else case all_except_option(s, xs') of
			     NONE => NONE
			   | SOME ys => SOME (x :: ys)

fun get_substitutions1 (substitutions, s) = 
    case substitutions of 
	[] => []
      | sub :: substitutions' => case all_except_option(s, sub) of
				     NONE => get_substitutions1(substitutions', s)
				   | SOME xs => xs @ get_substitutions1(substitutions', s) 

fun get_substitutions2 (substitutions, s) = 
    let fun loop (acc, subs) =
	    case subs of 
		[] => acc
	      | sub :: subs' => case all_except_option(s, sub) of
				    NONE => loop (acc, subs')
				  | SOME xs => loop (acc @ xs, subs')
    in loop ([], substitutions)
    end

fun similar_names (substitutions, {first = fst, middle = mid, last = lst}) =
    let fun loop (acc, names) = 
	    case names of
		[] => acc
	      | name :: names' => loop ({first = name, middle = mid, last = lst} :: acc, names')
    in rev (loop ([], fst :: get_substitutions2(substitutions, fst)))
    end

(* you may assume that Num is always used with values 2, 3, ..., 10
   though it will not really come up *)

datatype suit = Clubs | Diamonds | Hearts | Spades
datatype rank = Jack | Queen | King | Ace | Num of int 
type card = suit * rank

datatype color = Red | Black
datatype move = Discard of card | Draw 

exception IllegalMove

(* put your solutions for problem 2 here *)

fun card_color (s, _) = 
    case s of
	Clubs => Black
      | Spades => Black
      | _ => Red

fun card_value (_, rk) = 
    case rk of
	Num x => x
      | Ace => 11
      | _ => 10 

fun remove_card (cs, c, e) = 
    case cs of
        [] => raise e
      | x :: cs' => if (x = c) then cs' else x :: remove_card(cs', c, e)

fun all_same_color (cs) = 
    case cs of
	[] => true
      | c :: [] => true
      | c1 :: c2 :: cs' => card_color(c1) = card_color(c2) andalso all_same_color(c2 :: cs')
  
fun sum_cards cs = 
    let fun loop (acc, cards) = 
	    case cards of
		[] => acc
	      | c :: cards' => loop(acc + card_value(c), cards') 
    in loop(0, cs)
    end

fun score (held, goal) =  
    let val sum = sum_cards(held)
	val prel_score = if(sum > goal) then 3 * (sum - goal) else (goal - sum)
    in if(all_same_color(held)) then prel_score div 2 else prel_score
    end

fun officiate (deck, moves, goal) = 
    let fun process_move (deck_left, moves_left, held) =
	    case (deck_left, moves_left, held) of
		(_, [], held) => score(held, goal)
	      | (deck', (Discard c) :: moves', held) => process_move (deck', moves', remove_card(held, c, IllegalMove))
	      | ([], Draw :: _, held) => score(held, goal)
	      | (c :: deck', Draw :: moves', held) => let val held' = c :: held
						      in if (sum_cards held' > goal) 
							 then score (held', goal) 
							 else process_move (deck', moves', held')
						      end
    in process_move (deck, moves, [])
    end


 
(* Challenge *)

fun score_challenge (held, goal) = 
    let (* count how many aces are in the hand *)
	fun count_aces cs = 
	    case cs of
		[] => 0
	      | (_, rk) :: cs' => if(rk = Ace)
				  then 1 + count_aces cs'
				  else count_aces cs'
	val naces = count_aces held
	(* compute the score corresponding to a given sum *)
	fun score_sum sum = 
	    let	val prel_score = if(sum > goal) then 3 * (sum - goal) else (goal - sum)
	    in if(all_same_color(held)) then prel_score div 2 else prel_score
	    end
	(* given a sum and a number k of aces currently being used as 1s, find the best score *)
	fun best_score (sum, k) =
	    if (k >= naces)                             (* if all the aces are being used as 1s, *)
	    then score_sum sum                          (* return the corresponding score *) 
	    else let val score1 = score_sum sum         (* else compare the current score and *)
		     val score2 = score_sum (sum - 10)  (* the one obtained by using an additional ace as 1 *)
		 in if (score1 < score2)                (* if the current is better, *)
		    then score1                         (* return it *)
		    else best_score (sum - 10, k + 1)   (* else, recurse with one more ace used as 1 *)
		 end
    in best_score(sum_cards held, 0)
    end	    



fun officiate_challenge (deck, moves, goal) = 
    let fun process_move (deck_left, moves_left, held) = 
	    case (deck_left, moves_left, held) of
		(_, [], held) => score_challenge(held, goal)
	      | (deck', (Discard c) :: moves', held) => process_move (deck', moves', remove_card(held, c, IllegalMove))
	      | ([], Draw :: _, held) => score_challenge(held, goal)
	      | (c :: deck', Draw :: moves', held) => let val held' = c :: held
						      in if (sum_cards held' > goal) 
							 then score_challenge (held', goal) 
							 else process_move (deck', moves', held')
						      end
    in process_move (deck, moves, [])
    end


fun careful_player (deck, goal) = 
    (* Given the hand and the top card of the deck, check if we *)
    (* can reach the goal by discarding a card and then drawing *)
    (* Return the option of the card to discard *)
    let fun discard_draw (held, top_card) =
	    let val sum_held = sum_cards(held)
		fun loop (cs) = 
		    case cs of
			[] => NONE
		      | c :: cs' => if (sum_held - card_value(c) + card_value(top_card) = goal)
				    then SOME c
				    else loop (cs')
	    in loop (held) 
	    end
	(* This function conses the next move at the head of the past moves list *)				       
	fun make_move (deck_left, past_moves, held) =
	    if (goal - sum_cards held) > 10
	    then case deck_left of
		     [] => Draw :: past_moves
		   | top_card :: deck' => make_move(deck', Draw :: past_moves, top_card :: held)
	    else if (sum_cards held = goal)
	    then past_moves
	    else case deck_left of
		     [] => past_moves
		   | top_card :: deck' => case discard_draw (held, top_card) of
					      NONE => past_moves
					    | SOME c => Draw :: (Discard c) :: past_moves
    in rev(make_move(deck, [], []))          (* reverse the list to get the correct order *)
    end
