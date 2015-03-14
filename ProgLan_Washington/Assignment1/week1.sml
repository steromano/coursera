(* 1 *)
fun is_older (date1 : int * int * int, date2 : int * int * int) = 
    let val y1 = #1 date1
	val y2 = #1 date2
	val m1 = #2 date1
	val m2 = #2 date2
	val d1 = #3 date1
	val d2 = #3 date2
    in
	if (y1 <> y2)
	then y1 < y2
	else if (m1 <> m2)
	then m1 < m2
	else d1 < d2
    end

(* 2 *)
fun number_in_month (dates : (int * int * int) list, month: int) = 
    if (null dates) 
    then 0 
    else (if (#2 (hd dates) = month) then 1 else 0) + number_in_month(tl dates, month)

(* 3 *)
fun number_in_months (dates : (int * int * int) list, months : int list) = 
    if (null months) 
    then 0
    else number_in_month (dates, hd months) + number_in_months (dates, tl months)

(* 4 *)
fun dates_in_month (dates : (int * int * int) list, month : int) = 
    if (null dates)
    then []
    else if(#2 (hd dates) = month) 
    then (hd dates) :: dates_in_month(tl dates, month)
    else dates_in_month(tl dates, month)

(* 5 *)
fun dates_in_months (dates : (int * int * int) list, months : int list) = 
    if (null months)
    then []
    else dates_in_month(dates, hd months) @ dates_in_months(dates, tl months)

(* 6 *)
fun get_nth (xs : string list, n : int) = 
    if (n = 1)
    then hd xs
    else get_nth(tl xs, n - 1)

(* 7 *)
fun date_to_string (date : int * int * int) = 
    let val months = ["January", "February", "March", "April", "May", "June",
		      "July", "August", "September", "October", "November", "December"]
    in get_nth(months, #2 date) ^ " " ^ Int.toString(#3 date) ^ ", " ^ Int.toString(#1 date)
    end

(* 8 *)
fun number_before_reaching_sum(sum : int, xs : int list) = 
    if (hd xs >= sum)
    then 0
    else 1 + number_before_reaching_sum(sum - hd xs, tl xs)

(* 9 *)
fun what_month(year_day : int) = 
    let val month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    in number_before_reaching_sum(year_day, month_days) + 1
    end

(* 10 *)
fun month_range(day1 : int, day2 : int) = 
    if (day1 > day2)
    then []
    else what_month(day1) :: month_range(day1 + 1, day2)

(* 11 *)
fun oldest(dates : (int * int * int) list) = 
    if (null dates) 
    then NONE
    else
	let val oldest_tl = oldest(tl dates)
	in if(isSome oldest_tl andalso is_older(valOf oldest_tl, hd dates))
	   then oldest_tl
	   else SOME (hd dates)
	end

(* Challenge *)

(* Helper function to deduplicate a list *)
fun dedup (xs : int list) = 
    let 
	fun remove (x : int, ys : int list) = 
	    if (null ys)
	    then []
	    else if (hd ys = x)
	    then remove (x, tl ys)
	    else (hd ys) :: remove(x, tl ys)
    in 
	if (null xs)
	then []
	else (hd xs) :: dedup(remove (hd xs, tl xs))
    end

(* 12 *)
fun number_in_months_challenge (dates : (int * int * int) list, months : int list) = 
    number_in_months(dates, dedup(months))

fun dates_in_months_challenge (dates : (int * int * int) list, months : int list) = 
    dates_in_months(dates, dedup(months))

(* 13 *)
fun reasonable_date (date : int * int * int) = 
    let val y = #1 date
	val m = #2 date
	val d = #3 date
	val is_leap = y mod 400 = 0 orelse (y mod 4 = 0 andalso y mod 100 <> 0)
	val month_days = [31, if is_leap then 29 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	fun get_nth (xs : int list, n : int) = 
	    if n = 1 
	    then hd xs
	    else get_nth(tl xs, n-1)
    in
	if y <= 0
	then false 
	else if m < 1 orelse m > 12
	then false
	else if d < 1 orelse d > get_nth(month_days, m)
	then false
	else true
    end
